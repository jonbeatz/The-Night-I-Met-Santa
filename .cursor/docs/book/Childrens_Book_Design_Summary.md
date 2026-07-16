# Children's Book Design Summary: Requirements & Best Practices

> **Absorbed 2026-07-15** into living docs: `BOOK-PRODUCTION-SYSTEM.md` §8b + Print gates · `RESEARCH-VERDICT.md` (Lulu sRGB) · `BOOK-PLAN.md`.  
> Keep this file as the raw note; prefer the playbook when they differ. **Important correction:** Lulu full-color → **sRGB**, not CMYK-first.

## 1. Technical File Requirements
* **Interior Files**: Export as a single, multi-page PDF with all 32 pages in order.
* **Cover File**: A separate PDF containing the front cover, back cover, and spine, based on the printer's specific template.
* **Resolution**: All images must be at 300 DPI for print clarity.
* **Color Space**: CMYK is preferred for professional print to avoid color shifting, though some platforms can convert from RGB.
  * → **Lulu (our printer):** use **sRGB** for full-color interiors (their presses run sRGB; CMYK may convert poorly).
* **Bleed**: Include a 0.125” bleed on all outer edges to prevent white gaps during trimming.

## 2. Two-Page Spread Layouts
* **Design Workflow**: Design using two-page spreads within your software to maintain visual continuity across the gutter.
* **Gutter Safety**: Keep critical elements (faces, text, main subjects) away from the center "gutter" fold, as they can be obscured by binding.
* **Bleed on Spreads**: Apply the 0.125" bleed to the outside edges of the total spread.
* **Exporting**: Verify if your chosen printer (e.g., Lulu/BookBaby) requires the final PDF to be uploaded as individual single-page files or as consecutive spreads.
  * → **Lulu:** upload **single pages in reading order** (we design as spreads, then split L/R).

## 3. General Best Practices & Tips
* **Use Templates**: Always download the specific template for your chosen book size *before* starting your layout to ensure accurate margins and alignment.
  * → Cover template: after final page count + paper known (spine depends on both).
* **Flatten Layers**: Flatten your images before exporting your PDF to prevent text or image shifting during the print process.
  * → Our stack already flat JPEG via Pillow.
* **Order a Proof**: Always order one physical proof copy before committing to multiple copies to check color accuracy, text legibility, and binding quality.
* **Paper Weight**: Opt for "Premium Color" or heavier paper weights (70lb–80lb) to provide an heirloom feel and prevent bleed-through.
