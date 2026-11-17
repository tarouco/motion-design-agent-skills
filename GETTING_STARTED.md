# Getting Started with Motion Design Agent Skills

This repository ships **one installable plugin**, `motion-design-agent-skills`, with fifteen skills under [`skills/`](./skills), and **read-only reference playbooks and rubrics** under [`rubrics/`](./rubrics), [`playbooks/`](./playbooks), [`capabilities/`](./capabilities), and [`rankings/`](./rankings). Full plugin guide: [`PLUGIN.md`](./PLUGIN.md) · [guia em português](./docs/plugin-guide.pt-BR.md).

## 1. Discover the available skills

```bash
npx --yes skills add tarouco/motion-design-agent-skills --list
```

First-party workflows:

- `motion-design-orchestrator` (entry point and router)
- `motion-director`
- `site-motion-excellence-director`
- `web-motion-auditor`
- `remotion-video-agent`
- `generative-media-director`

Vendored MIT references: `gsap-core`, `gsap-timeline`, `gsap-scrolltrigger`, `gsap-plugins`, `gsap-react`, `gsap-frameworks`, `gsap-utils`, `gsap-performance`, and `motion-design`.

## 2. Read the skill before installing it

- [`skills/motion-design-orchestrator/SKILL.md`](./skills/motion-design-orchestrator/SKILL.md) and its [skill catalog](./skills/motion-design-orchestrator/references/skill-catalog.md)
- [`skills/motion-director/SKILL.md`](./skills/motion-director/SKILL.md)
- [`skills/site-motion-excellence-director/SKILL.md`](./skills/site-motion-excellence-director/SKILL.md)
- [`skills/web-motion-auditor/SKILL.md`](./skills/web-motion-auditor/SKILL.md)
- [`skills/remotion-video-agent/SKILL.md`](./skills/remotion-video-agent/SKILL.md)
- [`skills/generative-media-director/SKILL.md`](./skills/generative-media-director/SKILL.md)

## 3. Install

### Claude Code (plugin)

```bash
claude plugin marketplace add tarouco/motion-design-agent-skills
```

```bash
claude plugin install motion-design-agent-skills@tarouco-motion --scope user
```

### Claude.ai and Cowork

Download `motion-design-agent-skills.zip` from the [`skills-latest` release](https://github.com/tarouco/motion-design-agent-skills/releases/tag/skills-latest) and upload it in Customize > Plugins > Add > Upload plugin. Build it locally with `python3 scripts/build-plugin.py` if you prefer.

### Codex, Antigravity, Hermes Agent

```bash
npx --yes skills add tarouco/motion-design-agent-skills -a codex -g -y
```

```bash
npx --yes skills add tarouco/motion-design-agent-skills -a antigravity -g -y
```

```bash
npx --yes skills add tarouco/motion-design-agent-skills -a hermes-agent -g -y
```

Plugin installs are also available: `codex plugin marketplace add tarouco/motion-design-agent-skills` then `codex plugin add motion-design-agent-skills@tarouco-motion`, and `agy plugin install https://github.com/tarouco/motion-design-agent-skills`.

### Everything, including routing memory and the official Remotion skills

```bash
git clone https://github.com/tarouco/motion-design-agent-skills && cd motion-design-agent-skills && ./install.sh --agent all --with-remotion
```

Drop `-g` from the `npx skills` commands, or pass `--scope project` to `install.sh`, for a project-local install.

## 4. Verify what is installed

```bash
claude plugin details motion-design-agent-skills@tarouco-motion
```

```bash
npx --yes skills list
```

```bash
./install.sh --check-deps
```

## 5. If you only want the reference guides

- [`README.md`](./README.md)
- [`rubrics/motion-quality-rubric.md`](./rubrics/motion-quality-rubric.md)
- [`rubrics/site-motion-excellence-gate.md`](./rubrics/site-motion-excellence-gate.md)
- [`rankings/best-motion-design-stack.md`](./rankings/best-motion-design-stack.md)

## 6. Safety for third-party installs

For third-party skill packs, prefer official upstream repositories and scan them before installation with [`NVIDIA/SkillSpector`](https://github.com/NVIDIA/SkillSpector). Vendored skills in this repo are pinned by commit and SHA-256 in [`vendor/vendor-lock.json`](./vendor/vendor-lock.json).
