function [data_faulty, fault_log] = inject_faults(data, time, fault_config)
%INJECT_FAULTS Injects faults into a time-series dataset
%
%   INPUTS:
%       data:          (n x m) matrix or table of clean data (rows: time, cols: variables)
%       time:          (n x 1) vector of time (in days)
%       fault_config:  struct array with fields:
%                       - variable: column index or name (if table)
%                       - type: 'bias' | 'drift' | 'stuck' | 'spike' | 'dropout' | 'noise' | 'scaling'
%                       - param: struct with fault-specific parameters
%                       - t_start: start time (in days)
%                       - t_end: end time (in days)
%
%   OUTPUTS:
%       data_faulty:   data with faults injected
%       fault_log:     table summarizing all injected faults
%
%   Supported Fault Types and Parameters:
%     - 'bias':     param.offset (numeric scalar)
%     - 'drift':    param.slope (numeric scalar, linear change per step)
%     - 'stuck':    no parameters (value remains constant during fault)
%     - 'spike':    param.freq (0-1), param.magnitude (spike height)
%     - 'dropout':  param.freq (0-1, fraction of values to set to NaN)
%     - 'noise':    param.magnitude (standard deviation of added noise)
%     - 'scaling':  param.factor (scaling multiplier)

% Initialize
n = size(data,1);
data_faulty = data;
fault_log = []; % will become a table

if istable(data)
    isTable = true;
else
    isTable = false;
end

for i = 1:length(fault_config)
    cfg = fault_config(i);

    % Determine variable index
    if isTable
        if ischar(cfg.variable) || isstring(cfg.variable)
            var_name = cfg.variable;
        else
            var_name = data.Properties.VariableNames{cfg.variable};
        end
        x = data_faulty.(var_name);
    else
        var_idx = cfg.variable;
        x = data_faulty(:, var_idx);
    end

    % Find time range
    mask = (time >= cfg.t_start) & (time <= cfg.t_end);
    idx = find(mask);
    if isempty(idx), continue; end

    x_fault = x;

    % Apply fault
    switch lower(cfg.type)
        case 'bias'
            x_fault(idx) = x(idx) + cfg.param.offset;

        case 'drift'
            drift = linspace(0, cfg.param.slope * length(idx), length(idx))';
            x_fault(idx) = x(idx) + drift;

        case 'stuck'
            x_fault(idx) = x(idx(1));

        case 'spike'
            n_spikes = round(cfg.param.freq * length(idx));
            spike_idx = idx(randperm(length(idx), n_spikes));
            x_fault(spike_idx) = x(spike_idx) + cfg.param.magnitude * randn(size(spike_idx));

        case 'dropout'
            n_drop = round(cfg.param.freq * length(idx));
            drop_idx = idx(randperm(length(idx), n_drop));
            x_fault(drop_idx) = NaN;

        case 'noise'
            x_fault(idx) = x(idx) + cfg.param.magnitude * randn(length(idx),1);

        case 'scaling'
            x_fault(idx) = x(idx) * cfg.param.factor;

        otherwise
            warning('Unknown fault type: %s', cfg.type);
    end

    % Update data
    if isTable
        data_faulty.(var_name) = x_fault;
    else
        data_faulty(:, var_idx) = x_fault;
    end

    % Log entry
    fault_log = [fault_log; {
        cfg.variable, cfg.type, cfg.param, cfg.t_start, cfg.t_end
    }];
end

% Convert log to table
fault_log = cell2table(fault_log, 'VariableNames', {'Variable','Type','Param','StartTime','EndTime'});

end
