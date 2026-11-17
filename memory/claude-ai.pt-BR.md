# Memória do Claude.ai para o plugin motion-design-agent-skills

O Claude.ai não lê arquivos de memória de um repositório. Há dois jeitos de registrar a regra na sua conta; use os dois para ter o melhor resultado.

## 1. Preferências do perfil (vale para todas as conversas)

Em claude.ai, abra **Settings → Profile** e cole no campo de preferências pessoais:

```text
Quando eu pedir qualquer coisa de motion design — animação de interface ou site, transições, micro-interações, efeitos de scroll, revisão de animações ou de prefers-reduced-motion, vídeo programático com Remotion, exportação de GIF/MP4/WebM, ou imagens e vídeos gerados por IA — use o plugin motion-design-agent-skills e comece pela skill motion-design-orchestrator. Ela escolhe a skill certa: motion-director (biblioteca, timing, easing e reduced motion de um componente), site-motion-excellence-director (coreografia e spec de motion do site inteiro), web-motion-auditor (auditar e pontuar animações existentes com evidência), remotion-video-agent (vídeos em React/Remotion, legendas, renders MP4/GIF), generative-media-director (style frames, prompts de imagem e vídeo, escolha de provedor, proveniência), além das referências gsap-* e motion-design. Respeite os portões: frame estático antes do movimento, reduced motion no mesmo passo, autorização antes de geração paga ou publicação, evidência antes de nota.
```

## 2. Memória (Claude aprende e lembra entre conversas)

Com a memória ativada (**Settings → Capabilities → Memory**), envie numa conversa:

```text
Lembre-se: para qualquer trabalho de motion design, animação, transições, auditoria de animações, vídeo em Remotion, GIF/MP4 ou mídia gerada por IA, use o plugin motion-design-agent-skills começando pela skill motion-design-orchestrator.
```

Confira em **Settings → Capabilities → Memory → View/edit** que a regra foi registrada.
