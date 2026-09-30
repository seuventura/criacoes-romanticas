# CLAUDE.md: Criações Românticas (Projeto do Jonas)

> Documento de contexto para **qualquer IA ou pessoa** que for trabalhar neste projeto.
> Descreve **somente o estado ATUAL** do sistema. O que mudou, por que mudou e o que foi
> removido fica no **[HISTORICO.md](HISTORICO.md)**.

---

## 0. Protocolo obrigatório (leia antes de qualquer coisa)

1. **Ao começar:** leia este arquivo inteiro. Consulte o `HISTORICO.md` quando precisar entender
   o porquê de uma decisão ou antes de refazer algo que já foi tentado.
2. **Ao terminar CADA tarefa** (qualquer mudança em código, dados, configuração ou documentação), antes de responder ao usuário:
   - **Atualize este `CLAUDE.md`** para refletir o estado atual: arquivos novos ou removidos, funções,
     chaves de estado, comandos, regras, armadilhas, pendências. Remova daqui o que deixou de ser verdade.
   - **Acrescente uma entrada no `HISTORICO.md`** (no topo da seção "Registro"), no formato descrito lá:
     data, pedido, o que foi feito, decisões e motivos, o que foi removido e como foi verificado.
3. **O que vai em cada arquivo:**
   - `CLAUDE.md` = **como o sistema é agora** (informação ativa). Sem narrativa de mudanças, sem "antes era assim".
   - `HISTORICO.md` = **como chegou aqui** (mudanças, decisões, alternativas descartadas, código removido).
   - `DESIGN.md` = design system detalhado (cores, fontes, componentes, voz dos textos). Atualize se mexer no visual.
4. **Projeto de teste, separado do trabalho do Pedro:** **não registrar nada no Cérebro** (vault Obsidian):
   nem diário, nem Aprendizados, nem bloco "📥 Para o Cérebro". Isto sobrepõe a regra global do usuário nesta pasta.
5. Idioma: tudo (interface, código, comentários, docs) em **português do Brasil**, com acentuação correta.

---

## 1. Visão geral

- **O que é:** app web em **Streamlit** ("Criações Românticas") onde casais criam presentes personalizados
  e baixam os arquivos prontos para imprimir (PDF) ou enviar (PNG).
- **Produtos:** vale/ticket, mapa estelar astronômico real, cartão Polaroid, passatempos
  (quiz do casal, caça-palavras, desafio do dia).
- **Dono do projeto:** Jonas. Quem opera as sessões é o Pedro. Não há git neste diretório.
- **Status:** funcional, roda localmente. Ainda não publicado (ver Pendências, seção 16).
- **Princípio central:** *a prévia na tela é o próprio arquivo que será baixado.* Nada é simulado em HTML.

---

## 2. Como rodar, testar e parar

| Ação | Comando / forma |
|---|---|
| Rodar (Windows, usuário final) | Dois cliques em `Iniciar Criacoes Romanticas.bat` → abre `http://localhost:8501` |
| Rodar manual | `.venv/Scripts/python -m streamlit run app.py --server.address localhost` |
| Parar | Fechar a janela preta do `.bat` (ou encerrar o processo na porta 8501) |
| Testes | `PYTHONUTF8=1 .venv/Scripts/python -m pytest -q -p no:cacheprovider` (41 testes, ~8 s) |
| Regenerar catálogo astronômico | `.venv/Scripts/python scripts/gerar_catalogo.py` (raro; baixa ~53 MB) |
| Instalar dependências | `.venv/Scripts/python -m pip install -r requirements-dev.txt` |

**O que o `.bat` faz, em ordem:**
1. Se já houver um servidor respondendo em `/_stcore/health` na porta 8501, só abre o navegador.
2. Cria o `.venv` na primeira vez (exige Python no PATH).
3. Reinstala as dependências **só se** `requirements.txt` for diferente de `.venv\requirements.instalado`.
4. Dispara um PowerShell oculto que abre o navegador quando o servidor responde.
5. Roda o Streamlit na mesma janela (`--server.address localhost`: só acessível desta máquina).

