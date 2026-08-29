import json
import os
import argparse
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

def execute_x_post(thread):
    """Executes live X thread post via Tweepy if API keys exist in .env."""
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    if api_key and api_secret and access_token and access_token_secret:
        try:
            import tweepy
            client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
            print("\n[X (TWITTER) PUBLISHER - LIVE API]")
            previous_tweet_id = None
            for idx, tweet_text in enumerate(thread, 1):
                print(f"  Publishing Tweet {idx}/{len(thread)} to @GVFDYNAMICS...")
                if previous_tweet_id:
                    res = client.create_tweet(text=tweet_text, in_reply_to_tweet_id=previous_tweet_id)
                else:
                    res = client.create_tweet(text=tweet_text)
                previous_tweet_id = res.data["id"]
            print("Status: [LIVE SUCCESS] Thread Published to X (@GVFDYNAMICS).\n")
            return
        except Exception as e:
            print(f"\n[X API ERROR] Live tweet failed: {e}\nFalling back to simulation mode.")
    
    # Simulation fallback
    print("\n[X (TWITTER) PUBLISHER - SIMULATION]")
    print(f"-> Simulated posting {len(thread)}-part thread to X:")
    for idx, tweet in enumerate(thread, 1):
        print(f"   Tweet {idx}: {tweet}")
    print("Status: [SIMULATED SUCCESS] Thread Published.\n")

def execute_youtube_post(content):
    """Simulates posting to YouTube Community Tab."""
    print("\n[YOUTUBE PUBLISHER API]")
    print(f"-> Transmitting payload to YouTube Community Tab:\n{content}")
    print("Status: [SIMULATED SUCCESS] Posted to YouTube Community Tab.\n")

def main():
    parser = argparse.ArgumentParser(description="GVF Social Media Auto-Publisher with Live X API Integration")
    parser.add_argument("--payload", type=str, default="data/latest_agent_output.json", help="Path to payload file")
    args = parser.parse_args()

    if not os.path.exists(args.payload):
        print(f"Error: Payload file not found at {args.payload}")
        return

    with open(args.payload, "r") as f:
        payload = json.load(f)

    task_name = payload.get("task", "unknown")
    print(f"\n[ORCHESTRATOR] Ingesting agent output payload for task: {task_name}")

    # --- YouTube Review ---
    yt_draft = payload.get("youtube_community_post", "")
    if yt_draft:
        status, final_yt = prompt_review("YouTube Community Tab", yt_draft)
        if status == "approved":
            execute_youtube_post(final_yt)
        else:
            print("\n[YOUTUBE] Skipped by user.")

    # --- X (Twitter) Review & Live Execution ---
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
