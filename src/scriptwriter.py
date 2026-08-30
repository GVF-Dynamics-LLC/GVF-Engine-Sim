import json
import random
from pathlib import Path

class AlgorithmicHookAdapter:
    @staticmethod
    def generate_hooks(topic_name, gvf_remediation):
        return f"Modern AI infrastructure is facing a severe roadblock with {topic_name}. Here is how GVF phase-locked hardware governance resolves it at sub-0.01ms speeds."

class VideoScriptwriterAgent:
    def __init__(self, telemetry_payload, trend_payload=None):
        self.payload = telemetry_payload
        self.trend = trend_payload or {}
        self.task_name = telemetry_payload.get("task", "Neuromorphic Benchmark")
        self.results = telemetry_payload.get("results", {})
        
    def build_longform_script(self):
        topic = self.trend.get("detected_trend", "Edge AI Thermal Throttling & Energy Waste")
        anxiety = self.trend.get("industry_anxiety", "Autonomous vision sensors overheat and waste 70% of energy processing static zero-value frames.")
        solution = self.trend.get("gvf_remediation", "GVF Sub-0.01ms Phase-Locked Dynamic Thresholding gates sub-threshold FLOP waste at the transistor bitline layer.")
        mac_avoided = self.results.get("mac_reduction", "70.60%")

        return {
            "format": "Long-Form Technical Video (16:9)",
            "target_duration_sec": 150,
            "title": f"Solving {topic}: GVF Hardware Governance Architecture Breakdown",
            "tags": ["EdgeAI", "NeuromorphicComputing", "HardwareGovernance", "Semiconductors", "RISCV"],
            "chapters": [
                {
                    "section": "1. Executive Trend Analysis & Industry Anxiety",
                    "speech": f"Across modern artificial intelligence deployments, a major engineering crisis has emerged around {topic}. Specifically, {anxiety} As models scale, traditional GPUs and software pruning frameworks struggle to keep up without introducing unacceptable latency."
                },
                {
                    "section": "2. GVF Dynamic Threshold Core Architecture",
                    "speech": f"To solve this, GVF Dynamics developed bitline-level phase-locked dynamic thresholding. {solution} By enforcing physical gating before arithmetic logic units fire, sub-threshold waste is eliminated deterministically."
                },
                {
                    "section": "3. Empirical Benchmark Verification",
                    "speech": f"Let us inspect the empirical simulation telemetry from GVF Engine Sim during our {self.task_name} benchmark. As demonstrated on screen, event-driven signal bursts pass through cleanly while redundant cycles are pruned, achieving a confirmed {mac_avoided} reduction in compute waste."
                },
                {
                    "section": "4. Developer Access & SDK Licensing",
                    "speech": "The complete open-source simulation core is available on GitHub for evaluation. For commercial silicon IP licensing, FPGA integration, and enterprise SDK access, visit gvfdynamics.com or polar.sh/gvfdynamics."
                }
            ]
        }

    def build_shorts_script(self):
        mac_avoided = self.results.get("mac_reduction", "70.60%")
        topic = self.trend.get("detected_trend", "Edge AI Energy Waste")
        hook = f"We just eliminated {mac_avoided} of compute waste on edge silicon!"
        return {
            "format": "YouTube Shorts (9:16)",
            "target_duration_sec": 25,
            "title": f"70.6% FLOP Power Saved on Edge Silicon! #Shorts",
            "tags": ["Shorts", "EdgeAI", "Semiconductors"],
            "hook_speech": hook
        }

def generate_video_scripts(telemetry_file="data/latest_agent_output.json", trend_file="data/latest_trend_insight.json"):
    telemetry_data = {"task": "bench_dvs", "results": {"mac_reduction": "70.60%"}}
    trend_data = {}
    
    if Path(telemetry_file).exists():
        with open(telemetry_file, "r") as f:
            telemetry_data = json.load(f)
            
    if Path(trend_file).exists():
        with open(trend_file, "r") as f:
            trend_data = json.load(f)

    writer = VideoScriptwriterAgent(telemetry_data, trend_data)
    shorts = writer.build_shorts_script()
    longform = writer.build_longform_script()

    script_payload = {"shorts": shorts, "longform": longform}
    with open("data/latest_video_scripts.json", "w") as f:
        json.dump(script_payload, f, indent=2)

    print("[SCRIPTWRITER AGENT] Successfully generated Trend Remediation video scripts!")

if __name__ == "__main__":
    generate_video_scripts()