# bsm_anomaly_demo.py
# A self-contained Tkinter app with embedded Matplotlib:
# - Train MLP "autoencoder" on 2023 data
# - Save/load artifacts (scaler, model, thresholds, columns, window_size)
# - Stream forward through later data with a sliding window
# - Live plots: (top) chosen variable signal + shaded anomalies
#               (bottom) reconstruction error + threshold
# - Anomaly log table and CSV export
#
# Dependencies:
#   pip install numpy pandas scikit-learn matplotlib joblib
# (Tkinter ships with most Python builds; on some Linux you may need python3-tk)
#
# DATA EXPECTATION:
#   TRAIN_CSV contains a time index (parse_dates=True) and multiple numeric columns.
#   App splits by year: 2023 = training; others streamed.

import os
import threading
import time
from collections import deque
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import numpy as np
import pandas as pd
from joblib import dump, load
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# -------------------------
# User-config defaults
# -------------------------
DEFAULT_TRAIN_CSV = "Data_longer/BSM2-ASReactor2-Faulty.csv"
DEFAULT_FAULT_LOG = "Data_longer/BSM2-ASReactor2-FaultLog.csv"  # optional; not required
ARTIFACTS_PATH = "ae_artifacts.joblib"

DEFAULT_WINDOW_SIZE = 16
DEFAULT_THRESHOLD_PCTL = 98  # from training recon error
DEFAULT_INTERVAL_MS = 50     # UI update interval for streaming
DEFAULT_PLOT_WINDOW = 800    # number of recent points shown

# -------------------------
# Core training & artifacts
# -------------------------
def make_windows(arr, w):
    """Return windows of shape (N, w, F) from 2D array (T, F)."""
    if len(arr) < w:
        return np.empty((0, w, arr.shape[1]))
    return np.array([arr[i:i + w] for i in range(len(arr) - w + 1)])

def train_autoencoder(train_df, window_size, threshold_pctl):
    scaler = MinMaxScaler()
    train_scaled = scaler.fit_transform(train_df.values)
    X_train = make_windows(train_scaled, window_size)               # (N, W, F)
    X_train_flat = X_train.reshape((X_train.shape[0], -1))          # (N, W*F)

    model = MLPRegressor(hidden_layer_sizes=(128, 64, 128),
                         max_iter=100, random_state=0)
    model.fit(X_train_flat, X_train_flat)

    X_pred = model.predict(X_train_flat).reshape(X_train.shape)     # (N, W, F)
    recon_err_train = ((X_train - X_pred) ** 2).mean(axis=1)        # (N, F)
    thresholds = np.percentile(recon_err_train, threshold_pctl, axis=0)  # (F,)
    return scaler, model, thresholds

def save_artifacts(path, scaler, model, window_size, columns, thresholds):
    dump({
        "scaler": scaler,
        "model": model,
        "window_size": window_size,
        "columns": columns,
        "thresholds": thresholds
    }, path)

def load_artifacts(path):
    obj = load(path)
    return obj["scaler"], obj["model"], obj["window_size"], obj["columns"], obj["thresholds"]

# -------------------------
# Streaming detector
# -------------------------
class StreamDetector:
    def __init__(self, stream_df, scaler, model, window_size, columns, thresholds,
                 var_to_show, plot_window):
        self.stream_df = stream_df[columns].copy()
        self.scaler = scaler
        self.model = model
        self.window_size = window_size
        self.columns = columns
        self.thresholds = thresholds

        if var_to_show not in columns:
            raise ValueError(f"Variable '{var_to_show}' not found in data columns.")
        self.var = var_to_show
        self.var_idx = columns.index(self.var)

        # buffers
        self.buf_scaled = deque(maxlen=window_size)
        self.buf_raw = deque(maxlen=window_size)

        # plotting buffers (sliding window)
        self.ts = deque(maxlen=plot_window)
        self.sig = deque(maxlen=plot_window)
        self.err = deque(maxlen=plot_window)
        self.flags = deque(maxlen=plot_window)

        # anomaly log (dict list)
        self.records = []

        self.i = 0
        self.done = False

    def _window_error(self, window_scaled):
        X = window_scaled[None, ...]                               # (1, W, F)
        X_flat = X.reshape((1, -1))
        X_pred = self.model.predict(X_flat).reshape(X.shape)       # (1, W, F)
        err_vec = ((X - X_pred) ** 2).mean(axis=1).ravel()         # (F,)
        return err_vec

    def step(self):
        if self.i >= len(self.stream_df):
            self.done = True
            return None

        ts = self.stream_df.index[self.i]
        row = self.stream_df.iloc[self.i].astype(float)
        row_scaled = self.scaler.transform(row.values.reshape(1, -1)).ravel()

        self.buf_raw.append(row)
        self.buf_scaled.append(row_scaled)

        cur_err = np.nan
        flag = False
        cause = ""

        if len(self.buf_scaled) == self.window_size:
            w_scaled = np.vstack(self.buf_scaled)                  # (W, F)
            err_vec = self._window_error(w_scaled)                 # (F,)
            over = (err_vec > self.thresholds)
            flag = bool(over.any())
            cur_err = err_vec[self.var_idx]
            if flag:
                cause_vars = [self.columns[j] for j, t in enumerate(over) if t]
                cause = ",".join(cause_vars)
                self.records.append({
                    "timestamp": ts,
                    "flag": 1,
                    "cause_vars": cause,
                    "err_" + self.var: float(cur_err)
                })
        # update plotting buffers (always push last point to keep x advancing)
        self.ts.append(ts)
        self.sig.append(float(row[self.var]))
        self.err.append(float(cur_err) if np.isfinite(cur_err) else np.nan)
        self.flags.append(bool(flag))

        self.i += 1
        return ts, float(row[self.var]), float(cur_err) if np.isfinite(cur_err) else np.nan, flag, cause

