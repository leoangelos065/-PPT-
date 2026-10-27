---
name: image-to-ppt-function
description: Reconstruct images and diagrams as high-fidelity PowerPoint files with independently editable small components and carefully matched fonts, weights, and text formatting.
---

# 图片转ppt功能

Use this skill when the user wants an image, screenshot, infographic, workflow diagram, or image-generation result delivered as a PPTX. Default to PPTX when the user asks to generate an image for presentation use, unless they explicitly ask for an image-only output.

## Choose the right mode

### Direct image-to-PPT

Use this only when the user explicitly requests a flattened image slide. Otherwise default to editable high-fidelity reconstruction, including when they simply say “使用该skill转换图片”. Create one slide per source image and retain its native aspect ratio unless instructed otherwise.

### Editable high-fidelity reconstruction

Use this when the user says “可编辑”, “一模一样”, “一比一”, “可以修改文字”, or provides a diagram/infographic where text needs to change later.

- Make normal titles, labels, formulas, and body text real PowerPoint text boxes.
- Rebuild every simple card background, panel border, band, arrow, connector, divider, badge, circle, and basic geometry as an independent native PPT shape. Set fills, gradients, corner radii, outlines, and effects explicitly; suppress theme shadows that are absent from the reference. Use genuine ellipses for circular badges.
- Decompose to small meaningful components: each icon, label, number, card fill, border, connector, and illustration must be independently selectable and draggable. An icon with its label may additionally form an optional group, but its children must remain separately editable after ungrouping. Give objects descriptive names and use correct layer order.
- Do not flatten a whole column, card, panel, diagram, or bottom band into an image containing multiple separable components. Do not evade this by making screenshot tiles. A large photograph or continuous painting may remain one image because it is inherently raster content.
- Keep a complex illustration or detailed icon as an individual tightly cropped image/SVG only when faithful native reconstruction is impractical. SVG embedding alone does not prove native editability; verify conversion/ungroup behavior before claiming it. A diagram embedded within a photograph may remain photographic content; a standalone textbook diagram must be decomposed like other diagrams.
- For complex raster source artwork that contains text, remove the source text before placing the module, then overlay the corresponding editable text. Use tightly bounded, local repairs so illustrations are not damaged.
- Treat pictorial check marks, crosses, arrows and similar marks as artwork, not automatically as Unicode/font characters. Match the original silhouette, stroke width, terminal shape and angle with native paths or a tightly bounded independent image when that is more faithful. Keep surrounding labels as ordinary text; do not flatten the containing card or badge to fix one icon.

## Reconstruction workflow

### Default effort and review

- Default to one editable build and one quick visual review in the target app, using its on-screen view or a screenshot. There is no required number of revision rounds. Batch known corrections; repeat a check only for a material mismatch or a user-requested refinement.
- Full-slide PNG/PDF exports, comparison images and heatmaps are optional diagnostic artifacts. Generate them when the user asks or when a concrete unresolved problem needs that evidence. Do not export a full image after every edit or deliver preview images by default.
- Keep review focused on readable text, faithful content, obvious font/weight differences, line breaks, alignment and overlap. Stop chasing minor antialiasing or one-to-two-pixel differences once they no longer materially affect the result. Preserve any stricter fidelity target explicitly requested by the user.
- Reuse a valid prior visual check when a save only embeds fonts and verified visible text, typography and geometry are unchanged. Run the final structural audit once; repeat it only after a relevant artifact change or a failed check.

