# Random Instances and Data Generator

This repository contains 54 instances and the corresponding data generation code.

The details of each file are as follows:

- **instances/** contains the 54 instances used in the computational experiments, including:
  - The number of jobs, stages, parallel machines, and auxiliary resource types.
  - Processing times of jobs on different machines.
  - Machine processing speeds and corresponding power conversion factors.
  - Machine operating, idle, and reset power parameters.
  - Machine-dependent auxiliary resource requirements and resource capacities.

- **Data_generation.py** is used to generate random benchmark instances following the above data structure.