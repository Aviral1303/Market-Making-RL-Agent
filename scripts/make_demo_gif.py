#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import List

from PIL import Image, ImageDraw, ImageFont


def run_cmd(cmd: List[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return (p.stdout or "") + (p.stderr or "")


def monospace_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("Menlo.ttc", size)
    except Exception:
        try:
            return ImageFont.truetype("DejaVuSansMono.ttf", size)
        except Exception:
            return ImageFont.load_default()


def draw_frame(text_lines: List[str], width: int = 960, height: int = 340) -> Image.Image:
    img = Image.new("RGB", (width, height), color=(15, 17, 26))
    d = ImageDraw.Draw(img)
    # Header bar
    d.rectangle((0, 0, width, 40), fill=(30, 144, 255))
    header_font = monospace_font(18)
    d.text((16, 10), "MMRL Demo", fill=(255, 255, 255), font=header_font)
    # Body
    y = 60
    body_font = monospace_font(16)
    for line in text_lines:
        d.text((16, y), line, fill=(220, 220, 220), font=body_font)
        y += 22
        if y > height - 25:
            break
    return img


def main() -> None:
    assets = Path("docs/assets")
    assets.mkdir(parents=True, exist_ok=True)

    frames: List[Image.Image] = []

    # Frame 1: install hint
    frames.append(draw_frame(["$ pip install mmrl", "", "(Already installed for this demo)"]))

    # Run backtest and capture output
    out_bt = run_cmd(["python3", "-m", "mmrl.cli", "backtest"]).strip().splitlines()
    # Extract latest run dir
    latest_dir = None
    for line in out_bt:
        m = re.search(r"Saved artifacts to: (.+)$", line)
        if m:
            latest_dir = m.group(1).strip()
            break
    if latest_dir is None:
        latest_dir = "results/<latest>"
    # Frame 2: show command and key outputs (last few lines)
    tail = out_bt[-6:] if len(out_bt) > 6 else out_bt
    frames.append(draw_frame([f"$ mmrl backtest", "", *tail]))

    # Run report and capture
    out_rep = run_cmd(["python3", "-m", "mmrl.cli", "report", latest_dir, "--out", str(assets / "report.html")]).strip().splitlines()
    frames.append(draw_frame([f"$ mmrl report {latest_dir} --out docs/assets/report.html", "", *out_rep[-4:]]))

    # Final splash
    frames.append(draw_frame(["Done.", "", "Artifacts:", f"- {latest_dir}", "- docs/assets/report.html"]))

    # Save GIF
    gif_path = assets / "demo.gif"
    frames[0].save(
        str(gif_path), save_all=True, append_images=frames[1:], duration=[900, 1200, 1200, 800], loop=0
    )
    print(f"Wrote {gif_path}")


if __name__ == "__main__":
    main()

