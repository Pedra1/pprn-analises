"""
==============================================================================
PORTAL DE RESULTADOS • CONCURSO POLICIAL PENAL RN (PPRN 2026)
Aplicação Web Interativa em Python e Streamlit
==============================================================================
"""

import os
import streamlit as st

# 1. Configuração da Página
st.set_page_config(
    page_title="PPRN - Resultado Preliminar das Bancas de Cotas (23/10)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Carregamento do Design System CSS (4.2: Proteção Dark Mode e Mobile-First)
def carregar_estilos():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

carregar_estilos()

# 3. Importação dos Módulos da Aplicação
from src.components.meta_tags import render_meta_tags
from src.components.header import render_header
from src.components.dialogs import modal_aviso_legal
from src.components.footer import render_footer
from src.data_loader import carregar_dados, get_mapa_inscricoes
from src.tabs.tab_boletim import render_tab_boletim
from src.tabs.tab_simulador import render_tab_simulador
from src.tabs.tab_listas import render_tab_listas
from src.tabs.tab_regras import render_tab_regras
from src.tabs.tab_cronograma import render_tab_cronograma
from src.tabs.tab_sobre import render_tab_sobre

# 4. Meta Tags Open Graph para Redes Sociais e WhatsApp (4.1)
render_meta_tags()

# 5. Carga de Dados e Índices de Busca
df_base = carregar_dados()

if df_base is None:
    st.error("⚠️ Dados não carregados.")
    st.stop()

mapa_inscricoes = get_mapa_inscricoes(df_base)

# 6. Aviso Inicial / Disclaimer da Banca (Aberto para o candidato na primeira visita)
if "disclaimer_visto" not in st.session_state:
    modal_aviso_legal()

# 7. Cabeçalho Hero e Métricas Oficiais
render_header()

# 8. Navegação Principal em Abas Enxutas e Otimizadas para Mobile (1.3)
tab_busca, tab_simuladores, tab_listas, tab_regras, tab_cronograma, tab_sobre = st.tabs([
    "🔍 Meu Boletim",
    "🔮 Simuladores",
    "📋 Listas Oficiais",
    "🎯 Regras & Cortes",
    "📅 Cronograma",
    "ℹ️ Sobre o Portal"
])

# 8. Renderização das Seções
with tab_busca:
    render_tab_boletim(df_base, mapa_inscricoes)

with tab_simuladores:
    render_tab_simulador(df_base, mapa_inscricoes)

with tab_listas:
    render_tab_listas(df_base)

with tab_regras:
    render_tab_regras()

with tab_cronograma:
    render_tab_cronograma()

with tab_sobre:
    render_tab_sobre()

# 9. Rodapé Institucional
render_footer()
