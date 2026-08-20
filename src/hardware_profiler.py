import torch
import numpy as np
from test_dvs_gesture import GVFCarrierWaveGenerator

def profile_gvf_hardware_metrics():
    print("==================================================")
    print("GVF Hardware Efficiency & Sparsity Profiler (v1.0)")
    print("==================================================")
    
    timesteps = 500
    batch_size = 1
    input_dim = 128 * 128  # 16,384 neurons
    hidden_dim = 256
    
    # Total dense Multiply-Accumulate operations (MACs) without gating
    total_unweighted_macs = timesteps * (input_dim * hidden_dim)
    
    torch.manual_seed(42)
    gvf_gen = GVFCarrierWaveGenerator(v_base=1.0, amplitude=0.4, frequency=0.05)
    
    suppressed_macs = 0
    executed_macs = 0
    active_spikes = 0
    
    for t in range(timesteps):
        dynamic_sparsity = 0.15 + 0.10 * np.sin(2 * np.pi * 0.02 * t)
        frame_activity = (torch.rand(1, input_dim) < dynamic_sparsity).float()
        
        signal_energy = frame_activity.mean().item() * 6.67
        v_th = gvf_gen.get_threshold(t)
        
        layer_macs = input_dim * hidden_dim
        
        if signal_energy < v_th:
            # Bitline gating suppresses downstream ALU clock trees
            suppressed_macs += layer_macs
        else:
            executed_macs += layer_macs
            # Count actual spike operations (SOPs) on executed passes
            active_spikes += torch.count_nonzero(frame_activity).item() * hidden_dim

    flop_bypass_rate = (suppressed_macs / total_unweighted_macs) * 100
    synaptic_ops_sops = active_spikes
    memory_reads_avoided = suppressed_macs  # 1 MAC avoided = 1 SRAM weight read suppressed

    print(f"Total Theoretical MACs (Baseline DC): {total_unweighted_macs:,} ops")
    print(f"GVF Executed MACs:                   {executed_macs:,} ops")
    print(f"GVF Clock-Gated MACs (Suppressed):   {suppressed_macs:,} ops")
    print("--------------------------------------------------")
    print(f"[Metric 1] Synaptic Operations (SOPs): {synaptic_ops_sops:,}")
    print(f"[Metric 2] SRAM Weight Reads Avoided:  {memory_reads_avoided:,} reads")
    print(f"[Metric 3] Dynamic MAC Pruning Rate:  {flop_bypass_rate:.2f}%")
    print("==================================================")

if __name__ == "__main__":
    profile_gvf_hardware_metrics()
