---
name: full-art-outpaint
description: Convert an uploaded regular card-like illustration image into layered outpainted full-art card outputs using imagegen. Use when the user provides one image and wants the existing illustration extended across the full card face, including the outer border area, while preserving card UI/text as a separate readable overlay. Remove the horizontal middle species/info strip that separates the illustration from the rules area, generate an art-only full-face image and a UI/text-only overlay, correct colored text outlines to white only if needed, composite them, then also create a variant with the original outer border restored. Final selected images must be post-processed as PNGs with alpha channels and transparent rounded corners.
---

# Full Art Outpaint

## Contract

Use this skill as a one-image-in, layered-output workflow.

- Require an uploaded image. If no image is present, ask for the image in one short sentence.
- Do not ask for style, size, character, target area, or composition details.
- Do not output the prompt, analysis, source notes, validation notes, explanations, or attempt counts.
- Before finishing, post-process final composite images into PNGs with alpha channels and transparent rounded corners.
- Final response must show the rounded PNG outputs and include their absolute file paths.

## Workflow

1. Treat the uploaded image as the edit target and visual authority.
2. Locate the target strip: the narrow horizontal bar or divider around the lower edge of the illustration window, often containing species/info text or acting as a separator between the picture and the rules area.
3. Identify the visible main subject, pose, silhouette, expression, line style, rendering style, palette, lighting, camera angle, and visible environment without naming copyrighted characters, species, franchises, or card metadata.
4. Use imagegen to create and save an art-only full-card-face image:
   - preserve the visible main subject identity, anatomy, proportions, pose, expression, and action
   - preserve the source image's illustration medium, line weight, color design, lighting, and texture
   - remove all card UI/text, icons, printed logos, rules text, numbers, backing plates, and the target horizontal middle information strip
   - extend the original illustration across the full card face, including the area where the outer border/rim was, the top name/HP area, and the lower rules/attack area
   - keep the existing composition, subject scale, crop logic, and camera angle; extensions should be directly implied by the central illustration
   - save this intermediate as the art-only layer
5. Use imagegen to create and save a UI/text-only overlay layer from the original image:
   - include card UI/text, icons, title/name, stage/basic label, evolution line/backing plate, HP, type icons, attack text, numbers, rules text, weakness/resistance/retreat row, illustrator/set/copyright text, watermark-like printed details, and other non-art printed elements
   - exclude the target horizontal middle information strip and its text
   - exclude the original illustration-window frame lines if they would divide the full-art background
   - keep the overlay transparent wherever there is no UI/text/backing plate
   - do not include the original outer border/rim in this overlay; the original-border variant is created later as a separate output
6. Inspect the UI/text-only overlay for colored outer strokes inherited from the source card background color. This includes title/name, HP, attack names, rules text, damage numbers, weakness/resistance/retreat labels, illustrator text, set markings, copyright, and other printed text outside the removed strip.
   - If the text overlays already use clean white or neutral readable outer strokes, do not run any text-outline correction.
   - If any major text overlay has an obvious colored card-background outline, run one minimal local imagegen edit on the UI/text-only overlay to change only those colored text outlines to clean white outer strokes, matching the readability style of the lower attack text.
   - Preserve exact characters, numbers, positions, sizes, spacing, icons, backing plates, and all other UI pixels as much as possible.
7. Composite the accepted art-only layer and accepted UI/text-only overlay into a full-art card image without the original outer border/rim:
   - place the UI/text-only overlay exactly over the art-only layer
   - preserve all readable UI/text and the continuous full-card illustration
   - save this composited image as the no-original-border full-art output
8. Create a second final variant from the no-original-border composite by adding back the original image's outer rounded card border/rim:
   - preserve the composite image inside the border
   - restore only the original outer card border/rim and rounded printed frame from the source image
   - do not restore the original illustration-window frame or target horizontal middle information strip
   - save this as the original-border-restored full-art output
