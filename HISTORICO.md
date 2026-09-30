# HISTÓRICO: Criações Românticas (Projeto do Jonas)

Registro de **como o sistema chegou ao estado atual**: pedidos, mudanças, decisões, alternativas
descartadas e o que foi removido. O estado atual do sistema está no **[CLAUDE.md](CLAUDE.md)**.

## Como registrar

Ao fim de **cada tarefa**, acrescente uma entrada **no topo** da seção "Registro", neste formato:

```markdown
### AAAA-MM-DD — Título curto da tarefa
- **Pedido:** o que o usuário pediu (em uma ou duas linhas).
- **Feito:** o que mudou (arquivos, funcionalidades).
- **Decisões:** escolhas feitas e por quê; alternativas descartadas.
- **Removido/substituído:** o que deixou de existir (para não ser reintroduzido sem querer).
- **Verificação:** como foi testado (testes, navegador, arquivos gerados).
- **Pendências:** o que ficou em aberto (se houver).
```

Depois de registrar aqui, atualize o `CLAUDE.md` para refletir só o estado atual.

---

## Registro

### 2026-09-29 — CLAUDE.md completo + HISTORICO.md + AGENTS.md
- **Pedido:** CLAUDE.md detalhado para qualquer IA entender todos os níveis do sistema. Obrigação de atualizar
  CLAUDE.md e HISTORICO.md ao fim de cada tarefa. CLAUDE.md só com informação ativa; o resto aqui.
- **Feito:**
  - `CLAUDE.md` reescrito em 16 seções: protocolo, visão geral, rodar/testar, mapa de arquivos, páginas e fluxos,
    fluxo de execução, API do núcleo, estado da sessão, cache, astronomia, design, especificações das peças,
    testes, rede, convenções, armadilhas e pendências.
  - Criados `HISTORICO.md` (este arquivo) e `AGENTS.md` (ponteiro para o CLAUDE.md, para ferramentas que procuram esse nome).
- **Decisões:** a regra "não registrar no Cérebro" fica no protocolo do CLAUDE.md, porque este é um projeto de teste separado.
- **Verificação:** funções, constantes e chaves de estado levantadas direto do código antes de escrever.

### 2026-09-29 — Primeira versão do CLAUDE.md
- **Pedido:** criar um CLAUDE.md.
- **Feito:** versão curta (comandos, arquitetura, convenções, armadilhas). Substituída no mesmo dia pela versão completa acima.

### 2026-09-29 — Redesign completo (design system)
- **Pedido:** "foque em design, use toda sua capacidade e tudo que tiver na skill de design".
- **Método:** skills de design usadas: crítica, design system, acessibilidade (WCAG 2.1 AA) e textos da interface.
  Revisão visual no Chrome em desktop e em largura de celular (iframe de 390 px).
- **Diagnóstico da crítica:**
  - aparência genérica de Streamlit, emojis como ícones;
  - cabeçalho gigante repetido em toda página;
  - prévia abaixo do formulário (exigia rolar a cada ajuste);
  - botão coral com texto branco em 3,2:1 (reprovado);
  - peças com a fonte padrão DejaVu.
- **Feito:**
  - `core/design.py`: fonte única de cores e medidas. `DESIGN.md` documenta o design system.
  - Fontes Fraunces, DM Sans e Caveat em `static/fonts` (licença OFL), usadas na interface (`theme.fontFaces`) e nas peças.
  - `core/marca.py` (logotipo com coração vetorial) e `st.logo`. Navegação por seções com ícones Material e `url_path` em português.
  - Página inicial nova (`paginas/inicio.py`): herói, vitrine com miniaturas reais (`core/vitrine.py`) e "Como funciona".
  - Layout de estúdio (`estudio()`: controles à esquerda, prévia fixa à direita; no celular a prévia vem primeiro), com etapas numeradas.
  - Componentes em `core/estilo.py`: cabecalho_pagina, etapa, mostrar_previa, botoes_download, chips, cartao_desafio, placar, resposta_comparada.
  - **Vale redesenhado:** canhoto colorido com perfuração transparente, número estável e campos Para/De/Quando em colunas,
    com tamanho único para os três valores. A mensagem é manuscrita e o bloco é centralizado na vertical. Opção "sem data".
  - **Polaroid:** 5 molduras coloridas, 4 filtros (Original, P&B, Sépia, Memória), fita adesiva, legenda manuscrita e PNG transparente.
  - **Mapa:** 4 estilos de pôster (Céu azul, Noite profunda, Papel e tinta, Rosé), tipografia nova e espaçamento entre letras.
    Prévia ao vivo, sem botão de gerar; busca da cidade ao apertar Enter; coordenadas e fuso num expander.
  - **Caça-palavras:** folha com título em serifa, grade sobre cartão de papel e caixinhas para marcar.
  - **Passatempos:** segmented control para escolher o jogo; placar e respostas lado a lado no quiz; carta visual no desafio.
  - **Acessibilidade:** primário `#B5454E` (5,4:1), texto `#2B3346`, foco visível de 3 px, botões com 44 px,
    `lang=pt-BR` injetado (a página vinha em inglês), `prefers-reduced-motion`, toolbar mínima (sem "Deploy").
  - **Textos:** revisados (verbo nos botões, erros com causa e solução, estados vazios que convidam).
    Rodapé corrigido: dizia "gerado no seu navegador", mas a geração é no servidor.
