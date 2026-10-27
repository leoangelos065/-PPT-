# Cross-platform execution

## Start from the current device

Detect OS, Python, available presentation libraries, renderers and fonts. Keep build assets in a task-local directory and resolve bundled script paths relative to this skill. Never carry over a prior device's user name, drive letter, application path, font cache or COM assumptions.

## PowerPoint and rendering

- Windows: use installed PowerPoint automation when available; preserve existing open user documents and use task-specific output names.
- macOS: Windows COM and `win32com` are unavailable. Use an available supported PowerPoint export/UI/automation route, or export manually when that is the only permitted route. Do not assert that Windows automation ran on Mac. Never grant accessibility or automation permissions silently.
- A secondary renderer, such as LibreOffice, can help when PowerPoint is unavailable, but its typography and SVG support can differ. Identify the renderer in the report and leave native PowerPoint appearance unverified until checked there.
- If the user uses WPS and it is available, inspect and export the actual PPTX there. A LibreOffice preview with missing or substituted Chinese glyphs cannot validate WPS output. After external edits, close the stale task document without saving over the generated file, reopen the updated PPTX, and export again; preserve any concurrent user edits separately.
- WPS may append a suffix to an export rather than overwrite an older PNG. Verify the export's path, modification time and contents before making a comparison; normalize the newest verified render to the final filename so a stale preview is not delivered.
- With python-pptx/OOXML, explicit fills and lines may still inherit theme effects in WPS. When the reference has no shadow, suppress the shape's theme effect reference (`a:effectRef idx="0"`) and set an empty `a:effectLst` in its shape properties as needed. Apply this to native shapes and connectors, then verify the export; setting a fill alone does not clear inherited effects.
- Export the reconstructed slide, align it to the original image dimensions, and inspect local glyph masks, icon shapes and full composite badges. Do not stretch the image or alter its aspect ratio merely to lower a metric.

## Fonts

Inventory real family/style names on the current device. On macOS, user-installed fonts normally live under `~/Library/Fonts`; on Windows, use the OS font inventory rather than assuming one particular user's font directory. Use Font Book or the platform's normal mechanism where appropriate; verify the font is active and reopen the renderer after installation.

Download missing fonts only from legitimate sources and verify the license, family and required weight. Do not distribute commercial font files with the skill. Do not assume that naming a Windows-only font in a PPT guarantees it exists on Mac. Use permitted embedding where supported, otherwise disclose dependencies and inspect the target device's rendered output.

## Bundled audit

Run `python3 <skill-dir>/scripts/audit_pptx.py --pptx <deck> --report <report.json>` (or the current environment's Python command). It uses only the Python standard library and reads the PPTX without changing it.

The report lists slide components, text, declared fonts and basic structural problems, including grouped children. It does not identify the original font, measure actual rendered glyph overflow or out-of-slide bounds through group transforms, guarantee grouping usability, or prove pixel-perfect fidelity. Use the renderer and visual checks to establish those facts. Record verified exceptions instead of renaming objects to hide a problem.

## Self-improvement when authorized

Persist lessons in the installed skill during an active task after validating them. Keep a backup/diff before replacing local instructions with a newer GitHub version. Publish skill updates only when authorized, and include reusable instructions or helpers rather than the user's source images, PPTX files, rendered comparisons, personal paths or case-specific text unless the user separately requests those artifacts be published.
