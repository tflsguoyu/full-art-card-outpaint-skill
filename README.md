# Full Art Gen

A Codex skill for turning regular card-style illustrations into full-art card outpaints.

The skill first creates a pure art-only outpaint, then uses that image as the base for one complete card generation that restores the original outer border, title/HP area, stage or evolution labels, attack/rules text, icons, weakness/resistance/retreat row, copyright line, and other UI overlays. It removes the horizontal middle information strip and extends the illustration behind the top and lower card areas so the result reads as one continuous full-art scene.

## What It Does

- Converts one uploaded card image into an art-only image and one complete full-art card.
- Makes exactly one image-generation call for each output and accepts the first successful result without retries, variants, or corrective image edits.
- Removes the narrow horizontal species/info strip around the lower edge of the illustration window.
- Extends the original illustration into the top name/HP area and lower rules area.
- Keeps non-target card UI and text readable in approximately the original positions.
- Preserves the outer rounded card border and transparent rounded corners.
- Returns both output images and their absolute file paths.

## Examples

| Caterpie | Metapod | Butterfree |
| --- | --- | --- |
| ![Caterpie input](examples/readme/caterpie_input.png) | ![Metapod input](examples/readme/metapod_input.png) | ![Butterfree input](examples/readme/butterfree_input.png) |
| ![Caterpie full-art output](examples/readme/caterpie_output.png) | ![Metapod full-art output](examples/readme/metapod_output.png) | ![Butterfree full-art output](examples/readme/butterfree_output.png) |

## Installation

Copy the skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/full-art-outpaint ~/.codex/skills/
```

Restart Codex or start a new task so the skill is discovered.

## Usage

Upload a card image and ask Codex to use the skill:

```text
Use $full-art-outpaint on this image.
```

The skill is intentionally one-image-in, two-images-out. Each image is generated once: the first successful result becomes the output without regeneration or corrective image edits. The skill does not ask for style, size, character, target area, or composition details; the uploaded image is treated as the visual authority.

## Output

The final response shows:

- `art-only.png`, followed by `保存路径：` and its absolute file path
- `full-art-card.png`, followed by `保存路径：` and its absolute file path

Both images are displayed inline; the absolute paths are always shown even when the images render successfully.

The complete card is post-processed as an RGBA PNG with transparent rounded corners. Only pixels outside the card's rounded rectangle should become transparent; the restored card border itself is preserved.

## Repository Structure

```text
.
├── examples/
│   ├── Butterfree.jpg
│   ├── butterfree_full_art_outpaint.png
│   ├── Caterpie.jpg
│   ├── caterpie_full_art_outpaint.png
│   ├── Metapod.webp
│   ├── metapod_full_art_outpaint.png
│   └── readme/
│       ├── butterfree_input.png
│       ├── butterfree_output.png
│       ├── caterpie_input.png
│       ├── caterpie_output.png
│       ├── metapod_input.png
│       └── metapod_output.png
└── skills/
    └── full-art-outpaint/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        └── scripts/
            ├── apply_rounded_alpha.py
            └── normalize_rgb.py
```

## Notes

This repository contains a Codex skill, not a standalone image-generation app. The actual image edit is performed through Codex's image generation/editing capability, and `scripts/apply_rounded_alpha.py` handles the deterministic final rounded-corner alpha pass.

Example images are included to demonstrate the workflow and expected before/after behavior. This project is not affiliated with, endorsed by, or sponsored by any card game publisher or rights holder.
