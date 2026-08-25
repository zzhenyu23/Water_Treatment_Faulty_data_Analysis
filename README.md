# Water Treatment Faulty Data Analysis

## Overview

This repository provides a complete framework for the generation, detection, and reconstruction of faulty data in water treatment systems. The objective is to develop and evaluate data-driven approaches capable of identifying sensor faults, missing measurements, and anomalous observations while accurately reconstructing the affected data.

The repository contains the complete workflow, including:

- Dataset generation
- Fault injection
- Data quality assessment
- Feature and relationship analysis
- Model training
- Fault detection
- Data reconstruction
- Interactive result visualisation

All scripts required to reproduce the analyses are included.

---

## Dataset Development

### Confidentiality and Data Generation

The original datasets used in this work were derived from real water treatment operational data. However, due to confidentiality and privacy constraints, raw plant data cannot be publicly released.

To enable research reproducibility while protecting sensitive information, the published datasets were generated using real operational characteristics, including:

- Temporal patterns
- Daily operational profiles
- Seasonal variations
- Process dynamics
- Relationships between variables

Sensitive identifiers and confidential operational information were removed during dataset generation. The resulting datasets preserve realistic process behaviour and inter-variable relationships while remaining suitable for open research and benchmarking purposes.

---

## Fault Definition

Water treatment datasets are susceptible to various data quality issues caused by sensor failures, communication interruptions, calibration problems, and equipment malfunctions.

The following fault types are considered within this project:

### Missing Data

Measurements are unavailable for a period of time due to transmission, storage, or sensor failures.

### Spike Anomalies

Short-duration abnormal values that significantly deviate from expected operating conditions.

### Sensor Drift

Gradual deviation of sensor measurements from true values over time.

### Constant (Stuck) Values

Periods where a sensor repeatedly reports the same value despite changing process conditions.

### Bias Errors

Persistent offsets introduced into sensor measurements.

### Combined Faults

Multiple fault types occurring simultaneously within the same signal.

---

## Fault Injection

To provide controlled benchmarking datasets, faults are artificially injected into clean operational data.

The repository includes all fault injection scripts used in this study, allowing experiments to be fully reproduced.

Injected fault parameters include:

- Fault type
- Fault magnitude
- Fault duration
- Injection frequency
- Affected variables

This approach provides known ground truth, enabling quantitative evaluation of both fault detection and reconstruction performance.

---

## Relationship Analysis

Water treatment processes contain strong dependencies between operational and water quality variables. These relationships provide valuable information for identifying abnormal measurements and estimating missing values.

Relationship analysis is performed to:

- Identify correlated variables
- Capture process behaviour
- Support anomaly detection
- Improve reconstruction accuracy

The identified relationships are subsequently incorporated into the fault detection and data reconstruction workflow.

---

## Training and Testing Strategy

### Training Dataset

Model training is performed using data profiles that contain:

- No missing values
- No injected faults
- Stable operational conditions
- Representative process behaviour

These datasets are used to learn normal operating patterns and variable relationships.

### Testing Dataset

Testing datasets are generated through controlled fault injection.

The trained models are evaluated against datasets containing known faults to assess:

- Detection accuracy
- Reconstruction accuracy
- Robustness under different fault scenarios
- Generalisation capability

---

## Fault Detection and Reconstruction

The framework first identifies potentially faulty observations using learned process behaviour and variable relationships.

Detected anomalies are then reconstructed using information from:

- Historical temporal patterns
- Daily operational profiles
- Correlated process variables
- Machine learning models

The reconstructed values are compared against the available ground truth to quantify reconstruction performance.

---

## Results and Visualisation

All outputs are generated as interactive HTML visualisations.

HTML was selected as the primary output format because it enables:

- Interactive exploration
- Zooming and panning
- Inspection of individual anomalies
- Comparison of original, faulty, and reconstructed signals
- Easy sharing across platforms without specialised software

This flexibility allows users to investigate fault periods in detail and assess reconstruction quality more effectively than static figures.

---

## Reproducibility

This repository includes the complete source code required to reproduce the study, including:

- Data preprocessing
- Dataset generation
- Fault injection
- Relationship analysis
- Model training
- Model testing
- Fault detection
- Data reconstruction
- Visualisation and HTML report generation

---

## Applications

This framework is replicable and transferable, subject to appropriate domain knowledge, and can be applied to:

- Water treatment plants
- Wastewater treatment facilities
- Water distribution networks
- Energy systems
- Environmental monitoring systems
- Industrial process monitoring
