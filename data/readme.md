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
