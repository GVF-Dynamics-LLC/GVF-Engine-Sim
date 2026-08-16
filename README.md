# GlymphoVasomotor Field (GVF) SNN Simulator

**Computational Proof-of-Concept & Simulation Suite for Dynamic AC Threshold Modulation in Spiking Neural Networks.**

[![License: GPL v3](https://img.shields.org/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Overview
The **Gated Vector Field (GVF) Engine** introduces a dynamic, time-dependent AC threshold wave ($V_{\text{th}}(t)$) across Spiking Neural Network (SNN) membrane arrays. Rather than relying on static DC firing thresholds, GVF modulates neuronal sensitivity via a phase-locked sinusoidal carrier wave:

$$\text{Threshold}(t) = V_{\text{base}} + A \cdot \sin(2\pi f t + \phi)$$

## Key Architectural Applications
1. **Low-Power Global Workspaces:** Functions as an algorithmic metronome across middle-layer Feed-Forward Networks (FFNs), maintaining temporal coherence and reasoning stability at milliwatt edge power.
2. **Compute-In-Memory (CIM) Bitline Gating:** Integrates with hardware analog comparators to freeze downstream ALU clock trees in under 0.01 ms whenever activation vectors fall below $V_{\text{th}}(t)$.
3. **Environmental Harmonic Alignment:** Internal carrier wave frequencies ($f$) can be phase-locked to physical environment rhythms—such as a 60 Hz power grid for transient fault detection or a 1 Hz cardiac cycle for biomedical telemetry.


## Benchmark Summary (Tonic N-MNIST)
| Configuration | Amplitude ($A$) | Frequency ($f$) | Epoch 5 Accuracy | Optimization Delta |
| :--- | :--- | :--- | :--- | :--- |
| **Config C (DC Control)** | $0.0\text{V}$ | $0.0\text{ Hz}$ | 96.16% | Baseline |
| **Config B (GVF Sync)** | $0.4\text{V}$ | $50.0\text{ Hz}$ | **96.53%** | **+0.37% Accuracy Gain** |

## Patent & Intellectual Property Notice
**Copyright © 2026 TCPartsDirect, LLC. All rights reserved.**
The underlying hardware architectures, Compute-In-Memory (CIM) bitline gating mechanisms, and physical integrated clock-gating (ICG) methods associated with the Gated Vector Field (GVF) Engine are protected under pending U.S. Patent Applications owned by **TCPartsDirect, LLC** (Inventor: Antonio Gonzalez).