**Ambiente:** Windows 11, Python 3.14 no `.venv`. As versões mínimas estão em `requirements.txt`:
streamlit ≥1.50, skyfield, matplotlib, numpy, pandas, pillow, geopy e tzdata. Os testes usam
`requirements-dev.txt` (acrescenta pytest). As features de Streamlit usadas exigem uma versão recente:
`st.navigation`, `st.pills`, `st.segmented_control`, `st.html(unsafe_allow_javascript)`,
`download_button(on_click="ignore")`, `width="stretch"` e `theme.fontFaces`.

---

## 3. Mapa de arquivos

```
app.py                         Entrada: page_config, estilo, marca, st.navigation, barra lateral, rodapé
paginas/
  inicio.py                    Página inicial: herói, vitrine (4 cartões com miniaturas reais), "Como funciona"
  tickets.py                   Estúdio de vales (url /vales)
  mapa_estelar.py              Estúdio do mapa estelar (url /mapa-estelar)
  polaroid.py                  Estúdio da polaroid (url /polaroid)
  passatempos.py               Quiz, caça-palavras e desafio do dia (url /passatempos)
core/                          Lógica e geração das peças. SEM Streamlit, exceto estilo.py
  design.py                    Design system: CORES, CATEGORIA, fontes, ESCALA, ESPACO, RAIO, SOMBRA, MOVIMENTO
  estilo.py                    CSS global + componentes de interface (usa Streamlit)
  marca.py                     Logotipo e ícone (Pillow, com cache)
  fontes.py                    Carrega TTFs de static/fonts; texto_seguro(); registra fontes no matplotlib
  desenho.py                   Utilitários Pillow: quebra/ajuste de texto, tracking, coração vetorial, tracejados
  exportar.py                  PNG/PDF em bytes, remoção de transparência, nome de arquivo
  ticket.py                    Categorias e desenho do vale
  polaroid.py                  Molduras, fitas, filtros e desenho da polaroid
  astronomia.py                Cálculo do céu (Skyfield): estrelas, constelações, Lua, planetas
  mapa.py                      Pôster do mapa estelar (matplotlib), 4 estilos
  geolocalizacao.py            Cidade → latitude/longitude (geopy/Nominatim)
  caca_palavras.py             Gerador de grade + desenho da folha A4
  quiz.py                      Banco de perguntas + comparação tolerante de respostas
  desafios.py                  Banco de desafios + sorteio sem repetição
  vitrine.py                   Peças de exemplo da página inicial (inclui foto ilustrativa gerada por código)
assets/
  estrelas_hip.csv             8.871 estrelas do Hipparcos (mag ≤ 6,5 + estrelas das linhas), 515 KB
  constelacoes.fab             88 constelações (Stellarium v0.22.2, cultura "western")
static/fonts/                  Fraunces, DM Sans e Caveat (TTF, licença OFL) + LICENCAS.md
dados_skyfield/de421.bsp       Efemérides JPL (17 MB). Baixadas sozinhas no 1º mapa se faltarem
scripts/gerar_catalogo.py      Gera os dois arquivos de assets/
tests/                         conftest.py, test_nucleo.py (núcleo), test_paginas.py (páginas via AppTest)
.streamlit/config.toml         Tema, fontFaces, static serving, upload máx. 15 MB, toolbar mínima
Iniciar Criacoes Romanticas.bat  Inicializador Windows (CRLF obrigatório)
requirements.txt / requirements-dev.txt
README.md                      Instruções para pessoas
DESIGN.md                      Design system detalhado
HISTORICO.md                   Histórico de mudanças e decisões
AGENTS.md                      Ponteiro para este arquivo (para IAs que procuram AGENTS.md)
app_original.py                Backup do código original do Jonas. NÃO editar, NÃO importar
.venv/                         Ambiente virtual (não versionar)
```

---

## 4. Nível de produto: páginas e fluxos

Navegação (barra lateral, seções): **Início** · **Criar** (Vales e tickets, Mapa estelar, Polaroid) · **Brincar a dois** (Passatempos).
Todas as páginas começam com `cabecalho_pagina()` e terminam com o rodapé do `app.py`.

### 4.1 Início (`paginas/inicio.py`)
- Herói ("Pequenos gestos, *feitos com carinho.*"), 4 cartões com miniatura real + `st.page_link` para cada estúdio, e 3 passos de "Como funciona".
- As miniaturas vêm de `core/vitrine.py`, com `@st.cache_data` (geradas uma vez por processo, ~2 s na primeira).

