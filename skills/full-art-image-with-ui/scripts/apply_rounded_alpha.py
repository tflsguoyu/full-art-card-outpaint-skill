#!/usr/bin/env python3
"""Apply a transparent rounded-corner alpha mask to a card PNG."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input image path")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument(
        "--radius",
        type=int,
        default=0,
        help="Corner radius in pixels. Defaults to 5.6%% of the short side.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    src = Path(args.input)
    out = Path(args.output)

    image = Image.open(src).convert("RGBA")
    width, height = image.size
    radius = args.radius or round(min(width, height) * 0.056)

    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=radius, fill=255)

    image.putalpha(mask)
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out, "PNG")


if __name__ == "__main__":
    main()
