# Skill Catalog

Usage notes for every skill in the motion-design-agent-skills plugin. Use this to pick the skill, collect its inputs before loading it, and phrase the call.

## Invocation by host

| Host | How a skill is called | Example |
| --- | --- | --- |
| Claude Code (plugin) | Automatic from the description, or the slash command `/<plugin>:<skill>` | `/motion-design-agent-skills:web-motion-auditor http://localhost:3000/pricing` |
| Claude Code (plain skills install) | Automatic, or `/<skill>` | `/web-motion-auditor` |
| Cowork, claude.ai | Automatic from the description; naming the skill in the prompt makes the choice explicit | "Use web-motion-auditor on this page" |
| Codex (CLI, IDE extension) | Automatic, `$<skill>` mention, or the `/skills` picker | `$motion-director pick a runtime for this modal` |
| Antigravity | Automatic, or `/<skill>`; installed as a plugin the skill is `motion-design-agent-skills:<skill>` | `/remotion-video-agent` |
| Hermes Agent | Automatic, or `/<skill>` (up to five per message) | `/generative-media-director` |

Inside this plugin, load sibling skills by name; the host resolves the namespace.

## First-party workflow skills

### motion-design-orchestrator

- **Job:** classify the request, pick the lane, run multi-stage pipelines, enforce gates.
- **Use when:** the request is about motion in general, spans several stages, or the right skill is unclear.
- **Inputs:** goal, surface (site, app, video, social, docs), what exists already, deadline or budget limits.
- **Returns:** routing line, pipeline and current stage, specialist output, gate status, next stage.
- **Example prompts:** "Make our landing page feel premium without hurting conversion." / "Quero transformar o fluxo de onboarding num vídeo de 20 s para o LinkedIn."

### motion-director

- **Job:** motion direction for one component, interaction or UI surface; stack choice; timing, easing and stagger tokens; interruption rules; reduced-motion path.
- **Use when:** "which library", "how should this animate", "timing tokens", "make this modal/menu/toast feel better", turning audit findings into fixes.
- **Not for:** whole-site specs (site-motion-excellence-director); scoring existing motion (web-motion-auditor).
- **Inputs:** target component or route, existing runtime and tokens (read `package.json` and the design tokens), brand behavior keywords.
- **Returns:** motion goal, recommended stack, choreography, timing/easing tokens, reduced-motion path, implementation notes, QA checklist.
- **Pairs with:** `gsap-*` for GSAP API, `motion-design` for easing tables and choreography patterns, the bundled motion quality rubric.
- **Example prompts:** "Pick the lightest runtime for this accordion and give me tokens." / "Defina timing e easing para o menu mobile com fallback de reduced motion."

### site-motion-excellence-director

- **Job:** premium site or app motion: first-read diagnosis, still-frame gate, motion map, beat sequences, runtime choice, reduced-motion plan, excellence gate score.
- **Use when:** hero choreography, scroll story, site-wide motion system, launch pages, "make the site feel premium", a spec before implementation.
- **Not for:** a single micro-interaction (motion-director); video deliverables (remotion-video-agent, generative-media-director).
- **Inputs:** brand, route, audience, first user task, current screenshots, runtime already installed.
- **Returns:** motion thesis, first-read diagnosis, still-frame verdict, motion map, runtime choice, reduced-motion plan, implementation tasks, QA proof required, excellence score (target 45+/60 for premium launch).
- **Bundled:** site motion spec template and excellence gate.
- **Example prompts:** "Write the motion spec for our homepage hero and pricing scroll." / "Crie a coreografia de scroll da página de produto, com plano de reduced motion."

### web-motion-auditor

- **Job:** review, debug and score existing motion with evidence: keyboard, touch, reduced motion, interruption, navigation and resize, failure and performance probes.
- **Use when:** "review the animations", jank, missing `prefers-reduced-motion`, motion QA before release, before/after of a motion patch, baseline before a rollout.
- **Not for:** designing new motion (motion-director) or writing a site spec (site-motion-excellence-director).
- **Inputs:** URL or local route, revision, viewport(s), input modes; browser automation if available.
- **Returns:** per finding: severity, reproduction steps, file/line, fix, verification evidence; before/after table for patches; unobserved categories left unscored.
- **Dependencies:** Playwright (or another browser tool) for runtime probes; without it, completes source review and lists runtime checks as pending.
- **Example prompts:** "Audit motion on /pricing at 390px and 1440px, with reduced motion on." / "Revise as animações desta página e aponte o que trava."

