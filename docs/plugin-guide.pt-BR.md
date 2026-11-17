# Guia do plugin motion-design-agent-skills

Versão 2.0.0. Um único plugin que reúne as skills de motion design deste repositório para Claude Code, Claude.ai, Cowork, Codex, Antigravity e Hermes Agent.

## 1. Como o repositório organiza o trabalho

O repositório separa o motion design em cinco "faixas" (lanes), cada uma com uma skill responsável, e liga essas faixas em pipelines com portões de qualidade. A doutrina é a mesma em todas: primeiro a composição estática, depois o movimento; animar só para esclarecer estado ou narrativa; projetar o caminho de reduced motion junto com o movimento; e verificar com evidência visual.

| Faixa | Para que serve | Skill |
| --- | --- | --- |
| Motion de interface (product UI) | Decidir se e como um componente se move, escolher a biblioteca, definir tokens de tempo e easing | `motion-director` |
| Motion criativo de site | Coreografia premium de páginas: hero, scroll narrativo, sistema de motion do site, spec antes do código | `site-motion-excellence-director` |
| Captura e QA | Auditar animações existentes com probes de teclado, toque, reduced motion, interrupção e performance | `web-motion-auditor` |
| Vídeo programático | Vídeo em React com Remotion: explicativos, cortes para redes, legendas, renders MP4/GIF | `remotion-video-agent` |
| Mídia generativa | Imagens e vídeos gerados por IA: brief, style frame, prompts, escolha do provedor, proveniência | `generative-media-director` |

Os playbooks do repositório (`playbooks/site-motion-rollout.md`, `playbooks/gif-video-pipeline.md`, `playbooks/image-video-gif-production-workflow.md`, `playbooks/video-provider-routing.md`) descrevem como essas faixas se encadeiam. O plugin transforma isso numa skill orquestradora, `motion-design-orchestrator`, que classifica o pedido, escolhe a faixa e executa o pipeline na ordem certa.

### Pipelines

- **A. Rollout de motion num site:** auditoria de base (`web-motion-auditor`) → escolha de até quatro momentos-assinatura e spec (`site-motion-excellence-director`) → runtime e tokens (`motion-director`) → implementação com as referências `gsap-*` ou Motion → verificação (`web-motion-auditor`) → nota no excellence gate (45+/60 para lançamento premium) → virar padrão reutilizável.
- **B. Interação de componente:** direção (`motion-director`) → implementação → probes rápidos (`web-motion-auditor`) → rubrica (15+ demo pública, 18+ lançamento, 20+ superfície premium).
- **C. Interface real → GIF ou vídeo:** captura com Playwright → empacotamento opcional em Remotion (`remotion-video-agent`) → exportação com ffmpeg → rubrica.
- **D. Campanha com mídia gerada:** brief e style frame (`generative-media-director`) → roteamento de provedor → autorização → geração → acabamento em Remotion (texto exato, legendas, CTA, variações) → ffmpeg → QA e proveniência.
- **E. Auditar e corrigir:** achados (`web-motion-auditor`) → direção da correção (`motion-director`) → patch → nova auditoria com tabela antes/depois.

### Portões que nunca são pulados

1. **Frame estático:** não se anima uma composição fraca.
2. **Reduced motion:** o caminho alternativo é desenhado no mesmo passo.
3. **Autorização:** geração paga, upload externo, publicação e instalação global só com o seu "ok".
4. **Evidência:** nota só para o que foi observado; o resto fica como pendente.
5. **Proveniência:** todo asset gerado ou externo ganha registro (prompt, ferramenta, modelo, direitos, data, hash).

## 2. As skills do plugin e como chamar cada uma