1. Inspect the source at its native pixel dimensions. Match the slide ratio to the source unless the user requests a different format.
2. Transcribe and manually verify all text. Preserve intentional line breaks; fix OCR errors before building.
3. Build only the modules needed for the specific image. Use native objects for simple structure and independent image assets for complex visuals.
4. Perform the font-matching procedure below before final typography. Do not apply a universal Chinese or Latin fallback to the entire slide.
5. Avoid automatic wrapping for single-line labels. Widen the text box first, then tune font size and position. Use explicit line breaks only when the reference has them.
6. Review the actual PPTX in the user's target presentation app (such as PowerPoint or WPS) when available. Compare its visible result with the source at matching scale. Use an export or overlay only when requested or needed to diagnose a concrete mismatch. Correct material typography, wrapping or text-removal problems together, then check the affected regions. A library preview does not establish the app's actual appearance.
7. Run the bundled `scripts/audit_pptx.py` before delivery. Inspect its component/font inventory and resolve reported structural issues; use actual-render visual checks for text overflow, wrapping, geometry, palette and damaged media. A structural pass alone is not visual acceptance.

### Refining an existing PPT against its source image

- Preserve the original image and a task-specific snapshot of the starting PPTX during refinement. When the user asks to reproduce or correct against the original image, that image governs both wording and appearance. Transcribe it directly; use the existing deck only as an editable starting point or asset donor. Reuse photographs or icons only after confirming they match the image. Preserve wording that the user explicitly requested to change, and record those intentional differences instead of silently adopting a prior deck's text.
- Make a short, region-by-region discrepancy list before editing: font family and weight, line spacing and wrapping, card bounds and gaps, badges and check marks, colors, and stray formatting. Measure card edges before moving them; leave geometry that already aligns alone and make the smallest visible correction.
- Inspect paragraph-level formatting as well as font runs. Check inherited bullets or numbering, hanging indents, paragraph and line spacing, trailing empty paragraphs, text highlight or shading, and placeholder/theme defaults. These can create visible mismatches even when the selected font is correct.
- Batch related edits, then quickly check the affected regions in the target app. Add a labeled side-by-side export when the user requests it or a visual question remains unresolved; it is not required after every edit. Run the final structural audit and distinguish its result from the visual review.

## Match fonts and formatting

- Inventory each text role and mixed-format span: family, real font weight, bold, italic, size, color, character spacing, line spacing, paragraph alignment, baseline, superscript/subscript, and explicit breaks. Preserve partially bold text using separate runs rather than bolding the whole sentence. Use matching East Asian and Latin faces per run when the reference requires it.
- Infer candidate families from visible glyphs, not merely text-box width. Test serif/sans-serif classification, characteristic Chinese strokes, Latin letter forms, and numeral shapes. Raster images usually lack font metadata, so record identification confidence rather than treating a guess as the original font.
- Enumerate installed fonts first. Render representative title, header, body, and mixed-language crops through the actual PowerPoint renderer, varying family and real weight before tuning size and position. Prefer genuine Bold/Semibold/Black files over synthetic bold when their glyphs match the reference.
- If a promising or identified font is missing, search and download it autonomously from its official vendor, author repository, Google Fonts, or another legitimate distribution. Obtain the needed weight files and verify the family/style metadata, license, and file integrity. Use task-local downloads and per-user installation where needed; do not buy fonts, bypass licensing, or run untrusted installers. If a proprietary original cannot legally be obtained, report that limitation and identify any substitute explicitly.
- Reopen PowerPoint after font installation and verify that the requested face is actually rendered without font substitution. Set explicit East Asian and Latin typefaces in the PPTX. Embed fonts when supported and their embedding rights allow it; otherwise disclose the font dependency and retain lawful font files/source information with build assets.
- Compare tightly bounded text crops using glyph silhouettes/edges and foreground masks, with consistent alignment and resolution. Tune size, spacing, line breaks, and coordinates after family/weight matching. Whole-slide pixel averages are dominated by backgrounds and cannot by themselves identify a font or prove a match. Reject changes that lower an average while visibly worsening text.
- Calibrate visible text width and height independently. A line can have the correct width while its glyphs are too short. After confirming family and real weight, try font size and character spacing together to match both dimensions, then correct the baseline/position. Validate the resulting glyph shapes and inter-character gaps in the actual app; do not force a bounding-box match with colliding letters, excessive tracking, or unverified nonuniform stretching. Keep the text normally editable.