### 4.2 Vales e tickets (`paginas/tickets.py`)
- **Etapa 1, A experiência:** `st.pills` com 5 categorias (Cinema & séries, Jantar, Passeio, Relax & spa, Carinho).
  Trocar a categoria sobrescreve título e mensagem com a sugestão dela (callback `_sugerir_textos`).
  Título até 70 caracteres; mensagem até 120.
- **Etapa 2, Para quem:** Para / De (até 40 caracteres cada).
- **Etapa 3, Quando:** toggle "Sem data definida" (imprime "Quando quiser") ou uma data.
- **Saída:** vale 1800×780 px RGBA (15 × 6,5 cm a 300 dpi), PDF e PNG.

### 4.3 Mapa estelar (`paginas/mapa_estelar.py`)
- **Etapa 1, O momento:** data (de 1900 a 2050) e horário local (passo de 5 min).
- **Etapa 2, O lugar:** cidade. Ao apertar Enter, `_buscar_coordenadas` geocodifica e preenche latitude e longitude.
  O endereço encontrado aparece abaixo; erros aparecem como aviso. O expander "Ajustar coordenadas e fuso horário"
  tem latitude, longitude e fuso (fusos do Brasil primeiro, depois todos os IANA).
- **Etapa 3, O pôster:** título (até 60), estilo (4), quantidade de estrelas (Poucas 4,5 / Equilibrada 5,5 / Muitas 6,5
  = magnitude limite), camadas (Constelações, Lua e planetas, Grade).
- **Prévia:** regenerada a cada mudança (sem botão), com cache por conjunto de parâmetros. Mostra etiquetas com
  planetas visíveis, fase da Lua e horário em UTC.
- **Saída:** pôster 8 × 10,5 pol (20 × 27 cm). PNG a 150 dpi e PDF vetorial.

### 4.4 Polaroid (`paginas/polaroid.py`)
- **Etapa 1, A foto:** upload (jpg, jpeg, png, webp; até 15 MB) + filtro (Original, P&B, Sépia, Memória).
  A foto é corrigida pelo EXIF, recortada em quadrado no centro e cacheada por (bytes, filtro).
- **Etapa 2, A dedicatória:** legenda (até 60, em letra manuscrita) e data ou momento (até 30, em caixa-alta espaçada).
- **Etapa 3, O acabamento:** moldura (Branco clássico, Creme, Rosé, Azul sereno, Noite) e fita adesiva
  (Sem fita, Rosé, Azul, Mostarda, Menta).
- Sem foto, desenha "Sua foto aqui" e mesmo assim permite baixar.
- **Saída:** 1200×1425 px RGBA (cartão 1040×1265 + folga transparente de 80 px para a fita), PNG e PDF.

### 4.5 Passatempos (`paginas/passatempos.py`)
Um `st.segmented_control` escolhe o jogo. Só o jogo escolhido é executado.
- **Quiz do casal:** 5 perguntas sorteadas de 18 (a semente fica na sessão). Dois nomes (padrão Ana e Bia).
  Respostas em campos tipo senha, dentro de `st.form`. "Revelar respostas" compara com `quiz.respostas_combinam`
  e mostra placar, mensagem e cartões lado a lado. "Trocar perguntas" gera nova semente.
  Nada é persistido além da sessão do navegador.
- **Caça-palavras:** palavras separadas por vírgula, ponto e vírgula ou linha. Título, dificuldade (Fácil, Médio, Difícil),
  tamanho da grade (8 a 20, sugerido automaticamente), "Embaralhar de novo" e toggle de gabarito.
  Avisa as palavras que não couberam. **Saída:** folha A4 1240×1754 (150 dpi). O PDF tem 2 páginas (folha + gabarito); o PNG, só a folha.
- **Desafio do dia:** pílulas multisseleção de categorias (Em casa, Ao ar livre, Sem gastar nada). O sorteio não repete
  até esgotar a lista (aí avisa com um toast e recomeça). Mostra a carta do desafio e o histórico num expander.

---

## 5. Nível de arquitetura: fluxo de execução

