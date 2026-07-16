#!/usr/bin/env python3
"""Apply and validate an antialiased rounded-corner alpha mask."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input image path")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument(
        "--radius-ratio",
        type=float,
        required=True,
        help="Measured source corner radius divided by the source short side.",
    )
    parser.add_argument(
        "--supersample",
        type=int,
        default=4,
        help="Mask supersampling factor for antialiasing (default: 4).",
    )
    return parser.parse_args()


def validate_alpha(image: Image.Image, radius: int) -> None:
    width, height = image.size
    alpha = image.getchannel("A")
    corners = ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1))
    if any(alpha.getpixel(point) != 0 for point in corners):
        raise ValueError("rounded alpha validation failed: corner pixel is not transparent")

    side_centers = (
        (width // 2, 0),
        (width // 2, height - 1),
        (0, height // 2),
        (width - 1, height // 2),
    )
    if any(alpha.getpixel(point) != 255 for point in side_centers):
        raise ValueError("rounded alpha validation failed: side center is not opaque")

    for y in range(height):
        for x in range(width):
            value = alpha.getpixel((x, y))
            if 0 < value < 255:
                in_corner_x = x < radius or x >= width - radius
                in_corner_y = y < radius or y >= height - radius
                if not (in_corner_x and in_corner_y):
                    raise ValueError("rounded alpha validation failed: partial alpha outside corner arcs")


def main() -> None:
    args = parse_args()
    src = Path(args.input)
    out = Path(args.output)

    image = Image.open(src).convert("RGBA")
    width, height = image.size
    if not 0 < args.radius_ratio <= 0.5:
        raise ValueError("radius-ratio must be greater than 0 and at most 0.5")
    if args.supersample < 2 or args.supersample > 8:
        raise ValueError("supersample must be between 2 and 8")

    radius = round(min(width, height) * args.radius_ratio)
    if radius < 1 or radius > min(width, height) // 2:
        raise ValueError("radius must be between 1 and half the short side")

    scale = args.supersample
    mask = Image.new("L", (width * scale, height * scale), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        (0, 0, width * scale - 1, height * scale - 1),
        radius=radius * scale,
        fill=255,
    )
    mask = mask.resize((width, height), Image.Resampling.LANCZOS)
    for point in ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)):
        mask.putpixel(point, 0)

    image.putalpha(ImageChops.multiply(image.getchannel("A"), mask))
    validate_alpha(image, radius)
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out, "PNG")


if __name__ == "__main__":
    main()
