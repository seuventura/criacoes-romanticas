"""Criações Românticas: ponto de entrada do app Streamlit.

Rodar com:  streamlit run app.py   (ou o arquivo "Iniciar Criacoes Romanticas.bat")
"""

import streamlit as st

from core.estilo import aplicar_estilo, barra_lateral, marca, persistir_campos, rodape
from core.marca import icone

st.set_page_config(page_title="Criações Românticas", page_icon=icone(), layout="wide")

aplicar_estilo()
persistir_campos()
marca()

pagina = st.navigation(
    {
        "": [st.Page("paginas/inicio.py", title="Início", icon=":material/home:", default=True)],
        "Criar": [
            st.Page("paginas/tickets.py", title="Vales e tickets", icon=":material/confirmation_number:", url_path="vales"),
            st.Page("paginas/mapa_estelar.py", title="Mapa estelar", icon=":material/auto_awesome:", url_path="mapa-estelar"),
            st.Page("paginas/polaroid.py", title="Polaroid", icon=":material/photo_camera:", url_path="polaroid"),
        ],
        "Brincar a dois": [
            st.Page("paginas/passatempos.py", title="Passatempos", icon=":material/extension:", url_path="passatempos"),
        ],
    }
)

barra_lateral()
pagina.run()
rodape()
