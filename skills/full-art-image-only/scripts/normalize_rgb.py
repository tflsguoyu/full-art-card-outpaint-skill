#!/usr/bin/env python3
"""Save the first generated art-only image as an RGB PNG."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Generated art-only image")
    parser.add_argument("--output", required=True, help="Output RGB PNG path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image = Image.open(args.input)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, "PNG")


if __name__ == "__main__":
    main()
