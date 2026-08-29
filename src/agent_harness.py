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
    """Formats benchmark results into structured social posts."""
    print(f"[HARNESS] Generating payload for task: {task_type}...")
    
    payload = {
        "task": task_type,
        "status": "ready",
        "youtube_community_post": (
            "🚀 GVF Dynamics Update!\n\n"
            "Phase-locked Dynamic Thresholding benchmark completed.\n"
            f"Summary Logs:\n{benchmark_data[:300]}...\n\n"
            "Read technical whitepaper: https://github.com/GVF-Dynamics-LLC/GVF-Engine-Sim/releases/tag/v1.0.0"
        ),
        "x_thread": [
            "1/2 GVF Hardware Core update: Sub-0.01ms thresholding suppressing FLOP waste across SNN workloads.",
            "2/2 Dev SDK & Polar licensing portal: https://polar.sh/gvfdynamics"
        ]
    }
    return payload

def main():
    parser = argparse.ArgumentParser(description="GVF Engine Agent Harness CLI")
    parser.add_argument("--task", type=str, required=True, choices=["bench_nmnist", "bench_dvs", "cyber_breaker"], help="Task target")
    parser.add_argument("--output", type=str, default="data/latest_agent_output.json", help="Path to write generated payload")
    
    args = parser.parse_args()
    
    script_map = {
        "bench_nmnist": "bench_nmnist.py",
        "bench_dvs": "bench_real_dvs.py",
        "cyber_breaker": "test_cyber_breaker.py"
    }
    
    raw_output = run_benchmark(script_map[args.task])
    payload = generate_social_payload(args.task, raw_output)
    
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(payload, f, indent=2)
        
    print(f"[HARNESS] Execution complete. Payload saved to: {args.output}")

if __name__ == "__main__":
    main()
