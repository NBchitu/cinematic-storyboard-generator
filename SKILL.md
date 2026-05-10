---
name: cinematic-storyboard-generator
description: Turn user-provided stories, scripts, scenes, or plot outlines into cinematic storyboard plans, 3x3 storyboard image sheets, consistent professional video-generation prompts, and split storyboard frame assets. Use when Codex is asked to split a narrative into film shots, recommend director styles, visual styles, aspect ratios, video formats, write prompts for video models such as SeedDance, Veo, or Kling, cut a 3x3 storyboard sheet into individual frames, or generate storyboard images with image generation for films, microfilms, animation, ads, documentaries, promos, or mobile-shot videos.
---

# Cinematic Storyboard Generator

## Core Rule

Before generating storyboard images, analyze the user's story and ask the user to choose creative direction. Do not skip this choice step unless the user already provided all required choices or explicitly says to choose for them.

Present concise recommendations in Chinese when the user writes in Chinese. Include 2-3 options for each category:

- Director style: world-famous directors plus representative works.
- Visual style: recommend suitable image styles for the script.
- Aspect ratio: recommend video/image ratios.
- Video nature: recommend the production format.

Use [references/style-menus.md](references/style-menus.md) for option pools and adapt the shortlist to the story's tone, genre, characters, and intended audience.

## Workflow

1. Read the story for genre, emotional arc, location, period, cast, key props, and ending.
2. Recommend choices before production:
   - Director style: 2-3 options, each with director, representative work, and why it fits.
   - Visual style: 2-3 options, such as realism, claymation, Pixar-like animated film, ink-wash, stop-motion, hand-drawn anime, commercial realism, documentary, or phone footage.
   - Aspect ratio: 2-3 options. Include `16:9` when the user asks for storyboard sheets or video-friendly output.
   - Video nature: 2-3 options, such as film, microfilm, animation short, ad, promo, documentary, hand-held phone video, music video, or social short.
3. Ask the user to choose one option from each category. If the user says "你来定", select the strongest coherent package and state it briefly.
4. Build a shot breakdown after choices are known:
   - Preserve the story's chronology and emotional causality.
   - Use film grammar: establishing shot, inserts, over-the-shoulder, reaction shots, close-ups, tracking shots, reverses, silence beats, and epilogue shots where useful.
   - Avoid jumps between panels. Each panel should visibly motivate the next panel.
   - Keep character design, wardrobe, lighting, location geography, props, and weather consistent across all sheets.
5. Decide sheet count from story complexity:
   - Simple scene: 1 sheet, 9 panels.
   - Short complete story: 2-4 sheets, 18-36 panels.
   - Longer script: split by acts or major turning points, usually 3-6 sheets.
6. Build the final image prompt from the selected style preset:
   - For live-action film, microfilm, documentary, commercial, or phone-shot formats, use the matching cinematic prompt preset from `style-menus.md`.
   - For animation, use an animation-specific preset and negative constraints such as `not photorealistic`, `not live-action`, and `not realistic cinema still`.
   - Do not mix `ultra realistic` or `photorealistic` into animation prompts unless the selected style explicitly calls for stylized 3D realism.
7. Build a reusable video prompt style bible before writing per-shot video prompts:
   - Derive it from the chosen director influence, visual style preset, aspect ratio, video nature, character bible, setting, lighting, color palette, lens language, camera movement language, pacing, and negative constraints.
   - Keep this bible stable for every shot unless the story explicitly changes location, time, or emotional temperature.
   - For animation, keep the prompt consistently animated; do not drift into live-action or photorealistic camera language.
8. For every storyboard panel, output a matching professional video prompt for models such as SeedDance, Veo, Kling, or other text/image-to-video systems:
   - Treat each panel as one video clip, usually 4-8 seconds unless the user specifies duration.
   - Include cinematic camera language: shot size, lens feel, angle, camera movement, blocking, subject motion, emotional beat, lighting, atmosphere, and transition intent.
   - Keep continuity explicit: character identity, wardrobe, prop state, screen direction, location geography, weather, color temperature, and previous/next beat.
   - Make prompts model-agnostic and production-ready. Avoid mentioning a specific model unless the user asks for model-specific syntax.
   - Include a compact negative prompt for each clip to prevent style drift, identity drift, text artifacts, broken motion, and unwanted cuts.
9. Before each image generation call, show the exact prompt to the user for debugging when the user asks to inspect or tune prompts. Keep doing this for the rest of that task once requested.
10. Generate one image per sheet using the built-in `image_gen` tool unless the user explicitly chooses another workflow. Each generated image should be one storyboard sheet containing a 3x3 grid of nine equal panels in the selected aspect ratio. If no ratio is selected, default to `16:9`.
11. After generation, show all sheets in order and summarize the structure in a compact shot list plus the formatted video prompt list.
12. When the user asks to cut, split, export, slice, or separate a 3x3 storyboard sheet into individual frames, use `scripts/split_storyboard_grid.py`.
13. When the user asks to manage, select, edit, preview, or cut a 3x3 storyboard sheet interactively, copy `tools/storyboard-grid-manager.html` into the current project and point the user to it. The tool overlays 1-9 labels, lets users include/exclude panels, cuts selected panels into independent image files, creates a dedicated output folder when the browser supports directory writing, exports a JSON manifest, records per-panel edit instructions, and generates one combined image-edit prompt for multiple panel edits.

