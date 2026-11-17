# motion-design-agent-skills plugin

One plugin for motion design work in Claude Code, Claude.ai, Cowork, Codex, Antigravity and Hermes Agent: an orchestrator skill that routes each request, five workflow skills, and the official GSAP and LottieFiles motion references. Version 2.0.0.

Portuguese guide with the full workflow analysis: [docs/plugin-guide.pt-BR.md](docs/plugin-guide.pt-BR.md).

## What is inside

| Skill | Job | Call it for |
| --- | --- | --- |
| `motion-design-orchestrator` | Entry point and router | Any motion request, or a job with several stages |
| `motion-director` | Motion direction for one component or UI surface | Runtime choice, timing/easing tokens, reduced-motion path, fixes from an audit |
| `site-motion-excellence-director` | Premium site choreography | Hero and scroll stories, site-wide motion spec, excellence gate score |
| `web-motion-auditor` | Motion QA | Review, debug and score existing animation with evidence |
| `remotion-video-agent` | Programmatic video | Remotion compositions, captions, MP4/GIF renders, finishing generated footage |
| `generative-media-director` | Generative media | Style frames, image/video prompts, provider routing, provenance |
| `gsap-core`, `gsap-timeline`, `gsap-scrolltrigger`, `gsap-plugins`, `gsap-react`, `gsap-frameworks`, `gsap-utils`, `gsap-performance` | Official GSAP references (MIT) | GSAP API details while implementing |
| `motion-design` | LottieFiles motion principles (MIT) | Easing tables, choreography patterns, Disney principles for UI |

The official Remotion skills are installed separately because upstream ships no license file (`./install.sh --with-remotion`).

## Pipelines the orchestrator runs

- **Site motion rollout:** audit, choose signature moments, spec, tokens, implement, verify, score, promote.
- **Component interaction:** direction, implement, probe, rubric.
- **Real UI to GIF/video:** capture with Playwright, optional Remotion packaging, ffmpeg export.
- **Generated media campaign:** brief, still frame, provider routing, authorization, generation, Remotion finish, export, provenance.
- **Audit and fix:** findings, fix direction, patch, before/after re-audit.

Gates on every pipeline: still frame before motion, reduced motion in the same pass, authorization before paid generation or publication, evidence before scores, provenance for generated assets.

## Install

| Agent | Command |
| --- | --- |
| Claude Code | `/plugin marketplace add tarouco/motion-design-agent-skills` then `/plugin install motion-design-agent-skills@tarouco-motion` |
| Claude Code (one step, v2.1.275+) | `/plugin install motion-design-agent-skills --marketplace tarouco/motion-design-agent-skills` |
| Claude.ai, Cowork | Download `motion-design-agent-skills.zip` from the [`skills-latest` release](https://github.com/tarouco/motion-design-agent-skills/releases/tag/skills-latest), then Customize > Plugins > Add > Upload plugin |
| Codex | `codex plugin marketplace add tarouco/motion-design-agent-skills` then `codex plugin add motion-design-agent-skills@tarouco-motion`, or skills only: `npx skills add tarouco/motion-design-agent-skills -a codex -g -y` |
| Antigravity | `agy plugin install https://github.com/tarouco/motion-design-agent-skills`, or skills only: `npx skills add tarouco/motion-design-agent-skills -a antigravity -g -y` |
| Hermes Agent | `npx skills add tarouco/motion-design-agent-skills -a hermes-agent -g -y`, or `./install.sh --agent hermes` |
| Everything at once | `git clone https://github.com/tarouco/motion-design-agent-skills && cd motion-design-agent-skills && ./install.sh --agent all --with-remotion` |

`install.sh` also writes the routing memory block (`memory/motion-design-routing.md`) into `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md` and `~/.gemini/GEMINI.md`. In Claude Code the plugin's SessionStart hook loads the same note automatically. Claude.ai and Hermes keep memory on their side; see `memory/claude-ai.pt-BR.md` and `memory/hermes.md`.

## Calling a skill

| Host | Syntax |
| --- | --- |
| Claude Code, Cowork | Automatic, or `/motion-design-agent-skills:<skill>` |
| Claude.ai | Automatic; name the skill in the prompt to force it |
| Codex | Automatic, `$<skill>`, or `/skills` |
| Antigravity | Automatic, or `/<skill>` (`motion-design-agent-skills:<skill>` when installed as a plugin) |
| Hermes Agent | Automatic, or `/<skill>` |

## Dependencies

| Lane | Needs |
| --- | --- |
| Planning, specs, prompts, source review | Nothing |
| Capture and audit | Node.js 18+, Playwright with Chromium in the project |
| GIF/MP4/WebM export | ffmpeg |
| Programmatic video | Remotion in the project; optional official Remotion skills |
| Generative media | The image/video tools your session exposes, plus your own provider access |

Check with `./install.sh --check-deps`.

## License

First-party content: CC0-1.0. Vendored GSAP and LottieFiles skills: MIT, see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