## Component and typography acceptance

- Use the user's originally uploaded image file as the authoritative visual reference. A copy pasted into a PPT, screenshot of the app, or prior generated preview is only auxiliary evidence: scaling, cropping, compression, and color handling may have changed it. If the original is available, always compare to that file at its actual native dimensions. Preserve user-added reference slides and other edits while modifying the editable slide.
- Build a per-region calibration record for title spans, subtitle, headers, body paragraphs, captions, badges, and footer: visible glyph bounding box in source pixels, text baseline, gaps to neighboring objects, font size/weight, foreground RGB, fill RGB, and line spacing. Measure visible glyph extents rather than equating the text-box rectangle with the text itself. Convert pixels to points using the actual slide/export dimensions, and calibrate internal margins and vertical anchors explicitly.
- A title may contain differently sized phrases. Match those phrases using separate editable runs or text boxes. Sample colors from solid stroke interiors and flat background interiors, avoiding antialiased edges, shadows, and JPEG noise; record estimates and visually check them. Font matching includes size, position, spacing, color, and partial bold, not only family names.
- Verify PowerPoint's actual Font.Name, NameFarEast, and NameAscii (or equivalent) for representative Chinese, Latin, and mixed runs. Where a mixed text box needs different scripts, create intentional runs and document that selection may show multiple fonts. A correct East Asian typeface alone does not justify saying that the font-bar issue is fixed.
- When a detailed comparison is requested or necessary, export at the original image dimensions and inspect aligned overlays or enlarged regional crops. Revise the largest material discrepancies and record the relevant measurements. Do not accept a result based only on slide-wide similarity or a structural audit. If exact font identification remains uncertain, state that plainly.

- Keep a component inventory mapping source regions to PPT objects and noting each representation. Inspect the actual PPTX hierarchy: verify that small components are separate objects, that grouped children remain accessible, and that no panel-sized raster hides editable structure.
- Check an example from every component category by selecting/moving it independently in PowerPoint when available. Check text boxes for overflow and substitution using renderer measurements where possible, in addition to visual inspection.
- Inspect rendered text crops from every role at enlarged scale beside the reference. Record remaining family/weight uncertainty and local differences. An audit script passing means only its implemented checks passed; do not claim it proves no clipping, correct fonts, or exact visual fidelity.
- Never rename objects merely to evade an audit failure. Determine whether it is a real geometry error or a false-positive heuristic, then correct the geometry or document and verify the false positive with measurements.

### Text inside badges and diagrams

- Verify each label literally against an enlarged source crop, including case, punctuation, spelling and abbreviations. Disable inherited all-caps/small-caps formatting when absent from the reference. Do not silently replace an unusual source spelling with a more familiar word; record uncertain lettering separately.
- Calibrate the enclosing shape first: visible contour, width/height, fill and center. Then align the visible glyphs relative to that contour, with explicit text margins and baseline. Centering a text box does not prove that its visible lettering is optically centered. Check the badge as one composite region, not only as separate text and fill crops.
- Retain native shape and label objects separately, optionally grouped for moving together; verify that text remains directly editable inside the group and that children remain accessible after ungrouping. Do not trade away normal text editing merely to improve the badge's match. An isolated non-text icon may instead be a traced path or independent raster asset, with that representation disclosed.

## Task-driven self-improvement

When the user requests ongoing self-improvement of this skill, use demonstrated feedback and render comparisons to identify the cause, test a scoped correction, and persist the reusable decision rule in this installed skill without requiring the user to repeat the lesson. Preserve working typography and unrelated user edits; validate the skill and the revised artifact. Prefer refining existing guidance over accumulating duplicate rules. This applies during authorized task execution, not as a promise of background activity, automatic model retraining, or unrestricted changes to other skills/settings. Stop an iteration when further changes are unverified or regressions appear, and report remaining discrepancies honestly.

