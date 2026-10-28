#!/usr/bin/env python3
"""Render a short video from an actual captured CLI run (requires Pillow and ffmpeg)."""

import subprocess
import tempfile
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ghostline-demo.mp4"
W, H = 1280, 720


def font(size: int):
    for name in ("C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"):
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


def frame(title: str, lines: list[str], path: Path) -> None:
    im = Image.new("RGB", (W, H), "#10151c")
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((36, 30, W - 36, H - 30), radius=18, fill="#18222c", outline="#3a5261", width=2)
    draw.text((76, 68), title, font=font(32), fill="#8ee2b8")
    y = 145
    body = font(24)
    for line in lines:
        for part in textwrap.wrap(line, width=78, break_long_words=False, replace_whitespace=False) or [""]:
            draw.text((76, y), part, font=body, fill="#e3edf4")
            y += 36
        y += 14
    draw.text((76, H - 84), "ghostline  |  a fictional Git fixture  |  real open-weight model run", font=font(18), fill="#89a4b1")
    im.save(path)


def main() -> None:
    captured = (ROOT / "captured-run.txt").read_text(encoding="utf-8-sig")
    voice = captured.split("\n\n")[1].strip()
    slides = [
        ("1 / The vanished file", [
            "$ python demo/make_history.py demo-history",
            "$ python ghostline.py demo-history --file legacy_cache.py",
            "Git finds the deletion commit and retrieves the last surviving source.",
        ]),
        ("2 / The model speaks", [voice]),
        ("3 / Check the ghost's claim", [
            "The model called line 9 a potentially failed cache write.",
            "But source lines 7-8 return on TimeoutError:",
            "    except TimeoutError:",
            "        return cache.get(key)",
            "The write on line 9 is only on the success path.",
            "A real citation is evidence to inspect, not proof of a model's interpretation.",
        ]),
    ]
    with tempfile.TemporaryDirectory(dir=ROOT) as temp:
        folder = Path(temp)
        for index, (title, lines) in enumerate(slides):
            frame(title, lines, folder / f"slide-{index}.png")
        manifest = folder / "slides.txt"
        manifest.write_text("".join(f"file '{(folder / f'slide-{i}.png').as_posix()}'\nduration 5\n" for i in range(len(slides))) + f"file '{(folder / 'slide-2.png').as_posix()}'\n", encoding="utf-8")
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error", "-safe", "0", "-f", "concat", "-i", str(manifest),
            "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-crf", "24", "-movflags", "+faststart", str(OUT)
        ], check=True)
    print(OUT)


if __name__ == "__main__":
    main()