9. Validate outputs silently. Regenerate or redo the relevant layer with a tighter prompt if any of these fail:
   - the target horizontal information strip remains
   - the art-only layer still contains visible UI/text, icons, logos, backing plates, or card frame elements that should be on the overlay
   - the UI/text-only overlay contains background illustration where it should be transparent
   - the no-original-border composite is missing UI/text or has unreadable text
   - the original-border-restored output lacks the original outer rounded card border/rim or restores unwanted original frame/strip elements
   - the stage/basic label or the evolution line/backing plate under the name is missing, erased, or blended into the art
   - UI, text, borders, icons, symbols, attacks, numbers, copyright, or watermark outside the target strip were removed or changed
   - the visible main subject changes identity, pose, expression, scale, or camera angle
   - the top name/HP area or lower card area remains a flat/plain card background instead of becoming continuous outpainted artwork
   - the result looks redesigned, reposed, or like a new unrelated card rather than a full-art outpaint of the input
   - the outpainted top or lower area does not continue from the source image
   - important source colors, lighting, or drawing style are lost
10. Post-process both final outputs:
   - use `scripts/apply_rounded_alpha.py` from this skill folder
   - create or overwrite final PNG versions with alpha channels
   - make only the four outside corners transparent, matching the visible card's rounded-corner silhouette
   - preserve the card border and all non-corner pixels
   - validate that the PNG mode is RGBA and the four corner pixels are transparent
11. Return the rounded PNG images for both final outputs and their absolute file paths. Do not include prompt text, analysis, source notes, validation notes, explanations, or attempt counts.

## Prompt Patterns

Use these prompt structures internally. Adapt the bracketed details from the uploaded image; do not show the prompts to the user.

### Art-Only Layer

```text
Convert the uploaded image into an art-only full-card-face illustration layer. This should be only the continuous artwork, with no card UI, no text, no numbers, no icons, no printed logos, no rules area, no backing plates, no illustration-window frame, no outer card border/rim, and no horizontal middle information strip.

Preserve the visible main subject exactly: pose/action, expression, silhouette, camera angle, scale, line style, painting/rendering style, palette, lighting, and visible environmental motifs. Avoid naming the subject, franchise, card set, or character.

Extend the original illustration across the entire card rectangle, including the area where the original outer border/rim was, the top name/HP area, and the lower rules/attack area. Reconstruct the artwork hidden behind removed UI as a natural continuation of the same scene. Match the surrounding line art, color, lighting, texture, perspective, and environmental details.

Keep the original composition, subject placement, pose, scale, expression, crop logic, and scene logic. Do not create a new pose, new camera angle, new body design, new background concept, or new dramatic composition.

Do not add new characters, logos, typography, graphic design elements, or unrelated props. Do not turn it into a photo or 3D render unless the uploaded image already has that style.
```

### UI/Text-Only Overlay

```text
Convert the uploaded image into a transparent UI/text-only overlay layer for compositing over a full-art background. Keep only the card's non-art printed elements: title/name text, stage/basic label, evolution line and its horizontal backing plate below the name, HP text and number, type icons, attack text, damage numbers, rules text, weakness/resistance/retreat row, illustrator text, set markings, copyright line, watermark-like printed details, and other UI/text outside the target strip.

Remove the horizontal middle information strip/divider around the lower edge of the illustration window, including its text. Remove the original illustration-window frame lines if they would divide the full-art background. Do not include the original outer card border/rim in this overlay.

All areas without UI/text/backing plates should be transparent. Preserve exact characters, numbers, icons, symbols, positions, sizes, spacing, and backing-plate shapes as much as possible.

If any major text or number has an obvious colored outline inherited from the original card background color, change only that colored outer stroke to a clean white outer stroke for readability. Do not rewrite, translate, redesign, or move the text.
```

### Original-Border Variant

```text
Using the composited full-art card image as the target and the original uploaded card as the border reference, add back only the original outer rounded card border/rim and rounded printed frame.

Preserve the full-art composite inside the border. Do not restore the original illustration-window frame, the horizontal middle information strip, or any removed source-card flat color panels. Do not alter the subject, background art, UI/text overlay, icons, numbers, or backing plates.

The result should be the same full-art composite with the original card's outer border/rim visibly framing it.
```

### Rounded Alpha

```text
After selecting the final acceptable output, add an alpha channel and make the four outer corners transparent with `scripts/apply_rounded_alpha.py`. Preserve the rounded card border itself; only pixels outside the card's rounded rectangle should become transparent.
```
