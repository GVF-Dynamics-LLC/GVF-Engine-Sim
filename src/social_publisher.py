import json
import os
import shutil
import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

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

def get_latest_video(prefix, video_dir="data/videos"):
    video_path = Path(video_dir)
    if not video_path.exists():
        return None
    files = sorted(video_path.glob(f"{prefix}*.mp4"), key=os.path.getmtime, reverse=True)
    return str(files[0]) if files else None

def queue_video_for_later(video_file, queue_dir="data/queue"):
    q_path = Path(queue_dir)
    q_path.mkdir(parents=True, exist_ok=True)
    if video_file and Path(video_file).exists():
        target = q_path / Path(video_file).name
        shutil.move(video_file, target)
        print(f"[QUEUE SUCCESS] Daily YouTube limit hit. Video saved to queue: {target.name}")

def cleanup_video(video_file):
    if video_file and Path(video_file).exists():
        try:
            Path(video_file).unlink()
            print(f"[ORCHESTRATOR CLEANUP] Cleaned up staged render: {Path(video_file).name}")
        except Exception:
            pass

def upload_youtube_video(video_file, is_shorts=True, script_file="data/latest_video_scripts.json"):
    if not video_file or not Path(video_file).exists():
        print(f"[YOUTUBE PUBLISHER] No video file found for upload.")
        return False

    client_secret = Path("client_secret.json")
    if not client_secret.exists():
        print("[YOUTUBE PUBLISHER] client_secret.json missing. Running in SIMULATED UPLOAD mode.")
        cleanup_video(video_file)
        return True

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from googleapiclient.errors import HttpError

        SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
        creds = None
        token_path = Path("token.json")

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        youtube = build("youtube", "v3", credentials=creds)

        title = "GVF Dynamics Core Benchmark"
        tags = ["EdgeAI", "Semiconductors", "Neuromorphic"]

        if Path(script_file).exists():
            with open(script_file, "r") as f:
                s_data = json.load(f)
                key = "shorts" if is_shorts else "longform"
                v_info = s_data.get(key, {})
                title = v_info.get("title", title)
                tags = v_info.get("tags", tags)

        description = """🚀 GVF DYNAMICS - Sub-0.01ms Hardware-Enforced AI Governance

Eliminating execution entropy and FLOP waste on edge silicon.

🛒 Enterprise SDK & Commercial Licensing: https://polar.sh/gvfdynamics
🌐 Official Website: https://gvfdynamics.com
💻 Open-Source Simulation Core: https://github.com/GVF-Dynamics-LLC/GVF-Engine-Sim
📄 Privacy Policy & Legal: https://gvfdynamics.com/privacy.html

#EdgeAI #NeuromorphicComputing #Semiconductors #HardwareGovernance #RISCV"""

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "28"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/mp4")
        print(f"[YOUTUBE PUBLISHER LIVE] Uploading {Path(video_file).name} to YouTube with Polar & Asset links...")
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response = request.execute()

        video_id = response.get("id")
        print(f"Status: [LIVE SUCCESS] Video Uploaded to YouTube! Watch at: https://youtu.be/{video_id}")
        cleanup_video(video_file)
        return True

    except HttpError as e:
        if "uploadLimitExceeded" in str(e):
            print("\n[YOUTUBE QUOTA NOTICE] Daily channel upload limit reached for today.")
            queue_video_for_later(video_file)
        else:
            print(f"[YOUTUBE HTTP ERROR] Upload failed: {e}")
        return False
    except Exception as e:
        print(f"[YOUTUBE ERROR] Upload failed: {e}")
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
            "🚀 GVF Dynamics just suppressed FLOP waste on edge silicon during benchmark testing!",
            "Unregulated GPUs waste massive clock cycles on dynamic noise. GVF phase-locked thresholding gates waste at sub-0.01ms speeds.",
            "🔗 Open Core: github.com/GVF-Dynamics-LLC/GVF-Engine-Sim\n🛒 Commercial SDK: polar.sh/gvfdynamics #EdgeAI"
        ]

    # 1. YouTube Shorts Gate
    shorts_file = get_latest_video("shorts_render_")
    if shorts_file:
        yt_status, _ = prompt_review("YouTube Shorts Upload", f"Short Video File: {shorts_file}")
        if yt_status == "approved":
            upload_youtube_video(video_file=shorts_file, is_shorts=True)
        else:
            cleanup_video(shorts_file)

    # 2. YouTube Long-Form Gate
    long_file = get_latest_video("longform_render_")
    if long_file:
        yt_long_status, _ = prompt_review("YouTube Long-Form Video Upload", f"Long-Form Video File: {long_file}")
        if yt_long_status == "approved":
            upload_youtube_video(video_file=long_file, is_shorts=False)
        else:
            cleanup_video(long_file)

    # 3. X (Twitter) Gate
    x_status, x_content = prompt_review("X (Twitter)", x_thread)
    if x_status == "approved":
        print("[X TWITTER] Publishing thread to X API...")
        print("Status: [SIMULATED SUCCESS] Thread posted to X!")

if __name__ == "__main__":
    run_social_orchestrator()