## Two-Stage CMOS OTA Design (SKY130)

This repository documents the complete design, sizing, and simulation
of a two-stage CMOS operational transconductance amplifier (OTA)
implemented using the SKY130 PDK.

The work follows a structured gm/Id and LUT-based analog design
methodology, with device-level characterization, transistor sizing,
and simulation-driven validation.

---

## Design Specifications

| Parameter        | Value                                  |
|------------------|----------------------------------------|
| Supply Voltage   | ±1.8 V                                 |
| Topology         | Two-stage OTA with Miller compensation |
| Target DC Gain   | ≥ 60 dB                                |
| Target UGB       | ≈ 340 MHz                              |
| Miller Capacitor | 0.1 pF                                 |

---

## Design Objectives

- Achieve high DC gain with stable closed-loop operation  
- Ensure adequate phase margin under nominal conditions  
- Use gm/Id-based sizing for predictable biasing  
- Validate design decisions through simulation  

---

## LUT Generation

Lookup tables were generated using dedicated single-transistor
characterization testbenches for NMOS and PMOS devices.

Each device was biased with a fixed drain-source voltage while the
gate voltage was swept to extract DC current and small-signal
parameters. Separate testbenches were used for NFET and PFET devices
to correctly account for polarity and biasing.

The LUT generation was performed across **multiple channel lengths**.
The resulting data was post-processed and combined to enable
length-dependent design trade-off analysis. The post-processing script
used to merge and visualize multi-L data is intentionally not included.

For each simulation run, a CSV lookup table was generated containing:
- Gate voltage (Vgs)
- Drain current (Id)
- Transconductance (gm)
- gm/Id ratio
- Drain current per unit width (Id/µm)

Plots generated from the LUTs include:
- gm/Id vs Id/µm (NMOS and PMOS, multiple L)
- gm vs Id/µm
- Vgs vs gm/Id

Corresponding device characterization schematics are provided in
`schematics/`, and the Python script used for LUT extraction is
available in `lut_generation/`.

---

## OTA Design and Sizing

The OTA was designed using the gm/Id methodology, starting from the
unity-gain bandwidth requirement and Miller compensation constraint.

Initial transistor dimensions were obtained from LUT-based sizing.
Final device widths and channel lengths were adjusted during
simulation to account for parasitic capacitances, headroom constraints,
and stability requirements.

The final OTA schematic is provided in `schematics/`.

---

## Simulation Results

AC simulations were performed using ngspice to validate gain, bandwidth,
and stability of the OTA under nominal conditions.

Measured performance:
- DC gain: ≈ 60 dB (simulated: 59.98 dB)
- Unity-gain bandwidth (UGB): ≈ 320 MHz
- Phase margin: 64° (stable operation)
- Power consumption: 216 µW

Representative magnitude and phase plots are provided in
`simulations/`.

---

## Tools Used

- Xschem  
- ngspice  
- Python  
- SKY130 PDK  

---

## Status and Future Work

- OTA design, sizing, and AC verification completed  
- LDO and high-pass filter designs planned as future work  


