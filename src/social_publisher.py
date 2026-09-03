import json
import os
import shutil
import argparse
import sys
import time
import datetime
from pathlib import Path
from dotenv import load_dotenv
import tweepy

# YouTube API Imports
try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False

load_dotenv()

POLAR_CHECKOUT_URL = "https://polar.sh/checkout/polar_c_ifALsQATNmgCRfyPPhyLXThLudm4wnewFTX4I0QMeeR"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def sanitize_tweet_text(text):
    text = text.strip()
    if text.startswith("@"):
        text = f"🚀 {text}"
    return text

def prompt_review(platform, content):
    print("\n" + "="*60)
    print(f" [HUMAN REVIEW GATE] Draft Content for: {platform.upper()}")
    print("="*60)
    if isinstance(content, list):
        for idx, item in enumerate(content, 1):
            print(f"  [{idx}] {item}")
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

def get_youtube_credentials():
    # 1. Try environment variables from .env
    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")

    if client_id and client_secret and refresh_token:
        print("[YOUTUBE API] Loaded credentials directly from .env configuration.")
        return Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES
        )

    # 2. Fallback to token.json / client_secret.json
    token_path = Path("token.json")
    client_secrets = Path("client_secret.json")

    if token_path.exists():
        return Credentials.from_authorized_user_file(str(token_path), SCOPES)
    elif client_secrets.exists():
        flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets), SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())
        return creds

    return None

def upload_youtube_video(video_path, title, description, category_id="28", privacy_status="public"):
    if not YOUTUBE_AVAILABLE:
        print("[YOUTUBE WARNING] google-api-python-client missing. Skipping live upload.")
        return False

    creds = get_youtube_credentials()
    if not creds:
        print("[YOUTUBE ERROR] No valid YouTube credentials found in .env or json files.")
        return False

    try:
        youtube = build("youtube", "v3", credentials=creds)

        body = {
            "snippet": {
                "title": title[:100],
                "description": description,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status
            }
        }

        media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype="video/mp4")
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        print(f"[YOUTUBE UPLOADING] Uploading video asset: {Path(video_path).name}...")
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f" -> Upload progress: {int(status.progress() * 100)}%")

        video_id = response.get("id")
        print(f"\n[YOUTUBE SUCCESS] Live Video Published! Link: https://youtu.be/{video_id}")
        return True

    except Exception as e:
        print(f"[YOUTUBE ERROR] Upload failed: {e}")
        return False

def publish_x_thread(thread_tweets):
    api_key = os.getenv("TWITTER_API_KEY") or os.getenv("X_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET") or os.getenv("X_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN") or os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET") or os.getenv("X_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("[X TWITTER WARNING] API keys incomplete in .env. Running in SIMULATED mode.")
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
            if idx == 1:
                run_stamp = datetime.datetime.now().strftime("%H:%M")
                cleaned_text = f"[Run {run_stamp}] {sanitize_tweet_text(tweet_text)}"
                response = client.create_tweet(text=cleaned_text)
            else:
                cleaned_text = tweet_text.strip()
                response = client.create_tweet(text=cleaned_text, in_reply_to_tweet_id=last_tweet_id)

            last_tweet_id = response.data["id"]
            print(f"[X LIVE TWEET {idx}/{len(thread_tweets)}] Posted ID: {last_tweet_id}")
            time.sleep(1)

        print("\nStatus: [LIVE SUCCESS] Full Thread Successfully Published to Main Feed!")
        return True

    except Exception as e:
        print(f"[X TWITTER ERROR] Failed to post thread: {e}")
        return False

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

    x_status, x_content = prompt_review("X (Twitter)", x_thread)
    if x_status == "approved":
        print("[X TWITTER] Publishing live thread to X API...")
        publish_x_thread(x_content)

if __name__ == "__main__":
    run_social_orchestrator()