| Skill | Use quando você pedir | Exemplo de pedido |
| --- | --- | --- |
| `motion-design-orchestrator` | Qualquer coisa de motion, ou um trabalho com várias etapas | "Quero que a landing pareça premium sem atrapalhar a conversão." |
| `motion-director` | Biblioteca, timing, easing, stagger, reduced motion de um componente; corrigir achados de auditoria | "Defina timing e easing do menu mobile com fallback de reduced motion." |
| `site-motion-excellence-director` | Hero, scroll narrativo, sistema de motion do site, spec antes de implementar | "Crie a coreografia de scroll da página de produto." |
| `web-motion-auditor` | Revisar, depurar e pontuar animações que já existem | "Revise as animações de /precos em 390px e 1440px com reduced motion ligado." |
| `remotion-video-agent` | Vídeo em React/Remotion, legendas, MP4/GIF, variações de formato | "Faça um vídeo de 15 s 1080x1920 com estas telas e legendas." |
| `generative-media-director` | Style frames, prompts de imagem e vídeo, escolha de provedor, proveniência | "Escreva os prompts para um anúncio vertical de 8 s, começando pelo frame estático." |
| `gsap-core`, `gsap-timeline`, `gsap-scrolltrigger`, `gsap-plugins`, `gsap-react`, `gsap-frameworks`, `gsap-utils`, `gsap-performance` | Detalhes da API do GSAP durante a implementação (skills oficiais da GreenSock, MIT) | "Use ScrollTrigger para fixar esta seção com scrub." |
| `motion-design` | Princípios de motion, tabelas de easing, padrões de coreografia (skill oficial da LottieFiles, MIT) | "Qual easing usar para entrada e saída deste toast?" |

### Sintaxe de chamada por plataforma

| Plataforma | Como chamar |
| --- | --- |
| Claude Code e Cowork | Automático pela descrição, ou `/motion-design-agent-skills:<skill>` (ex.: `/motion-design-agent-skills:web-motion-auditor http://localhost:3000`) |
| Claude.ai | Automático; para forçar, cite a skill no pedido ("use a web-motion-auditor") |
| Codex | Automático, `$<skill>` (ex.: `$motion-director`) ou o seletor `/skills` |
| Antigravity | Automático ou `/<skill>`; instalado como plugin, a skill vira `motion-design-agent-skills:<skill>` |
| Hermes Agent | Automático ou `/<skill>` (até cinco por mensagem); `/reload-skills` depois de instalar |

Na dúvida, chame só a orquestradora: ela anuncia a faixa escolhida numa linha (por exemplo `Lane: Motion QA -> web-motion-auditor`) e segue o pipeline.

## 3. Instalação

### Claude Code

```bash
claude plugin marketplace add tarouco/motion-design-agent-skills
```

```bash
claude plugin install motion-design-agent-skills@tarouco-motion --scope user
```

Dentro do Claude Code, o equivalente é `/plugin marketplace add tarouco/motion-design-agent-skills` e `/plugin install motion-design-agent-skills@tarouco-motion`. Marketplaces de terceiros não se atualizam sozinhos; ative o auto-update na aba Marketplaces ou rode `claude plugin update motion-design-agent-skills@tarouco-motion`.

### Claude.ai e Cowork

