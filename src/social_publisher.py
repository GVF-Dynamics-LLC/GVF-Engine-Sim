import json
import os
import shutil
import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv
import tweepy

load_dotenv()

POLAR_CHECKOUT_URL = "https://polar.sh/checkout/polar_c_ifALsQATNmgCRfyPPhyLXThLudm4wnewFTX4I0QMeeR"

def sanitize_tweet_text(text):
    text = text.strip()
    # If a tweet starts directly with an @ handle, prefix it with an emoji/space so X doesn't hide it in Replies
    if text.startswith("@"):
        text = f"🚀 {text}"
    return text

def prompt_review(platform, content):
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
            print("\nEnter replacement text below:")
            new_text = input("> ").strip()
            updated_content = [t.strip() for t in new_text.split(",")] if isinstance(content, list) else new_text
            return "approved", updated_content
        else:
            print("Invalid selection. Please enter y, n, or e.")

def publish_x_thread(thread_tweets):
    api_key = os.getenv("TWITTER_API_KEY") or os.getenv("X_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET") or os.getenv("X_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN") or os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET") or os.getenv("X_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("[X TWITTER WARNING] API keys incomplete in .env. Running in SIMULATED mode.")
        print("Status: [SIMULATED SUCCESS] Thread logged.")
        return False

    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

        last_tweet_id = None
        for idx, tweet_text in enumerate(thread_tweets, 1):
            cleaned_text = sanitize_tweet_text(tweet_text)
            
            if last_tweet_id:
                response = client.create_tweet(text=cleaned_text, in_reply_to_tweet_id=last_tweet_id)
            else:
                response = client.create_tweet(text=cleaned_text)

            last_tweet_id = response.data["id"]
            print(f"[X LIVE TWEET {idx}/{len(thread_tweets)}] Posted ID: {last_tweet_id}")

        print("\nStatus: [LIVE SUCCESS] Full Thread Successfully Published to Main Feed!")
        return True

    except Exception as e:
        print(f"[X TWITTER ERROR] Failed to post thread: {e}")
        return False

def get_latest_video(prefix, video_dir="data/videos"):
    video_path = Path(video_dir)
    if not video_path.exists():
        return None
    files = sorted(video_path.glob(f"{prefix}*.mp4"), key=os.path.getmtime, reverse=True)
    return str(files[0]) if files else None

def cleanup_video(video_file):
    if video_file and Path(video_file).exists():
        try:
            Path(video_file).unlink()
            print(f"[ORCHESTRATOR CLEANUP] Cleaned up staged render: {Path(video_file).name}")
        except Exception:
            pass

def run_social_orchestrator():
    payload_file = Path("data/latest_agent_output.json")
    x_thread = []

    if payload_file.exists():
        with open(payload_file, "r") as f:
            data = json.load(f)
            x_thread = data.get("social_payloads", {}).get("x_twitter", {}).get("thread", [])

    if not x_thread:
        x_thread = [
            "GVF Dynamics just suppressed FLOP waste on edge silicon during benchmark testing!",
            "Unregulated GPUs waste massive clock cycles on dynamic noise. GVF phase-locked thresholding gates waste at sub-0.01ms speeds.",
            f"🔗 Open Core: github.com/GVF-Dynamics-LLC/GVF-Engine-Sim\n🛒 Commercial SDK: {POLAR_CHECKOUT_URL} #EdgeAI"
        ]

    # X (Twitter) Gate
    x_status, x_content = prompt_review("X (Twitter)", x_thread)
    if x_status == "approved":
        print("[X TWITTER] Publishing live thread to X API...")
        publish_x_thread(x_content)

if __name__ == "__main__":
    run_social_orchestrator()