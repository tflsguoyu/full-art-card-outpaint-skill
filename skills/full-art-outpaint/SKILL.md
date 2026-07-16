---
name: full-art-outpaint
description: >-
  Convert one uploaded regular card-like illustration into two full-art outputs using exactly one imagegen call per output: an opaque RGB art-only image with no UI or borders, and a rounded transparent final card created from that art-only image with the original card UI, outer border, and bottom copyright line restored together. Use when the user wants the central illustration extended across the full card face while removing the illustration-window frame and horizontal species/info strip, preserving the remaining card UI and copyright text, accepting each first successful generation without retries or corrective image edits, and displaying both completed images with their absolute save paths. Current version: 20260715-223910.
---

# Full Art Outpaint

## Version

Current version: `20260715-223910`

- Treat the version as the skill's local modification timestamp in `YYYYMMDD-HHMMSS` format.
- At the start of every invocation, make the first user-visible line exactly: `full-art-outpaint 版本：20260715-223910`.
- Display that line before any other progress update or task-specific explanation.
- Whenever any file in this skill changes, update the version in both the frontmatter description and this section to the current local modification time, then synchronize the system-installed and project-local copies.

## Contract

Use this skill as a one-image-in, two-image-out workflow.

- Require one uploaded image. If none is present, ask for it in one short sentence.
- Do not ask for style, size, character, target area, composition, or border measurements.
- Use the uploaded image as the visual, UI, text, and outer-border authority.
- Do not create a separate UI-only layer or a separate no-border card output.
- Do not expose prompts, detailed validation notes, or attempt counts in the final response. During long tool work, provide brief progress updates without revealing prompts or internal validation details.
- Reserve one final output directory per run at `outputs/full-art-outpaint/YYYYMMDD-HHMMSS/`, using the local run start time. Work in a sibling `.staging-YYYYMMDD-HHMMSS/` directory and create the final directory only after both generations and required deterministic post-processing complete. Do not use the uploaded source filename, hash, generated-image identifier, or temporary filename in a final output name.
- Use these exact final filenames: `art-only.png` and `full-art-card.png`.
- If the timestamp directory already exists, append `-02`, `-03`, and so on instead of overwriting an earlier run.
- Make exactly one imagegen call for the art-only stage and exactly one imagegen call for the complete-card stage. Accept the first successfully returned image from each call as-is, regardless of visual defects or instruction drift. Do not retry, regenerate, create candidates or variants, or make corrective image edits. If either imagegen call errors or returns no image, delete the staging directory, leave no partial final directory, and return a concise failure.
- Do not make any imagegen call beyond those two stage calls.
- Keep imagegen prompts concise and reference-driven. Do not transcribe long source text, enumerate every visible UI item, or repeat source-specific names when the referenced image already identifies them.
- After generation and file promotion finish, display both output images and the absolute save path of each file. Never omit the paths even when both images render inline.

## Generation Efficiency

- Use the canonical prompt patterns below as written, adding only source-specific visual details needed to preserve the subject or scene.
- Prefer phrases such as "the visible subject" and "the non-target UI present in the reference" over lists of names, labels, rules, numbers, logos, or copyright strings.
- Keep negative instructions grouped by category instead of repeating each forbidden element separately.
- If imagegen rejects or fails a request, do not evade the safety system, rephrase for another attempt, or retry.
- Preserve each first successfully returned stage artifact and use it as the sole input to the next step.
- Use deterministic scripts only for RGB conversion, alpha masking, and file promotion. These operations may change file mode or corner alpha but must not repair, redraw, or semantically alter generated content.

## Workflow

1. Inspect the source and identify:
   - the card bounds, excluding any photographed or scanned margin outside the card
   - the main subject, pose, expression, scale, crop, rendering style, palette, lighting, and visible environment
   - the target horizontal species/info strip at the lower edge of the illustration window
   - the outer card border/rim, illustration-window frame, copyright line, and all other UI elements
   - the visible outer-border width on each side as a proportion of the source card's short side; measure from the outer card edge to the inner edge of the outer rim and keep the four side measurements separate when they differ
   - the outer rounded-corner radius as a proportion of the source card's short side; use this measured ratio when applying final alpha
   - whether the source includes any exterior scan/background margin; exclude that margin so the measured card silhouette, not the uploaded canvas, defines the card bounds
2. Generate the art-only image with exactly one imagegen call using the source as the edit target:
   - start with the concise Art Only prompt pattern; do not add a UI inventory or literal source-text transcription
   - preserve the subject identity, anatomy, pose, expression, action, scale, crop logic, and camera angle
   - preserve the illustration medium, line weight, palette, lighting, texture, and scene logic
   - remove all UI, text, letters, numbers, icons, logos, symbols, backing plates, rules panels, frame lines, the target strip, and the outer border/rim
   - extend the central illustration naturally across the entire card rectangle, including the former top UI, lower rules area, illustration frame, and outer-border area
   - do not add typography, graphic-design elements, unrelated props, or additional characters
