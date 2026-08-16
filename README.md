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
