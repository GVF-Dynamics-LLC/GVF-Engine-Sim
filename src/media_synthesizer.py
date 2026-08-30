import json
import os
import gc
import math
import asyncio
from pathlib import Path
import edge_tts
import moviepy as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wav

def generate_ambient_synth_wav(duration_sec, output_wav_path, sample_rate=44100):
    """Generates a soft, atmospheric ambient synth pad background track."""
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)
    
    # Ambient Chord (C minor pad: C3, Eb3, G3)
    f1, f2, f3 = 130.81, 155.56, 196.00
    layer1 = 0.25 * np.sin(2 * np.pi * f1 * t)
    layer2 = 0.20 * np.sin(2 * np.pi * f2 * t + 0.4)
    layer3 = 0.15 * np.sin(2 * np.pi * f3 * t + 0.8)
    
    # 0.4 Hz LFO volume modulation for breathing effect
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.4 * t)
    combined = (layer1 + layer2 + layer3) * lfo * 0.12  # Attenuated to 12%
    
    audio_int16 = (combined * 32767).astype(np.int16)
    wav.write(output_wav_path, sample_rate, audio_int16)

def generate_youtube_thumbnail(task_name="bench_dvs", results={}, output_path="data/videos/thumbnail.jpg"):
    """Generates a high-contrast 16:9 YouTube thumbnail image (1280x720)."""
    dpi = 100
    fig, ax = plt.subplots(figsize=(1280/dpi, 720/dpi), dpi=dpi)
    fig.patch.set_facecolor('#030712')
    ax.set_facecolor('#0b0f19')

    if task_name == "bench_latency":
        p99_val = results.get("p99_reduction", "98.45%")
        main_headline = f"{p99_val} TAIL LATENCY KILLED"
        sub_text = "SUB-0.01ms HARDWARE GOVERNANCE PROOF"
        accent_color = '#38bdf8'
    elif task_name == "bench_thermal":
        temp_val = results.get("thermal_jitter_avoided", "34.0°C")
        main_headline = f"{temp_val} THERMAL JITTER STOPPED"
        sub_text = "SRAM BUS BANDWIDTH SAVED"
        accent_color = '#f43f5e'
    else:
        mac_val = results.get("mac_reduction", "70.60%")
        main_headline = f"{mac_val} FLOP POWER SAVED"
        sub_text = "HARDWARE-ENFORCED AI GOVERNANCE"
        accent_color = '#10b981'

    x = np.linspace(0, 10, 500)
    y = np.sin(x) * 0.5
    ax.plot(x, y + 1.2, color=accent_color, alpha=0.3, linewidth=3)
    ax.plot(x, -y - 1.2, color=accent_color, alpha=0.3, linewidth=3)

    ax.text(0.5, 0.82, "GVF DYNAMICS CORE", color='#38bdf8', fontsize=22, fontweight='bold', ha='center', transform=ax.transAxes)
    ax.text(0.5, 0.52, main_headline, color='white', fontsize=34, fontweight='bold', ha='center', transform=ax.transAxes)
    ax.text(0.5, 0.28, sub_text, color='yellow', fontsize=18, fontweight='bold', ha='center', transform=ax.transAxes)
    ax.text(0.5, 0.12, "polar.sh/gvfdynamics | github.com/GVF-Dynamics-LLC", color='#94a3b8', fontsize=14, ha='center', transform=ax.transAxes)

    ax.axis('off')
    fig.tight_layout()
    
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_file, dpi=dpi, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print(f"[THUMBNAIL GENERATOR] Generated 16:9 thumbnail image: {out_file.name}")
    return str(out_file)

def rotate_old_renders(output_dir="data/videos", keep_count=2):
    output_path = Path(output_dir)
    if not output_path.exists():
        return
    gc.collect()

    for prefix in ["shorts_render_", "longform_render_"]:
        mp4_files = sorted(output_path.glob(f"{prefix}*.mp4"), key=os.path.getmtime, reverse=True)
        if len(mp4_files) > keep_count:
            for old_file in mp4_files[keep_count:]:
                try:
                    old_file.unlink()
                except Exception:
                    pass