```
Navegador ──> Streamlit roda app.py a cada interação (rerun completo)
  app.py: set_page_config → aplicar_estilo() (CSS + lang=pt-BR) → persistir_campos() → marca()
          → st.navigation(...) → barra_lateral() → pagina.run() → rodape()
  paginas/X.py: cabecalho_pagina → valores_iniciais → estudio() → widgets (key="campo_...")
          → lê st.session_state → chama core (desenhar_* / calcular_ceu) → mostrar_previa → botoes_download
  core/*: funções puras que devolvem PIL.Image ou matplotlib Figure → exportar.py converte em bytes
```

**Regras de dependência entre camadas:**
- `paginas/*` podem importar `core/*` e `streamlit`.
- `core/*` **não** importa Streamlit (exceto `estilo.py`) nem `paginas/*`. Isso permite testar o núcleo sem servidor.
- `core/design.py` é a folha da árvore: não importa nada do projeto.
- Toda cor ou fonte usada em peça ou interface vem de `design.py` (ou de paletas locais documentadas:
  `mapa.ESTILOS`, `polaroid.MOLDURAS/FITAS`, `ticket.CATEGORIAS`).

---

## 6. Nível de módulos: API do núcleo

| Módulo | Principais nomes | Observações |
|---|---|---|
| `design` | `CORES`, `CATEGORIA`, `FAMILIA_*`, `ESCALA`, `ESPACO`, `RAIO`, `SOMBRA`, `MOVIMENTO` | Contrastes documentados no docstring e no DESIGN.md |
| `fontes` | `ESTILOS` (titulo, titulo_regular, titulo_italico, titulo_italico_medio, texto, texto_medio, texto_negrito, manuscrito, manuscrito_medio), `fonte(estilo, tamanho)`, `caminho(estilo)`, `texto_seguro(texto, estilo)`, `registrar_no_matplotlib()` | `texto_seguro` remove todo caractere sem glifo na fonte (emojis) |
| `desenho` | `rgb`, `misturar`, `quebrar_linhas`, `ajustar_texto(draw, texto, estilo, tam_max, tam_min, largura, max_linhas, equilibrar)`, `escrever_linhas`, `texto_espacado`, `coracao`, `linha_tracejada`, `retangulo_tracejado`, `linha_pontilhada`, `data_por_extenso` | `ajustar_texto` reduz a fonte até caber, equilibra as linhas e corta com "…" no mínimo |
| `exportar` | `png_bytes(img, dpi)`, `pdf_bytes([imgs], dpi)`, `sem_transparencia(img)`, `figura_bytes(fig, formato, dpi)`, `nome_arquivo(base, ext)` | O PDF compõe o RGBA sobre branco |
| `ticket` | `Categoria`, `CATEGORIAS`, `DadosTicket(titulo, destinatario, remetente, data\|None, mensagem, cor, rotulo)`, `desenhar_ticket`, `numero_do_vale` | Número "Nº 0000" estável via CRC32 de título, para e de |
| `polaroid` | `MOLDURAS`, `FITAS`, `FILTROS`, `preparar_foto(arquivo)`, `aplicar_filtro(foto, filtro)`, `desenhar_polaroid(foto, legenda, data, moldura, fita)`, `sombra_suave` | `sombra_suave` só para exibição, não vai para o arquivo |
| `astronomia` | `calcular_ceu(lat, lon, data, hora, fuso) -> Ceu`, `para_utc`, `formatar_coordenadas`, `Astro`, `Ceu`, `DATA_MIN`, `DATA_MAX`, `PLANETAS`, `catalogo()`, `constelacoes()`, `efemerides()` | Carregadores com `lru_cache`. Lança `ValueError` fora do intervalo de datas |
| `mapa` | `ESTILOS` (Céu azul, Noite profunda, Papel e tinta, Rosé), `EstiloMapa`, `projetar(alt, az)`, `desenhar_mapa(ceu, titulo, local, legenda_momento, coordenadas, estilo, magnitude_limite, mostrar_*)` | Usa `matplotlib.figure.Figure` (sem pyplot, sem vazamento de memória) |
| `geolocalizacao` | `buscar_lugar(consulta) -> Lugar\|None`, `ErroBusca` | Nominatim, timeout de 8 s, user_agent "criacoes-romanticas-mapa-estelar" |
| `caca_palavras` | `DIRECOES`, `TAMANHO_MIN/MAX`, `normalizar`, `separar_palavras`, `tamanho_sugerido`, `Grade`, `gerar_grade(palavras, tamanho, dificuldade, semente)`, `desenhar_pagina(grade, titulo, gabarito)` | Mesma semente = mesma grade. Maiores primeiro, 400 tentativas por palavra |
| `quiz` | `PERGUNTAS` (18), `sortear_perguntas(n, semente)`, `respostas_combinam(a, b)`, `mensagem_resultado` | Combina se a similaridade for ≥ 0,8 ou se ≥ 50% das palavras relevantes coincidirem |
| `desafios` | `DESAFIOS` (3 categorias, 22 desafios), `sortear(categorias, ja_sorteados) -> (desafio, reiniciou)` | |
| `marca` | `logotipo()`, `icone()` | RGBA, desenhados a 4x |
| `vitrine` | `foto_exemplo()`, `exemplo_ticket/mapa/polaroid/caca_palavras()`, `miniatura()` | Só para a página inicial |
| `estilo` | `esc`, `aplicar_estilo`, `persistir_campos`, `valores_iniciais`, `marca`, `barra_lateral`, `rodape`, `cabecalho_pagina`, `etapa`, `estudio`, `mostrar_previa`, `botoes_download`, `chips`, `cartao_desafio`, `placar`, `resposta_comparada`, `PREFIXO_CAMPO` | CSS com variáveis `--cr-*` geradas de `design.py` |

