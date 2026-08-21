# TCPartsDirect, LLC — Provisional Patent Limitation Matrix
**Application No.:** 64/134,522  
**Target Non-Provisional Status:** Hardware-Centered Independent Claims (35 U.S.C. §§ 101, 112)

| Claim Element / Invention Limitation | Provisional App No. 64/134,522 Support | Physical Code / RTL Verification Proof |
| :--- | :--- | :--- |
| **1. Dynamic Bitline Comparator** | Temporally modulated activation threshold comparison before execution. | `hardware/rtl/gvf_bitline_comparator.sv` (`v_th_carrier` vs `signal_energy`) |
| **2. Integrated Clock Gating (ICG)** | Physical switching suppression tree based on memory-side decision. | `hardware/rtl/gvf_bitline_comparator.sv` (`gated_clk_enable` output logic) |
| **3. Safe Decision Region ($\epsilon$ Band)** | Thermal/analog noise fail-open buffer around dynamic threshold. | `hardware/rtl/gvf_bitline_comparator.sv` (`EPSILON = 16'h000F` condition) |
| **4. Pillar 3 Entropy Breaker** | Malformed signal / cyber-attack flood lockout mechanism. | `hardware/rtl/gvf_bitline_comparator.sv` (`entropy_val > entropy_thresh`) |
| **5. Real Neuromorphic Pruning** | Measured dynamic MAC operation reduction on sparse physical event data. | `src/bench_nmnist.py` (**15.56% MACs Avoided**) |
| **6. Sparse Gesture Stream Pruning** | High-sparsity spatiotemporal event stream MAC suppression. | `src/bench_real_dvs.py` (**70.60% MACs Avoided**) |
| **7. Physical Cyber-Mitigation** | 100% clock suppression during spike-storm flood attacks. | `src/test_cyber_breaker.py` (**100.00% $H(x)$ Mitigation**) |