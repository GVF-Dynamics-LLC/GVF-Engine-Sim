# GVF Engine™: Commercial Access & Licensing Policy

**Copyright (c) 2026 TCPartsDirect, LLC. All rights reserved.**  
**Sole Inventor:** Antonio Gonzalez  
**Patent Status:** Intellectual Property Pending / Patent Reservation Active  

This document defines the official access tiers, usage rights, and commercial boundaries for the **GVF Engine™** (Phase-Locked AC Dynamic Thresholding, Bitline-Level SRAM Gating, and Clock-Tree Suppression Architecture) and its associated orchestration software.

---

## 🏛️ Architecture Overview: Software vs. Silicon IP

The GVF technology ecosystem is strictly separated into two distinct layers:
1. **The Software Emulation & Orchestrator Toolchain:** PyTorch / snnTorch simulation environments, benchmark scripts, and automated execution harnesses.
2. **The Hardware Intellectual Property (RTL):** Synthesizable SystemVerilog models, analog/digital threshold generator top-level schematics, bitline comparator specs, and clock-tree freeze circuit descriptions.

---

## 📊 Three-Tier Access Model

| Feature / Asset | Tier 1: Open Simulation | Tier 2: Commercial Tooling | Tier 3: Enterprise Soft IP |
| :--- | :--- | :--- | :--- |
| **Target Audience** | Academics, Researchers, Public | Independent Engineers, AI Devs | SoC Architects, Chip Designers |
| **Primary Channel** | Open GitHub Repository | [Polar.sh Commercial Tier](https://polar.sh/checkout/polar_c_ifALsQATNmgCRfyPPhyLXThLudm4wnewFTX4I0QMeeR) | Technical Evaluation Agreement (TEA) |
| **License Type** | GNU General Public License v3 | Commercial Developer License | Proprietary / NDA Soft IP License |
| **PyTorch Simulation Engine** | Full Access (GVF-Engine-Sim) | Full Access | Full Access |
| **Agent Orchestrator & Harness** | Basic Scripts | Advanced Tooling & Media Suite | Full Source & Custom Pipeline |
| **SystemVerilog / RTL Access** | ❌ Restricted | ❌ Restricted | ✅ Provided Under NDA / TEA |
| **Silicon Rights / Production** | ❌ Prohibited | ❌ Prohibited | ✅ Negotiated Royalty / License |

---

## 🔍 Tier Details

### Tier 1: Public / Open Source (GPLv3)
* **Purpose:** Academic research, community validation, and open emulation.
* **Included:** PyTorch/snnTorch algorithmic simulation models (src/), basic benchmark evaluation scripts, public documentation, and disclaimers.
* **Limitations:** Code is governed by GNU GPLv3. All quantitative metrics derived from this tier represent software simulation outcomes only (no silicon or FPGA validation). Does **not** convey rights to synthesizable hardware descriptions or commercial silicon fabrication.

### Tier 2: Commercial Developer Access (Polar.sh)
* **Purpose:** Internal commercial evaluation, automated benchmarking, and advanced parameter sweeps.
* **Included:** Full source access to the multi-agent orchestrator harness, automated telemetry rendering (16:9 & 9:16 assets), dynamic thresholding (V_th(t)) parameter sweep tools, and commercial evaluation rights.
* **Access Link:** [Purchase Commercial Developer Access on Polar.sh](https://polar.sh/checkout/polar_c_ifALsQATNmgCRfyPPhyLXThLudm4wnewFTX4I0QMeeR)
* **Limitations:** Grants commercial software usage rights for the orchestrator and SDK only. **Does not include SystemVerilog RTL, netlists, or hardware manufacturing rights.**

### Tier 3: Enterprise Soft IP (RTL & Silicon Licensing)
* **Purpose:** FPGA mapping, ASIC integration, and SoC hardware design.
* **Included:** Synthesizable SystemVerilog modules (V_th(t) AC envelope generator, bitline-level SRAM gating interfaces, and downstream clock-tree freeze logic), timing constraints, verification testbenches, and direct engineering support.
* **Process:** Executed via a formal **Technical Evaluation Agreement (TEA)** and Bilateral Non-Disclosure Agreement (NDA).

---

## 📬 Enterprise & Silicon Licensing Contact

SoC architectural teams, edge-AI chipmakers, and hardware engineering groups seeking Technical Evaluation Agreements (TEAs) or synthesizable RTL access should contact:

* **Entity:** TCPartsDirect, LLC  
* **Lead Inventor:** Antonio Gonzalez  
* **Inquiries & TEAs:** contact@gvfdynamics.com  
* **Official Repository:** [github.com/GVF-Dynamics-LLC/GVF-Engine-Sim](https://github.com/GVF-Dynamics-LLC/GVF-Engine-Sim)  