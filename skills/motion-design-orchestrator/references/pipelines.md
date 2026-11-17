# Motion Pipelines

Each pipeline lists the stage, the skill that owns it, what it must produce, and the gate that ends it. Run stages in order; a failed gate stops the pipeline and is reported with the evidence that failed.

## A. Site motion rollout

Use for a new site, a redesign, or a "make this site feel premium" request.

| # | Stage | Skill | Produces | Gate |
| --- | --- | --- | --- | --- |
| 0 | Baseline audit | `web-motion-auditor` | Route list, current libraries, desktop and phone first-viewport captures, reduced-motion behavior, findings | Revision and URL recorded |
| 1 | Choose signature moments | `site-motion-excellence-director` | At most one hero moment, one product-proof moment, one shared interaction pattern, one media/export opportunity | "What stays still" is written down |
| 2 | Write the spec | `site-motion-excellence-director` | One site motion spec per moment (first read, thesis, still-frame gate, beat sequence, runtime, reduced-motion route, proof artifact) | Still-frame gate passes |
| 3 | Direction and tokens | `motion-director` | Runtime per moment, duration/easing/stagger tokens, interruption and cleanup rules | Lightest runtime that preserves intent |
| 4 | Implement | `gsap-*` references for GSAP; Motion docs for Motion; CSS for simple states | Code patch using existing tokens and dependencies | Builds; no new dependency unless approved |
| 5 | Verify | `web-motion-auditor` | Desktop, phone, keyboard, touch, reduced-motion, interruption and navigation probes; frame or video capture | Every scored category cites evidence |
| 6 | Score | `site-motion-excellence-director` | Excellence gate score | 45+/60 premium launch; no automatic fail |
| 7 | Promote | `motion-director` | Tokens, reusable component or recipe, documented reduced-motion behavior | Before/after proof saved |

Runtime defaults: Motion for React for component choreography and dashboards; GSAP ScrollTrigger only for pinned, scrubbed or authored signature moments; Rive for interactive vector state machines; Lottie/dotLottie for portable loops; Three.js only when 3D is central and has a fallback.

## B. Component or UI interaction

| # | Stage | Skill | Produces |
| --- | --- | --- | --- |
| 1 | Decide whether motion helps | `motion-director` | Motion goal, or a recommendation not to animate |
| 2 | Direction | `motion-director` | Stack, timing tokens (start at 150-250 ms ease-out for occasional UI), reduced-motion path, interruption rules |
| 3 | Implement | `gsap-react` / `gsap-core` or the Motion docs | Patch |
| 4 | Probe | `web-motion-auditor` | Keyboard, touch, reduced motion, rapid repeat, interrupted transition |
| 5 | Score | motion quality rubric (bundled in `motion-director` and `web-motion-auditor`) | 15+ public demo, 18+ launch, 20+ premium surface |

## C. Real product UI to GIF or video

1. Build or open the real interaction (local dev server or preview URL).
2. Capture with Playwright: record video from the browser context at the target viewport; take a reduced-motion capture with `reducedMotion: 'reduce'`.
3. Trim the source clip.
4. Optional: package in Remotion (`remotion-video-agent`) when titles, captions, overlays or aspect-ratio variants are needed.
5. Export with ffmpeg:

   ```bash
   ffmpeg -i input.mp4 -vf "fps=15,scale=900:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
   ```

6. Check loop seam, file size, readability and crop; provide a poster frame. MP4 is the delivery format; GIF is for previews and docs only.

## D. Generated media campaign

| # | Stage | Skill | Produces | Gate |
| --- | --- | --- | --- | --- |
| 1 | Brief | `generative-media-director` | Audience, surface, format, viewer action, brand role | Source of truth chosen per element |
| 2 | Still frame first | `generative-media-director` | Image prompt (structured shape) and selected style frames | Visual direction approved by the user |
| 3 | Route | `generative-media-director` | Tool actually available in this session, with cost, access and rights checked | Authorization for paid generation or upload |
| 4 | Video prompt and generation | `generative-media-director` | Video prompt (source frame, camera, motion, audio, beginning/middle/end) and raw takes | Raw output and prompt saved |
| 5 | Finish | `remotion-video-agent` | Exact text, captions, logo lockup, CTA, aspect-ratio variants | Text is editable code, not baked into generated pixels |
| 6 | Export | ffmpeg | MP4/WebM/GIF variants and poster | Size and playback checked on target surface |
| 7 | QA and provenance | `generative-media-director` | QA checklist and provenance record | Unknown values marked, nothing invented |

Exact typography, UI and data belong in Remotion; real product proof belongs in Playwright capture; generation providers are for pixels and footage only.

## E. Audit and fix

1. `web-motion-auditor`: findings with severity, reproduction steps, file/line, fix and evidence; unobserved categories left unscored.
2. `motion-director`: fix direction for each accepted finding (shorter transitions, transform/opacity, fewer staggered items, reduced-motion branch, state-explaining motion).
3. Patch the owned code only.
4. Re-run the same probes and return a before/after table with the same revision metadata.

## Handoff record

Pass this between stages, in the reply or in a file the user approved:

```text
Target: route / URL / composition id
Revision: commit or preview id
Decisions: runtime, tokens, spec path
Evidence: capture paths, scores with cited evidence
Pending: checks that could not run here and why
Next: stage and skill
```
