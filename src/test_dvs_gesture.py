import torch
import numpy as np

class GVFCarrierWaveGenerator:
    def __init__(self, v_base=1.0, amplitude=0.4, frequency=0.05, phase=0.0):
        self.v_base = v_base
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def get_threshold(self, step):
        return self.v_base + self.amplitude * np.sin(2 * np.pi * self.frequency * step + self.phase)

def run_synthetic_dvs_test():
    print("==================================================")
    print("Synthetic DVS Event Stream & GVF Wave Execution")
    print("==================================================")
    
    timesteps = 500
    sensor_res = (128, 128)
    
    torch.manual_seed(42)
    gvf_gen = GVFCarrierWaveGenerator(v_base=1.0, amplitude=0.4, frequency=0.05)
    suppressed_steps = 0
    
    # Generate realistic dynamic event stream with varying energy density over time
    for t in range(timesteps):
        # Vary sparsity dynamically between 5% and 25% (simulating gesture movement)
        dynamic_sparsity = 0.15 + 0.10 * np.sin(2 * np.pi * 0.02 * t)
        frame = (torch.rand(*sensor_res) < dynamic_sparsity).float()
        
        # Scale energy to oscillate around the 1.0V baseline
        signal_energy = frame.mean().item() * 6.67 
        v_th = gvf_gen.get_threshold(t)
        
        if signal_energy < v_th:
            suppressed_steps += 1
            
    bypassed_ratio = (suppressed_steps / timesteps) * 100
    print("--------------------------------------------------")
    print(f"[Result] Total Timesteps: {timesteps} | GVF Suppressed Timesteps: {suppressed_steps}")
    print(f"[Result] FLOP Bypassing Ratio: {bypassed_ratio:.2f}%")
    print("==================================================")

if __name__ == "__main__":
    run_synthetic_dvs_test()
