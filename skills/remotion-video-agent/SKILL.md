---
name: remotion-video-agent
description: Use when creating or editing Remotion videos, programmatic explainers, motion graphics, MP4 renders, GIF renders, social cutdowns, captions, or React-authored and data-driven video templates, and when finishing generated footage with exact text, overlays, CTA and aspect-ratio variants. Not for AI-generated footage itself (use generative-media-director) or in-page web animation (use motion-director).
---

# Remotion Video Agent

## When to use

- Building or editing a Remotion composition: explainers, product demos, social cutdowns, captions, templated or data-driven video.
- Finishing generated or captured footage with exact typography, logo lockups, CTA and variants.
- Rendering MP4 (delivery) or GIF (previews only).

## When not to use

- Generating footage or stills with AI providers: use `generative-media-director` first, then return here to finish.
- Animating a live web page: use `motion-director` or `site-motion-excellence-director`.

Load the official Remotion skills (`remotion-best-practices`, `/remotion-docs`) when installed; they are installed separately, see the orchestrator's dependency notes.

## Workflow

1. Confirm the composition format: aspect ratio, duration, FPS, destination, and voice/music requirements.
2. Break the video into scenes with frame ranges.
3. Build scenes as React components with deterministic, frame-derived timing. Avoid wall-clock time, unseeded randomness, and network-dependent rendering.
4. Use Remotion helpers for interpolation, sequencing, audio, static files, and rendering.
5. Prefer MP4 for delivery. Use GIF only for previews or documentation.
6. Render and inspect before final delivery. Name the composition, input props, source revision, output path, and render command actually used.

## Implementation and recovery

- Read current [Remotion documentation](https://www.remotion.dev/docs/) and the relevant [official Remotion skills](https://github.com/remotion-dev/skills) before implementation. Use the existing project's compatible package versions; do not copy APIs from memory or upgrade dependencies as a side effect.
- Preflight fonts, asset paths, duration metadata, codec, and output dimensions. Keep exact text as editable code.
- Use frame ranges for the hook, explanation, demonstration, and final hold. Inspect first/last frames and scene boundaries, plus the finished playback.
- Preserve a previous usable export until its replacement succeeds. On failure, retain the input props and error, repair the failing scene or asset, and retry within an explicit time/resource budget.
- Do not render into an input asset or silently reuse a stale export. Check output existence, duration, dimensions, audio, and decode/playback before saying the render succeeded.
- Provide captions where speech carries meaning and a useful poster or still sequence for viewers who cannot use motion. README previews need a static alternative and a link to a controllable video.
- Confirm asset rights and current Remotion licensing for the intended use. This skill is workflow guidance; a renderer, paid service, and publication permission are separate requirements.

## Useful Defaults

- 30 FPS for general video.
- 60 FPS only when motion quality requires it.
- 1080x1920 for vertical social.
- 1920x1080 for YouTube/demo.
- 1200x630 or 1600x900 for launch preview loops.

## QA

- No text cut off.
- No scene timing dead air.
- Motion supports the script.
- Assets are licensed or owned.
- Audio levels are not clipped.
- GIF exports are size-conscious.