- **Decisões:**
  - Paleta original aprovada mantida; coral e azul passaram a ser só decorativos por falta de contraste.
  - Cores das categorias do vale escurecidas para ≥ 4,5:1: roxo `#9B59B6`→`#7B4F8E`, verde `#52BE80`/`#3F9E67`→`#3D7456`,
    teal `#48C9B0`/`#2FA58E`→`#2C7470`; bordô `#8B0000`→`#8E2F3C`.
  - As mesmas TTFs na tela e nos arquivos, em vez de fontes do sistema, para a tela e o impresso ficarem idênticos.
  - Coração desenhado como vetor com supersampling: nenhuma das fontes tem ♥, e o Pillow não suaviza polígonos.
  - Vale e polaroid em RGBA: a sombra da prévia (CSS `drop-shadow`) segue o recorte real. O PDF compõe sobre branco.
  - Mobile: `order: -1` na coluna da prévia (o `flex-direction: column-reverse` não funcionou com o wrap das colunas).
- **Removido/substituído:**
  - Cabeçalho global "✨ Criações Românticas ✨" em toda página (a marca foi para a barra lateral).
  - Botão "Calcular e Gerar Mapa Estelar" (o mapa atualiza sozinho) e botão "Buscar coordenadas" (virou Enter no campo).
  - Categorias renomeadas: "Cinema / Entretenimento" → "Cinema & séries", "Jantar / Gastronomia" → "Jantar",
    "Viagem / Passeio ao Ar Livre" → "Passeio", "Momento Relax / Spa" → "Relax & spa". Nova categoria "Carinho".
  - Toggles de constelações, planetas e grade → pílulas "Mostrar no pôster". Slider de magnitude → Poucas/Equilibrada/Muitas.
  - Radio de passatempos → segmented control. Estilos de mapa "Céu azul (clássico)" → "Céu azul".
  - Fontes DejaVu (do matplotlib) nas peças. Estilos de fonte antigos ("normal", "negrito", "mono"...) → novos nomes em `fontes.ESTILOS`.
  - Dataclass `Tema` de `design.py` (não era usada).
- **Verificação:** 41 testes passando; revisão visual de todas as páginas no Chrome; upload real de foto testado; celular simulado.
- **Pendências:** texto alternativo das imagens (limitação do `st.image`); a linha do arquivo enviado segue em inglês; AdSense.

### 2026-09-29 — Inicializador `.bat`
- **Pedido:** um `.bat` para executar o servidor e abrir o sistema.
- **Feito:** `Iniciar Criacoes Romanticas.bat`:
  - detecta se o sistema já está aberto;
  - cria o `.venv` e reinstala dependências só quando o `requirements.txt` muda;
  - abre o navegador quando o servidor responde;
  - servidor restrito a `localhost`.
- **Decisões:** `--server.headless true` para evitar o prompt de e-mail do Streamlit na primeira execução. A abertura
  do navegador fica a cargo de um PowerShell oculto que consulta `/_stcore/health`.
- **Verificação:** executado de verdade pelo PowerShell (o Git Bash quebrava o nome com espaços).

### 2026-09-29 — Implementação do plano de melhorias (Fases 0 a 4)
- **Pedido:** "aplique todas as correções" do plano de ação.
- **Feito:**
  - Fase 0: correção do `set_theta_zero_direction` (método inexistente, o mapa quebrava sempre), `html.escape`,
    `plt.close`, `requirements.txt`.
  - Fase 1: mapa estelar real (Hipparcos, Stellarium, de421, fuso horário, Lua e planetas, geocodificação).
  - Fase 2: upload de foto na polaroid, caça-palavras gerado de verdade com gabarito, quiz com comparação, desafios sem repetição.
  - Fase 3: exportação PNG e PDF de todas as peças.
  - Fase 4: separação em `core/` e `paginas/`, tema em `config.toml`, testes automatizados, README.
- **Decisões:**
  - Catálogo Hipparcos pré-filtrado e embutido (515 KB), em vez de baixar 53 MB a cada inicialização.
  - URL de constelações fixada no Stellarium v0.22.2 (a do exemplo oficial do Skyfield dava 404).
  - Projeção estereográfica em eixos cartesianos, em vez de eixo polar do matplotlib: linhas retas e sem salto em 0°/360°.
  - Prévias como imagem gerada, em vez de HTML: WYSIWYG e sem risco de injeção.
  - `persistir_campos()` com prefixo `campo_`, porque o Streamlit apaga o estado de widgets ao trocar de página.
- **Removido/substituído:**
  - `app.py` monolítico original (backup em `app_original.py`); estrelas aleatórias com `np.random.seed(42)`;
  - grade fixa do caça-palavras; botões "Imprimir" que só diziam "pressione Ctrl+P".

### 2026-09-29 — Análise inicial e plano de ação
- **Pedido:** ler o `app.py` do Jonas e analisar; depois, criar um plano de melhorias mantendo Streamlit.
- **Achados:**
  - o mapa "real" usava estrelas aleatórias e quebrava por um método inexistente do matplotlib;
  - polaroid sem upload; caça-palavras fixo; quiz sem comparação; "imprimir" só com Ctrl+P;
  - HTML sem escape; contraste baixo; sem requirements.
- **Plano:** 5 fases (base, mapa real, completar telas, exportação, organização e publicação). A Fase 5 (publicação) segue pendente.