1. Baixe `motion-design-agent-skills.zip` da release [`skills-latest`](https://github.com/tarouco/motion-design-agent-skills/releases/tag/skills-latest) (ou gere com `python3 scripts/build-plugin.py`).
2. Em claude.ai: **Customize → Plugins → Add → Upload plugin** e escolha o ZIP.
3. O plugin enviado também é sincronizado com o Claude Code como `motion-design-agent-skills@synced`. Se você instalar pelo marketplace também, a cópia do marketplace é a que carrega.

No Claude.ai (chat web) só as skills carregam; o hook de sessão é ignorado lá, por isso a memória da conta (seção 4) é importante.

### Codex

```bash
codex plugin marketplace add tarouco/motion-design-agent-skills
```

```bash
codex plugin add motion-design-agent-skills@tarouco-motion
```

Sem suporte a plugins (por exemplo na extensão de IDE), instale só as skills em `~/.agents/skills`:

```bash
npx skills add tarouco/motion-design-agent-skills -a codex -g -y
```

### Antigravity

```bash
agy plugin install https://github.com/tarouco/motion-design-agent-skills
```

Como plugin, ele traz a regra `rules/motion-design-routing.md` (sempre ativa). Para instalar só as skills em `~/.gemini/config/skills`:

```bash
npx skills add tarouco/motion-design-agent-skills -a antigravity -g -y
```

### Hermes Agent

```bash
npx skills add tarouco/motion-design-agent-skills -a hermes-agent -g -y
```

Ou, a partir de um clone, `./install.sh --agent hermes`, que copia as skills para `~/.hermes/skills/motion-design/`. Depois rode `/reload-skills` numa sessão.

### Tudo de uma vez (macOS, Linux, WSL)

```bash
git clone https://github.com/tarouco/motion-design-agent-skills && cd motion-design-agent-skills && ./install.sh --agent all --with-remotion
```

Opções do instalador: `--agent claude-code|codex|antigravity|hermes|all`, `--scope user|project`, `--no-memory`, `--with-remotion`, `--check-deps`, `--dry-run`, `--uninstall`. No Windows sem WSL, use os comandos de plugin e `npx skills` acima, que são multiplataforma.

## 4. Memória: como o agente sabe que deve usar o plugin

| Plataforma | Mecanismo | O que fazer |
| --- | --- | --- |
| Claude Code | Hook `SessionStart` do plugin injeta a nota de roteamento em toda sessão; além disso o instalador grava o bloco em `~/.claude/CLAUDE.md` | Nada além de instalar |
| Claude.ai | Preferências do perfil e memória da conta | Cole o texto de `memory/claude-ai.pt-BR.md` em Settings → Profile e envie a mensagem de memória |
| Cowork | Skills do plugin + preferências da conta | Igual ao Claude.ai |
| Codex | `~/.codex/AGENTS.md` | O instalador grava o bloco |
| Antigravity | Regra do plugin (`rules/`) ou `~/.gemini/GEMINI.md` | O plugin traz a regra; o instalador grava o bloco no modo só-skills |
| Hermes Agent | `MEMORY.md` é gerido pelo próprio Hermes | Envie a mensagem de `memory/hermes.md` uma vez |

O bloco de memória é o mesmo em todas as plataformas (`memory/motion-design-routing.md`), delimitado por marcadores, então reinstalar não duplica e `--uninstall` remove.

## 5. Dependências

| Faixa | Precisa de | Instalação |
| --- | --- | --- |
| Planejamento, specs, prompts, revisão de código | Nada | — |
| Captura e auditoria | Node.js 18+ e Playwright com Chromium no projeto | `npm i -D @playwright/test && npx playwright install chromium` |
| Exportar GIF/MP4/WebM | ffmpeg | macOS `brew install ffmpeg`; Ubuntu `sudo apt-get install ffmpeg`; Windows `winget install Gyan.FFmpeg` |
| Vídeo programático | Remotion no projeto; skills oficiais do Remotion (opcional) | `npm create video@latest`; `npx remotion skills add` |
| Mídia generativa | As ferramentas de imagem/vídeo da sua sessão e o seu acesso aos provedores | Credenciais nunca vão no chat nem no repositório |

As skills do GSAP e da LottieFiles vêm dentro do plugin (MIT, commits fixados em `vendor/vendor-lock.json`). As skills oficiais do Remotion ficam de fora porque o repositório de origem não tem arquivo de licença; o instalador baixa da fonte oficial com `--with-remotion`. O servidor MCP do Remotion foi desligado em 26/10/2026 e foi substituído pela skill `/remotion-docs`.

## 6. Manutenção

- Atualizar as skills de terceiros: `python3 scripts/sync-vendor-skills.py` (depois de mudar os commits em `vendor/vendor-lock.json`).
- Conferir tudo: `python3 scripts/verify-repo.py`, `python3 scripts/verify-skill-packages.py`, `python3 scripts/sync-vendor-skills.py --check`, `claude plugin validate .`.
- Gerar os pacotes: `python3 scripts/build-plugin.py` (saída em `dist/`). No `main`, o workflow Skills Release publica os ZIPs na release `skills-latest`.
- Ao mudar a versão, atualize `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `plugin.json` e `.antigravity-plugin/plugin.json` juntos; o verificador recusa versões divergentes.
