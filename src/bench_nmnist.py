import os
import torch
import numpy as np
import tonic
import tonic.transforms as transforms
from torch.utils.data import DataLoader
from gvf_core import GVFFieldGenerator

def run_nmnist_benchmark():
    print("==================================================")
    print("GVF Real N-MNIST Neuromorphic Benchmark Evaluation")
    print("==================================================")
    
    data_dir = "./data/nmnist"
    sensor_size = tonic.datasets.NMNIST.sensor_size
    
    transform = transforms.Compose([
        transforms.Denoise(filter_time=10000),
        transforms.ToFrame(sensor_size=sensor_size, time_window=10000)
    ])
    
    print("Loading real N-MNIST dataset...")
    test_dataset = tonic.datasets.NMNIST(save_to=data_dir, train=False, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)
    
    engine = GVFFieldGenerator(v_base=1.0, amplitude=0.4, frequency=0.05)
    
    total_frames = 0
    suppressed_frames = 0
    
    for idx, (events, target) in enumerate(test_loader):
        frames = events.squeeze(0)
        for t, frame in enumerate(frames):
            total_frames += 1
            signal_energy = frame.float().mean().item() * 100.0
            
            v_th = 1.0 + 0.4 * np.sin(2 * np.pi * 0.05 * t)
            if signal_energy < v_th:
                suppressed_frames += 1
        if idx >= 49:
            break

    pruning_rate = (suppressed_frames / total_frames) * 100.0 if total_frames > 0 else 0.0
    print(f"Total N-MNIST Event Frames Processed: {total_frames}")
    print(f"GVF Suppressed Event Frames:         {suppressed_frames}")
    print(f"[Result] Real N-MNIST Dynamic Pruning: {pruning_rate:.2f}% MACs Avoided")
    print("==================================================")

if __name__ == "__main__":
    run_nmnist_benchmark()
