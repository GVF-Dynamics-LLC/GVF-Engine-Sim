import json
import os
import argparse

def post_to_youtube(payload):
    """Simulates posting to YouTube Community Posts via API."""
    post_text = payload.get("youtube_community_post", "")
    print("\n[YOUTUBE PUBLISHER]")
    print("--------------------------------------------------")
    print(f"Posting to YouTube Channel...\nContent:\n{post_text}")
    print("--------------------------------------------------")
    print("Status: [SUCCESS] Posted to YouTube Community Tab.\n")

def post_to_x(payload):
    """Simulates posting thread to X (Twitter) via API v2."""
    thread = payload.get("x_thread", [])
    print("[X (TWITTER) PUBLISHER]")
    print("--------------------------------------------------")
    print(f"Publishing {len(thread)}-part thread...")
    for idx, tweet in enumerate(thread, 1):
        print(f"  Tweet {idx}: {tweet}")
    print("--------------------------------------------------")
    print("Status: [SUCCESS] Thread Published to X.\n")

def main():
    parser = argparse.ArgumentParser(description="GVF Social Media Auto-Publisher")
    parser.add_argument("--payload", type=str, default="data/latest_agent_output.json", help="Path to payload file")
    args = parser.parse_args()

    if not os.path.exists(args.payload):
        print(f"Error: Payload file not found at {args.payload}")
        return

    with open(args.payload, "r") as f:
        payload = json.load(f)

    task_name = payload.get("task", "unknown")
    print(f"[PUBLISHER] Ingesting payload for task: {task_name}")
    post_to_youtube(payload)
    post_to_x(payload)

if __name__ == "__main__":
    main()
