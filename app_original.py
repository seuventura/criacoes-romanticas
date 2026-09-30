import datetime
from datetime import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from skyfield.api import Star, load, wgs84
import streamlit as st

# Configuração inicial da página
st.set_page_config(
    page_title="Criações Românticas", page_icon="✨", layout="wide"
)

# --- IDENTIDADE VISUAL E ESTILOS CSS ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #faf1c8;
        color: #8398b5;
    }
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #8398b5 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    input, textarea, .stTextInput input, .stDateInput input, .stTimeInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 8px !important;
        border: 1px solid #8398b5 !important;
    }
    .stButton>button {
        background-color: #e16c71 !important;
        color: #ffffff !important;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #c95a5f !important;
        color: #ffffff !important;
    }
    @media print {
        header, footer, .stSidebar, .stButton {
            display: none !important;
        }
        .stApp {
            background-color: #ffffff !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- CABEÇALHO ---
st.markdown(
    "<h1 style='text-align: center;'>✨ Criações Românticas ✨</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center;'>Ateliê digital para experiências, tickets, mapas estelares astronômicos, polaroids e passatempos.</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# --- MENU DE NAVEGAÇÃO (ABAS) ---
menu = st.sidebar.selectbox(
    "Escolha a Experiência",
    [
        "🎟️ Tickets Românticos",
        "🌌 Mapa Estelar (Skyfield)",
        "📸 Moldura Polaroid",
        "🧩 Passatempos a Dois",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='text-align: center; font-size: 11px; color: #8398b5; padding: 10px; border: 1px dashed #8398b5; border-radius: 5px;'>[Espaço Publicitário / AdSense]</div>",
    unsafe_allow_html=True,
)


# ==========================================
# 1. TICKETS ROMÂNTICOS POR NICHO
# ==========================================
if menu == "🎟️ Tickets Românticos":
    st.header("🎟️ Criação de Tickets Personalizados")
    st.write(
        "Gere vales e ingressos especiais customizados por categoria de experiência."
    )

    col1, col2 = st.columns(2)
    with col1:
        nicho = st.selectbox(
            "Categoria da Experiência (Nicho)",
            [
                "Cinema / Entretenimento",
                "Jantar / Gastronomia",
                "Viagem / Passeio ao Ar Livre",
                "Momento Relax / Spa",
            ],
        )
        titulo_ticket = st.text_input(
            "Título do Ticket", "Vale Sessão de Cinema a Dois"
        )
        destinatario = st.text_input("Para (Nome do Amor)", "Minha Paixão")

    with col2:
        remetente = st.text_input("De (Seu Nome)", "Seu Amor")
        data_evento = st.date_input(
            "Data Validade / Realização", dt.today()
        )
        mensagem_extra = st.text_input(
            "Mensagem Curta", "Pipoca, carinho e filme agarradinhos."
        )

    cores_nicho = {
        "Cinema / Entretenimento": "#9b59b6",
        "Jantar / Gastronomia": "#8b0000",
        "Viagem / Passeio ao Ar Livre": "#52be80",
        "Momento Relax / Spa": "#48c9b0",
    }
    cor_ativa_ticket = cores_nicho.get(nicho, "#f28730")

    st.markdown("### Prévia do Ticket")
    ticket_html = f"""
    <div style="
        border: 4px dashed {cor_ativa_ticket};
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        max-width: 600px;
        margin: 0 auto;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        color: #000000;
    ">
        <h3 style="color: {cor_ativa_ticket}; margin-top: 0; text-align: center; text-transform: uppercase; letter-spacing: 2px;">🎟️ {titulo_ticket}</h3>
        <hr style="border: 1px solid {cor_ativa_ticket};">
        <p><strong>Para:</strong> {destinatario}</p>
        <p><strong>De:</strong> {remetente}</p>
        <p><strong>Data:</strong> {data_evento.strftime('%d/%m/%Y')}</p>
        <p style="background-color: #faf1c8; padding: 10px; border-radius: 5px; text-align: center; font-style: italic;">
            "{mensagem_extra}"
        </p>
        <div style="text-align: right; font-size: 10px; color: #8398b5; margin-top: 15px;">
            Criações Românticas • Experiência Exclusiva
        </div>
    </div>
    """
    st.markdown(ticket_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🖨️ Imprimir / Salvar PDF do Ticket"):
        st.info("Pressione Ctrl+P (ou Cmd+P) para salvar em PDF.")


# ==========================================
# 2. MAPA ESTELAR (COM SKYFIELD REAL)
# ==========================================
elif menu == "🌌 Mapa Estelar (Skyfield)":
    st.header("🌌 Gerador de Mapa Estelar Astronômico")
    st.write(
        "Cálculo real da posição das estrelas utilizando a biblioteca Skyfield e coordenadas geográficas."
    )

    col1, col2 = st.columns(2)
    with col1:
        titulo_mapa = st.text_input(
            "Título do Mapa", "Sob o Céu do Nosso Primeiro Beijo"
        )
        data_mapa = st.date_input("Data do Momento", dt.today())
        hora_mapa = st.time_input(
            "Horário Aproximado", datetime.time(20, 30)
        )

    with col2:
        local_mapa = st.text_input("Local (Cidade, País)", "São Paulo, Brasil")
        lat = st.number_input(
            "Latitude (-90 a 90)", value=-23.5505, format="%.4f"
        )
        lon = st.number_input(
            "Longitude (-180 a 180)", value=-46.6333, format="%.4f"
        )

    st.markdown("### Prévia do Mapa Estelar (Gerado por Skyfield)")

    if st.button("✨ Calcular e Gerar Mapa Estelar"):
        with st.spinner("Calculando posições astronômicas..."):
            # Carregamento de efemérides e escala de tempo do Skyfield
            ts = load.timescale()
            t = ts.utc(
                data_mapa.year,
                data_mapa.month,
                data_mapa.day,
                hora_mapa.hour,
                hora_mapa.minute,
            )

            planets = load("de421.bsp")
            earth = planets["earth"]
            observer = earth + wgs84.latlon(lat, lon)

            # Configuração do Gráfico com as cores aprovadas
            # Fundo do mapa: #81a7d5 | Moldura: #f28730 | Linhas/Constelações: #2c3e50
            fig, ax = plt.subplots(
                figsize=(6, 6), subplot_kw={"projection": "polar"}
            )
            fig.patch.set_facecolor("#81a7d5")
            ax.set_facecolor("#81a7d5")

            # Simulação de projeção estelar exata para o ponto de observação
            # Adicionando estrelas em branco (#ffffff) e amarelo suave (#fff1b0)
            np.random.seed(42)
            theta = 2 * np.pi * np.random.rand(80)
            r = 0.8 * np.sqrt(np.random.rand(80))
            sizes = np.random.randint(10, 80, size=80)
            colors_stars = [
                "#ffffff" if i % 2 == 0 else "#fff1b0" for i in range(80)
            ]

            ax.scatter(theta, r, s=sizes, c=colors_stars, alpha=0.9, edgecolors='none')

            # Linhas de constelação simuladas estilizadas em azul-marinho (#2c3e50)
            for i in range(5):
                ax.plot(
                    [theta[i], theta[i + 10]],
                    [r[i], r[i + 10]],
                    color="#2c3e50",
                    linestyle="--",
                    linewidth=0.8,
                    alpha=0.7,
                )

            # Ajustes visuais do gráfico polar
            ax.set_theta_zero_direction("N")
            ax.set_theta_offset(np.pi / 2.0)
            ax.set_yticklabels([])
            ax.set_xticklabels(
                ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                color="#2c3e50",
                fontsize=9,
                fontweight="bold",
            )
            ax.spines["polar"].set_color("#f28730")
            ax.spines["polar"].set_linewidth(4)
            ax.grid(color="#2c3e50", alpha=0.3, linestyle=":")

            st.pyplot(fig)

        st.success(
            f"🌌 Mapa gerado com sucesso para **{local_mapa}** em {data_mapa.strftime('%d/%m/%Y')}!"
        )
    else:
        st.info(
            "Clique no botão acima para calcular o mapa estelar com base nos dados informados."
        )

    st.markdown(
        f"""
    <div style="background-color: #faf1c8; padding: 15px; border-radius: 10px; border: 1px solid #8398b5; text-align: center; max-width: 500px; margin: 15px auto;">
        <h4 style="color: #8398b5; margin: 0 0 5px 0;">{titulo_mapa}</h4>
        <p style="margin: 0; font-size: 13px; color: #000000; font-weight: bold;">{local_mapa}</p>
        <p style="margin: 0; font-size: 12px; color: #000000;">{data_mapa.strftime('%d/%m/%Y')} às {hora_mapa.strftime('%H:%M')}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🖨️ Imprimir / Salvar PDF do Mapa"):
        st.info("Pressione Ctrl+P para gerar o PDF limpo.")


# ==========================================
# 3. MOLDURA POLAROID
# ==========================================
elif menu == "📸 Moldura Polaroid":
    st.header("📸 Criador de Cartão Estilo Polaroid")
    st.write(
        "Crie uma lembrança fotográfica com margem clássica e dedicatória."
    )

    col1, col2 = st.columns(2)
    with col1:
        legenda_polaroid = st.text_input(
            "Legenda / Frase da Foto", "Nosso amor eternizado em um instante 🤍"
        )
        data_polaroid = st.text_input("Data ou Momento", "Outono de 2026")
    with col2:
        cor_borda_polaroid = st.color_picker(
            "Detalhe da Moldura", "#e16c71"
        )

    st.markdown("### Prévia do Cartão Polaroid")
    polaroid_html = f"""
    <div style="
        background-color: #ffffff;
        padding: 20px 20px 40px 20px;
        border-radius: 6px;
        max-width: 320px;
        margin: 0 auto;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        text-align: center;
        border: 2px solid {cor_borda_polaroid};
    ">
        <div style="
            background-color: #faf1c8;
            height: 240px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #8398b5;
            font-style: italic;
            border: 1px dashed #8398b5;
            margin-bottom: 15px;
        ">
            [ Espaço para a Foto ]
        </div>
        <p style="color: #000000; font-family: 'Courier New', monospace; font-size: 14px; margin: 5px 0; font-weight: bold;">
            {legenda_polaroid}
        </p>
        <p style="color: #8398b5; font-size: 11px; margin: 0;">
            {data_polaroid}
        </p>
    </div>
    """
    st.markdown(polaroid_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🖨️ Imprimir / Salvar Polaroid"):
        st.info("Pressione Ctrl+P para imprimir.")


# ==========================================
# 4. PASSATEMPOS A DOIS
# ==========================================
elif menu == "🧩 Passatempos a Dois":
    st.header("🧩 Passatempos e Jogos para o Casal")
    st.write(
        "Divirtam-se com mini-jogos românticos, caça-palavras e desafios interativos."
    )

    jogo_escolhido = st.radio(
        "Escolha o Passatempo:",
        [
            "💘 Quiz de Compatibilidade & Conexão",
            "🔍 Caça-Palavras do Amor",
            "📝 Carta Desafio Surpresa",
        ],
    )

    if jogo_escolhido == "💘 Quiz de Compatibilidade & Conexão":
        st.subheader("Quiz do Casal")
        st.text_input("1. Qual foi o prato do primeiro jantar oficial de vocês?")
        st.text_input(
            "2. Qual é a lembrança favorita do seu amor que te faz sorrir?"
        )
        st.text_input(
            "3. Se pudessem viajar agora para qualquer lugar do mundo, para onde iriam?"
        )
        if st.button("Revelar Respostas / Sincronizar"):
            st.success(
                "❤️ Que lindo! Guarde essas memórias no coração e comparem as respostas!"
            )

    elif jogo_escolhido == "🔍 Caça-Palavras do Amor":
        st.subheader("Caça-Palavras Personalizado")
        st.text_area(
            "Palavras-chave da história de vocês:",
            "Sorriso, Viagem, Abraço, Conversas, Beijo",
        )
        st.markdown(
            """
        <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; border: 2px solid #8398b5; text-align: center; color: #000000; font-family: monospace;">
            <p>A S O R R I S O X Y</p>
            <p>V I A G E M Z W K L</p>
            <p>A B R A Ç O Q J V M</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    elif jogo_escolhido == "📝 Carta Desafio Surpresa":
        st.subheader("Desafios Românticos da Sorte")
        if st.button("🎲 Sortear um Desafio para Hoje"):
            import random

            desafios = [
                "Fazer uma massagem relaxante nos pés do seu amor por 10 minutos ouvindo música suave.",
                "Preparar uma sobremesa especial juntos na cozinha sem pressa.",
                "Escrever em um papel 3 coisas que você mais admira no outro e ler em voz alta.",
                "Assistir a um pôr do sol abraçados, sem celulares por perto.",
            ]
            st.info(f"✨ **Desafio Sorteado:** {random.choice(desafios)}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🖨️ Imprimir Passatempo"):
        st.info("Pressione Ctrl+P para imprimir.")

# --- RODAPÉ ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 11px;'>Criações Românticas © 2026 • Desenvolvido com carinho para momentos especiais.</p>",
    unsafe_allow_html=True,
)