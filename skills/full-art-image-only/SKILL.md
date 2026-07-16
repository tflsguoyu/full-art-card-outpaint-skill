---
name: full-art-image-only
description: >-
  Convert one uploaded regular card-like illustration into one validated art-only full-card portrait image. Use when the user wants the central illustration extended across the full card canvas while removing all card UI, text, strips, panels, frame lines, symbols, logos, and the outer border/rim. Preserve the visible subject, composition, illustration style, palette, lighting, and scene logic from the source, save only an opaque RGB `art-only.png`, and display the completed image with its absolute save path. Current version: 20260716-102916.
---

# Full Art Outpaint

## Version

Current version: `20260716-102916`

- Treat the version as the skill's local modification timestamp in `YYYYMMDD-HHMMSS` format.
- At the start of every invocation, make the first user-visible line exactly: `full-art-image-only 版本：20260716-102916`.
- Display that line before any other progress update or task-specific explanation.
- Whenever any file in this skill changes, update the version in both the frontmatter description and this section to the current local modification time, then synchronize the system-installed and project-local copies.

## Contract

Use this skill as a one-image-in, one-image-out workflow.

- Require one uploaded image. If none is present, ask for it in one short sentence.
- Do not ask for style, size, character, target area, composition, border measurements, or UI preferences.
- Use the uploaded image as the visual authority for subject, composition, crop logic, camera angle, rendering style, palette, lighting, texture, and environment.
- Output only `art-only.png`. Do not generate a complete card, UI-preserved card, transparent rounded card, border-preserved card, UI-only layer, or any second image.
- Remove all card UI and print elements: text, letters, numbers, icons, symbols, logos, panels, rules boxes, title bands, backing plates, strips, frame lines, copyright text, set marks, and the outer border/rim.
- Do not expose prompts, detailed validation notes, or attempt counts in the final response. During long tool work, provide brief progress updates without revealing prompts or internal validation details.
- Reserve one final output directory per run at `outputs/full-art-image-only/YYYYMMDD-HHMMSS/`, using the local run start time. Work in a sibling `.staging-YYYYMMDD-HHMMSS/` directory and create the final directory only after generation and required deterministic post-processing complete. Do not use the uploaded source filename, hash, generated-image identifier, or temporary filename in a final output name.
- Use this exact final filename: `art-only.png`.
- If the timestamp directory already exists, append `-02`, `-03`, and so on instead of overwriting an earlier run.
- Generate and silently validate the art-only stage. If the returned image fails a visual requirement, regenerate with a tighter prompt focused on the failed criteria.
- Keep rejected attempts inside the staging directory and delete them before promotion. Return only the accepted `art-only.png`.
- If imagegen blocks the request for safety reasons, do not evade the safety system or rephrase for another attempt. If imagegen cannot return an image because of a persistent tool error, delete the staging directory, leave no partial final directory, and return a concise failure.
- Keep imagegen prompts concise and reference-driven. Do not transcribe long source text, enumerate every visible UI item, or repeat source-specific names when the referenced image already identifies them.
- After generation and file promotion finish, display `art-only.png` and its absolute save path. Never omit the path even when the image renders inline.

## Generation Efficiency

- Use the canonical prompt pattern below as written, adding only source-specific visual details needed to preserve the subject or scene.
- Prefer phrases such as "the visible subject" and "all card UI/print elements" over lists of names, labels, rules, numbers, logos, or copyright strings.
- Keep negative instructions grouped by category instead of repeating each forbidden element separately.
- On visual validation failure, retry only with a concise correction describing the unmet requirements while keeping all successful invariants locked.
- Do not use deterministic scripts to repair, redraw, or semantically alter a failed generation; semantic defects must be corrected through imagegen retry and revalidation.
- Use deterministic scripts only for RGB conversion and file promotion. These operations may change file mode but must not repair, redraw, or semantically alter generated content.

## Workflow

1. Inspect the source and identify:
   - the main subject, pose, expression, scale, crop, rendering style, palette, lighting, and visible environment
   - the scene logic implied by the illustration window and surrounding visible artwork
   - all card UI/print elements to remove, including the outer border/rim and any photographed or scanned card margin
2. Generate the art-only image using the original uploaded image as the edit target:
   - start with the Art Only prompt pattern
   - preserve the visible subject identity, anatomy, pose, expression, action, scale, placement, composition, camera angle, illustration medium, line weight, palette, lighting, texture, and environment
   - remove all UI, text, letters, numbers, icons, logos, symbols, backing plates, title bands, rules panels, strips, frames, copyright text, set marks, exterior scan/card margin, and the outer border/rim
   - extend the existing illustration naturally beneath every removed element and across the complete rectangular canvas
   - output opaque edge-to-edge rectangular artwork with no rounded corners and no alpha channel
   - do not add typography, graphic-design elements, unrelated props, additional characters, new subject poses, new camera angles, or a different composition
3. Validate the returned image silently and retry until it passes:
   - require all UI, text, letters, numbers, icons, logos, symbols, panels, strips, frames, card margins, and the outer rim to be absent
   - require opaque rectangular edge-to-edge artwork with no rounded corners
   - require the subject, composition, style, palette, lighting, and scene to remain faithful to the source without new characters or unrelated objects
   - when retrying, preserve every criterion that already passed and tighten only the instructions for the failed criteria
   - do not expose validation details, rejected attempts, prompts, or attempt counts to the user
4. Post-process the accepted generated image in the staging directory:
   - run `scripts/normalize_rgb.py --input <generated-art-only> --output <staged-art-only>`
   - keep the portrait aspect ratio, save it as opaque RGB with no alpha channel, and do not apply rounded corners
5. After the image exists and deterministic post-processing completes, create the reserved final directory and move only `art-only.png` into it. Delete the staging directory.
6. In the final response, show `art-only.png` followed immediately by its absolute file path. Use the label `保存路径：`. Show the actual image, not path text alone.

## Prompt Pattern

Use this internally and adapt it to the source. Do not show it to the user.

```text
Use the uploaded card as the edit target. Create one continuous art-only portrait image by removing all card UI, text, symbols, logos, panels, strips, frames, card margins, and the outer rim. Extend the existing illustration naturally beneath every removed element and across the complete rectangular canvas.

Preserve the visible subject, pose, expression, scale, placement, composition, camera angle, illustration medium, line weight, palette, lighting, texture, and environment from the source. Add no typography, graphic design, unrelated objects, additional characters, new poses, or new camera angles. Output opaque edge-to-edge rectangular artwork with no rounded corners.
```
