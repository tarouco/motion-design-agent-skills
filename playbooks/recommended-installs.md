# Recommended Installs

This is the install posture for FrankX, Arcanea, and Starlight motion design work. Keep installs minimal, official, and scoped to the repo where the motion work actually happens.

## Keep Enabled In Codex

- Figma plugin/connector
- Canva plugin/connector
- Vercel plugin/connector
- Browser automation
- GitHub CLI/connector
- Image generation

These are already visible or locally available in this environment.

## Add To Motion/Video Projects

```bash
npm i motion gsap
npm i -D @playwright/test
```

For Remotion projects:

```bash
npm create video@latest
npm i @remotion/lottie lottie-web @remotion/rive
```

For 3D or cinematic web scenes:

```bash
npm i three @react-three/fiber @react-three/drei
npm i @theatre/core @theatre/studio
```

For interactive vector animation:

```bash
npm i @rive-app/react-canvas
```

For Lottie in React UI:

```bash
npm i lottie-react
```

## Add Agent Skills

The `motion-design-agent-skills` plugin already bundles the official GSAP skills (greensock/gsap-skills, MIT) and the LottieFiles `motion-design` skill (MIT), pinned in `vendor/vendor-lock.json`. Install the plugin once per agent; see [PLUGIN.md](../PLUGIN.md).

The official Remotion skills are not redistributed (upstream ships no license file). Inside a Remotion project, the official docs recommend:

```bash
npx remotion skills add
```

Outside a Remotion project:

```bash
npx skills add remotion-dev/skills
```

Run this in the agent environment where the video work will happen, or pass `--with-remotion` to `install.sh`. The pinned source revision is recorded in `skills-lock.json` (checked 2026-11-17: `skills/remotion-best-practices/SKILL.md`).

Other high-value third-party skill references:

- LottieFiles dotLottie web skill: https://github.com/LottieFiles/dotlottie-web/blob/main/SKILL.md

## Add MCP Carefully

Recommended:

- Figma MCP for design context and write-back: https://developers.figma.com/docs/figma-mcp-server/
- Figma MCP catalog for client setup: https://www.figma.com/mcp-catalog/
- Canva MCP for asset/design creation and collateral: https://www.canva.dev/docs/mcp/
- Remotion MCP: shut down on 2026-10-26; use the `/remotion-docs` skill from the official Remotion skills instead (https://www.remotion.dev/docs/ai/mcp).
- Vercel connector for deploy/preview/log workflows.

Security rule: install MCP servers from official vendors or audited source only. Review scopes, command execution behavior, and whether the tool can read secrets or write files.

## Local Machine Status

Checked on 2026-06-18; source recommendations refreshed on 2026-06-19:

- `git` is available.
- `gh` is available.
- `node` is available.
- `npm` is available.
- `ffmpeg` is available.