---

## 7. Estado da sessão (`st.session_state`)

**Campos persistentes** (prefixo `campo_`, sobrevivem à troca de página via `persistir_campos()` no `app.py`):
- Vale: `campo_ticket_categoria`, `_titulo`, `_mensagem`, `_para`, `_de`, `_data`, `_sem_data`
- Mapa: `campo_mapa_titulo`, `_data`, `_hora`, `_local`, `_lat`, `_lon`, `_fuso`, `_estilo`, `_densidade`, `_camadas`
- Polaroid: `campo_polaroid_legenda`, `_data`, `_moldura`, `_filtro`, `_fita`
- Passatempos: `campo_jogo`, `campo_quiz_nome_1`, `campo_quiz_nome_2`, `campo_caca_palavras`, `_titulo`, `_dificuldade`, `_gabarito`, `campo_desafio_categorias`

**Estado interno** (sem prefixo):
- `quiz_semente`, `quiz_revelado`, e as respostas `quiz_{semente}_{1|2}_{i}`
- `caca_semente`, `caca_tamanho_{sugerido}` (slider: a chave muda quando o tamanho sugerido muda, e o valor volta ao sugerido)
- `desafios_sorteados` (lista)
- `mapa_aviso` (tupla tipo/mensagem, consumida com `pop`), `mapa_endereco`

**Regras:** valor inicial só por `valores_iniciais(...)` (usa `setdefault`) e **nunca** `value=` no widget.
Campos alterados por callback (`on_change`) podem ser escritos no `session_state` dentro do callback.
Botões, uploader e form não podem ter o prefixo `campo_`: o Streamlit proíbe atribuir valor a eles.

---

## 8. Cache e desempenho

| Onde | Mecanismo | Chave |
|---|---|---|
| Efemérides, catálogo, constelações, escala de tempo | `functools.lru_cache` (por processo) | — |
| Fontes Pillow, glifos, logotipo | `lru_cache` | (estilo, tamanho) |
| Mapa (PNG + PDF + resumo) | `st.cache_data(max_entries=32)` | dict de parâmetros |
| Geocodificação | `st.cache_data(ttl=24 h)` | texto da cidade. Exceções não são cacheadas |
| Foto da polaroid | `st.cache_data(max_entries=8)` | (bytes, filtro) |
| Miniaturas da vitrine | `st.cache_data` | — |

Tempos medidos: cálculo do céu ~0,1 s; desenho do pôster ~0,6 s; vale e polaroid < 0,3 s.

---

## 9. Astronomia em detalhe

- **Dados:** catálogo Hipparcos filtrado (`assets/estrelas_hip.csv`, colunas `hip, magnitude, ra_hours, dec_degrees,
  ra_mas_per_year, dec_mas_per_year, parallax_mas, epoch_year`); linhas do Stellarium (`assets/constelacoes.fab`,
  pares de números HIP); efemérides `de421.bsp` (Terra, Sol, Lua, planetas).