# -------------------------
# Tk GUI
# -------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Anomaly Detection Demo (MLP Autoencoder)")
        self.geometry("1200x800")

        # state
        self.df = None
        self.columns = []
        self.train_df = None
        self.stream_df = None
        self.detector = None
        self.streaming = False
        self.after_id = None

        # defaults
        self.window_size = tk.IntVar(value=DEFAULT_WINDOW_SIZE)
        self.thresh_pctl = tk.IntVar(value=DEFAULT_THRESHOLD_PCTL)
        self.interval_ms = tk.IntVar(value=DEFAULT_INTERVAL_MS)
        self.plot_window = tk.IntVar(value=DEFAULT_PLOT_WINDOW)
        self.var_to_show = tk.StringVar(value="")

        # artifacts in memory
        self.scaler = None
        self.model = None
        self.thresholds = None

        self._build_ui()

    def _build_ui(self):
        # Top control bar
        ctrl = ttk.Frame(self)
        ctrl.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        ttk.Button(ctrl, text="Load CSV…", command=self.on_load_csv).pack(side=tk.LEFT)
        ttk.Label(ctrl, text="Window").pack(side=tk.LEFT, padx=(10, 2))
        ttk.Entry(ctrl, textvariable=self.window_size, width=5).pack(side=tk.LEFT)
        ttk.Label(ctrl, text="Pctl").pack(side=tk.LEFT, padx=(10, 2))
        ttk.Entry(ctrl, textvariable=self.thresh_pctl, width=5).pack(side=tk.LEFT)
        ttk.Label(ctrl, text="Interval ms").pack(side=tk.LEFT, padx=(10, 2))
        ttk.Entry(ctrl, textvariable=self.interval_ms, width=7).pack(side=tk.LEFT)
        ttk.Label(ctrl, text="Plot pts").pack(side=tk.LEFT, padx=(10, 2))
        ttk.Entry(ctrl, textvariable=self.plot_window, width=7).pack(side=tk.LEFT)

        ttk.Button(ctrl, text="Train + Save", command=self.on_train_save).pack(side=tk.LEFT, padx=10)
        ttk.Button(ctrl, text="Load Artifacts", command=self.on_load_artifacts).pack(side=tk.LEFT)

        ttk.Label(ctrl, text="Show Var").pack(side=tk.LEFT, padx=(10, 2))
        self.var_combo = ttk.Combobox(ctrl, textvariable=self.var_to_show, width=12, state="readonly")
        self.var_combo.pack(side=tk.LEFT)

        ttk.Button(ctrl, text="Start Stream", command=self.on_start).pack(side=tk.LEFT, padx=10)
        ttk.Button(ctrl, text="Pause", command=self.on_pause).pack(side=tk.LEFT)
        ttk.Button(ctrl, text="Reset", command=self.on_reset).pack(side=tk.LEFT, padx=(6,0))
        ttk.Button(ctrl, text="Export Anomalies CSV", command=self.on_export_csv).pack(side=tk.RIGHT)

        # Status
        self.status = tk.StringVar(value="Load a CSV to begin.")
        ttk.Label(self, textvariable=self.status, anchor="w").pack(side=tk.TOP, fill=tk.X, padx=8)

        # Main area: plots (left) + anomaly table (right)
        main = ttk.Frame(self)
        main.pack(fill=tk.BOTH, expand=True)

        # Matplotlib figure
        self.fig = Figure(figsize=(7.0, 5.5), dpi=100)
        self.ax1 = self.fig.add_subplot(2,1,1)
        self.ax2 = self.fig.add_subplot(2,1,2)

        self.l_sig, = self.ax1.plot([], [], label="Signal")
        self.ax1.grid(True); self.ax1.legend(loc="upper left")

        self.l_err, = self.ax2.plot([], [], label="Recon. Error")
        self.err_thr_line = self.ax2.axhline(0, linestyle="--", label="Threshold")
        self.ax2.grid(True); self.ax2.legend(loc="upper left")

        self.canvas = FigureCanvasTkAgg(self.fig, master=main)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8,4), pady=8)

        # Anomaly table
        table_frame = ttk.Frame(main)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(4,8), pady=8)

        ttk.Label(table_frame, text="Detected Anomalies").pack(anchor="w")
        cols = ("timestamp", "cause_vars", "err")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=25)
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("cause_vars", text="Cause Vars")
        self.tree.heading("err", text="Err (shown var)")

        self.tree.column("timestamp", width=160)
        self.tree.column("cause_vars", width=150)
        self.tree.column("err", width=90, anchor="e")
        self.tree.pack(fill=tk.BOTH, expand=True)

    # --------------- Events ---------------
    def on_load_csv(self):
        path = filedialog.askopenfilename(
            title="Select CSV",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not path:
            return
        try:
            df = pd.read_csv(path, index_col=0, parse_dates=True)
            if not isinstance(df.index, pd.DatetimeIndex):
                messagebox.showerror("Error", "Index must be a datetime (parse_dates).")
                return
            self.df = df.copy()
            self.columns = df.columns.tolist()
            self.var_combo["values"] = self.columns
            if not self.var_to_show.get() and self.columns:
                self.var_to_show.set(self.columns[0])

            # Split: 2023 train, others stream
            train_mask = self.df.index.year == 2023
            self.train_df = self.df[train_mask].copy()
            self.stream_df = self.df[~train_mask].copy()

            self.status.set(f"Loaded {os.path.basename(path)} | Train: {len(self.train_df)} rows, Stream: {len(self.stream_df)} rows.")
        except Exception as e:
            messagebox.showerror("Error loading CSV", str(e))

    def on_train_save(self):
        if self.train_df is None or self.train_df.empty:
            messagebox.showerror("Error", "Load a CSV first. Need 2023 rows for training.")
            return
        w = int(self.window_size.get())
        p = int(self.thresh_pctl.get())
        try:
            self.status.set("Training…")
            self.update_idletasks()
            scaler, model, thresholds = train_autoencoder(self.train_df, w, p)
            save_artifacts(ARTIFACTS_PATH, scaler, model, w, self.columns, thresholds)
            self.scaler, self.model, self.thresholds = scaler, model, thresholds
            messagebox.showinfo("Done", f"Artifacts saved to {ARTIFACTS_PATH}")
            self.status.set("Training complete. Artifacts saved.")
        except Exception as e:
            messagebox.showerror("Training failed", str(e))
            self.status.set("Training failed.")

    def on_load_artifacts(self):
        path = filedialog.askopenfilename(
            title="Select artifacts", filetypes=[("Joblib", "*.joblib"), ("All Files", "*.*")]
        )
        if not path:
            return
        try:
            scaler, model, w, cols, thresholds = load_artifacts(path)
            if self.df is None:
                messagebox.showwarning("Note", "Load a CSV next; columns must match the artifacts.")
            self.scaler, self.model, self.thresholds = scaler, model, thresholds
            self.window_size.set(int(w))
            self.columns = cols
            self.var_combo["values"] = self.columns
            if not self.var_to_show.get() and self.columns:
                self.var_to_show.set(self.columns[0])
            self.status.set(f"Loaded artifacts from {os.path.basename(path)}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _ensure_detector(self):
        if self.stream_df is None or self.stream_df.empty:
            raise RuntimeError("No stream data. Load a CSV.")
        if self.scaler is None or self.model is None or self.thresholds is None:
            raise RuntimeError("Artifacts missing. Train + Save or Load Artifacts first.")
        var = self.var_to_show.get()
        self.detector = StreamDetector(
            self.stream_df, self.scaler, self.model,
            int(self.window_size.get()), self.columns, self.thresholds,
            var_to_show=var, plot_window=int(self.plot_window.get())
        )
        # clean table
        for i in self.tree.get_children():
            self.tree.delete(i)
        # init axes
        self.ax1.clear(); self.ax2.clear()
        self.l_sig, = self.ax1.plot([], [], label=f"{var} (signal)")
        self.ax1.grid(True); self.ax1.legend(loc="upper left")
        self.l_err, = self.ax2.plot([], [], label="Recon. Error")
        thr = float(self.thresholds[self.columns.index(var)])
        self.err_thr_line = self.ax2.axhline(thr, linestyle="--", label=f"Threshold ({thr:.3g})")
        self.ax2.grid(True); self.ax2.legend(loc="upper left")
        self.canvas.draw_idle()

    def on_start(self):
        try:
            if self.detector is None or self.detector.done:
                self._ensure_detector()
            if not self.streaming:
                self.streaming = True
                self.status.set("Streaming…")
                self._tick()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _tick(self):
        if not self.streaming or self.detector is None:
            return
        record = self.detector.step()
        if record is not None:
            ts, sig, err, flag, cause = record
            # update plots
            x = list(self.detector.ts)
            y = list(self.detector.sig)
            e = list(self.detector.err)
            f = np.array(self.detector.flags, dtype=bool)

            self.ax1.clear(); self.ax2.clear()
            self.ax1.plot(x, y, label=f"{self.detector.var} (signal)")
            self.ax1.grid(True); self.ax1.legend(loc="upper left")
            # shade anomalies on signal
            if len(x) > 1 and f.any():
                self.ax1.fill_between(x, np.nanmin(y), np.nanmax(y), where=f, alpha=0.25)

            self.ax2.plot(x, e, label="Recon. Error")
            thr = float(self.thresholds[self.detector.var_idx])
            self.ax2.axhline(thr, linestyle="--", label=f"Threshold ({thr:.3g})")
            self.ax2.grid(True); self.ax2.legend(loc="upper left")
            # shade anomalies on error plot
            if len(x) > 1 and f.any():
                finite_e = [val for val in e if np.isfinite(val)]
                ymax = max(finite_e) if finite_e else 0.0
                self.ax2.fill_between(x, 0, ymax, where=f, alpha=0.2)

            self.fig.tight_layout()
            self.canvas.draw_idle()

            # push anomaly row to table
            if flag:
                self.tree.insert("", tk.END, values=(ts.strftime("%Y-%m-%d %H:%M:%S"), cause, f"{err:.4g}"))

        if self.detector.done:
            self.streaming = False
            self.status.set("Stream complete.")
            return
        # schedule next tick
        self.after_id = self.after(int(self.interval_ms.get()), self._tick)

    def on_pause(self):
        self.streaming = False
        if self.after_id:
            try:
                self.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None
        self.status.set("Paused.")

    def on_reset(self):
        self.on_pause()
        self.detector = None
        # clear plots and table
        self.ax1.clear(); self.ax2.clear()
        self.l_sig, = self.ax1.plot([], [], label="Signal")
        self.ax1.grid(True); self.ax1.legend(loc="upper left")
        self.l_err, = self.ax2.plot([], [], label="Recon. Error")
        self.ax2.grid(True); self.ax2.legend(loc="upper left")
        self.canvas.draw_idle()
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.status.set("Reset.")

    def on_export_csv(self):
        if self.detector is None or not self.detector.records:
            messagebox.showwarning("Nothing to export", "No anomalies have been detected yet.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")], title="Save anomalies CSV"
        )
        if not path:
            return
        pd.DataFrame(self.detector.records).to_csv(path, index=False)
        messagebox.showinfo("Saved", f"Anomalies exported to:\n{path}")

# -------------------------
# main
# -------------------------
if __name__ == "__main__":
    app = App()
    # Optional: auto-load your default CSV if it exists
    if os.path.exists(DEFAULT_TRAIN_CSV):
        try:
            df = pd.read_csv(DEFAULT_TRAIN_CSV, index_col=0, parse_dates=True)
            if isinstance(df.index, pd.DatetimeIndex):
                app.df = df.copy()
                app.columns = df.columns.tolist()
                app.var_combo["values"] = app.columns
                if app.columns:
                    app.var_to_show.set(app.columns[0])
                mask = app.df.index.year == 2023
                app.train_df = app.df[mask].copy()
                app.stream_df = app.df[~mask].copy()
                app.status.set(f"Auto-loaded {DEFAULT_TRAIN_CSV} | Train: {len(app.train_df)} rows, Stream: {len(app.stream_df)} rows.")
            else:
                app.status.set("Default CSV loaded but index is not datetime.")
        except Exception:
            pass
    app.mainloop()
