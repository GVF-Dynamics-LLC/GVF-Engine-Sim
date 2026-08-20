# GlymphoVasomotor Field (GVF) SNN Simulator

**Computational Proof-of-Concept & Simulation Suite for Dynamic AC Threshold Modulation in Spiking Neural Networks.**

[![License: GPL v3](https://img.shields.org/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Overview
The **Gated Vector Field (GVF) Engine** introduces a dynamic, time-dependent AC threshold wave ($V_{\text{th}}(t)$) across Spiking Neural Network (SNN) membrane arrays. Rather than relying on static DC firing thresholds, GVF modulates neuronal sensitivity via a phase-locked sinusoidal carrier wave:

$$\text{Threshold}(t) = V_{\text{base}} + A \cdot \sin(2\pi f t + \phi)$$

### Architectural Pillars
* **1. Compute-In-Memory Bitline Gating:** Evaluates activation energy inside SRAM arrays to freeze downstream ALU clock trees in under 0.01 ms when vectors fall below $V_{\text{th}}(t)$.
* **2. Global Workspace Synchronization:** Functions as an algorithmic metronome across middle layers, stabilizing latent reasoning states at milliwatt edge power.
* **3. Environmental Harmonic Alignment:** Phase-locks internal carrier frequencies ($f$) to physical domain rhythms (e.g., 60 Hz power grid, 1 Hz cardiac cycles).
* **4. Entropy-Aware Fail-Safes:** Automatically monitors activation entropy ($H(x)$) and bypasses gating during complex logical spikes to ensure zero loss of context.



## Benchmark Summary (Tonic N-MNIST)
| Configuration | Amplitude ($A$) | Frequency ($f$) | Epoch 5 Accuracy | Optimization Delta |
| :--- | :--- | :--- | :--- | :--- |
| **Config C (DC Control)** | $0.0\text{V}$ | $0.0\text{ Hz}$ | 96.16% | Baseline |
| **Config B (GVF Sync)** | $0.4\text{V}$ | $50.0\text{ Hz}$ | **96.53%** | **+0.37% Accuracy Gain** |

## Patent & Intellectual Property Notice
**Copyright © 2026 TCPartsDirect, LLC. All rights reserved.**
The underlying hardware architectures, Compute-In-Memory (CIM) bitline gating mechanisms, and physical integrated clock-gating (ICG) methods associated with the Gated Vector Field (GVF) Engine are protected under pending U.S. Patent Applications owned by **TCPartsDirect, LLC** (Inventor: Antonio Gonzalez).

---

### Patent & Licensing Notice
* **Software License:** The Python simulation scripts contained in `src/` are licensed under the GNU General Public License v3.0 (GPLv3).
* **Hardware Patent Reservation:** The software license granted herein applies exclusively to the execution and modification of the software code. NO LICENSE, express or implied, by estoppel or otherwise, is granted under GPLv3 to manufacture, fabricate, sell, or distribute physical hardware architectures, including but not limited to SRAM Compute-In-Memory (CIM) bitline gating circuits, Integrated Clock Gating (ICG) logic, entropy-aware bypass circuitry, or phase-locked environmental synchronization hardware described in the documentation. These hardware innovations are protected under U.S. Provisional Patent Application No. 64/134,522 owned by TCPartsDirect, LLC.
* **Implementation Scope:** The files in `src/` provide algorithmic PyTorch/snnTorch software emulation ($V_{\text{th}}(t)$). Physical SystemVerilog / RTL models for SRAM CIM bitlines and ICG cell trees are maintained in private repositories under TCPartsDirect, LLC.
* **Frequency Notation:** Frequency parameters ($f = 0.05$) represent cycles per simulation step, corresponding to $50\text{ Hz}$ under a $1\text{ ms}$ discrete time-step ($\Delta t = 1\text{ ms}$).

---

### Ownership, Authorship & Assignee Attestation
* **Sole Author & Inventor:** Antonio Gonzalez (GitHub Account: `gonguz123-blip`).
* **Copyright Holder & Assignee:** TCPartsDirect, LLC.
* **Legal Chain of Title:** Antonio Gonzalez is the sole author of the codebase and sole inventor under U.S. Provisional Patent Application No. 64/134,522. All intellectual property, copyrights, trade secrets, and patent rights embodied in this repository are assigned exclusively to TCPartsDirect, LLC. There are no third-party contributors or undisclosed co-inventors.
