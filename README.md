## Two-Stage CMOS OTA Design (SKY130)

This repository documents the complete design, sizing, and simulation
of a two-stage CMOS operational transconductance amplifier (OTA)
implemented using the SKY130 PDK.

The work focuses on methodical analog design using LUT-based sizing,
stability analysis, and simulation-driven validation.

---

## Design Objectives

- Achieve high DC gain with stable closed-loop operation
- Ensure adequate phase margin under nominal load conditions
- Use gm/Id-based sizing for predictable performance
- Validate design decisions through simulation

---

## Design Methodology

The OTA was designed using a structured workflow:

1. Device-level characterization using ngspice
2. LUT generation for gm/Id, output resistance, and ft
3. Transistor sizing based on target gain and stability
4. Frequency compensation for robust phase margin
5. Iterative AC and transient simulations for verification

Python scripts were used to automate LUT generation and visualize
design trade-offs.

---

## LUT Generation

Lookup tables were generated using dedicated single-transistor
characterization testbenches for NMOS and PMOS devices.

Each device was biased with a fixed drain-source voltage while the
gate voltage was swept to extract DC current and small-signal
parameters. Separate testbenches were used for NFET and PFET devices
to correctly account for polarity and biasing.

For each simulation run, a CSV lookup table was generated containing:
- Gate voltage (Vgs)
- Drain current (Id)
- Transconductance (gm)
- gm/Id ratio
- Drain current per unit width (Id/µm)

The LUTs were used for sizing and trade-off analysis, while plots of
Id vs Vgs, gm vs Vgs, and gm/Id vs Vgs were generated for verification
and visualization.

Corresponding schematics are provided in `schematics/`, and the
Python script used for LUT generation is available in
`lut_generation/`.

---

## Key Results

- DC gain: ~60 dB
- Phase margin: ~64°
- Topology: two-stage OTA with frequency compensation

---

## Tools Used

- Xschem
- ngspice
- Python
- SKY130 PDK

---

## Status and Future Work

- OTA design and simulations completed
- LDO and high-pass filter designs planned as future work
