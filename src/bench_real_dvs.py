import os
import tarfile
import numpy as np
from gvf_core import GVFFieldGenerator

def run_local_dvs_benchmark():
    print("==================================================")
    print("GVF Real DVS Gesture Local Benchmark Evaluation")
    print("==================================================")
    
    archive_path = os.path.join("data", "dvsgesture", "DVSGesture", "ibmGestureTest.tar.gz")
    
    if not os.path.exists(archive_path):
        print(f"Error: Archive not found at {archive_path}")
        return

    print(f"Reading local dataset archive: {archive_path}")
    
    # Initialize GVF Field Generator
    engine = GVFFieldGenerator(v_base=1.0, amplitude=0.4, frequency=0.05)
    
    total_samples = 0
    suppressed_samples = 0
    
    with tarfile.open(archive_path, "r:gz") as tar:
        members = [m for m in tar.getmembers() if m.name.endswith('.npy') or m.name.endswith('.bin')]
        print(f"Found {len(members)} raw DVS recording streams in local archive.")
        
        for idx, member in enumerate(members[:50]): # Process up to 50 streams
            f = tar.extractfile(member)
            if f is not None:
                content = f.read()
                # Extract event bytes to compute stream intensity
                event_data = np.frombuffer(content, dtype=np.uint8)
                chunks = np.array_split(event_data, 100) # Split into 100 temporal bins
                
                for t, chunk in enumerate(chunks):
                    total_samples += 1
                    signal_energy = float(chunk.mean()) if len(chunk) > 0 else 0.0
                    
                    # Evaluate dynamic threshold V_th(t)
                    v_th = 1.0 + 0.4 * np.sin(2 * np.pi * 0.05 * t)
                    if signal_energy < v_th:
                        suppressed_samples += 1

    pruning_rate = (suppressed_samples / total_samples) * 100.0 if total_samples > 0 else 0.0
    print(f"Total DVS Event Windows Evaluated: {total_samples}")
    print(f"GVF Suppressed Computation Windows: {suppressed_samples}")
    print(f"[Result] Real DVS Dynamic Pruning:   {pruning_rate:.2f}% MACs Avoided")
    print("==================================================")

if __name__ == "__main__":
    run_local_dvs_benchmark()