## Choice Prompt Template

Use this structure before generation:

```text
我先根据剧情推荐一组创作方向，请你各选一个：

导演风格：
1. <导演>《<代表作>》：<适配原因>
2. <导演>《<代表作>》：<适配原因>
3. <导演>《<代表作>》：<适配原因>

视觉风格：
1. <风格>：<适配原因>
2. <风格>：<适配原因>
3. <风格>：<适配原因>

视频比例：
1. <比例>：<适配原因>
2. <比例>：<适配原因>
3. <比例>：<适配原因>

视频性质：
1. <性质>：<适配原因>
2. <性质>：<适配原因>
3. <性质>：<适配原因>

回复格式示例：导演 1，视觉 2，比例 1，性质 1。
如果你想让我直接决定，回复“你来定”。
```

## Storyboard Image Prompt Rules

Each sheet prompt must specify:

- Use case: `illustration-story`.
- Asset type: `cinematic storyboard sheet, <selected aspect ratio> overall image, 3x3 grid`.
- No text, no captions, no speech bubbles, no logos, no watermarks unless the user explicitly wants labels.
- Thin gutters between panels.
- Every panel exactly matches the selected aspect ratio. Use `16:9` only when the user selected it or gave no ratio preference.
- Sequential reading order: left-to-right, top-to-bottom.
- Consistent characters with age, build, face, wardrobe, and emotional state.
- Consistent location, time of day, weather, props, and color temperature.
- A panel-by-panel list with exact camera framing and story action.
- The selected prompt preset from `style-menus.md`, including style-positive terms and avoid terms.

Use this prompt skeleton:

```text
Use case: illustration-story
Asset type: cinematic storyboard sheet, <selected aspect ratio> overall image containing a precise 3x3 grid of nine equal <selected aspect ratio> storyboard panels. Thin black gutters. No text, captions, speech bubbles, logos, or watermarks.
Primary request: Generate storyboard sheet <n> of <total> for <title>. Continue directly from the previous sheet if any.
Director influence: <chosen director + representative work>, adapted as inspiration only.
Visual style preset: <copy the selected preset terms from style-menus.md>.
Avoid: <copy preset avoid terms, especially for animation>.
Video nature: <chosen video nature>.
Consistent setting: <place, time, weather, layout, props>.
Consistent characters: <character bible>.
Sheet layout: 3 rows x 3 columns, every panel exactly <selected aspect ratio>, sequential left-to-right top-to-bottom.
Panel 1: <camera + action + emotion>.
...
Panel 9: <camera + action + emotion>.
```

## Video Prompt Output Rules

When delivering a storyboard, include a `Video Prompt Style Bible` and a `Video Prompt List` unless the user only asked for still-image storyboards.

The style bible is the anchor for visual consistency. Keep it short, reusable, and stable:

```text
Video Prompt Style Bible
Project: <title>
Format: <video nature>, <selected aspect ratio>, <default clip duration>, <frame rate if requested>
Director influence: <chosen director + representative work>, adapted as inspiration only
Visual style: <selected visual style preset, rewritten as one coherent style direction>
Camera grammar: <dominant shot language, lenses, camera movement rules, handheld/stabilized/dolly rules>
Lighting and color: <time of day, color temperature, contrast, palette, atmosphere>
Characters: <consistent character bible with wardrobe, face, age, build, props>
World continuity: <location geography, weather, period, recurring props, screen direction>
Motion rules: <performance style, speed, gesture scale, allowed transitions>
Global negative prompt: no text, captions, logos, watermarks, style drift, identity drift, warped faces, extra limbs, flicker, jitter, random cuts, inconsistent wardrobe, inconsistent lighting
```

Write one prompt per panel/shot. Use this structure by default:

```text
Shot <sheet.panel> / Clip <number>
Duration: <4-8s or user-specified>
Continuity anchor: <same character/wardrobe/location/prop state; note what changed from previous shot>
Video prompt: <one polished paragraph with shot size, lens feel, camera angle, camera movement, blocking, subject action, emotional beat, lighting, atmosphere, and end frame>
Transition intent: <cut/match cut/push in/pull back/hold to next shot>
Negative prompt: <global negative prompt plus shot-specific avoid terms>
```

Professional camera language examples to use naturally where appropriate:

- Shot size: extreme wide shot, wide shot, full shot, medium shot, medium close-up, close-up, extreme close-up, insert, over-the-shoulder, point-of-view, reaction shot.
- Angle and lens: eye-level, low angle, high angle, top shot, profile, three-quarter view, shallow depth of field, deep focus, 24mm wide, 35mm natural, 50mm intimate, 85mm portrait compression, anamorphic widescreen.
- Movement: locked-off, slow push-in, dolly-in, dolly-out, lateral tracking, handheld drift, steadicam follow, crane up, tilt down, pan reveal, rack focus, parallax move.
- Blocking: foreground/background separation, screen-left to screen-right movement, reveal from occlusion, character enters frame, character exits frame, motivated eyeline, reaction beat.

