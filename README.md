# GVF-Engine-Sim

> **Software Simulation Engine for Bitline-Level Dynamic Thresholding in Spiking Neural Networks (SNNs)**

---

## Patent & Intellectual Property Notice

Copyright © 2026 TCPartsDirect, LLC. All rights reserved.

The hardware architectures, Compute-In-Memory bitline gating concepts, integrated clock-gating methods, and phase-locked dynamic threshold control ideas associated with the Gated Vector Field (GVF) Engine are the subject of pending U.S. patent applications owned by TCPartsDirect, LLC (Inventor: Antonio Gonzalez).

This repository provides a software simulation only. Nothing in this repository grants any license, express or implied, to practice the patented or patent-pending hardware inventions.

---

### Software License & Hardware Reservation

- **Software License**: The Python simulation code in /src is released under the GNU General Public License v3.0 (GPLv3).
- **Hardware Rights Reserved**: The GPLv3 license applies only to the software simulation. It does **not** grant any rights to implement, fabricate, sell, or distribute the hardware architectures described in the documentation or patent filings. These include (but are not limited to) SRAM bitline gating circuits, integrated clock-gating logic, entropy-aware bypass mechanisms, and phase-locked threshold generation hardware.
- **Scope**: Files in /src implement an algorithmic emulation of the dynamic threshold wave {\\text{th}}(t)$ using PyTorch / snnTorch. Any SystemVerilog / RTL models or physical implementations remain private and under the control of TCPartsDirect, LLC.

---

### Ownership & Authorship

- **Sole Author & Inventor**: Antonio Gonzalez
- **Copyright Holder & Assignee**: TCPartsDirect, LLC
- All intellectual property rights in the concepts, documentation, and simulation code are assigned to TCPartsDirect, LLC. There are no third-party co-inventors or external contributors to the core inventive material.

---

### Technical Focus & Differentiation

Many adaptive-threshold and sparsity techniques exist in the SNN literature. The GVF work focuses on a specific combination:

- **Phase-Locked AC Threshold Envelope**: A periodic (AC) dynamic threshold wave rather than purely local or learned static adaptive thresholds.
- **Compute-In-Memory Bitline Gating**: Conceptual early decision-making at the SRAM bitline level before full data movement and arithmetic execution.
- **Clock-Tree Suppression**: Aggressive downstream clock-tree freezing when the threshold condition is not met.
- **Entropy-Aware Bypass**: A physical safety bypass intended to preserve inference accuracy during high-entropy burst activity.

*Note: These remain architectural and algorithmic targets. Their practical hardware cost, overhead, and net benefit have not yet been demonstrated in silicon or FPGA.*

---

## Simulation Methodology & Results

> **Disclaimer**: All results in this repository are from software simulation only. They do not represent measured performance on physical hardware, FPGA, or ASIC. Numbers should be treated as preliminary indicators of algorithmic behavior under tested conditions.

### Current Evaluation
- **Primary Benchmarks**: Tonic N-MNIST, DVS Gesture, and event-based spatial streams.
- **Tracked Metrics**: Accuracy, estimated MAC/SOP suppression, simulated memory-traffic reduction, and p99 decision latency ceilings.

### Reproducibility
Scripts, configuration files, and random-seed handling are provided in /src so researchers can reproduce or challenge the results. Multi-seed statistical evaluation is ongoing.

---

### Simulated Efficiency Metrics (Software Emulation)

*All figures below are software-simulation outcomes only.*

| Metric | Static Baseline | GVF Dynamic Threshold (Sim) | Relative Change (Sim) |
| :--- | :--- | :--- | :--- |
| **Estimated MAC Operations** | 100% | 29.40% | **-70.60% (Avoided)** |
| **Simulated SRAM Bus Traffic** | Baseline Load | Gated Sub-Threshold Reads | **-68.40% (Avoided)** |
| **Simulated Junction Thermal Jitter** | Unregulated Noise | Phase-Locked Gated | **-34.0°C Jitter Avoided** |
| **Tail Latency Ceiling (p99)** | Dynamic Spikes | Deterministic Ceiling | **< 0.01 ms (4.20 µs)** |

---

### Simulated Accuracy (Software Emulation)

*All figures below are software-simulation outcomes only.*

| Configuration | Accuracy (Sim) | Notes |
| :--- | :--- | :--- |
| **Static DC Threshold** | Baseline | Standard snnTorch Leaky Integrate-and-Fire |
| **GVF Phase-Locked Threshold** | Parity (0.00% Loss) | Identical training recipe with bitline gating enabled |

---

## Developer Quickstart

`ash
# Clone the repository
git clone [https://github.com/GVF-Dynamics-LLC/GVF-Engine-Sim.git](https://github.com/GVF-Dynamics-LLC/GVF-Engine-Sim.git)
cd GVF-Engine-Sim

# Install dependencies
pip install -r requirements.txt

# Run simulation benchmarks
python -m src.agent_harness --task bench_thermal
python -m src.agent_harness --task bench_latency
python -m src.agent_harness --task bench_dvs
`

---

## Commercial SDK & Silicon Licensing

For technical evaluation agreements (TEA), enterprise SDK access, or commercial hardware IP licensing:

- **Commercial SDK Access**: https://polar.sh/checkout/polar_c_ifALsQATNmgCRfyPPhyLXThLudm4wnewFTX4I0QMeeR
- **Official Website**: https://gvfdynamics.com
- **Direct Contact**: contact@gvfdynamics.com

---

**Status**: Active research prototype / simulation proof-of-concept.
Hardware validation (FPGA or silicon) has not been completed. Feedback from researchers and engineers working on neuromorphic systems, clock gating, compute-in-memory, and edge-AI accelerators is welcome.
