#!/usr/bin/env python3
"""Assemble Partenon video v2 from clips and voiceover."""

import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
CLIPS = ASSETS / "clips"
VOICE = ASSETS / "voice" / "voiceover.mp3"
FINAL = ASSETS / "final" / "partenon-hackathon-video-v2-draft.mp4"
SCENES = ROOT / "scenes.json"

WIDTH, HEIGHT, FPS = 720, 1280, 24


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def build_scene(clip_path: Path, duration: float, out_path: Path) -> None:
    """Loop or trim a clip to an exact duration and normalize format."""
    run(
        [
            "ffmpeg",
            "-y",
            "-stream_loop", "-1",
            "-i", str(clip_path),
            "-t", str(duration),
            "-vf",
            f"fps={FPS},scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-an",
            str(out_path),
        ]
    )


def main() -> None:
    if not VOICE.exists():
        raise FileNotFoundError(f"Voice file not found: {VOICE}")

    with SCENES.open() as f:
        scenes = json.load(f)

    total = sum(s["duration"] for s in scenes)

    # Get voice duration and scale scene durations to match exactly
    probe = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(VOICE),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    voice_duration = float(probe.stdout.strip())
    scale = voice_duration / total
    print(f"Planned video duration: {total:.2f}s")
    print(f"Voice duration: {voice_duration:.2f}s")
    print(f"Scene scale factor: {scale:.4f}")

    for s in scenes:
        s["duration"] = round(s["duration"] * scale, 2)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        list_file = tmp / "concat.txt"
        scene_files = []

        for scene in scenes:
            clip = CLIPS / scene["clip"]
            if not clip.exists():
                raise FileNotFoundError(f"Missing clip: {clip}")
            out = tmp / f"scene-{scene['id']}.mp4"
            build_scene(clip, scene["duration"], out)
            scene_files.append(out)

        # Write concat demuxer list
        with list_file.open("w") as f:
            for sf in scene_files:
                f.write(f"file '{sf}'\n")

        FINAL.parent.mkdir(parents=True, exist_ok=True)

        # Concatenate video and add voiceover
        run(
            [
                "ffmpeg",
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(list_file),
                "-i", str(VOICE),
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                str(FINAL),
            ]
        )

    print(f"\nDraft saved to: {FINAL}")
    print(f"Duration: {total:.2f}s")


if __name__ == "__main__":
    main()
