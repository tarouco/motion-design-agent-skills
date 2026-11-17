# Dependencies

The skills are instructions. They ship no browser, renderer or provider account. Check only what the current lane needs, report what is missing, and ask before any global install.

## Bundled with the plugin

| Dependency | Where | License | Why |
| --- | --- | --- | --- |
| GSAP official skills (`gsap-core`, `gsap-timeline`, `gsap-scrolltrigger`, `gsap-plugins`, `gsap-react`, `gsap-frameworks`, `gsap-utils`, `gsap-performance`) | vendored, pinned commit | MIT (GreenSock) | Current GSAP API for the implementation stage |
| LottieFiles `motion-design` | vendored, pinned commit | MIT (LottieFiles) | Motion principles, easing tables, choreography patterns |

## Installed separately (not redistributable here)

| Dependency | Install | Notes |
| --- | --- | --- |
| Official Remotion skills (`remotion-best-practices` and siblings such as `/remotion-docs`) | Inside a Remotion project: `npx remotion skills add`. Elsewhere: `npx skills add remotion-dev/skills` | Upstream ships no license file; install from source. The hosted Remotion MCP server was shut down on 26 October 2026; use `/remotion-docs` instead. |

## Local tools by lane

| Lane | Tool | Check | Install (ask first) |
| --- | --- | --- | --- |
| Capture, audit, GIF from UI | Node.js 18+ | `node --version` | https://nodejs.org |
| Capture, audit | Playwright + Chromium | `npx playwright --version` | Project: `npm i -D @playwright/test && npx playwright install chromium` |
| GIF/MP4/WebM export | ffmpeg | `ffmpeg -version` | macOS `brew install ffmpeg`; Debian/Ubuntu `sudo apt-get install ffmpeg`; Windows `winget install Gyan.FFmpeg` |
| Programmatic video | Remotion | `npx remotion --version` inside the project | New project: `npm create video@latest` |
| Web UI motion | Motion, GSAP | `package.json` | Project: `npm i motion` or `npm i gsap` (only when the spec picks that runtime) |
| Interactive vector | Rive, dotLottie | `package.json` | `npm i @rive-app/react-canvas`, `npm i @lottiefiles/dotlottie-react` |
| 3D | Three.js / React Three Fiber | `package.json` | `npm i three @react-three/fiber @react-three/drei` |

Project packages go into the project that owns the motion work, never into the plugin.

## Optional connectors (design context)

Figma, Canva and Vercel connectors improve the workflow when the user already has them connected. Prefer official vendor MCP servers, review scopes, and never add an unofficial server without reviewing its source.

## Generative media providers

Discover the image and video tools actually exposed in the session. Provider APIs (OpenAI Sora, Google Veo, xAI Grok Imagine, Luma, Runway) need the user's own credentials and authorization to spend. Never ask for keys in chat and never commit them.
