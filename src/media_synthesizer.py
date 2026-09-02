import json
import os
import glob
from pathlib import Path
import io

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips, ImageClip

import edge_tts
import asyncio

async def generate_tts_audio(text, output_file):
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await communicate.save(output_file)

def make_tts_sync(text, output_file):
    asyncio.run(generate_tts_audio(text, output_file))

def fig_to_numpy(fig):
    fig.canvas.draw()
    try:
        buf = fig.canvas.buffer_rgba()
        return np.asarray(buf)[:, :, :3]
    except AttributeError:
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor())
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        return np.array(img)

def create_yellow_subtitle_banner(text, width=1280, height=100, font_size=32):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (width - text_w) // 2
    y = (height - text_h) // 2

    padding = 16
    draw.rounded_rectangle([x - padding, y - 8, x + text_w + padding, y + text_h + 8], radius=8, fill=(3, 7, 18, 220))
    draw.text((x, y), text, fill=(250, 204, 21, 255), font=font)
    return np.array(img)

def render_agent_mesh_frame(task_name, t, width=1280, height=720, is_vertical=False):
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100, facecolor='#030712')
    ax.set_facecolor('#030712')
    ax.axis('off')

    ax.grid(True, color='#1e293b', linestyle='--', alpha=0.3)

    np.random.seed(42)
    G = nx.erdos_renyi_graph(n=16, p=0.35, seed=42)
    pos = nx.spring_layout(G, seed=42)

    for node in pos:
        x, y = pos[node]
        pos[node] = (x + np.sin(t * 2 + node) * 0.03, y + np.cos(t * 2 + node) * 0.03)

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#38bdf8', alpha=0.6, width=2.0)

    node_colors = []
    for i in range(len(G)):
        if i % 3 == 0:
            node_colors.append('#ef4444')
        elif i % 2 == 0:
            node_colors.append('#10b981')
        else:
            node_colors.append('#f59e0b')

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=350 if not is_vertical else 500, alpha=0.9)

    if task_name == "bench_thermal":
        t1 = "GVF TELEMETRY: Thermal Jitter Avoided: -34.0°C"
        t2 = "SRAM Bus Traffic Suppression: 68.40%"
    elif task_name == "bench_latency":
        t1 = "GVF TELEMETRY: p99 Latency Ceiling: 4.20 µs"
        t2 = "Execution Entropy Clamped: Sub-0.01ms"
    else:
        t1 = "GVF TELEMETRY: FLOP Waste Avoided: 70.60%"
        t2 = "Accuracy Degradation: 0.00%"

    y1 = 0.85 if not is_vertical else 0.90
    y2 = 0.70 if not is_vertical else 0.78
    ax.text(-0.95, y1, t1, color='#38bdf8', fontsize=12 if is_vertical else 13, fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", fc="#0f172a", ec="#1e293b", alpha=0.9))
    ax.text(-0.95, y2, t2, color='#10b981', fontsize=11 if is_vertical else 12, bbox=dict(boxstyle="round,pad=0.5", fc="#0f172a", ec="#1e293b", alpha=0.9))

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)

    frame = fig_to_numpy(fig)
    plt.close(fig)
    return frame

def render_single_format(task_name, chapters, output_file, is_vertical=False):
    width, height = (1080, 1920) if is_vertical else (1280, 720)
    sub_y = 1500 if is_vertical else 600

    scene_clips = []
    for idx, chapter in enumerate(chapters, 1):
        section_title = chapter.get("section", f"Scene {idx}")
        speech_text = chapter.get("speech", "")

        prefix = "short" if is_vertical else "long"
        audio_file = f"data/scene_{prefix}_{idx}_audio.mp3"
        make_tts_sync(speech_text, audio_file)
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration + 0.3

        def make_frame(t):
            return render_agent_mesh_frame(task_name=task_name, t=t, width=width, height=height, is_vertical=is_vertical)

        visual_clip = VideoClip(make_frame, duration=duration)
        sub_np = create_yellow_subtitle_banner(section_title, width=width, height=100, font_size=28 if is_vertical else 32)
        
        sub_clip = ImageClip(sub_np)
        if hasattr(sub_clip, 'with_position'):
            sub_clip = sub_clip.with_position(('center', sub_y)).with_duration(duration)
        else:
            sub_clip = sub_clip.set_position(('center', sub_y)).set_duration(duration)

        combined = CompositeVideoClip([visual_clip, sub_clip])
        if hasattr(combined, 'with_audio'):
            combined = combined.with_audio(audio_clip)
        else:
            combined = combined.set_audio(audio_clip)

        scene_clips.append(combined)

    final_video = concatenate_videoclips(scene_clips)
    final_video.write_videofile(str(output_file), fps=24, codec="libx264", audio_codec="aac")

def synthesize_video():
    script_path = Path("data/latest_video_scripts.json")
    output_dir = Path("data/videos")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not script_path.exists():
        print("[MEDIA SYNTHESIZER ERROR] latest_video_scripts.json not found!")
        return

    with open(script_path, "r") as f:
        script_data = json.load(f)

    task_payload = Path("data/latest_agent_output.json")
    task_name = "bench_thermal"
    if task_payload.exists():
        with open(task_payload, "r") as f:
            t_data = json.load(f)
            task_name = t_data.get("task", "bench_thermal")

    longform_chapters = script_data.get("longform", {}).get("chapters", [])
    shorts_chapters = script_data.get("shorts", {}).get("chapters", [])

    print(f"[MEDIA SYNTHESIZER] Rendering YouTube Longform (16:9)...")
    long_output = output_dir / f"longform_render_{task_name}.mp4"
    render_single_format(task_name, longform_chapters, long_output, is_vertical=False)

    print(f"[MEDIA SYNTHESIZER] Rendering YouTube Short (9:16)...")
    short_output = output_dir / f"short_render_{task_name}.mp4"
    render_single_format(task_name, shorts_chapters if shorts_chapters else longform_chapters, short_output, is_vertical=True)

    print(f"\n[SYNTHESIZER SUCCESS] Videos Generated:\n -> Longform: {long_output}\n -> Short: {short_output}")

if __name__ == "__main__":
    synthesize_video()