Keep video prompts visually consistent across providers:

- SeedDance / Veo / Kling compatible prompts should be plain-language cinematic prompts with no vendor-only tags by default.
- Use the same style bible terms in every prompt, but vary the action and camera movement for story rhythm.
- If the user requests image-to-video, start each video prompt with `Use the storyboard panel as the first-frame visual reference` and describe only the intended motion, camera move, and ending frame.
- If the user requests text-to-video, make character and setting identity explicit inside each prompt because the model may not share memory across clips.

## Storyboard Sheet Cutting Rules

Use `scripts/split_storyboard_grid.py` when the user asks to split a generated 3x3 sheet into independent storyboard images. This is a deterministic crop operation, not an image-generation task.

Default behavior:

- Input: one 3x3 storyboard sheet image.
- Output directory: create a dedicated folder next to the source image named `<source-stem>_shots` unless the user specifies another folder.
- Crop order: left-to-right, top-to-bottom.
- Crop geometry: equal 3x3 division of the source image. Because the full sheet and each cell share the selected ratio, a `16:9` sheet produces nine `16:9` frames, a `9:16` sheet produces nine `9:16` frames, and so on.
- Naming: use continuous, sortable filenames: `shot_001_s01_p01.png`, `shot_002_s01_p02.png`, ... `shot_009_s01_p09.png`.
- Multiple sheets: continue global numbering across sheets by setting `--sheet-index` and `--start-index`, such as sheet 2 using `--sheet-index 2 --start-index 10`.
- Manifest: always keep the generated `manifest.json`; it records sheet index, panel index, row, column, crop box, size, source path, and output path.

Command examples:

```bash
python3 /Users/binjietu/.codex/skills/cinematic-storyboard-generator/scripts/split_storyboard_grid.py ./storyboard-sheet-01.png --aspect-ratio 16:9
python3 /Users/binjietu/.codex/skills/cinematic-storyboard-generator/scripts/split_storyboard_grid.py ./storyboard-sheet-02.png --sheet-index 2 --start-index 10 --aspect-ratio 16:9
python3 /Users/binjietu/.codex/skills/cinematic-storyboard-generator/scripts/split_storyboard_grid.py ./vertical-sheet-01.png --output-dir ./storyboard_frames --aspect-ratio 9:16
```

If the sheet has visible gutters, keep the equal-cell crop unless the user asks to remove gutters. If exact ratio correction is needed, pass `--aspect-ratio <ratio>` so each panel is center-cropped to the selected storyboard ratio.

## Quality Checks

Before final response, check:

- Does the full set cover beginning, conflict, revelation, turn, and ending?
- Is every panel causally connected to the next?
- Are the requested ratio and 3x3 layout honored?
- Are characters visually consistent across sheets?
- Do all video prompts reuse the same style bible and preserve visual continuity?
- Does each video prompt include camera movement, subject motion, emotional beat, lighting, and a usable end frame?
- If frames were cut, are there exactly nine outputs per sheet, continuous names, matching aspect ratio, and a `manifest.json`?
- Are generated images shown in story order?

If an output fails an essential requirement, regenerate only the affected sheet with a tighter prompt.

## Storyboard Grid Manager Tool

Use `tools/storyboard-grid-manager.html` as a standalone local preview, selection, editing, and browser-based cutting tool for generated 3x3 storyboard sheets.

When copying it into a project:

- Preserve it as a single HTML file unless the project already has an app shell that should absorb the UI.
- Keep the fixed 3x3 overlay and 1-9 labels.
- Use the `切割图片` / `切割选中分镜` buttons to split the loaded sheet into independent frame images. The tool crops from the source image pixels in 3x3 reading order, so each output frame keeps the same per-panel aspect ratio as the storyboard sheet.
- Use the generated manifest as the source of truth after cutting. It records source size, output folder, output file names, crop boxes, panel indexes, and frame sizes.
- The naming pattern is continuous and sortable: `shot_001_s01_p01.png`, `shot_002_s01_p02.png`, and so on. Users can change prefix, sheet index, start index, and output format in the tool.
- In browsers that support `showDirectoryPicker`, the tool asks the user to choose a parent folder and creates `<source-stem>_shots`. In other browsers, it falls back to downloading the frame files and `manifest.json`.
- For AI edits, pass the full original storyboard sheet image to the image model and use the generated combined prompt. The prompt intentionally names each target panel, row, column, and percentage crop region, and instructs the model to preserve every other panel.
- The `修改图片` button sends a payload to `window.storyboardGridManager.editImage(payload)` when the host page provides it, or to `window.electronAPI.editStoryboardImage(payload)` when an Electron bridge provides it. In standalone HTML mode, it copies the combined prompt and tells the user to submit the full storyboard sheet plus the copied prompt to the image editing model.
