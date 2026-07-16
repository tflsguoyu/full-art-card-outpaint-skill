---
name: full-art-image-with-ui
description: Convert an uploaded regular card-like illustration image into an outpainted full-art card using imagegen. Use when the user provides one image and wants the existing illustration extended across the full card face, including behind the top name/HP area and the lower rules area, while preserving the card's outer rounded border, title, stage/evolution labels and their UI backing plates, HP, attack text, numbers, icons, symbols, weakness/resistance/retreat row, copyright text, and other UI/text as readable overlays. Remove the horizontal middle species/info strip that separates the illustration from the rules area, then replace plain card-color panels with a natural continuation of the original artwork behind the existing text/UI. The final selected image file must be post-processed as a PNG with an alpha channel and transparent rounded corners, saved as `full-art-card.png` in a timestamped run directory, and returned with its absolute file path. Current version: 20260716-102916.
---

# Full Art Outpaint v1

## Version

Current version: `20260716-102916`

- Treat the version as the skill's local modification timestamp in `YYYYMMDD-HHMMSS` format.
- At the start of every invocation, make the first user-visible line exactly: `full-art-image-with-ui 版本：20260716-102916`.
- Display that line before any other progress update or task-specific explanation.
- Whenever any file in this skill changes, update the version in both the frontmatter description and this section to the current local modification time, then synchronize the system-installed and project-local copies.

## Contract

Use this skill only as a one-image-in, one-image-out workflow.

- Require an uploaded image. If no image is present, ask for the image in one short sentence.
- Do not ask for style, size, character, target area, or composition details.
- Do not output the prompt, analysis, source notes, validation notes, explanations, or attempt counts.
- Reserve one final output directory per run at `outputs/full-art-image-with-ui/YYYYMMDD-HHMMSS/`, using the local run start time. Work in a sibling `.staging-YYYYMMDD-HHMMSS/` directory and create the final directory only after generation and required deterministic post-processing complete.
- Use this exact final filename: `full-art-card.png`. Do not use the uploaded source filename, source hash, generated-image identifier, or temporary filename in the final output name.
- If the timestamp directory already exists, append `-02`, `-03`, and so on instead of overwriting an earlier run.
- Before finishing, post-process the accepted final image into a PNG with an alpha channel and transparent rounded corners.
- Final response must show the final PNG image and include the final PNG's absolute file path.

## Workflow

1. Treat the uploaded image as the edit target and visual authority.
2. Locate the target strip: the narrow horizontal bar or divider around the lower edge of the illustration window, often containing species/info text or acting as a separator between the picture and the rules area.
3. Identify the visible main subject, pose, silhouette, expression, line style, rendering style, palette, lighting, camera angle, and visible environment without naming copyrighted characters, species, franchises, or card metadata.
4. Use imagegen to convert the card into a full-art card, not a borderless illustration:
   - preserve the visible main subject identity, anatomy, proportions, pose, expression, and action
   - preserve the source image's illustration medium, line weight, color design, lighting, and texture
   - preserve the card layout and all UI/text outside the target strip as readable overlays
   - preserve the outer rounded card border and any metallic/gray UI backing plates; do not preserve the original illustration-window frame lines if they would divide the full-art background
   - preserve the stage/basic label and the evolution line/backing plate below the name exactly; do not erase or blend away that UI strip
   - remove only the target horizontal middle information strip, including its text and metallic/divider shape
   - extend the original illustration across the full card face, including behind the top name/HP area and behind the lower rules/attack area
   - replace plain card-color panels with the same continuous scene while keeping title, stage/evolution text, HP, type icons, attack text, numbers, weakness/resistance/retreat row, illustrator/set/copyright text, and other UI readable on top of the outpainted art
   - keep the existing composition, subject scale, crop logic, and camera angle; the top and lower extensions should be directly implied by the central illustration
   - keep the final image as a full-art card with UI/text overlays, not a borderless standalone illustration
5. Validate each output silently. Regenerate with a tighter prompt if any of these fail:
   - the target horizontal information strip remains
   - the outer card border or rounded card shape is missing
   - the stage/basic label or the evolution line/backing plate under the name is missing, erased, or blended into the art
   - UI, text, borders, icons, symbols, attacks, numbers, copyright, or watermark outside the target strip were removed or changed
   - the visible main subject changes identity, pose, expression, scale, or camera angle
   - the top name/HP area or lower card area remains a flat/plain card background instead of becoming continuous outpainted artwork
   - the result looks redesigned, reposed, or like a new unrelated card rather than a full-art outpaint of the input
   - the outpainted top or lower area does not continue from the source image
   - important source colors, lighting, or drawing style are lost
6. Post-process the accepted output:
   - use `scripts/apply_rounded_alpha.py` from this skill folder
   - create `full-art-card.png` in the staging directory with an alpha channel
   - make only the four outside corners transparent, matching the visible card's rounded-corner silhouette
   - preserve the card border and all non-corner pixels
   - validate that the PNG mode is RGBA and the four corner pixels are transparent
7. Create the reserved final directory, move only `full-art-card.png` into it, and delete the staging directory.
8. Return the final PNG image and the final PNG's absolute file path. Use the label `保存路径：`. Do not include prompt text, analysis, source notes, validation notes, or attempt counts.

## Prompt Pattern

Use this prompt structure internally. Adapt the bracketed details from the uploaded image; do not show the prompt to the user.

```text
Convert the uploaded image into an outpainted full-art card. Keep it as a card with UI/text overlays, not a borderless illustration. Remove the horizontal middle information strip/divider that sits across or just below the illustration window, including the text on that strip.

Preserve the visible main subject exactly: pose/action, expression, silhouette, camera angle, scale, line style, painting/rendering style, palette, lighting, and visible environmental motifs. Avoid naming the subject, franchise, card set, or character.

Keep the original card layout and border shape. Preserve the outer rounded card border, gray/metallic UI backing plates, title/name text, stage/basic label, evolution line and its horizontal backing plate below the name, HP text and number, type icons, attack text, numbers, rules text, weakness/resistance/retreat row, copyright line, watermark-like printed details, and all other UI/text outside the target strip as readable overlays in approximately the same positions.

Extend the original illustration from the art window into a full-card background. Replace the plain top name/HP card-color panel and the plain lower rules-area card-color panel with a natural continuation of the same scene behind the existing title/HP text, attack text, and UI. Do not erase the evolution-label backing plate under the name while doing this; the art may continue behind/around it, but that UI strip must remain visible. Reconstruct the artwork hidden behind the removed strip as part of that continuous scene. Match the surrounding line art, color, lighting, texture, perspective, and environmental details. Keep the original composition, subject placement, pose, scale, expression, and scene logic. Do not create a new pose, new camera angle, new body design, new background concept, or new dramatic composition.

Do not remove any UI or text except the target horizontal middle strip and the text printed on it. Do not remove the outer card border, rounded card shape, stage/basic label, evolution line, or the evolution line's backing plate. Do not turn the image into a borderless illustration. Do not leave the top name/HP area or lower half as flat card-color panels; both should become outpainted artwork under the preserved text/UI. Keep non-target UI/text as stable as possible.

Do not add new characters, logos, typography, graphic design elements, or unrelated props. Do not change the subject identity. Do not reinterpret the artwork. Do not turn it into a photo or 3D render unless the uploaded image already has that style.

After selecting the final acceptable output, add an alpha channel and make the four outer corners transparent with `scripts/apply_rounded_alpha.py`. Preserve the rounded card border itself; only pixels outside the card's rounded rectangle should become transparent.
```