3. Save the accepted art-only output as `art-only.png` in the staging directory:
   - use `scripts/normalize_rgb.py`
   - keep the source card's portrait aspect ratio
   - save as opaque RGB with no alpha channel
   - do not apply rounded corners
   - cache this first returned image in the staging directory and use it as the sole art input for the complete-card call
4. Generate the complete full-art card with exactly one imagegen call, using `art-only.png` as the primary edit target and the original uploaded card only as the UI, text, icon, and outer-border reference:
   - start with the concise Complete Card prompt pattern and rely on the original reference instead of listing its wording or branding in the prompt
   - keep the continuous full-card artwork from `art-only.png`; minor local illustration changes are acceptable
   - restore the original outer rounded card border/rim together with all retained UI in one generation
   - make the outermost rounded card silhouette the exact canvas boundary: at the horizontal center the rim must reach the top and bottom canvas edges, and at the vertical center it must reach the left and right canvas edges
   - leave no white, transparent, solid-color, or scanned-background band between any outer-rim edge and the corresponding canvas edge
   - match the source outer-border width on each side using the measured short-side proportions; each generated side should differ from its source proportion by no more than `1%` of the card's short side
   - restore only the non-target UI elements that are visibly present in the source, such as the title/name, stage/basic label, evolution line and backing plate, HP, type icons, attacks, damage numbers, rules text, weakness/resistance/retreat row, illustrator credit, set/regulation markings, flavor text, watermark-like printed details, logos, and bottommost copyright/manufacturer line; never invent an absent UI element
   - preserve the source wording, characters, numbers, icons, relative positions, hierarchy, backing-plate shapes, border appearance, and copyright line as closely as possible
   - remove the target horizontal species/info strip and all text printed on it
   - remove the original illustration-window frame lines
   - do not leave flat card-color panels behind the top or lower UI; continuous artwork must remain visible beneath and around the UI inside the outer border
   - use clean white or neutral text and number outlines where contrast is needed; do not add colored card-background halos
5. Accept both first successful imagegen results without visual rejection or semantic validation. Do not inspect for the purpose of deciding whether to retry, and do not run `scripts/validate_card_canvas.py` as an acceptance gate.
6. Save the first returned complete-card image in the staging directory, then run `scripts/apply_rounded_alpha.py --input <complete-card> --output <staged-final> --radius-ratio <measured-source-ratio>`:
   - keep the generated card dimensions and portrait aspect ratio
   - add an alpha channel and make only the pixels outside the rounded outer card silhouette transparent
   - use the measured source corner-radius ratio; do not use a universal default radius
   - generate the alpha mask with antialiasing and verify that partial-alpha pixels occur only along the four corner arcs, all four corner pixels are transparent, and each side center remains opaque
   - preserve the outer border and all interior artwork and UI pixels
   - validate that the final PNG is RGBA and all four corner pixels have alpha `0`
7. After both images exist and deterministic post-processing completes, create the reserved final directory and move only `art-only.png` and `full-art-card.png` into it. Delete the staging directory.
8. In the final response, show `art-only.png` followed immediately by its absolute file path, then show `full-art-card.png` followed immediately by its absolute file path. Use the label `保存路径：` for each path. Show the actual images, not path text alone, and do not number the outputs.

## Prompt Patterns

Use these internally and adapt them to the source. Do not show them to the user.

### Art Only

```text
Use the uploaded card as the edit target. Create one continuous art-only portrait image by removing all card UI, text, symbols, logos, panels, strips, frames, and the outer rim. Extend the existing illustration naturally across the complete rectangular canvas.

Preserve the visible subject, pose, expression, scale, placement, composition, style, palette, lighting, and environment. Add no typography, graphic design, unrelated objects, or additional characters. Output opaque edge-to-edge artwork with no rounded corners.
```

### Complete Card With UI and Outer Border

```text
Use the art-only image as the primary edit target and the original card as the UI and outer-rim reference. Add the source's rounded outer rim and only the non-target UI visibly present in that reference, preserving its characters, numbers, icons, positions, hierarchy, and bottom copyright line. Invent nothing.

Keep the continuous artwork visible beneath and around the UI. Omit the original horizontal species/info strip and illustration-window frame, and add no flat card-color panels. Make the outer rim reach all four canvas edges with no exterior band. Preserve the art-only subject and composition; use clean neutral outlines where needed.
```