async def generate_neural_audio(text, output_file, voice="en-US-ChristopherNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def generate_scene_frame(t, width, height, scene_id=1):
    dpi = 100
    fig, ax = plt.subplots(figsize=(width/dpi, (height*0.50)/dpi), dpi=dpi)
    fig.patch.set_facecolor('#030712')
    ax.set_facecolor('#0b0f19')

    if scene_id == 1:
        gauge_val = 70.60 + 2.0 * np.sin(3 * t)
        ax.barh(["FLOP Waste Suppressed"], [gauge_val], color='#10b981', height=0.4)
        ax.set_xlim(0, 100)
        ax.set_title("SCENE 1: EXECUTION ENTROPY REDUCTION", color='#38bdf8', fontsize=14, pad=10, fontweight='bold')
        ax.tick_params(colors='white', labelsize=10)

    elif scene_id == 2:
        x = np.linspace(0, 10, 200)
        uncapped = np.sin(x - 5*t) + 0.5 * np.random.randn(200)
        gated = np.copy(uncapped)
        gated[np.abs(gated) < 0.8] = 0
        ax.plot(x, uncapped, color='#f43f5e', alpha=0.5, label='Uncapped GPU Waste')
        ax.plot(x, gated, color='#10b981', linewidth=2.5, label='GVF Bitline Gating')
        ax.set_title("SCENE 2: UNREGULATED GPU VS. GVF BITLINE GATING", color='#38bdf8', fontsize=14, pad=10, fontweight='bold')
        ax.legend(loc='upper right', facecolor='#0f172a', labelcolor='white')

    elif scene_id == 3:
        x = np.linspace(0, 10, 300)
        signal = np.sin(x - 4*t) + 0.6 * np.sin(2.5*x + 5*t)
        gvf_gated = np.copy(signal)
        gvf_gated[np.abs(gvf_gated) < 0.85] = 0.0
        ax.plot(x, signal, color='#f43f5e', alpha=0.35, linewidth=1.5, label='Raw Event Waste')
        ax.plot(x, gvf_gated, color='#10b981', linewidth=2.8, label='GVF Dynamic Core')
        ax.axhline(y=0.85, color='#38bdf8', linestyle='--', linewidth=1.8, label='Phase-Locked Threshold')
        ax.set_title("SCENE 3: LIVE PHASE-LOCKED THRESHOLD GATING", color='#38bdf8', fontsize=14, pad=10, fontweight='bold')
        ax.legend(loc='upper right', facecolor='#0f172a', labelcolor='white')

    else:
        ax.text(0.5, 0.7, "GVF DYNAMICS DEVELOPER SDK", color='#38bdf8', fontsize=16, ha='center', fontweight='bold')
        ax.text(0.5, 0.4, "Commercial Licensing: polar.sh/gvfdynamics\nGitHub Core: github.com/GVF-Dynamics-LLC", color='white', fontsize=12, ha='center')
        ax.axis('off')

    fig.tight_layout()
    fig.canvas.draw()
    rgba = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    rgba = rgba.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    plt.close(fig)
    return rgba[:, :, :3]

def synthesize_video(script_file="data/latest_video_scripts.json", telemetry_file="data/latest_agent_output.json", output_dir="data/videos"):
    script_path = Path(script_file)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    if not script_path.exists():
        print(f"[MEDIA SYNTHESIZER] Script file missing at {script_file}.")
        return

    with open(script_path, "r") as f:
        data = json.load(f)

    task_name = "bench_dvs"
    results = {}
    if Path(telemetry_file).exists():
        with open(telemetry_file, "r") as tf:
            tdata = json.load(tf)
            task_name = tdata.get("task", "bench_dvs")
            results = tdata.get("results", {})

    generate_youtube_thumbnail(task_name=task_name, results=results)

    shorts_data = data.get("shorts", {})
    hook_speech = shorts_data.get("hook_speech", "GVF phase-locked dynamic thresholding benchmark.")

    # 1. SHORTS RENDER (9:16) WITH MIXED AUDIO
    tts_shorts_path = output_path / "temp_shorts_vo.mp3"
    bg_shorts_wav = output_path / "temp_bg_shorts.wav"
    asyncio.run(generate_neural_audio(hook_speech, str(tts_shorts_path)))
    
    vo_shorts = mp.AudioFileClip(str(tts_shorts_path))
    duration_shorts = max(vo_shorts.duration, 8.0)
    
    generate_ambient_synth_wav(duration_shorts, str(bg_shorts_wav))
    bg_audio_shorts = mp.AudioFileClip(str(bg_shorts_wav))
    
    mixed_audio_shorts = mp.CompositeAudioClip([vo_shorts, bg_audio_shorts])

    width, height = 1080, 1920
    bg_clip = mp.ColorClip(size=(width, height), color=(3, 7, 18)).with_duration(duration_shorts)
    header_clip = mp.TextClip(text="GVF DYNAMICS\nHardware-Enforced AI Governance", font_size=36, color="cyan", size=(width - 240, None), method="caption").with_position(("center", 240)).with_duration(duration_shorts)
    wave_clip = mp.VideoClip(lambda t: generate_scene_frame(t, width-140, height, scene_id=3), duration=duration_shorts).with_position(("center", 560))
    body_clip = mp.TextClip(text=hook_speech, font_size=32, color="white", size=(width - 200, None), method="caption").with_position(("center", 1250)).with_duration(duration_shorts)
    footer_clip = mp.TextClip(text="EMPIRICAL BENCHMARK PROOF\npolar.sh/gvfdynamics", font_size=28, color="yellow", size=(width - 200, None), method="caption").with_position(("center", 1620)).with_duration(duration_shorts)

    video_shorts = mp.CompositeVideoClip([bg_clip, header_clip, wave_clip, body_clip, footer_clip]).with_audio(mixed_audio_shorts)
    timestamp_str = int(script_path.stat().st_mtime)
    shorts_out = output_path / f"shorts_render_{timestamp_str}.mp4"
    video_shorts.write_videofile(str(shorts_out), fps=15, codec="libx264", audio_codec="aac", logger=None)
    
    video_shorts.close()
    vo_shorts.close()
    bg_audio_shorts.close()

    # 2. LONG-FORM RENDER (16:9) WITH MIXED AUDIO
    longform_data = data.get("longform", {})
    chapters = longform_data.get("chapters", [])
    full_long_speech = " ".join([ch.get("speech", "") for ch in chapters]) if chapters else hook_speech

    tts_long_path = output_path / "temp_long_vo.mp3"
    bg_long_wav = output_path / "temp_bg_long.wav"
    asyncio.run(generate_neural_audio(full_long_speech, str(tts_long_path)))
    
    vo_long = mp.AudioFileClip(str(tts_long_path))
    duration_long = vo_long.duration
    
    generate_ambient_synth_wav(duration_long, str(bg_long_wav))
    bg_audio_long = mp.AudioFileClip(str(bg_long_wav))
    
    mixed_audio_long = mp.CompositeAudioClip([vo_long, bg_audio_long])

    lw, lh = 1920, 1080
    scene_dur = duration_long / 4.0

    c1 = mp.VideoClip(lambda t: generate_scene_frame(t, lw-300, lh, scene_id=1), duration=scene_dur)
    c2 = mp.VideoClip(lambda t: generate_scene_frame(t, lw-300, lh, scene_id=2), duration=scene_dur)
    c3 = mp.VideoClip(lambda t: generate_scene_frame(t, lw-300, lh, scene_id=3), duration=scene_dur)
    c4 = mp.VideoClip(lambda t: generate_scene_frame(t, lw-300, lh, scene_id=4), duration=scene_dur)

    visual_storyboard = mp.concatenate_videoclips([c1, c2, c3, c4]).with_position(("center", 180))
    l_bg = mp.ColorClip(size=(lw, lh), color=(3, 7, 18)).with_duration(duration_long)
    l_header = mp.TextClip(text="GVF Dynamics Core Architecture Breakdown", font_size=40, color="cyan", size=(lw-240, None), method="caption").with_position(("center", 60)).with_duration(duration_long)
    l_footer = mp.TextClip(text="SDK & Licensing: polar.sh/gvfdynamics | Core: github.com/GVF-Dynamics-LLC", font_size=26, color="yellow", size=(lw-240, None), method="caption").with_position(("center", 920)).with_duration(duration_long)

    video_long = mp.CompositeVideoClip([l_bg, l_header, visual_storyboard, l_footer]).with_audio(mixed_audio_long)
    long_out = output_path / f"longform_render_{timestamp_str}.mp4"
    video_long.write_videofile(str(long_out), fps=15, codec="libx264", audio_codec="aac", logger=None)
    
    video_long.close()
    vo_long.close()
    bg_audio_long.close()
    visual_storyboard.close()

    for p in [tts_shorts_path, tts_long_path, bg_shorts_wav, bg_long_wav]:
        if p.exists():
            try:
                os.remove(p)
            except Exception:
                pass

    rotate_old_renders(output_dir=output_dir, keep_count=2)
    print(f"[MEDIA SYNTHESIZER SUCCESS]\n -> Shorts rendered with ambient audio: {shorts_out.name}\n -> 4-Scene Long-Form rendered with ambient audio: {long_out.name}")

if __name__ == "__main__":
    synthesize_video()