## Fidelity and editability rules

### Fine-detail acceptance gate

- Inventory all thin/dotted/dashed lines, footnotes, citations, tiny labels and punctuation before rebuilding. Never omit them because they are small. Transcribe small text from an enlarged original crop; preserve content, punctuation, deliberate breaks, alignment and margins. Mark genuinely unreadable glyphs as uncertain rather than replacing wording with a paraphrase.
- For each dashed line, record endpoints, baseline, stroke width, color, dash length, gap, phase, and cap shape. Compare at native scale and enlarged scale. If a PowerPoint preset differs visibly, build separate editable short segments with explicit properties. Remove theme effects from lines and connectors as well as from shapes. Verify corner radii, border thickness, and shape fill separately.
- Maintain a discrepancy checklist by source region. After rendering, record fixed items and remaining text-family, glyph-size, position, color, and dash mismatches, with enlarged comparison evidence. Structural checks and naming changes cannot clear a visual discrepancy. Preserve source uncertainty caused by JPEG compression or illegible small lettering.
- A demand for “完全一模一样” sets the fidelity target, not evidence that it has been attained. Only claim exactness if the claimed aspect was actually verified. When native editable text still differs, deliver the best verified editable result with the remaining differences and concrete alternatives; do not replace editable text with raster or outlined text without explaining the loss of normal text editing.
- If requested, research alternative conversion tools using official project documentation, distinguish tested results from README claims, and explain limitations against the user's two requirements (independent component editing and font fidelity). A raster editor may help masks, color sampling and tracing without providing PPTX export or font recovery. Do not upload the user's image to third-party services unless that external processing is authorized. Keep advice about tools tied to the observed failure.
- When the user authorizes trying alternatives, produce separate normal-text and outlined-text variants rather than silently changing editability. Source glyph masks can be traced with Inkscape/Potrace and converted into native PowerPoint custom-geometry groups; verify that these can move and ungroup, and state clearly that outlined letters are no longer ordinary editable text. Compare both against the original using local crops. Report substituted OCR/inpainting backends in any open-source converter trial; results from an adapted backend do not establish how every original backend performs.
- Work from a task-specific snapshot when comparing candidates. Re-read live source files before taking new input: users may be editing the deck concurrently. Preserve their edited file, and keep reproduction of the original image separate from their revised wording; do not inadvertently score different text against the original reference.

- Never claim pixel-perfect identity for independently rendered text unless it has been verified. Raster originals do not expose their font metadata or anti-aliasing settings.
- State any remaining limitation only when it materially affects use. Typical residuals are font rasterization and complex icon internals.
- If the user permits it, use a source crop for a complex icon that cannot be recreated faithfully; tell them that only that icon is not independently editable.
- Do not delete prior deliverables unless the user explicitly asks. When task-folder cleanup is authorized, finish the final render, comparison and audit first, then retain the final outputs and necessary reference/build inputs while removing superseded drafts, duplicate exports and temporary crops within that scope. Check script dependencies before deleting assets, preserve the user's original files and unrelated work, and verify the retained file list.

## Delivery

Save the final PPTX in the user’s requested folder, use a descriptive Chinese filename when the source is Chinese, and provide a clickable local file link. State which content remains raster and any unconfirmed font match. Keep the object inventory, font source/weight records, and before/after evidence in the private build folder. Do not label a result “字体一致” or “完全一样” while a material family, weight, or formatting discrepancy remains.

## Cross-platform execution

Read [references/cross-platform.md](references/cross-platform.md) when moving between Windows and macOS, choosing a renderer, or installing fonts. Do not assume Windows COM, a particular user's paths, another installed skill, or bundled commercial fonts are available. Preserve the same fidelity/editability acceptance criteria on both platforms, and disclose when target-device rendering has not been tested.