- **Tempo:** data e hora locais + fuso IANA → `para_utc` (zoneinfo, inclui horário de verão histórico) → `ts.from_datetime`.
- **Cálculo:** `(earth + wgs84.latlon(lat, lon)).at(t).observe(Star.from_dataframe(df)).apparent().altaz()`, vetorizado.
  Planetas: Mercúrio, Vênus, Marte, Júpiter (baricentro) e Saturno (baricentro), só se estiverem acima do horizonte.
  Lua: posição + `fraction_illuminated(sun)`.
- **Linhas de constelação:** mantidas se uma das pontas estiver acima de 0° e nenhuma abaixo de -40°. O desenho recorta no horizonte.
- **Projeção (`mapa.projetar`):** estereográfica centrada no zênite, `r = tan((90° - alt)/2)`, `x = -r·sen(az)`, `y = r·cos(az)`.
  Norte no topo e **Leste à esquerda** (como num mapa do céu visto de baixo). A borda do disco é o horizonte.
- **Tamanho das estrelas:** `2·(0,6 + mag_limite - mag)²`. Estrelas com magnitude < 1,5 usam a cor "estrela_brilhante".
- **Validação conhecida:** Polaris ≈ latitude no hemisfério norte; invisível em São Paulo; Saturno a leste em 29/09/2026 20:30 SP (há testes).

---

## 10. Design system (resumo; o completo está no `DESIGN.md`)

- **Cores principais:** fundo `creme #FAF1C8` · superfícies `papel #FFFCF3` · texto `tinta #2B3346` (11,1:1) ·
  secundário `tinta_suave #5D6B85` (4,7:1) · ação `rose_forte #B5454E` (branco sobre ele 5,4:1).
  `rose #E16C71` e `azul #8398B5` são **só decorativos** (não passam contraste para texto).
- **Fontes:** Fraunces (títulos), DM Sans (interface), Caveat (manuscrita). São as mesmas TTFs na tela e nas peças.
  Na tela, são servidas por `app/static/fonts/...` (config `enableStaticServing = true`).
- **Padrões de interface:** layout de estúdio (controles 5/12 à esquerda, prévia 7/12 fixa à direita; no celular a prévia vem primeiro),
  etapas numeradas, botão primário "Baixar PDF para imprimir" + secundário "Baixar imagem", títulos com trecho em itálico rosé.
- **Acessibilidade:** foco visível de 3 px, botões com 44 px, `lang=pt-BR` injetado por JS, `prefers-reduced-motion` respeitado.
- **CSS depende de seletores internos do Streamlit** (`data-testid=...`, `.st-key-<key>`). Se atualizar o Streamlit, revise o visual.
  Containers estilizados por chave: `controles`, `previa`, `vitrine_*`.

---

## 11. Peças geradas: especificações

| Peça | Pixels | Modo | Impressão | Fontes |
|---|---|---|---|---|
| Vale | 1800×780 | RGBA (recortes transparentes) | 15 × 6,5 cm, 300 dpi | Fraunces, DM Sans, Caveat |
| Polaroid | 1200×1425 (cartão 1040×1265) | RGBA | 8,8 × 10,7 cm, 300 dpi | Caveat, DM Sans |
| Mapa | 8 × 10,5 pol | matplotlib | 20 × 27 cm; PNG 150 dpi, PDF vetorial | Fraunces, DM Sans |
| Caça-palavras | 1240×1754 | RGB | A4, 150 dpi | Fraunces, DM Sans |

- Nome do arquivo: `exportar.nome_arquivo(título)` (slug sem acento, até 60 caracteres).
- Emojis são removidos dos arquivos (`texto_seguro`), mas aparecem na tela.

---

## 12. Testes

- `tests/test_nucleo.py`:
  - fuso e horário de verão, Polaris, céu muda com a data, data fora do intervalo;
  - coordenadas; caça-palavras (todas legíveis, não cabe, deduplicação, semente);
  - quiz (parametrizado); desafios sem repetição;
  - emojis; vale, polaroid e filtros; PDF sem transparência; número do vale;
  - 4 estilos de mapa; marca; nome de arquivo.
