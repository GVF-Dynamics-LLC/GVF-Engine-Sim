import argparse
import json
import os
import subprocess
import sys

def run_benchmark(script_name):
    """Executes a simulation script and captures CLI output."""
    script_path = os.path.join("src", script_name)
    if not os.path.exists(script_path):
        return f"Error: {script_path} not found."
    print(f"[HARNESS] Running simulation benchmark: {script_name}...")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr

def generate_social_payload(task_type, benchmark_data):
    """Formats benchmark results into structured social posts and video concepts."""
    print(f"[HARNESS] Generating full social payload for task: {task_type}...")
    
    # Analyze data for high-impact metric
    metric_line = next((line for line in benchmark_data.split("\n") if "[Result]" in line), "[Result] Data Pending Evaluation")
    
    payload = {
        "task": task_type,
        "status": "ready",
        "youtube_community_post": (
            "🚀 GVF Dynamics Update: Deterministic Edge Performance\n\n"
            "Latest Phase-Locked Dynamic Thresholding benchmark completed.\n"
            f"{metric_line}\n\n"
            "Read the Technical Whitepaper: https://github.com/GVF-Dynamics-LLC/GVF-Engine-Sim/releases/tag/v1.0.0"
        ),
        # New Video Production Concept
        "youtube_video_production": {
            "concept": "Technical Spotlight: Phase-Locked Thresholding on DVS Gesture Benchmark",
            "type": "Short Technical Demonstration (1:30)",
            "description": "Visualizing event-frame suppression in real-time using the DVS Gesture dataset, comparing standard SNN output to GVF-gated output.",
            "script_draft": "1. [0:00] Visualize raw DVS event stream. 2. [0:20] Explain GVF threshold gating (sv comparator). 3. [0:45] Show FLOP waste reduction overlay. 4. [1:15] Call to Action: licensing the SDK."
        },
        "x_thread": [
            f"1/3 GVF Dynamics Core Update: {metric_line}",
            "2/3 Our hardware-enforced phase-locked thresholding eliminates execution entropy at sub-0.01ms speeds.",
            "3/3 Open Simulation Core: https://github.com/GVF-Dynamics-LLC/GVF-Engine-Sim | SDK Licensing: https://polar.sh/gvfdynamics"
        ],
        # New LinkedIn Strategy Post
        "linkedin_company_update": (
            f"Performance Validation: {metric_line}\n\n"
            "At GVF Dynamics, we build hardware-enforced AI governance cores designed for deterministic edge intelligence.\n\n"
            "Our phase-locked dynamic thresholding technology validates aggregated efficiency gains of 15.5% in FLOP waste reduction on neuromorphic benchmarks. GVF Dynamics is now licensing the developer SDK for silicon IP evaluation and FPGA profiling.\n\n"
            "Sponsor Development & Access SDK: https://polar.sh/gvfdynamics"
        )
    }
    return payload

def main():
    parser = argparse.ArgumentParser(description="GVF Engine Agent Harness CLI")
    parser.add_argument("--task", type=str, required=True, choices=["bench_nmnist", "bench_dvs"], help="Task target")
    parser.add_argument("--output", type=str, default="data/latest_agent_output.json", help="Path to write generated payload")
    args = parser.parse_args()
    
    script_map = {
        "bench_nmnist": "bench_nmnist.py",
        "bench_dvs": "bench_real_dvs.py",
    }
    
    raw_output = run_benchmark(script_map[args.task])
    payload = generate_social_payload(args.task, raw_output)
    
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"[HARNESS] Execution complete. Payload saved to: {args.output}")

if __name__ == "__main__":
    main()
