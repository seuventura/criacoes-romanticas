# Design system: Criações Românticas

Referência de identidade visual, componentes e textos. Os valores vivem em
`core/design.py` e valem **para a interface e para os arquivos gerados**
(ticket, polaroid, mapa, caça-palavras). O tema do Streamlit fica em
`.streamlit/config.toml`, e o CSS e os componentes em `core/estilo.py`.

## Princípios

1. **O presente é o protagonista.** A interface é moldura: neutra, calma, e a peça em destaque na prévia.
2. **O que se vê é o que se baixa.** A prévia é o próprio arquivo final, nunca uma simulação.
3. **Papelaria, não software.** Serifa suave, papel creme, detalhes manuscritos. Nada de cara de painel administrativo.
4. **Acessível por padrão.** Contraste AA, foco visível, alvos de 44 px e idioma declarado.

## Cores

| Token | Hex | Uso | Contraste |
|---|---|---|---|
| `creme` | `#FAF1C8` | Fundo das páginas (cor da marca) | — |
| `papel` | `#FFFCF3` | Cartões, campos, peças impressas | — |
| `papel_rebaixado` | `#F4E9C1` | Barra lateral | — |
| `linha` | `#E5D8A6` | Divisórias e bordas de cartões | decorativa |
| `borda_campo` | `#8C98AE` | Borda de campos de formulário | 3:1 no papel |
| `tinta` | `#2B3346` | Texto principal | 11,1:1 no creme |
| `tinta_suave` | `#5D6B85` | Texto secundário, legendas | 4,7:1 no creme |
| `rose_forte` | `#B5454E` | Botão primário, links, foco, seleção | branco sobre ele 5,4:1 |
| `rose_escuro` | `#963640` | Hover do primário | — |
| `rose_claro` | `#FBE3E1` | Fundo de item selecionado, selos | — |
| `rose` | `#E16C71` | **Só decoração** (corações, números grandes) | 3,2:1: não usar em texto pequeno |
| `azul` | `#8398B5` | **Só decoração** (ícones, filetes) | 2,6:1: não usar em texto |
| `laranja` / `ceu` | `#F28730` / `#81A7D5` | Estilo "Céu azul" do mapa (paleta original aprovada) | — |

**Categorias de vale** (todas ≥ 4,5:1 sobre o papel): ameixa `#7B4F8E` (cinema), bordô `#8E2F3C` (jantar), floresta `#3D7456` (passeio), petróleo `#2C7470` (relax), rosé `#B5454E` (carinho).

## Tipografia

Três famílias, todas Google Fonts com licença OFL, servidas pelo próprio app (`static/fonts`).

| Família | Papel | Onde |
|---|---|---|
| **Fraunces** (600, 400 itálico) | Títulos e momentos de destaque | Títulos das páginas, etapas, títulos das peças |
| **DM Sans** (400, 500, 700) | Interface e texto corrido | Tudo o que não é título |
| **Caveat** (700) | Toque manuscrito | Dedicatórias do vale, legenda da polaroid, respostas do quiz |

Escala da interface: título de página 2–2,6rem · h2 1,6rem · etapa 1,15rem · corpo 1rem · pequeno .875rem · sobretítulo .75rem em caixa-alta, com espaçamento de .16em, na cor `rose_forte`.
Destaque em título: trecho em *Fraunces itálico* na cor `rose_forte` (`<em>` dentro do título).

## Medidas

- **Espaço:** 4 · 8 · 12 · 16 · 24 · 32 · 48 px
- **Raio:** 8 (pequeno) · 12 (campos) · 20 (cartões e painéis) · pílula (botões)
- **Sombra:** `cartao` (repouso) · `elevada` (hover, cartas) · `peca` (prévia das peças, via `drop-shadow`, que segue o recorte)
- **Movimento:** 120 ms (hover) · 200 ms (cartões). Tudo é desligado com `prefers-reduced-motion`.

## Componentes (`core/estilo.py`)

| Componente | Quando usar |
|---|---|
| `cabecalho_pagina(sobretitulo, titulo_html, descricao)` | Topo de toda página. Sobretítulo "Estúdio · X" nas páginas de criação |
| `estudio()` | Páginas que geram uma peça: controles à esquerda (5/12), prévia fixa à direita (7/12). No celular, a prévia vem primeiro |
| `etapa(n, titulo, dica)` | Agrupa campos em passos numerados (no máximo 3 ou 4 por página) |
| `mostrar_previa(img, largura, nota)` | Única forma de exibir a peça. A nota informa o tamanho de impressão |
| `botoes_download(nome, png, pdf)` | Sempre os dois: **PDF para imprimir** (primário) e **imagem** (secundário) |
| `chips([(rótulo, valor)])` | Metadados curtos (planetas visíveis, fase da Lua) |
| `cartao_desafio`, `placar`, `resposta_comparada` | Passatempos |

Escolhas entre poucas opções: `st.pills` (até ~6 opções curtas, pode quebrar linha) ou `st.segmented_control` (2 a 4 opções curtíssimas, uma linha). Use sempre `required=True` quando a escolha for obrigatória.

## Peças impressas

- Vale: 15 × 6,5 cm. Polaroid: 8,8 × 10,7 cm. Pôster: 20 × 27 cm. Caça-palavras: A4. Todos a 300 dpi (caça-palavras a 150).
- PNG com fundo transparente quando a peça tem recorte (vale, polaroid). No PDF, o fundo é branco.
- Emojis não existem nas fontes de impressão: são removidos do arquivo (mas aparecem na tela).
- Coração: sempre o vetor `desenho.coracao()`, nunca o caractere ♥.

## Voz e textos

- **Tom:** carinhoso e claro, em segunda pessoa do plural quando fala com o casal ("vocês").
- **Botões começam com verbo:** "Baixar PDF para imprimir", "Sortear um desafio", "Revelar respostas".
- **Termos fixos:** *vale* (não "ticket" no texto corrido), *prévia*, *dedicatória*, *baixar* (não "download").
- **Erros:** o que aconteceu + por quê + o que fazer. Ex.: "Não encontramos “X”. Tente escrever como “Cidade, Estado, País”."
- **Estados vazios:** explique e convide. Ex.: "Escolham os tipos de desafio e sorteiem."

## Acessibilidade (WCAG 2.1 AA)

- Contraste verificado para todos os pares de texto da tabela de cores.
- Foco visível: contorno de 3 px em `rose_forte` em botões, links e campos.
- Alvos de toque: botões com 44 px de altura mínima e pílulas com 40 px.
- Idioma da página declarado como `pt-BR`, para os leitores de tela pronunciarem certo.
- Cor nunca é o único sinal: "Combinou/Diferente" tem texto, e itens selecionados mudam de cor e de peso.
- **Limitação conhecida:** `st.image` não aceita texto alternativo. A nota abaixo de cada prévia descreve a peça.
