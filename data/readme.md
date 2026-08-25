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
List of Variables and Descriptions 
1. SI (Soluble Inert Organic Matter): Represents soluble organic materials that are 
biologically inert and do not degrade. 
2. SS (Readily Biodegradable Substrate): Refers to easily degradable organic substances 
available for microbial consumption. 
3. XI (Particulate Inert Organic Matter): Denotes particulate organic materials that are 
non-biodegradable and persist within the system. 
4. XS (Slowly Biodegradable Substrate): Reflects organic materials that degrade at a 
slower rate compared to readily biodegradable substances. 
5. XBH (Heterotrophic Biomass): Represents the biomass of heterotrophic microorganisms 
responsible for breaking down organic substrates. 
6. XBA (Autotrophic Biomass): Refers to autotrophic microorganisms that are mainly 
involved in nitrification processes, such as ammonia oxidation. 
7. XP (Particulate Products from Biomass Decay): Denotes particulate materials resulting 
from the decay of microorganisms. 
8. SO (Dissolved Oxygen): Concentration of oxygen dissolved in the water, essential for 
biological processes. 
9. SNO (Nitrate and Nitrite Nitrogen): Total concentration of nitrate and nitrite nitrogen, 
key indicators of nitrogen removal efficiency. 
10. SNH (Ammonium and Ammonia Nitrogen): Level of ammonium and ammonia in the 
reactor, critical for nitrification processes. 
11. SND (Soluble Organic Nitrogen): Refers to soluble organic nitrogen compounds present 
in the water. 
12. XND (Particulate Organic Nitrogen): Denotes particulate organic nitrogen compounds. 
13. SALK (Alkalinity): Indicates the buffering capacity of the system, which helps maintain 
stable pH levels. 
14. TSS (Total Suspended Solids): Concentration of suspended solid particles in the reactor. 
15. FlowRate: The flow rate of wastewater passing through the reactor. 
16. Temperature: The temperature of the reactor, crucial for maintaining optimal 
conditions for microbial activity. 
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

