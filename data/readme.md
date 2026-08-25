The dataset originates from simulations utilizing the Benchmark Simulation Model No. 2 
(BSM2), a recognized framework for the dynamic simulation and evaluation of wastewater 
treatment plant processes. The variables presented in this document were derived under a 
dynamic input scenario, incorporating time-dependent influent variations to emulate real
world conditions and operational complexities observed in full-scale wastewater treatment 
facilities. 
Reactor outputs, formatted as a matrix with dimensions 58451x16, illustrate the temporal 
progression of key biological, chemical, and physical parameters within the reactor. These 
variables offer valuable insights into the reactor's performance, facilitating further analysis of 
its dynamic behavior and efficiency in response to fluctuating inputs. 
Reactor Variables  
This file provides detailed explanations of the variables extracted from each reactor in the 
MATLAB and Simulink simulation of the BSM2 model. Below is an overview of each variable: 
Each CSV file contains 42 columns and multiple time steps. The columns represent simulation time, input variables, and reactor state variables.

### Column Definitions

| Column Name         | Description                               | Unit          |
|---------------------|-------------------------------------------|---------------|
| Time [days]         | Simulation time in days                   | days          |
| S_I                 | Soluble inert organic matter (influent)   | mg COD/L      |
| S_S                 | Readily biodegradable substrate           | mg COD/L      |
| X_I                 | Particulate inert organic matter          | mg COD/L      |
| X_S                 | Slowly biodegradable substrate            | mg COD/L      |
| X_BH                | Active heterotrophic biomass              | mg COD/L      |
| X_BA                | Ammonia oxidizing biomass (AOB)           | mg COD/L      |
| X_P                 | Particulate products from biomass decay   | mg COD/L      |
| S_O                 | Dissolved oxygen                          | mg O₂/L       |
| S_NO3               | Nitrate nitrogen                          | mg N/L        |
| S_NH                | Ammonium nitrogen                         | mg N/L        |
| S_ND                | Soluble organic nitrogen                  | mg N/L        |
| X_ND                | Particulate organic nitrogen              | mg N/L        |
| S_ALK               | Alkalinity                                | mol/m³        |
| S_NO2               | Nitrite nitrogen                          | mg N/L        |
| S_NO                | Nitric oxide                              | mg N/L        |
| S_N2O               | Nitrous oxide                             | mg N/L        |
| S_N2                | Dinitrogen gas                            | mg N/L        |
| X_BA2               | Nitrite oxidizing biomass (NOB)           | mg COD/L      |
| Temp                | Temperature of influent                   | °C            |
| TSS_influent        | Total Suspended Solids of influent        | mg/L          |
| Flow_influent       | Influent flow rate                        | m³/d          |
| Kla                 | Oxygen transfer coefficient               | 1/d           |
| S_I_reactor to Temp_reactor | State values in the bioreactor for the above 19 ASM1 components | same as above |

### Notes

- The first 23 columns are input data (`u` matrix), including influent characteristics and operating parameters.
- The last 19 columns (`y` matrix) represent the internal states of the bioreactor.
- The files correspond to rainy scenarios for reactors R1, R2, R4, and R5.

### Origin

- Model: BSM1 + ASMG1
- Scenario: Rainy conditions
- Generated using MATLAB scripts including `get_mat_data.m`, `main_training.m`, and `main_testing.m`.

