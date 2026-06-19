# Paper 58 VLA Highlight Hardening Plan

Objective: make Paper 58's boxed PDF highlights match the VLA-v4 role-model PDF while preserving the final full-scale robotic invariance audit benchmark and observer-only claim boundary.

## Role-Model Target

- Citation links use green rectangular borders with no fill.
- Internal references use red rectangular borders with no fill.
- URL links use the same green border family as citations.
- Border width is `pdfborder={0 0 1}`, matching the VLA-v4 annotation metadata.
- Boxes stay tight to linked text and must not affect typography, spacing, figure captions, tables, or scientific content.

## Current Paper 58 Mismatch

- `Downloads/58.pdf` is a 25-page final v3 full-scale submission candidate.
- Link annotations appear on pages 3, 4, 5, 6, 7, 8, 9, 10, 20, and 21.
- Annotation colors are already in the VLA red/green families: 16 red internal-reference links and 22 green citation links.
- All 38 links have invisible border width `0`, so the page appearance does not match the VLA-v4 role model.
- `paper/main.tex` uses `\hypersetup{hidelinks}`, which suppresses the visible link boxes.

## Execution Plan

1. Keep RAM use low by rendering only affected pages before and after the edit: pages 3, 4, 5, 6, 7, 8, 9, 10, 20, and 21.
2. Replace `\hypersetup{hidelinks}` in `paper/main.tex` with explicit VLA-style link annotation settings:
   - `colorlinks=false`
   - `pdfborder={0 0 1}`
   - `citebordercolor={0 1 0}`
   - `linkbordercolor={1 0 0}`
   - `urlbordercolor={0 1 0}`
3. Rebuild with `build_pdf.ps1`, which exports the canonical final PDF to `C:\Users\wangz\Downloads\58.pdf`, writes build metadata, and removes local `paper/main.pdf`.
4. Validate the rebuilt PDF annotation metadata with `pypdf`; expected result is 16 red internal-reference boxes and 22 green citation boxes, all with border `0 0 1`.
5. Render pages 3, 4, 5, 6, 7, 8, 9, 10, 20, and 21 again and visually compare with the VLA-v4 role model.
6. Update README/status/build metadata and SHA text if the rebuild changes the canonical PDF.
7. Remove Paper 58 temporary render folders, then commit and push the clean repo.

## Non-Goals

- Do not rerun the full-scale benchmark.
- Do not change tables, figures, result claims, page count target, or observer-only boundary language.
- Do not pad the paper or alter manuscript content beyond link-box styling and stale metadata.
