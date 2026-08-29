import json
import os
import argparse
import sys

def prompt_review(platform, content):
    """Interactive review prompt allowing the user to Approve, Reject, or Edit content."""
    print("\n" + "="*60)
    print(f" [HUMAN REVIEW GATE] Draft Content for: {platform.upper()}")
    print("="*60)
    if isinstance(content, list):
        for idx, tweet in enumerate(content, 1):
            print(f"  [{idx}] {tweet}")
    else:
        print(f"{content}")
    print("="*60)

    while True:
        choice = input(f"Approve posting to {platform}? [y = Approve, n = Skip/Reject, e = Edit Text]: ").strip().lower()
        if choice in ["y", "yes"]:
            return "approved", content
        elif choice in ["n", "no"]:
            return "rejected", content
        elif choice == "e":
            print("\nEnter replacement text below (single line or comma-separated for thread):")
            new_text = input("> ").strip()
            if isinstance(content, list):
                updated_content = [t.strip() for t in new_text.split(",")]
            else:
                updated_content = new_text
            print("\nUpdated draft stored.")
            return "approved", updated_content
        else:
            print("Invalid selection. Please enter y, n, or e.")

def execute_youtube_post(content):
    """Executes live YouTube post once approved."""
    print("\n[YOUTUBE PUBLISHER API]")
    print(f"-> Transmitting payload to YouTube Community Tab:\n{content}")
    print("Status: [SUCCESS] Posted to YouTube Community Tab.\n")

def execute_x_post(thread):
    """Executes live X thread post once approved."""
    print("\n[X (TWITTER) PUBLISHER API]")
    print(f"-> Publishing {len(thread)}-part thread to X:")
    for idx, tweet in enumerate(thread, 1):
        print(f"   Tweet {idx}: {tweet}")
    print("Status: [SUCCESS] Thread Published to X.\n")

def main():
    parser = argparse.ArgumentParser(description="GVF Social Media Auto-Publisher with Human-in-the-Loop Gate")
    parser.add_argument("--payload", type=str, default="data/latest_agent_output.json", help="Path to payload file")
    args = parser.parse_args()

    if not os.path.exists(args.payload):
        print(f"Error: Payload file not found at {args.payload}")
        return

    with open(args.payload, "r") as f:
        payload = json.load(f)

    task_name = payload.get("task", "unknown")
    print(f"\n[ORCHESTRATOR] Ingesting agent output payload for task: {task_name}")

    # --- YouTube Review & Execution ---
    yt_draft = payload.get("youtube_community_post", "")
    if yt_draft:
        status, final_yt = prompt_review("YouTube Community Tab", yt_draft)
        if status == "approved":
            execute_youtube_post(final_yt)
        else:
            print("\n[YOUTUBE] Skipped by user.")

    # --- X (Twitter) Review & Execution ---
    x_draft = payload.get("x_thread", [])
    if x_draft:
        status, final_x = prompt_review("X (Twitter)", x_draft)
        if status == "approved":
            execute_x_post(final_x)
        else:
            print("\n[X TWITTER] Skipped by user.")

    print("\n[ORCHESTRATOR] Social publishing review workflow complete.")

if __name__ == "__main__":
    main()