- `tests/test_paginas.py`:
  - cada página abre sem exceção nem erro (via `AppTest`); app completo abre na página inicial com 4 page_links;
  - mapa gera botões de download; data fora do intervalo não quebra;
  - vale por categoria e sem data; os 3 passatempos.
- `tests/conftest.py` põe a raiz no `sys.path` e faz `chdir` para ela.
- **Ao criar funcionalidade:** teste a lógica no núcleo (sem Streamlit) e acrescente um teste de abertura da página.

---

## 13. Dependências externas e rede

| Recurso | Quando usa rede | Falha tratada como |
|---|---|---|
| Nominatim (OpenStreetMap) | Ao buscar cidade | Aviso na tela; latitude e longitude continuam editáveis |
| `de421.bsp` (JPL) | Só se faltar em `dados_skyfield/` | `st.error` pedindo conexão (captura `OSError`) |
| Fontes | Nunca (locais em `static/fonts`) | — |
| Catálogo e constelações | Nunca (em `assets/`) | — |

---

## 14. Convenções de código

- Nomes de variáveis, funções e comentários em português, sem abreviações obscuras. Densidade de comentários baixa (só o porquê).
- Nova página que gera peça: use `estudio()`, `etapa()`, `mostrar_previa()` e `botoes_download()`. Registre-a em `app.py` com ícone `:material/...:` e `url_path`.
- Escolha única obrigatória: `st.pills` ou `st.segmented_control` com `required=True`. Texto de interface segue o `DESIGN.md` (verbo nos botões, "vale", "baixar").
- Texto do usuário dentro de HTML: sempre `esc()`. No matplotlib, escapar `$`. Em Pillow: `texto_seguro()` (já embutido em `ajustar_texto`).
- Coração: `desenho.coracao()` (nenhuma fonte tem ♥). Espaçamento entre letras: `texto_espacado()` (Pillow) ou `mapa._texto_espacado` (matplotlib).
- Nada de `st.stop()` nas páginas: corta o rodapé. Use funções com `return`.
- Não usar `pyplot`: crie `matplotlib.figure.Figure` direto.

---

## 15. Armadilhas conhecidas (ativas)

- **Mudou `core/` ou `.streamlit/config.toml`? Reinicie o servidor.** O Streamlit não recarrega módulos importados nem o tema.
- `st.page_link` só funciona dentro do `st.navigation`: teste `inicio.py` via `AppTest.from_file("app.py")`.
- `AppTest.from_file` resolve caminhos relativos ao arquivo de teste: use caminho absoluto.
- Pillow não suaviza polígonos (desenhe em 4x e reduza) e não tem espaçamento entre letras (`texto_espacado`).
- Imagem RGBA salva em PDF sem compor fica com fundo preto: use `sem_transparencia` (já dentro de `pdf_bytes`).
- `ImageDraw` com `fill` RGBA **substitui** o pixel, não mistura: para brilho ou transparência, use `alpha_composite` ou cor misturada.
- O `.bat` precisa de CRLF. O `sed -i` do Git Bash remove os `\r`: reconverta (`sed -i 's/\r$//; s/$/\r/'`).
- Rodar o `.bat` pelo Git Bash (`cmd //c`) quebra no nome com espaços: use o PowerShell `& '.\Iniciar Criacoes Romanticas.bat'`
  ou `Start-Process` para abrir numa janela própria.
- Console do Windows: use `PYTHONUTF8=1` para imprimir acentos e símbolos.
- `zoneinfo` no Windows depende do pacote `tzdata`.
- As efemérides só cobrem 1900 a 2050 (`DATA_MIN`/`DATA_MAX`).
- `st.image` não aceita texto alternativo, e o uploader vem em inglês (traduzido em parte via CSS em `estilo.py`).

---

## 16. Pendências e decisões em aberto

- **Monetização:** a barra lateral tem só um marcador "Publicidade". O AdSense não funciona bem dentro do Streamlit; a decisão é do Jonas.
- **Publicação:** ainda não publicado. Opções: Streamlit Community Cloud ou container (Render/Railway). `de421.bsp` (17 MB) está no projeto.
- **Acessibilidade:** texto alternativo das prévias (limitação do `st.image`); a linha do arquivo enviado segue em inglês.
- **Git:** o diretório não é um repositório. Considerar `git init` antes de novas mudanças grandes.