### remotion-video-agent

- **Job:** programmatic video in React with Remotion: scene breakdown by frame range, deterministic timing, captions, MP4/GIF renders, social cutdowns, data-driven templates, finishing generated footage.
- **Use when:** explainer, product demo video, social cutdown, captions, animated title cards in code, render MP4/GIF, aspect-ratio variants.
- **Not for:** generating footage with AI providers (generative-media-director first); live web page animation (motion-director).
- **Inputs:** aspect ratio, duration, FPS, destination, voice/music, assets and their rights, existing Remotion project or not.
- **Returns:** composition plan, implementation, render command used, output path, QA (text cut-off, dead air, audio levels, GIF size).
- **Dependencies:** Node.js 18+, Remotion in the project, ffmpeg for extra formats; the official Remotion skills (`remotion-best-practices`, `/remotion-docs`) when installed.
- **Defaults:** 30 FPS; 1080x1920 vertical; 1920x1080 landscape; 1200x630 or 1600x900 preview loops.
- **Example prompts:** "Create a 15 s 1080x1920 Remotion promo from these screenshots with captions." / "Renderize uma versão GIF leve para o README."

### generative-media-director

- **Job:** AI-generated images and video: brief, still frame before video, provider routing based on the tools actually available, structured image and video prompts, finishing plan, QA and provenance.
- **Use when:** style frames, posters, image-to-video, generated social ads, cinematic brand clips, editing generated footage, provider choice (image tools, Sora, Veo, Grok Imagine, Luma, Runway).
- **Not for:** exact text or UI in video (remotion-video-agent); proof of real product motion (capture the real UI).
- **Inputs:** audience, surface, output format, viewer action, brand role, references and their rights, budget and authorization to spend.
- **Returns:** creative diagnosis, workflow, provider routing, still-frame prompt, video prompt, finishing plan, QA checklist, provenance template.
- **Gate:** no paid generation, upload or publication without explicit authorization; no silent switch to a paid provider.
- **Example prompts:** "Plan a 6 s cinematic hero loop for the launch, still frame first." / "Escreva os prompts de imagem e de vídeo para um anúncio vertical de 8 s."

## Bundled references (third-party, MIT)

| Skill | Load when implementing |
| --- | --- |
| `gsap-core` | Tweens (`to`, `from`, `fromTo`), easing, stagger, defaults, `gsap.matchMedia()` and reduced motion |
| `gsap-timeline` | Sequencing, position parameter, nesting, playback control |
| `gsap-scrolltrigger` | Scroll-linked animation, pinning, scrub, snapping, refresh and cleanup |
| `gsap-plugins` | Flip, Draggable, Observer, SplitText, ScrollSmoother, MorphSVG, DrawSVG, CustomEase and plugin registration |
| `gsap-react` | `useGSAP`, refs, `gsap.context()`, cleanup in React and Next.js |
| `gsap-frameworks` | Vue, Nuxt, Svelte, SvelteKit lifecycle and cleanup |
| `gsap-utils` | `clamp`, `mapRange`, `interpolate`, `snap`, `wrap`, `toArray` and other helpers |
| `gsap-performance` | Transforms over layout, batching, `will-change`, jank reduction |
| `motion-design` | Motion personality, emotion mapping, Disney principles for UI, timing/easing tables, entrance/exit, state feedback, ambient and multi-element patterns |

## External (install separately)

| Skill | Source | Use |
| --- | --- | --- |
| `remotion-best-practices` and siblings (`/remotion-create`, `/remotion-markup`, `/remotion-render`, `/remotion-captions`, `/remotion-docs` ...) | `remotion-dev/skills` | Current Remotion API while `remotion-video-agent` implements or renders |
