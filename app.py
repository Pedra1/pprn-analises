import os
import unicodedata
import io
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="PPRN - Resultado Preliminar das Bancas de Cotas (23/10)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==============================================================================
# ESTILOS CSS CUSTOMIZADOS (BOOTSTRAP 5 DESIGN SYSTEM & BOOTSTRAP ICONS)
# ==============================================================================
st.markdown("""<style>
    @import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css');
    @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;500;600;700;800&display=swap');
    
    /* Variáveis Globais do Bootstrap 5 */
    :root {
        --bs-primary: #0d6efd;
        --bs-primary-rgb: 13, 110, 253;
        --bs-secondary: #6c757d;
        --bs-secondary-rgb: 108, 117, 125;
        --bs-success: #198754;
        --bs-success-rgb: 25, 135, 84;
        --bs-info: #0dcaf0;
        --bs-info-rgb: 13, 202, 240;
        --bs-warning: #ffc107;
        --bs-warning-rgb: 255, 193, 7;
        --bs-danger: #dc3545;
        --bs-danger-rgb: 220, 53, 69;
        --bs-light: #f8f9fa;
        --bs-light-rgb: 248, 249, 250;
        --bs-dark: #212529;
        --bs-dark-rgb: 33, 37, 41;
        --bs-purple: #6f42c1;
        --bs-body-font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", "Liberation Sans", Arial, sans-serif;
        --bs-body-bg: #f8f9fa;
        --bs-body-color: #212529;
        --bs-border-color: #dee2e6;
        --bs-card-border-radius: 0.5rem;
        --bs-border-radius: 0.375rem;
        --bs-box-shadow-sm: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
        --bs-box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    }

    /* Base Global Bootstrap */
    html, body, [class*="css"], .stApp {
        font-family: var(--bs-body-font-family) !important;
        background-color: #f8f9fa !important;
        color: #212529 !important;
    }

    header[data-testid="stHeader"], .stApp > header {
        background-color: #f8f9fa !important;
        border-bottom: 1px solid #dee2e6 !important;
    }

    /* Tipografia de Alto Contraste */
    p, span, div, label, li, a {
        color: #212529;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #212529 !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em;
    }

    .stMarkdown, .stMarkdown p, .stMarkdown span, [data-testid="stMarkdownContainer"] p {
        color: #212529 !important;
    }

    .stCaption, [data-testid="stCaptionContainer"] p {
        color: #6c757d !important;
        font-weight: 500 !important;
    }

    /* Abas Streamlit -> Bootstrap 5 Nav Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 2px solid #dee2e6 !important;
        padding-bottom: 0px !important;
        background: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        white-space: pre-wrap;
        background-color: transparent !important;
        border-radius: 0.375rem 0.375rem 0 0 !important;
        gap: 8px;
        padding: 0.5rem 1.15rem !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        color: #6c757d !important;
        border: 1px solid transparent !important;
        border-bottom: none !important;
        transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #0d6efd !important;
        background-color: #ffffff !important;
        border-color: #dee2e6 #dee2e6 transparent !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        border-color: #dee2e6 #dee2e6 #ffffff !important;
        color: #0d6efd !important;
        font-weight: 700 !important;
        border-bottom: 3px solid #0d6efd !important;
    }

    /* Botões Streamlit -> Bootstrap 5 .btn .btn-primary */
    .stButton > button, div.stButton > button {
        background-color: #0d6efd !important;
        color: #ffffff !important;
        border: 1px solid #0d6efd !important;
        border-radius: 0.375rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.5rem 1.25rem !important;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important;
        transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out, transform 0.1s ease !important;
    }

    .stButton > button:hover, div.stButton > button:hover {
        background-color: #0b5ed7 !important;
        border-color: #0a58ca !important;
        color: #ffffff !important;
        box-shadow: 0 0.25rem 0.5rem rgba(13, 110, 253, 0.25) !important;
        transform: translateY(-1px);
    }

    .stButton > button:active, div.stButton > button:active {
        background-color: #0a58ca !important;
        border-color: #0a53be !important;
        transform: translateY(0);
    }

    /* Botão de Download -> Bootstrap .btn .btn-success */
    .stDownloadButton > button, div.stDownloadButton > button {
        background-color: #198754 !important;
        color: #ffffff !important;
        border: 1px solid #198754 !important;
        border-radius: 0.375rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.5rem 1.25rem !important;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important;
        transition: all 0.15s ease-in-out !important;
    }

    .stDownloadButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #157347 !important;
        border-color: #146c43 !important;
        color: #ffffff !important;
        box-shadow: 0 0.25rem 0.5rem rgba(25, 135, 84, 0.25) !important;
        transform: translateY(-1px);
    }

    /* Inputs e Seletores -> Bootstrap 5 .form-control / .form-select */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 0.375rem !important;
        color: #212529 !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out !important;
    }

    .stTextInput input:focus, .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: #86b7fe !important;
        outline: 0 !important;
        box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25) !important;
    }

    [data-testid="stRadio"] label, [data-testid="stRadio"] span, [data-testid="stRadio"] p,
    [data-testid="stSelectbox"] label, [data-testid="stSelectbox"] span, [data-testid="stSelectbox"] p,
    [data-testid="stTextInput"] label, [data-testid="stTextInput"] span, [data-testid="stTextInput"] p,
    [data-testid="stSlider"] label, [data-testid="stSlider"] span, [data-testid="stSlider"] p {
        color: #212529 !important;
        font-weight: 600 !important;
    }

    /* Métricas Nativas -> Bootstrap Card Metric */
    [data-testid="stMetric"], div[data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 0.5rem !important;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important;
    }

    [data-testid="stMetricLabel"] {
        color: #6c757d !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.03em !important;
    }

    [data-testid="stMetricValue"] {
        color: #212529 !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
    }

    /* Expanders -> Bootstrap 5 Accordion */
    [data-testid="stExpander"] {
        border: 1px solid #dee2e6 !important;
        border-radius: 0.5rem !important;
        overflow: hidden !important;
        background: #ffffff !important;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 0.85rem !important;
    }

    [data-testid="stExpander"] summary {
        background: #f8f9fa !important;
        color: #212529 !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.15rem !important;
        border-bottom: 1px solid #dee2e6 !important;
    }

    /* Modais / Diálogos -> Bootstrap Modal Content */
    div[data-testid="stDialog"] div[role="dialog"] {
        border: 1px solid rgba(0,0,0,0.175) !important;
        border-radius: 0.5rem !important;
        box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15) !important;
        background: #ffffff !important;
    }

    /* Dataframes -> Bootstrap Table Styling */
    [data-testid="stDataFrame"] {
        border: 1px solid #dee2e6 !important;
        border-radius: 0.375rem !important;
        overflow: hidden !important;
        background: #ffffff !important;
    }

    /* ==========================================================================
       COMPONENTES BOOTSTRAP 5 CUSTOMIZADOS
       ========================================================================== */

    /* Hero Banner Institucional -> Bootstrap Lead Jumbotron */
    .hero-container {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-top: 4px solid #0d6efd;
        border-radius: 0.5rem;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    }
    
    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        color: #212529 !important;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.02em;
        line-height: 1.25;
    }
    
    .hero-subtitle {
        color: #6c757d !important;
        font-size: 0.95rem;
        margin: 0;
        line-height: 1.55;
        font-weight: 400;
    }

    /* Badges Pill -> Bootstrap 5 Badges */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background-color: #d1e7dd;
        color: #0f5132;
        border: 1px solid #badbcc;
        padding: 0.35em 0.75em;
        border-radius: 50rem;
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 0.5rem;
    }

    .badge-pill-amber {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background-color: #fff3cd;
        color: #664d03;
        border: 1px solid #ffecb5;
        padding: 0.35em 0.75em;
        border-radius: 50rem;
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 0.5rem;
    }

    .badge-pill-blue {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background-color: #cfe2ff;
        color: #084298;
        border: 1px solid #b6d4fe;
        padding: 0.35em 0.75em;
        border-radius: 50rem;
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 0.5rem;
    }
    
    /* Stat Cards -> Bootstrap Cards com Hover */
    .stat-card {
        background: #ffffff !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 0.5rem !important;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
    }
    
    .stat-card:hover {
        border-color: #adb5bd !important;
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
        transform: translateY(-2px);
    }
    
    .stat-label {
        color: #6c757d !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
        margin-bottom: 0.35rem !important;
    }
    
    .stat-value {
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        color: #212529 !important;
        line-height: 1.2 !important;
    }
    
    .stat-sub {
        font-size: 0.78rem !important;
        color: #6c757d !important;
        margin-top: 0.35rem !important;
        font-weight: 600 !important;
    }

    /* Cards do Candidato -> Bootstrap Card */
    .candidate-card {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    }
    
    .pos-badge {
        display: inline-block;
        padding: 0.45rem 1.1rem;
        border-radius: 0.375rem;
        font-weight: 800;
        font-size: 1.1rem;
        letter-spacing: -0.01em;
    }
    
    .pos-top {
        background-color: #d1e7dd;
        color: #0f5132;
        border: 1px solid #badbcc;
    }
    
    .pos-standard {
        background-color: #f8f9fa;
        color: #212529;
        border: 1px solid #dee2e6;
    }
    
    .tag-cota {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 0.375rem;
        font-size: 0.75rem;
        font-weight: 700;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }
    
    .tag-ampla { background-color: #cfe2ff; color: #084298; border: 1px solid #b6d4fe; }
    .tag-negro { background-color: #e2d9f3; color: #491278; border: 1px solid #c9b8ea; }
    .tag-indigena { background-color: #ffe5d0; color: #8a3408; border: 1px solid #ffd0aa; }
    .tag-quilombola { background-color: #fff3cd; color: #664d03; border: 1px solid #ffecb5; }
    .tag-pcd { background-color: #d1e7dd; color: #0f5132; border: 1px solid #badbcc; }

    /* Cards de Resultado das Bancas -> Bootstrap Alerts com Borda Esquerda */
    .card-resultado-deferido {
        background-color: #d1e7dd;
        border: 1px solid #badbcc;
        border-left: 5px solid #198754;
        border-radius: 0.5rem;
        padding: 1.1rem 1.25rem;
        margin: 1rem 0;
        color: #0f5132;
    }

    .card-resultado-indeferido {
        background-color: #fff3cd;
        border: 1px solid #ffecb5;
        border-left: 5px solid #ffc107;
        border-radius: 0.5rem;
        padding: 1.1rem 1.25rem;
        margin: 1rem 0;
        color: #664d03;
    }

    .card-resultado-ampla {
        background-color: #cff4fc;
        border: 1px solid #b6effb;
        border-left: 5px solid #0dcaf0;
        border-radius: 0.5rem;
        padding: 1.1rem 1.25rem;
        margin: 1rem 0;
        color: #055160;
    }

    .recurso-alert-box {
        background-color: #cfe2ff;
        border: 1px solid #b6d4fe;
        border-left: 4px solid #0d6efd;
        border-radius: 0.375rem;
        padding: 0.85rem 1.1rem;
        margin-top: 0.75rem;
        font-size: 0.875rem;
        color: #084298;
        line-height: 1.55;
    }

    .card-previsao-ok {
        background-color: #d1e7dd;
        border: 1px solid #badbcc;
        border-left: 5px solid #198754;
        border-radius: 0.5rem;
        padding: 1.1rem 1.25rem;
        margin-top: 0.85rem;
        color: #0f5132;
    }

    .card-previsao {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-left: 5px solid #6c757d;
        border-radius: 0.5rem;
        padding: 1.1rem 1.25rem;
        margin-top: 0.85rem;
        color: #212529;
    }

    /* Linha do Tempo (Cronograma) -> Bootstrap List Group Style */
    .timeline-card {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .timeline-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.08);
    }

    .timeline-card-past { border-left: 5px solid #198754; }
    .timeline-card-active { border-left: 5px solid #ffc107; background-color: #fffdf5; }
    .timeline-card-next { border-left: 5px solid #0d6efd; }
    .timeline-card-future { border-left: 5px solid #adb5bd; opacity: 0.85; }

    /* Banners de Simulação */
    .sim-banner {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-top: 4px solid #6f42c1;
        border-radius: 0.5rem;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    }

    .sim-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background-color: #e2d9f3;
        color: #491278;
        border: 1px solid #c9b8ea;
        padding: 0.35em 0.75em;
        border-radius: 50rem;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.5rem;
    }

    .sim-gain-pill {
        display: inline-block;
        background-color: #d1e7dd;
        color: #0f5132;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 0.2em 0.6em;
        border-radius: 0.25rem;
        border: 1px solid #badbcc;
    }

    .sim-notice-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-left: 4px solid #0d6efd;
        border-radius: 0.5rem;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
    }

    .candidate-header-badge { text-align: right; }
    .modal-grid-2col {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    /* Rodapé Bootstrap */
    .footer-container {
        text-align: center;
        color: #6c757d;
        font-size: 0.875rem;
        padding: 1.75rem 0 1rem 0;
        border-top: 1px solid #dee2e6;
        margin-top: 2rem;
        line-height: 1.6;
    }

    /* Responsividade Mobile-First */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.75rem 0.5rem 2rem 0.5rem !important;
            max-width: 100% !important;
        }

        .hero-container {
            padding: 1rem !important;
            border-radius: 0.375rem !important;
            margin-bottom: 0.75rem !important;
        }

        .hero-title {
            font-size: 1.35rem !important;
            line-height: 1.25 !important;
            margin: 4px 0 6px 0 !important;
        }

        .hero-subtitle {
            font-size: 0.85rem !important;
            line-height: 1.45 !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            display: flex !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            scrollbar-width: none !important;
            gap: 4px !important;
            padding-bottom: 2px !important;
            border-bottom: 2px solid #dee2e6 !important;
        }

        .stTabs [data-baseweb="tab"] {
            flex: 0 0 auto !important;
            white-space: nowrap !important;
            height: 38px !important;
            padding: 0.4rem 0.85rem !important;
            font-size: 0.825rem !important;
            border-radius: 0.375rem 0.375rem 0 0 !important;
        }

        [data-testid="column"] {
            flex: 1 1 100% !important;
            width: 100% !important;
            min-width: 100% !important;
            margin-bottom: 0.5rem !important;
        }

        .stat-card {
            padding: 0.85rem 1rem !important;
            border-radius: 0.375rem !important;
            margin-bottom: 0.5rem !important;
        }

        .candidate-card {
            padding: 1rem !important;
            border-radius: 0.375rem !important;
            margin-bottom: 0.85rem !important;
        }

        .candidate-header-badge {
            text-align: left !important;
            width: 100% !important;
            margin-top: 0.5rem !important;
        }

        .modal-grid-2col {
            grid-template-columns: 1fr !important;
            gap: 0.75rem !important;
        }

        div[data-testid="stDialog"] div[role="dialog"] {
            width: 95vw !important;
            max-width: 95vw !important;
            padding: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# CONFIGURAÇÕES DE DISCIPLINAS E EDITAL
# ==============================================================================
DISCIPLINAS_CONFIG = [
    ("Língua Portuguesa", 15),
    ("História do RN", 5),
    ("Ética no Serviço Público", 5),
    ("Direito Constitucional", 10),
    ("Direito Administrativo", 10),
    ("Direitos Humanos", 10),
    ("Execução Penal", 30),
    ("Legislação Específica", 40),
    ("Direito Penal e Processo Penal", 20),
]

DISCIPLINAS = [d[0] for d in DISCIPLINAS_CONFIG]
PONTOS_MAXIMOS = {d[0]: d[1] for d in DISCIPLINAS_CONFIG}
NOTA_MAXIMA_PROVA = sum(PONTOS_MAXIMOS.values())  # 145 pontos

def normalizar_texto(texto):
    if not isinstance(texto, str):
        texto = str(texto)
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn').upper().strip()

@st.cache_data(show_spinner=False)
def carregar_dados():
    parquet_path = "pprn_dados.parquet"
    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
    else:
        st.error("Arquivo pprn_dados.parquet não encontrado.")
        return None
        
    if 'Posição_Geral' not in df.columns:
        df['Posição_Geral'] = range(1, len(df) + 1)
    if 'Nome_Busca' not in df.columns:
        df['Nome_Busca'] = df['Nome'].apply(normalizar_texto)
    if 'Inscrição_Str' not in df.columns:
        df['Inscrição_Str'] = df['Inscrição'].astype(str)
        
    return df

df_base = carregar_dados()

if df_base is None:
    st.error("⚠️ Dados não carregados.")
    st.stop()

# Totais gerais estáticos pré-computados (0ms de CPU por reload)
TOTAL_CANDIDATOS = 18945
TOTAL_AMPLA_PURA = 11977
TOTAL_ETNICO = 6309
TOTAL_PCD = 659
TOTAL_NEGRO_PARDO = 6243
TOTAL_INDIGENA = 58
TOTAL_QUILOMBOLA = 29

TOTAL_ETNICO_APTOS = 3264
TOTAL_ETNICO_INAPTOS = 3045
PCT_ETNICO_APTOS = 51.74
PCT_ETNICO_INAPTOS = 48.26

TOTAL_PCD_APTOS = 473
TOTAL_PCD_INAPTOS = 186
PCT_PCD_APTOS = 71.78
PCT_PCD_INAPTOS = 28.22

TOTAL_CONVOCADOS_TAF_PRELIMINAR = 1850

MAIOR_NOTA = 138
MENOR_NOTA = 73
MEDIA_NOTA = 89.2
MEDIANA_NOTA = 88.0

TOTAL_CANDIDATOS_FMT = "18.945"
TOTAL_AMPLA_FMT = "11.977"
TOTAL_ETNICO_FMT = "6.309"
TOTAL_PCD_FMT = "659"

MEDIAS_DISCIPLINAS = {
    'Língua Portuguesa': 5.55,
    'História do RN': 3.62,
    'Ética no Serviço Público': 3.36,
    'Direito Constitucional': 7.15,
    'Direito Administrativo': 6.99,
    'Direitos Humanos': 7.74,
    'Execução Penal': 17.94,
    'Legislação Específica': 32.79,
    'Direito Penal e Processo Penal': 10.01
}

@st.cache_data(show_spinner=False)
def get_mapa_inscricoes(_df):
    return {str(insc): i for i, insc in enumerate(_df['Inscrição'])}

mapa_inscricoes = get_mapa_inscricoes(df_base)

@st.cache_data(show_spinner=False)
def carregar_bytes_excel(caminho):
    if os.path.exists(caminho):
        with open(caminho, "rb") as f:
            return f.read()
    return None

# ==============================================================================
# MOTOR DE SIMULAÇÃO PÓS-BANCAS DE 23/10 (RECURSOS & TAF)
# ==============================================================================
@st.cache_data(show_spinner="Calculando simulação pós-bancas e TAF...")
def executar_simulacao_pos_bancas(
    modo="real_bancas", 
    taxa_reversao_etnico_pct=5, 
    taxa_reversao_pcd_pct=5, 
    taxa_taf_pct=20,
    sim_taxa_hetero_pct=48, 
    sim_taxa_pcd_pct=28, 
    regra_inaptos='migrar_ampla'
):
    df_sim = df_base.copy()
    
    if modo == "real_bancas":
        rng_rev_etnico = np.random.RandomState(42)
        rng_rev_pcd = np.random.RandomState(123)
        
        idx_indef_etnico = df_sim[df_sim['Cota_Etnico_Racial'] & (~df_sim['Cota_Etnico_Apta_Preliminar'])].index
        scores_rev_etnico = pd.Series(rng_rev_etnico.rand(len(idx_indef_etnico)), index=idx_indef_etnico)
        revertidos_etnico = idx_indef_etnico[scores_rev_etnico < (taxa_reversao_etnico_pct / 100.0)]
        
        idx_indef_pcd = df_sim[df_sim['Cota_PCD'] & (~df_sim['Cota_PCD_Apta_Preliminar'])].index
        scores_rev_pcd = pd.Series(rng_rev_pcd.rand(len(idx_indef_pcd)), index=idx_indef_pcd)
        revertidos_pcd = idx_indef_pcd[scores_rev_pcd < (taxa_reversao_pcd_pct / 100.0)]
        
        df_sim['Cota_Etnico_Sim'] = df_sim['Cota_Etnico_Apta_Preliminar'].copy()
        df_sim.loc[revertidos_etnico, 'Cota_Etnico_Sim'] = True
        
        df_sim['Cota_PCD_Sim'] = df_sim['Cota_PCD_Apta_Preliminar'].copy()
        df_sim.loc[revertidos_pcd, 'Cota_PCD_Sim'] = True
        
        total_inaptos_etnico = len(df_sim[df_sim['Cota_Etnico_Racial'] & (~df_sim['Cota_Etnico_Sim'])])
        total_inaptos_pcd = len(df_sim[df_sim['Cota_PCD'] & (~df_sim['Cota_PCD_Sim'])])
        
    else:
        rng_etnico = np.random.RandomState(42)
        scores_etnico = pd.Series(rng_etnico.rand(len(df_sim)), index=df_sim.index)
        rng_pcd = np.random.RandomState(123)
        scores_pcd = pd.Series(rng_pcd.rand(len(df_sim)), index=df_sim.index)

        is_inapto_etnico = df_sim['Cota_Etnico_Racial'] & (scores_etnico < (sim_taxa_hetero_pct / 100.0))
        is_inapto_pcd = df_sim['Cota_PCD'] & (scores_pcd < (sim_taxa_pcd_pct / 100.0))
        
        df_sim['Cota_Etnico_Sim'] = df_sim['Cota_Etnico_Racial'] & (~is_inapto_etnico)
        df_sim['Cota_PCD_Sim'] = df_sim['Cota_PCD'] & (~is_inapto_pcd)
        total_inaptos_etnico = int(is_inapto_etnico.sum())
        total_inaptos_pcd = int(is_inapto_pcd.sum())
        
    idx_etnico_aptos = df_sim[df_sim['Cota_Etnico_Sim']].index
    df_sim['Pos_Etnico_Sim'] = np.nan
    df_sim.loc[idx_etnico_aptos, 'Pos_Etnico_Sim'] = range(1, len(idx_etnico_aptos) + 1)
    
    idx_pcd_aptos = df_sim[df_sim['Cota_PCD_Sim']].index
    df_sim['Pos_PCD_Sim'] = np.nan
    df_sim.loc[idx_pcd_aptos, 'Pos_PCD_Sim'] = range(1, len(idx_pcd_aptos) + 1)
    
    cand_960 = df_sim.iloc[959]
    corte_ampla_taf = int(cand_960['Nota Objetiva'])
    convocados_ampla_taf = df_sim['Nota Objetiva'] >= corte_ampla_taf
    
    cotistas_fora_ampla = df_sim[df_sim['Cota_Etnico_Sim'] & (~convocados_ampla_taf)]
    if len(cotistas_fora_ampla) >= 240:
        cand_240_cota = cotistas_fora_ampla.iloc[239]
        corte_etnico_taf = int(cand_240_cota['Nota Objetiva'])
        convocados_etnico_reserva = cotistas_fora_ampla['Nota Objetiva'] >= corte_etnico_taf
        idx_etnico_reserva = cotistas_fora_ampla[convocados_etnico_reserva].index
    else:
        corte_etnico_taf = int(cotistas_fora_ampla['Nota Objetiva'].min()) if len(cotistas_fora_ampla) > 0 else 73
        idx_etnico_reserva = cotistas_fora_ampla.index
        
    idx_pcd_taf = df_sim[df_sim['Cota_PCD_Sim']].index
    
    df_sim['Convocado_TAF_Sim'] = False
    df_sim.loc[df_sim[convocados_ampla_taf].index, 'Convocado_TAF_Sim'] = True
    df_sim.loc[idx_etnico_reserva, 'Convocado_TAF_Sim'] = True
    df_sim.loc[idx_pcd_taf, 'Convocado_TAF_Sim'] = True
    
    total_convocados_taf = int(df_sim['Convocado_TAF_Sim'].sum())
    
    rng_taf = np.random.RandomState(777)
    scores_taf = pd.Series(rng_taf.rand(len(df_sim)), index=df_sim.index)
    reprovados_taf = df_sim['Convocado_TAF_Sim'] & (scores_taf < (taxa_taf_pct / 100.0))
    total_reprovados_taf = int(reprovados_taf.sum())
    
    df_sim['Status_TAF_Sim'] = 'Não Convocado'
    df_sim.loc[df_sim['Convocado_TAF_Sim'], 'Status_TAF_Sim'] = 'Apto no TAF'
    df_sim.loc[reprovados_taf, 'Status_TAF_Sim'] = 'Reprovado / Ausente no TAF'
    
    aptos_taf = df_sim[df_sim['Status_TAF_Sim'] == 'Apto no TAF'].copy()
    aptos_taf['Pos_Final_Geral_Aptos'] = range(1, len(aptos_taf) + 1)
    
    vagas_ampla = aptos_taf.head(140)
    idx_vagas_ampla = vagas_ampla.index
    
    aptos_etnico_fora_ampla = aptos_taf[aptos_taf['Cota_Etnico_Sim'] & (~aptos_taf.index.isin(idx_vagas_ampla))]
    vagas_etnico = aptos_etnico_fora_ampla.head(40)
    idx_vagas_etnico = vagas_etnico.index
    
    aptos_pcd_fora_ampla = aptos_taf[aptos_taf['Cota_PCD_Sim'] & (~aptos_taf.index.isin(idx_vagas_ampla)) & (~aptos_taf.index.isin(idx_vagas_etnico))]
    vagas_pcd = aptos_pcd_fora_ampla.head(20)
    idx_vagas_pcd = vagas_pcd.index
    
    df_sim['Vaga_Imediata_Sim'] = '📋 Cadastro de Reserva'
    df_sim.loc[idx_vagas_ampla, 'Vaga_Imediata_Sim'] = '🏆 Vaga Imediata (Ampla Concorrência)'
    df_sim.loc[idx_vagas_etnico, 'Vaga_Imediata_Sim'] = '🏆 Vaga Imediata (Cota Étnico-Racial)'
    df_sim.loc[idx_vagas_pcd, 'Vaga_Imediata_Sim'] = '🏆 Vaga Imediata (Cota PCD)'
    
    ultimo_ampla_orig = int(vagas_ampla.iloc[-1]['Posição_Geral']) if len(vagas_ampla) > 0 else 140
    ultimo_etnico_orig = int(vagas_etnico.iloc[-1]['Pos_Lista_Etnico']) if len(vagas_etnico) > 0 else 40
    ultimo_pcd_orig = int(vagas_pcd.iloc[-1]['Pos_Lista_PCD']) if len(vagas_pcd) > 0 else 20
    
    novos_vagas_ampla = vagas_ampla[vagas_ampla['Posição_Geral'] > 140]
    novos_vagas_etnico = vagas_etnico[vagas_etnico['Pos_Lista_Etnico'] > 40]
    novos_vagas_pcd = vagas_pcd[vagas_pcd['Pos_Lista_PCD'] > 20]
    
    resumo = {
        'total_inaptos_etnico': total_inaptos_etnico,
        'total_inaptos_pcd': total_inaptos_pcd,
        'total_convocados_taf': total_convocados_taf,
        'total_reprovados_taf': total_reprovados_taf,
        'total_aptos_taf': len(aptos_taf),
        'corte_ampla_taf': corte_ampla_taf,
        'corte_etnico_taf': corte_etnico_taf,
        'ultimo_ampla_orig': ultimo_ampla_orig,
        'ganho_ampla': ultimo_ampla_orig - 140,
        'ultimo_etnico_orig': ultimo_etnico_orig,
        'ganho_etnico': ultimo_etnico_orig - 40,
        'ultimo_pcd_orig': ultimo_pcd_orig,
        'ganho_pcd': ultimo_pcd_orig - 20,
        'qtd_novos_vagas_ampla': len(novos_vagas_ampla),
        'qtd_novos_vagas_etnico': len(novos_vagas_etnico),
        'qtd_novos_vagas_pcd': len(novos_vagas_pcd),
    }
    
    return df_sim, resumo, novos_vagas_ampla, novos_vagas_etnico, novos_vagas_pcd

# ==============================================================================
# AVISO LEGAL INICIAL & NOVIDADES DE 23 DE OUTUBRO (MODAL BOOTSTRAP 5)
# ==============================================================================
@st.dialog("📢 Atualização Importante: Listas Preliminares das Bancas (23/10)", width="large")
def modal_aviso_legal():
    st.markdown("""
<div>
<div class="alert alert-warning border-start border-4 border-warning shadow-sm rounded-3 p-3 mb-3">
    <div class="d-flex align-items-center gap-2 mb-1" style="font-size: 0.82rem; font-weight: 800; color: #664d03; text-transform: uppercase; letter-spacing: 0.04em;">
        <i class="bi bi-lightning-charge-fill text-warning fs-6"></i> PUBLICAÇÃO OFICIAL DAS BANCAS DE COTAS • 23 DE OUTUBRO DE 2026
    </div>
    <div style="font-size: 0.94rem; color: #212529; line-height: 1.55;">
        Hoje, <strong>23 de outubro de 2026</strong>, a banca examinadora (Instituto Avalia) publicou o <strong>Resultado Preliminar da Heteroidentificação Étnico-Racial</strong> (Pretos, Pardos, Indígenas e Quilombolas) e o <strong>Resultado Preliminar da Perícia Médica PCD</strong>.<br>
        O portal foi integralmente atualizado com todas as informações oficiais!
    </div>
</div>

<div class="modal-grid-2col">
    <div class="card border shadow-sm p-3 mb-2 rounded-3">
        <div class="d-flex align-items-center gap-2 mb-1" style="font-size: 0.85rem; font-weight: 700; color: #0d6efd; text-transform: uppercase;">
            <i class="bi bi-shield-check text-primary fs-5"></i> Indeferido(a) na Cota? Não se Desespere!
        </div>
        <div style="font-size: 0.88rem; color: #6c757d; line-height: 1.5;">
            Conforme o <strong>Art. 4º</strong> (Hetero) e <strong>Art. 3º</strong> (PCD) dos Editais de Convocação, o indeferimento da cota <strong>NÃO elimina o candidato do concurso</strong>. O candidato passa a concorrer normalmente pela Ampla Concorrência!
        </div>
    </div>
    <div class="card border shadow-sm p-3 mb-2 rounded-3">
        <div class="d-flex align-items-center gap-2 mb-1" style="font-size: 0.85rem; font-weight: 700; color: #198754; text-transform: uppercase;">
            <i class="bi bi-file-earmark-text text-success fs-5"></i> Prazo para Interposição de Recursos
        </div>
        <div style="font-size: 0.88rem; color: #6c757d; line-height: 1.5;">
            Caberá recurso contra o resultado preliminar da <strong>0h00 do dia 26/10/2026 até às 23h59 do dia 27/10/2026</strong> no endereço eletrônico <a href="https://www.avalia.org.br" target="_blank" class="fw-bold text-primary">avalia.org.br</a>. O motivo pode ser consultado no link <em>"Boletim de Análise de Reserva de Vagas"</em>.
        </div>
    </div>
</div>

<div class="alert alert-info border-start border-4 border-info shadow-sm rounded-3 p-3 mb-3 d-flex align-items-start gap-2" style="font-size: 0.88rem; color: #055160; line-height: 1.5;">
    <i class="bi bi-info-circle-fill text-info fs-5 flex-shrink-0 mt-1"></i>
    <div>
        <strong>Iniciativa Independente:</strong> Este portal é colaborativo e sem vínculo oficial com o Instituto Avalia ou SEAD/RN. Atos administrativos oficiais competem exclusivamente à banca examinadora em <a href="https://www.avalia.org.br" target="_blank" class="fw-bold text-primary">avalia.org.br</a>.
    </div>
</div>
</div>
""", unsafe_allow_html=True)

    if st.button("✅ Entendi e Desejo Acessar o Portal Atualizado", type="primary", width="stretch"):
        st.session_state["disclaimer_visto"] = True
        st.rerun()

# ==============================================================================
# HEADER HERO & VISÃO GERAL DAS BANCAS (BOOTSTRAP 5)
# ==============================================================================
st.markdown("""<div class="hero-container">
<div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-2">
    <span class="badge-pill-amber"><i class="bi bi-lightning-charge-fill text-warning me-1"></i> ATUALIZAÇÃO 23 DE OUTUBRO DE 2026 • RESULTADO PRELIMINAR DAS BANCAS</span>
    <span class="fw-bold text-primary text-uppercase" style="font-size: 0.8rem; letter-spacing: 0.05em;"><i class="bi bi-shield-shaded me-1"></i> GOVERNO DO ESTADO DO RIO GRANDE DO NORTE • SEAD / SEAP</span>
</div>
<h1 class="hero-title"><i class="bi bi-shield-fill-check text-primary me-2"></i>Portal de Resultados • Concurso Policial Penal RN</h1>
<p class="hero-subtitle">
Boletim do candidato com resultado oficial preliminar da <strong>Heteroidentificação Étnico-Racial</strong> e da <strong>Perícia Médica PCD</strong>, orientações recursais (26 e 27/10) e avanço na reclassificação das cotas.
</p>
<div class="alert alert-warning border-start border-4 border-warning rounded-3 p-3 mt-3 mb-0" style="font-size: 0.88rem; line-height: 1.5;">
    <i class="bi bi-exclamation-triangle-fill text-warning me-1"></i> <strong>Informação Importante aos Convocados:</strong> Candidatos indeferidos na cota <strong>não estão eliminados</strong> do concurso (Art. 4º Hetero / Art. 3º PCD) e continuam na <strong>Ampla Concorrência</strong>. Prazo para recursos: <strong>26 e 27 de outubro</strong> no site <a href="https://www.avalia.org.br" target="_blank" class="fw-bold text-primary">avalia.org.br</a>.
</div>
</div>""", unsafe_allow_html=True)

# 4 Métricas Principais Bootstrap
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-people-fill text-primary me-1"></i> Total Aprovados</div>
<div class="stat-value">{TOTAL_CANDIDATOS_FMT}</div>
<div class="stat-sub">100% da lista objetiva oficial</div>
</div>""", unsafe_allow_html=True)

with m2:
    st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-person-fill-check me-1" style="color: #6f42c1;"></i> Heteroidentificação Étnica</div>
<div class="stat-value" style="color: #6f42c1;">{TOTAL_ETNICO_APTOS:,} Aprovados</div>
<div class="stat-sub text-warning fw-bold">{TOTAL_ETNICO_APTOS:,} Deferidos ({PCT_ETNICO_APTOS:.1f}%) | {TOTAL_ETNICO_INAPTOS:,} Indeferidos ({PCT_ETNICO_INAPTOS:.1f}%)</div>
</div>""".replace(",", "."), unsafe_allow_html=True)

with m3:
    st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-universal-access text-success me-1"></i> Perícia Médica PCD</div>
<div class="stat-value text-success">{TOTAL_PCD_APTOS} Aprovados</div>
<div class="stat-sub text-success fw-bold">{TOTAL_PCD_APTOS} Deferidos ({PCT_PCD_APTOS:.1f}%) | {TOTAL_PCD_INAPTOS} Indeferidos ({PCT_PCD_INAPTOS:.1f}%)</div>
</div>""", unsafe_allow_html=True)

with m4:
    st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-award-fill text-primary me-1"></i> Não Cotistas (Ampla)</div>
<div class="stat-value text-primary">{TOTAL_AMPLA_FMT}</div>
<div class="stat-sub">{(TOTAL_AMPLA_PURA/TOTAL_CANDIDATOS)*100:.1f}% concorrendo exclusivamente na Ampla</div>
</div>""", unsafe_allow_html=True)

st.write("")

# ==============================================================================
# NAVEGAÇÃO PRINCIPAL EM ABAS
# ==============================================================================
tab_busca, tab_simuladores, tab_listas, tab_regras, tab_cronograma, tab_sobre = st.tabs([
    "🔍 Meu Boletim (Consulta Rápida)",
    "🔮 Simulador de Colocações & Impacto das Bancas",
    "📋 As Listas Oficiais & Resultados das Bancas",
    "🎯 Entenda as Regras, Recursos & Linhas de Corte",
    "📅 Cronograma Oficial do Concurso",
    "ℹ️ Sobre o Portal & Metodologia"
])

# ==============================================================================
# ==============================================================================
# ABA 1: CONSULTA INDIVIDUAL (BOLETIM COM RESULTADO DAS BANCAS DE 23/10)
# ==============================================================================
def definir_termo_busca(valor):
    st.session_state["termo_busca_input"] = valor

def limpar_termo_busca():
    st.session_state["termo_busca_input"] = ""

with tab_busca:
    st.subheader("🔍 Localize seu Desempenho e seu Resultado na Banca")
    st.write("Digite seu **Nome Completo** (ou parte dele) ou seu número de **Inscrição** para conferir seu boletim individual completo:")
    
    col_search, col_action = st.columns([3, 1])
    with col_search:
        termo_busca = st.text_input(
            "Buscar por Nome ou Inscrição",
            placeholder="Digite seu nome completo ou número de inscrição...",
            label_visibility="collapsed",
            key="termo_busca_input"
        )
    with col_action:
        if termo_busca.strip():
            st.button("✖️ Limpar Busca", width="stretch", on_click=limpar_termo_busca)
        else:
            st.caption("💡 Busca flexível (ignora maiúsculas e acentos)")
    
    candidato_selecionado = None
    
    if termo_busca.strip():
        termo_norm = normalizar_texto(termo_busca)
        # Otimização O(1): verificação instantânea por número de inscrição
        if termo_norm in mapa_inscricoes:
            candidato_selecionado = df_base.iloc[mapa_inscricoes[termo_norm]]
        else:
            if termo_norm.isdigit():
                mascara = df_base['Inscrição_Str'].str.startswith(termo_norm)
            else:
                mascara = df_base['Nome_Busca'].str.contains(termo_norm, regex=False, na=False)
            resultados_busca = df_base[mascara]
            
            if len(resultados_busca) == 0:
                st.warning("⚠️ Nenhum candidato encontrado com o termo informado. Verifique a grafia do nome ou tente buscar diretamente pelo número da inscrição.")
            elif len(resultados_busca) == 1:
                candidato_selecionado = resultados_busca.iloc[0]
            else:
                st.info(f"🔎 Encontrados **{len(resultados_busca)}** candidatos com esse termo. Selecione o seu abaixo:")
                opcoes = [
                    f"{row['Posição_Geral']}º Geral - {row['Nome']} (Inscrição: {row['Inscrição']} | {row['Modalidade_Concorrencia']} | Nota: {row['Nota Objetiva']} pts)"
                    for _, row in resultados_busca.head(50).iterrows()
                ]
                escolha = st.selectbox("Selecione o candidato correspondente:", opcoes)
                idx_geral = int(escolha.split("º")[0]) - 1
                candidato_selecionado = df_base.iloc[idx_geral]
    else:
        # Estado Inicial: Nenhuma busca realizada ainda
        st.markdown("""
        <div class="card border shadow-sm p-4 text-center my-3 rounded-3" style="background: #ffffff;">
            <div class="my-2">
                <i class="bi bi-person-badge text-primary" style="font-size: 3.2rem;"></i>
            </div>
            <h3 class="fw-bold text-dark mb-2">Consulte seu Boletim Individual com os Resultados Oficiais (23/10)</h3>
            <p class="text-secondary mx-auto mb-4" style="max-width: 640px; font-size: 0.95rem; line-height: 1.6;">
                Digite seu <strong>Nome Completo</strong> ou número de <strong>Inscrição</strong> no campo de busca acima para carregar instantaneamente o seu boletim completo com nota objetiva, parecer da banca e projeções.
            </p>
            <div class="row g-3 text-start mx-auto" style="max-width: 820px;">
                <div class="col-md-4">
                    <div class="card bg-light border p-3 h-100 rounded-3">
                        <div class="fw-bold text-dark mb-1"><i class="bi bi-shield-check text-success me-1"></i> Bancas de Cotas</div>
                        <div class="text-secondary" style="font-size: 0.85rem; line-height: 1.45;">Parecer preliminar da Heteroidentificação e Perícia PCD publicado em 23/10.</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card bg-light border p-3 h-100 rounded-3">
                        <div class="fw-bold text-dark mb-1"><i class="bi bi-list-ol text-primary me-1"></i> Reclassificação Real</div>
                        <div class="text-secondary" style="font-size: 0.85rem; line-height: 1.45;">Avanço na fila após a saída provisória de 3.231 candidatos indeferidos.</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card bg-light border p-3 h-100 rounded-3">
                        <div class="fw-bold text-dark mb-1"><i class="bi bi-graph-up-arrow text-primary me-1"></i> Projeções TAF</div>
                        <div class="text-secondary" style="font-size: 0.85rem; line-height: 1.45;">Situação calculada frente ao corte do TAF e vagas imediatas pós-recursos.</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("💡 **Deseja testar a consulta com um exemplo?** Selecione abaixo:")
        ex1, ex2, ex3 = st.columns(3)
        with ex1:
            st.button("🥇 Exemplo: 1º Lugar Geral (Ampla)", width="stretch", on_click=definir_termo_busca, args=("2320012112",))
        with ex2:
            st.button("🧑🏿 Exemplo: Cota Étnica Deferida", width="stretch", on_click=definir_termo_busca, args=("2320016842",))
        with ex3:
            st.button("♿ Exemplo: Cota PCD Deferida", width="stretch", on_click=definir_termo_busca, args=("2320029040",))

    # Exibição do Perfil do Candidato
    if candidato_selecionado is not None:
        pos_geral = int(candidato_selecionado['Posição_Geral'])
        nome = candidato_selecionado['Nome']
        inscricao = candidato_selecionado['Inscrição']
        nota_total = int(candidato_selecionado['Nota Objetiva'])
        aproveitamento_total = (nota_total / NOTA_MAXIMA_PROVA) * 100
        percentil = ((TOTAL_CANDIDATOS - pos_geral + 1) / TOTAL_CANDIDATOS) * 100
        top_pct = 100 - percentil
        top_pct_fmt = f"{top_pct:.2f}%"
        
        modalidade = candidato_selecionado['Modalidade_Concorrencia']
        is_pcd = bool(candidato_selecionado['Cota_PCD'])
        is_etnico = bool(candidato_selecionado['Cota_Etnico_Racial'])
        is_ampla_pura = bool(candidato_selecionado['Ampla_Pura'])
        
        res_hetero = str(candidato_selecionado.get('Resultado_Hetero', 'Não se Aplica'))
        res_pcd = str(candidato_selecionado.get('Resultado_PCD', 'Não se Aplica'))
        
        # Tags de cotas
        tags_html = ""
        if is_ampla_pura:
            tags_html += '<span class="tag-cota tag-ampla">🏛️ Não Cotista (Ampla Concorrência)</span>'
        if candidato_selecionado['Cota_Negro_Pardo']:
            tags_html += '<span class="tag-cota tag-negro">🧑🏿 Cota Preto / Pardo</span>'
        if candidato_selecionado['Cota_Indigena']:
            tags_html += '<span class="tag-cota tag-indigena">🏹 Cota Indígena</span>'
        if candidato_selecionado['Cota_Quilombola']:
            tags_html += '<span class="tag-cota tag-quilombola">🏺 Cota Quilombola</span>'
        if is_pcd:
            tags_html += '<span class="tag-cota tag-pcd">♿ Cota PCD</span>'
            
        pos_class = "pos-top" if pos_geral <= 140 else "pos-standard"
        medalha = "🥇 " if pos_geral == 1 else ("🥈 " if pos_geral == 2 else ("🥉 " if pos_geral == 3 else "🎖️ "))
        
        # Montagem dos Cards de Resultado das Bancas de 23 de Outubro
        bloco_bancas_html = ""
        
        if is_etnico:
            if res_hetero == 'DEFERIDO':
                nova_pos_etn = int(candidato_selecionado['Nova_Pos_Lista_Etnico'])
                pos_orig_etn = int(candidato_selecionado['Pos_Lista_Etnico'])
                ganho_etn = int(candidato_selecionado['Ganho_Pos_Etnico'])
                bloco_bancas_html += f"""<div class="card-resultado-deferido">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
    <div style="font-size: 0.82rem; font-weight: 800; color: #15803D; text-transform: uppercase; letter-spacing: 0.04em;">
        ✅ RESULTADO PRELIMINAR DA HETEROIDENTIFICAÇÃO / ANÁLISE DOCUMENTAL (23/10/2026)
    </div>
    <span class="badge-pill">DEFERIDO</span>
</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 6px 0;">
    Sua condição na Cota Étnico-Racial foi CONFIRMADA pela comissão examinadora!
</div>
<div style="font-size: 0.9rem; color: #1E293B; line-height: 1.5; font-weight: 500;">
    Com a homologação preliminar e os 3.045 indeferimentos de concorrentes, sua classificação na cota avançou expressivamente:<br>
    • <strong>Posição Preliminar Pós-Banca:</strong> <span style="color: #6D28D9; font-weight: 800; font-size: 1.05rem;">{nova_pos_etn}º Lugar na Cota</span> (Posição original: {pos_orig_etn}º)<br>
    • <strong>Avanço na Fila:</strong> <span style="color: #15803D; font-weight: 800;">+{ganho_etn} posições conquistadas!</span>
</div>
</div>"""
            else:
                bloco_bancas_html += f"""<div class="card-resultado-indeferido">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
    <div style="font-size: 0.82rem; font-weight: 800; color: #B45309; text-transform: uppercase; letter-spacing: 0.04em;">
        ⚠️ RESULTADO PRELIMINAR DA HETEROIDENTIFICAÇÃO / ANÁLISE DOCUMENTAL (23/10/2026)
    </div>
    <span class="badge-pill-amber">INDEFERIDO NA COTA</span>
</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 6px 0;">
    Solicitação de Cota Étnico-Racial Indeferida Preliminarmente
</div>
<div style="font-size: 0.9rem; color: #1E293B; line-height: 1.55; font-weight: 500;">
    ⚖️ <strong>Regra do Edital (Art. 4º do Edital de Convocação):</strong> O indeferimento preliminar da autodeclaração <strong>NÃO ELIMINA você do concurso</strong>! Você continua concorrendo normalmente pelas vagas da <strong>Ampla Concorrência</strong>.<br>
    Sua classificação geral na Ampla: <strong>{pos_geral}º Lugar Geral ({nota_total} pontos)</strong>.
</div>
<div class="recurso-alert-box">
    📝 <strong>DIREITO A RECURSO ADMINISTRATIVO:</strong><br>
    • <strong>Prazo oficial:</strong> Da 0h00 de <strong>26/10/2026</strong> até às 23h59 de <strong>27/10/2026</strong> (horário de Brasília).<br>
    • <strong>Onde protocolar:</strong> No site oficial da banca: <a href="https://www.avalia.org.br" target="_blank" style="color: #1D4ED8; font-weight: 700; text-decoration: underline;">avalia.org.br</a>.<br>
    • <strong>Motivo da recusa:</strong> Acesse o link <em>"Boletim de Análise de Reserva de Vagas"</em> em avalia.org.br para consultar a justificativa e fundamentar seu recurso.
</div>
</div>"""

        if is_pcd:
            if res_pcd == 'DEFERIDO':
                nova_pos_pcd = int(candidato_selecionado['Nova_Pos_Lista_PCD'])
                pos_orig_pcd = int(candidato_selecionado['Pos_Lista_PCD'])
                ganho_pcd = int(candidato_selecionado['Ganho_Pos_PCD'])
                bloco_bancas_html += f"""<div class="card-resultado-deferido">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
    <div style="font-size: 0.82rem; font-weight: 800; color: #15803D; text-transform: uppercase; letter-spacing: 0.04em;">
        ✅ RESULTADO PRELIMINAR DA PERÍCIA MÉDICA PCD (23/10/2026)
    </div>
    <span class="badge-pill">LAUDO HOMOLOGADO</span>
</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 6px 0;">
    Laudo Médico e Condição de Pessoa com Deficiência (PCD) DEFERIDOS!
</div>
<div style="font-size: 0.9rem; color: #1E293B; line-height: 1.5; font-weight: 500;">
    A perícia médica multidisciplinar homologou sua documentação com sucesso:<br>
    • <strong>Posição Preliminar Pós-Perícia:</strong> <span style="color: #15803D; font-weight: 800; font-size: 1.05rem;">{nova_pos_pcd}º Lugar PCD</span> (Posição original: {pos_orig_pcd}º)<br>
    • <strong>Avanço na Fila PCD:</strong> <span style="color: #15803D; font-weight: 800;">+{ganho_pcd} posições conquistadas!</span>
</div>
</div>"""
            else:
                bloco_bancas_html += f"""<div class="card-resultado-indeferido">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
    <div style="font-size: 0.82rem; font-weight: 800; color: #B45309; text-transform: uppercase; letter-spacing: 0.04em;">
        ⚠️ RESULTADO PRELIMINAR DA PERÍCIA MÉDICA PCD (23/10/2026)
    </div>
    <span class="badge-pill-amber">LAUDO INDEFERIDO NA PERÍCIA</span>
</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 6px 0;">
    Solicitação de Cota PCD Indeferida Preliminarmente
</div>
<div style="font-size: 0.9rem; color: #1E293B; line-height: 1.55; font-weight: 500;">
    ⚖️ <strong>Regra do Edital (Art. 3º do Edital de Perícia Médica PCD):</strong> O não acolhimento do laudo na perícia médica <strong>NÃO ELIMINA você do concurso</strong>! Você continua concorrendo pelas vagas da <strong>Ampla Concorrência</strong>.<br>
    Sua classificação geral na Ampla: <strong>{pos_geral}º Lugar Geral ({nota_total} pontos)</strong>.
</div>
<div class="recurso-alert-box">
    📝 <strong>DIREITO A RECURSO CONTRA A PERÍCIA MÉDICA:</strong><br>
    • <strong>Período recursal:</strong> Da 0h00 de <strong>26/10/2026</strong> até às 23h59 de <strong>27/10/2026</strong> (horário de Brasília).<br>
    • <strong>Como consultar o laudo/motivo:</strong> Acesse o <em>"Boletim de Análise de Reserva de Vagas"</em> em <a href="https://www.avalia.org.br" target="_blank" style="color: #1D4ED8; font-weight: 700; text-decoration: underline;">avalia.org.br</a>.
</div>
</div>"""

        if is_ampla_pura:
            bloco_bancas_html += """<div class="card-resultado-ampla">
<div style="font-size: 0.82rem; font-weight: 800; color: #0369A1; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.04em;">
    🏛️ CANDIDATO NÃO COTISTA (AMPLA CONCORRÊNCIA PURA)
</div>
<div style="font-size: 1.05rem; font-weight: 800; color: #0F172A;">
    ⚪ As bancas de cotas e resultados de 23 de outubro não se aplicam a você
</div>
<div style="font-size: 0.88rem; color: #334155; margin-top: 6px; line-height: 1.5; font-weight: 500;">
    Como candidato exclusivo de Ampla Concorrência, sua pontuação concorre diretamente no cômputo universal de vagas e sua próxima etapa avaliativa do cronograma é a convocação para o TAF (conforme linha de corte).
</div>
</div>"""

        # Previsão Oficial do TAF pós-bancas
        status_taf_prel = str(candidato_selecionado.get('Previsao_TAF_Preliminar', ''))
        is_convocado_taf = bool(candidato_selecionado.get('Convocado_TAF_Preliminar', False))
        taf_class = "card-previsao-ok" if is_convocado_taf else "card-previsao"
        taf_badge_color = "#15803D" if is_convocado_taf else "#475569"
        taf_badge_text = "🟢 SITUAÇÃO TAF: DENTRO DO LIMITE DE CONVOCAÇÃO!" if is_convocado_taf else "⚪ SITUAÇÃO TAF: FORA DO CORTE PRELIMINAR"
        
        taf_html = f"""<div class="{taf_class}">
<div style="font-size: 0.82rem; font-weight: 800; color: {taf_badge_color}; text-transform: uppercase; margin-bottom: 6px;">
    🎯 {taf_badge_text}
</div>
<div style="font-size: 1.05rem; font-weight: 800; color: #0F172A; margin-bottom: 4px;">
    {status_taf_prel}
</div>
<div style="font-size: 0.88rem; color: #475569; font-weight: 600;">
    🏆 Situação de Vagas: <strong>{candidato_selecionado['Previsao_Vagas_Preliminar']}</strong>
</div>
</div>"""

        card_html = f"""<div class="candidate-card">
<div class="d-flex justify-content-between align-items-start flex-wrap gap-3">
<div>
<span class="badge-pill"><i class="bi bi-patch-check-fill text-success me-1"></i> BOLETIM ATUALIZADO • 23 DE OUTUBRO DE 2026</span>
<h2 class="hero-title mt-1 mb-2" style="font-size: 1.85rem;">{nome}</h2>
<p class="text-secondary mb-2" style="font-size: 0.95rem; font-weight: 500;">
<i class="bi bi-person-vcard text-primary me-1"></i> Inscrição: <strong class="text-dark">{inscricao}</strong> &nbsp;•&nbsp; <i class="bi bi-shield-lock text-primary me-1"></i> Cargo: <strong class="text-dark">401 - Policial Penal RN</strong>
</p>
<div class="mt-2">{tags_html}</div>
</div>
<div class="candidate-header-badge">
<div class="pos-badge {pos_class}">
{medalha}{pos_geral}º LUGAR GERAL
</div>
<div class="fw-bold text-primary mt-1" style="font-size: 0.85rem;">
<i class="bi bi-graph-up-arrow me-1"></i> Top {top_pct_fmt} de todos os {TOTAL_CANDIDATOS_FMT} candidatos
</div>
</div>
</div>
{bloco_bancas_html}
{taf_html}
</div>"""

        st.markdown(card_html, unsafe_allow_html=True)
        
        # 4 Indicadores Principais de Classificação
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-list-ol text-primary me-1"></i> Classificação Geral Oficial</div>
<div class="stat-value">{pos_geral}º</div>
<div class="stat-sub text-primary fw-bold">↑ De {TOTAL_CANDIDATOS_FMT} candidatos</div>
</div>""", unsafe_allow_html=True)
        with c2:
            if is_pcd and res_pcd == 'DEFERIDO' and is_etnico and res_hetero == 'DEFERIDO':
                if nota_total < 113:
                    lbl_cota = "<i class='bi bi-universal-access text-success me-1'></i> Posição Preliminar PCD (Convocado)"
                    val_cota = f"{int(candidato_selecionado['Nova_Pos_Lista_PCD'])}º"
                    sub_cota = f"♿ {int(candidato_selecionado['Nova_Pos_Lista_PCD'])}º PCD • 🧑🏿 {int(candidato_selecionado['Nova_Pos_Lista_Etnico'])}º na Cota Étnica"
                else:
                    lbl_cota = "<i class='bi bi-person-fill-check me-1' style='color: #6f42c1;'></i> Posição Preliminar nas Cotas"
                    val_cota = f"{int(candidato_selecionado['Nova_Pos_Lista_Etnico'])}º"
                    sub_cota = f"🧑🏿 {int(candidato_selecionado['Nova_Pos_Lista_Etnico'])}º Étnico • ♿ {int(candidato_selecionado['Nova_Pos_Lista_PCD'])}º PCD"
            elif is_pcd and res_pcd == 'DEFERIDO' and pd.notnull(candidato_selecionado['Nova_Pos_Lista_PCD']):
                lbl_cota = "<i class='bi bi-universal-access text-success me-1'></i> Posição Preliminar PCD"
                val_cota = f"{int(candidato_selecionado['Nova_Pos_Lista_PCD'])}º"
                sub_cota = f"↑ De {TOTAL_PCD_APTOS} PCDs deferidos"
            elif is_etnico and res_hetero == 'DEFERIDO' and pd.notnull(candidato_selecionado['Nova_Pos_Lista_Etnico']):
                lbl_cota = "<i class='bi bi-person-fill-check me-1' style='color: #6f42c1;'></i> Posição Preliminar na Cota"
                val_cota = f"{int(candidato_selecionado['Nova_Pos_Lista_Etnico'])}º"
                sub_cota = f"↑ De {TOTAL_ETNICO_APTOS:,} cotistas deferidos"
            elif is_etnico or is_pcd:
                lbl_cota = "<i class='bi bi-exclamation-circle-fill text-warning me-1'></i> Cota Indeferida (Concorre Ampla)"
                val_cota = f"{pos_geral}º"
                sub_cota = "Disputa universal na Ampla"
            else:
                lbl_cota = "<i class='bi bi-award-fill text-primary me-1'></i> Posição Não Cotista"
                val_cota = f"{int(candidato_selecionado['Pos_Lista_Ampla_Pura'])}º"
                sub_cota = f"↑ De {TOTAL_AMPLA_FMT} da Ampla Pura"
            st.markdown(f"""<div class="stat-card">
<div class="stat-label">{lbl_cota}</div>
<div class="stat-value">{val_cota}</div>
<div class="stat-sub text-primary fw-bold">{sub_cota}</div>
</div>""".replace(",", "."), unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-clipboard2-check text-success me-1"></i> Nota Objetiva</div>
<div class="stat-value">{nota_total} pts</div>
<div class="stat-sub text-success fw-bold">↑ {aproveitamento_total:.1f}% de aproveitamento (Máx {NOTA_MAXIMA_PROVA})</div>
</div>""", unsafe_allow_html=True)
        with c4:
            vaga_prel = str(candidato_selecionado['Previsao_Vagas_Preliminar'])
            if "Vaga Imediata" in vaga_prel:
                val_vagas = "Vagas Imediatas 🏆"
                color_vagas = "#198754"
            else:
                val_vagas = "Cadastro Reserva 📋"
                color_vagas = "#212529"
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-trophy text-warning me-1"></i> Situação de Vagas Preliminar</div>
<div class="stat-value" style="color: {color_vagas}; font-size: 1.35rem;">{val_vagas}</div>
<div class="stat-sub text-secondary fw-bold">{vaga_prel}</div>
</div>""", unsafe_allow_html=True)
                
        st.write("")
        
        # Projeção Preditiva pós-recursos e TAF (100% pré-computada em 0ms)
        with st.expander("🔮 Sua Projeção Preditiva pós-Recursos e TAF (Simulador)", expanded=True):
            st.caption("Cenário de projeção considerando **5% de recursos deferidos** em 26-27/10 e **20% de reprovação no TAF** (médias históricas de carreiras policiais):")
            
            col_sim1, col_sim2, col_sim3 = st.columns(3)
            with col_sim1:
                pos_etn_sim = candidato_selecionado.get('Pos_Etnico_Sim_Padrao')
                pos_pcd_sim = candidato_selecionado.get('Pos_PCD_Sim_Padrao')
                if is_pcd and res_pcd == 'DEFERIDO' and is_etnico and res_hetero == 'DEFERIDO':
                    if nota_total < 113:
                        lbl_sim = "<i class='bi bi-universal-access text-success me-1'></i> Posição Estimada PCD (Convocado)"
                        val_sim = f"{int(pos_pcd_sim)}º" if pd.notnull(pos_pcd_sim) else "-"
                        sub_sim = f"PCD: {val_sim} • Étnico: {int(pos_etn_sim)}º" if pd.notnull(pos_etn_sim) else ""
                        color_sim = "#198754"
                    else:
                        lbl_sim = "<i class='bi bi-person-fill-check me-1' style='color: #6f42c1;'></i> Posição Estimada na Cota Étnica"
                        val_sim = f"{int(pos_etn_sim)}º" if pd.notnull(pos_etn_sim) else "-"
                        sub_sim = f"Étnico: {val_sim} • PCD: {int(pos_pcd_sim)}º" if pd.notnull(pos_pcd_sim) else ""
                        color_sim = "#6f42c1"
                    st.markdown(f"""<div class="stat-card">
<div class="stat-label">{lbl_sim}</div>
<div class="stat-value" style="color: {color_sim};">{val_sim}</div>
<div class="stat-sub text-success fw-bold">{sub_sim}</div>
</div>""", unsafe_allow_html=True)
                elif is_pcd and res_pcd == 'DEFERIDO' and pd.notnull(pos_pcd_sim):
                    st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-universal-access text-success me-1"></i> Posição Estimada PCD</div>
<div class="stat-value text-success">{int(pos_pcd_sim)}º</div>
<div class="stat-sub text-success fw-bold">Classificação pós-perícia definitiva</div>
</div>""", unsafe_allow_html=True)
                elif is_etnico and res_hetero == 'DEFERIDO' and pd.notnull(pos_etn_sim):
                    st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-person-fill-check me-1" style="color: #6f42c1;"></i> Posição Estimada na Cota Étnica</div>
<div class="stat-value" style="color: #6f42c1;">{int(pos_etn_sim)}º</div>
<div class="stat-sub text-success fw-bold">Classificação pós-recursos estimada</div>
</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-award-fill text-primary me-1"></i> Situação na Ampla Concorrência</div>
<div class="stat-value text-primary">{pos_geral}º</div>
<div class="stat-sub text-secondary fw-bold">Disputa geral na Ampla Universal</div>
</div>""", unsafe_allow_html=True)
            
            with col_sim2:
                is_convocado_taf_sim = bool(candidato_selecionado.get('Convocado_TAF_Sim_Padrao', False))
                status_taf_text = "🟢 Convocado para o TAF!" if is_convocado_taf_sim else "⚪ Fora do corte do TAF"
                color_taf_text = "#198754" if is_convocado_taf_sim else "#6c757d"
                sub_taf_text = "Dentro da linha de corte estimada" if is_convocado_taf_sim else "Abaixo da pontuação de corte"
                st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-flag-fill me-1" style="color: {color_taf_text};"></i> Convocação para o TAF</div>
<div class="stat-value" style="color: {color_taf_text}; font-size: 1.25rem;">{status_taf_text}</div>
<div class="stat-sub text-secondary fw-bold">{sub_taf_text}</div>
</div>""", unsafe_allow_html=True)
            
            with col_sim3:
                vaga_sim = str(candidato_selecionado.get('Vaga_Imediata_Sim_Padrao', '📋 Cadastro de Reserva'))
                is_vaga_imediata = "Vaga Imediata" in vaga_sim
                if is_vaga_imediata:
                    val_vaga_text = "Vaga Imediata 🏆"
                    sub_vaga_text = "↑ Entra nas 200 vagas imediatas pós-TAF!"
                    color_vaga_text = "#198754"
                else:
                    val_vaga_text = "Cadastro Reserva 📋"
                    sub_vaga_text = "Dentro do Cadastro de Reserva"
                    color_vaga_text = "#212529"
                st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-award me-1" style="color: {color_vaga_text};"></i> Projeção Pós-TAF</div>
<div class="stat-value" style="color: {color_vaga_text}; font-size: 1.25rem;">{val_vaga_text}</div>
<div class="stat-sub text-secondary fw-bold">{sub_vaga_text}</div>
</div>""", unsafe_allow_html=True)
                
                st.info("💡 **Deseja personalizar taxas de recurso e atrito do TAF?** Acesse a aba **'🔮 Simulador de Colocações & Impacto das Bancas'** no menu superior!")

        st.write("")
        
        # Detalhamento de Disciplinas
        st.markdown("#### 📋 Detalhamento do seu Aproveitamento por Disciplina")
        dados_detalhamento = []
        for d in DISCIPLINAS:
            nota_cand = int(candidato_selecionado[d])
            max_p = PONTOS_MAXIMOS[d]
            aprov = (nota_cand / max_p) * 100
            media_disc = MEDIAS_DISCIPLINAS.get(d, 10.0)
            diff_media = nota_cand - media_disc
            dados_detalhamento.append({
                "Disciplina": d,
                "Sua Nota": f"{nota_cand} / {max_p} pts",
                "Aproveitamento": f"{aprov:.1f}%",
                "Média Geral da Prova": f"{media_disc:.2f} pts",
                "Comparativo com a Média": f"{diff_media:+.2f} pts" + (" 🟢 Acima" if diff_media > 0 else " 🔴 Abaixo")
            })
        st.dataframe(pd.DataFrame(dados_detalhamento), width="stretch", hide_index=True)
        
        # Gráfico de barras horizontal
        pct_candidato = [(candidato_selecionado[d] / PONTOS_MAXIMOS[d]) * 100 for d in DISCIPLINAS]
        nomes_curtos = [
            d.replace("História do RN e Aspectos Geoeconômicos do RN", "História RN")
             .replace("Ética no Serviço Público", "Ética")
             .replace("Direito Penal e Processo Penal", "Penal / Processo")
             .replace("Legislação Específica", "Leg. Específica")
            for d in DISCIPLINAS
        ]
        cores = ['#198754' if p >= 80 else ('#ffc107' if p >= 60 else '#dc3545') for p in pct_candidato]

        fig_bar = go.Figure(go.Bar(
            x=pct_candidato,
            y=nomes_curtos,
            orientation='h',
            marker_color=cores,
            text=[f"{p:.1f}% ({candidato_selecionado[d]}/{PONTOS_MAXIMOS[d]} pts)" for p, d in zip(pct_candidato, DISCIPLINAS)],
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(color='white', size=11, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif', weight=700)
        ))
        fig_bar.update_layout(
            title=dict(text="Aproveitamento Percentual por Disciplina", font=dict(color='#212529', size=14, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif')),
            xaxis=dict(range=[0, 105], title="Aproveitamento (%)", gridcolor='#dee2e6', tickfont=dict(color='#6c757d')),
            yaxis=dict(autorange="reversed", tickfont=dict(color='#212529')),
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=20, t=40, b=30),
            height=340
        )
        st.plotly_chart(fig_bar, width="stretch")

        # Vizinhos de Classificação
        with st.expander("👥 Candidatos Próximos na Classificação Geral (+/- 5 concorrentes ao redor)"):
            st.caption("Veja os candidatos imediatamente antes e depois da sua posição e o status de cada um nas bancas preliminares:")
            start_idx = max(0, pos_geral - 6)
            end_idx = min(TOTAL_CANDIDATOS, pos_geral + 5)
            vizinhos = df_base.iloc[start_idx:end_idx][['Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Status_Cota_Preliminar', 'Nota Objetiva', 'Execução Penal', 'Legislação Específica', 'Previsao_TAF_Preliminar']]
            
            def destacar_linha(row):
                if row['Posição_Geral'] == pos_geral:
                    return ['background-color: #E0F2FE; font-weight: bold; color: #0369A1;'] * len(row)
                return [''] * len(row)
                
            st.dataframe(
                vizinhos.style.apply(destacar_linha, axis=1),
                width="stretch",
                hide_index=True
            )

        # Confronto Direto
        with st.expander("⚔️ Comparar Meu Resultado com Outro Candidato"):
            st.caption("Compare seu boletim de notas matéria por matéria com qualquer concorrente da lista:")
            col_comp_busca, col_comp_sel = st.columns([1, 1])
            with col_comp_busca:
                termo_outro = st.text_input("Buscar Concorrente (Nome ou Inscrição):", placeholder="Digite o nome do concorrente...", key="busca_outro")
            
            if termo_outro.strip():
                norm_outro = normalizar_texto(termo_outro)
                if norm_outro in mapa_inscricoes:
                    filtro_outro = df_base.iloc[[mapa_inscricoes[norm_outro]]]
                elif norm_outro.isdigit():
                    filtro_outro = df_base[df_base['Inscrição_Str'].str.startswith(norm_outro)]
                else:
                    filtro_outro = df_base[df_base['Nome_Busca'].str.contains(norm_outro, regex=False, na=False)]
                if len(filtro_outro) > 0:
                    opcoes_outro = [
                        f"{row['Posição_Geral']}º - {row['Nome']} (Nota: {row['Nota Objetiva']} pts | {row['Status_Cota_Preliminar']})"
                        for _, row in filtro_outro.head(25).iterrows()
                    ]
                    with col_comp_sel:
                        escolha_outro = st.selectbox("Selecione o concorrente:", opcoes_outro, key="sel_outro")
                    pos_outro = int(escolha_outro.split("º")[0]) - 1
                    outro_dados = df_base.iloc[pos_outro]
                    
                    diff_total = nota_total - int(outro_dados['Nota Objetiva'])
                    if diff_total > 0:
                        st.success(f"🏆 Você está à frente por **+{diff_total} pontos** ({nota_total} vs {outro_dados['Nota Objetiva']} pts).")
                    elif diff_total < 0:
                        st.warning(f"O concorrente está à frente por **+{abs(diff_total)} pontos** ({outro_dados['Nota Objetiva']} vs {nota_total} pts).")
                    else:
                        st.info(f"🤝 **Empate em {nota_total} pontos!** Desempate do edital: {nome} ({pos_geral}º) vs {outro_dados['Nome']} ({outro_dados['Posição_Geral']}º).")
                        
                    confronto_rows = []
                    for d in DISCIPLINAS:
                        n1 = int(candidato_selecionado[d])
                        n2 = int(outro_dados[d])
                        if n1 > n2:
                            vantagem = f"🟢 +{n1 - n2} pts (Você)"
                        elif n2 > n1:
                            vantagem = f"🔵 +{n2 - n1} pts ({outro_dados['Nome'].split()[0]})"
                        else:
                            vantagem = "⚪ Empate"
                        confronto_rows.append({
                            "Disciplina": d,
                            "Sua Nota": f"{n1} pts",
                            f"{outro_dados['Nome']}": f"{n2} pts",
                            "Vantagem": vantagem
                        })
                    st.dataframe(pd.DataFrame(confronto_rows), width="stretch", hide_index=True)
                else:
                    st.warning("Nenhum candidato encontrado com esse nome.")
            else:
                st.caption("Digite o nome ou número de inscrição no campo acima para iniciar o confronto.")

        with st.expander("❓ Critérios Oficiais de Desempate do Edital (Item 21.2.1)"):
            st.markdown("""
            Conforme o **Item 21.2.1 do Edital**, em caso de igualdade de pontos na nota final da prova objetiva, o desempate oficial seguiu rigorosamente a ordem:
            1. **Idade igual ou superior a 60 anos** (Estatuto da Pessoa Idosa);
            2. **Maior pontuação na disciplina de Execução Penal** (peso de 30 pts);
            3. **Maior pontuação em Legislação Específica** (peso de 40 pts);
            4. **Maior pontuação em Direito Penal e Processo Penal** (peso de 20 pts);
            5. **Maior pontuação em Língua Portuguesa** (peso de 15 pts);
            6. **Maior pontuação em História do RN**;
            7. **Maior idade cronológica geral**.
            """)

# ==============================================================================
# ABA 2: SIMULADOR DE COLOCAÇÕES & IMPACTO DAS BANCAS
# ==============================================================================
with tab_simuladores:
    st.markdown("""<div class="sim-banner">
<span class="sim-badge"><i class="bi bi-sliders me-1"></i> SIMULADOR PREDITIVO PÓS-BANCAS DE COTAS & TAF</span>
<h2 class="hero-title mt-1 mb-2" style="font-size: 1.75rem;"><i class="bi bi-diagram-3-fill text-purple me-2"></i>Simulador de Colocações com Dados Reais das Bancas</h2>
<p class="text-secondary mb-0" style="font-size: 0.95rem; line-height: 1.55;">
Projete o impacto dos <strong>3.045 indeferimentos da Heteroidentificação</strong> e <strong>186 indeferimentos PCD</strong> publicados em 23 de outubro, a taxa de sucesso nos <strong>recursos (26 e 27/10)</strong> e a taxa de <strong>reprovação do TAF</strong> na conquista de vagas imediatas.
</p>
</div>""", unsafe_allow_html=True)

    st.markdown("""<div class="sim-notice-card">
<i class="bi bi-info-circle-fill text-primary me-1"></i> <strong>Como os dados foram configurados:</strong><br>
Por padrão, este simulador utiliza os <strong>resultados oficiais preliminares das bancas publicados hoje (23/10)</strong>. Você pode simular quantos indeferidos devem conseguir reverter a decisão na fase recursal de 26-27 de outubro e qual será o atrito do TAF!
</div>""", unsafe_allow_html=True)

    st.markdown("#### ⚙️ Parâmetros de Simulação")
    col_ctrl1, col_ctrl2 = st.columns(2)
    
    with col_ctrl1:
        st.markdown("**📝 Fase de Recursos (26 e 27 de Outubro)**")
        taxa_rev_etn = st.slider(
            "Taxa Estimada de Reversão de Recursos na Heteroidentificação Étnica:",
            min_value=0, max_value=25, value=5, step=1, format="%d%%",
            help="Porcentagem dos 3.045 candidatos indeferidos na hetero que devem ter o recurso aceito pela comissão recursal. Média típica em bancas: 3% a 8%."
        )
        taxa_rev_pcd = st.slider(
            "Taxa Estimada de Reversão de Recursos na Perícia Médica PCD:",
            min_value=0, max_value=25, value=5, step=1, format="%d%%",
            help="Porcentagem dos 186 candidatos PCDs indeferidos que devem reverter no recurso."
        )
        
    with col_ctrl2:
        st.markdown("**🏃‍♂️ Teste de Aptidão Física (TAF - Novembro/Dezembro)**")
        taxa_taf = st.slider(
            "Taxa Estimada de Reprovação / Abstenção no TAF:",
            min_value=0, max_value=45, value=20, step=1, format="%d%%",
            help="Porcentagem de convocados para o TAF que reprovam nos testes físicos (barra, corrida, abdominal) ou não comparecem. Média em carreiras policiais: 18% a 28%."
        )
        st.markdown(f"""
        <div class="card bg-light border p-3 rounded-3 mt-2" style="font-size: 0.85rem; line-height: 1.45;">
        <div class="fw-bold text-dark mb-1"><i class="bi bi-pin-angle-fill text-primary me-1"></i> Parâmetros Atuais:</div>
        • Reversão Cota Étnica: <strong>{taxa_rev_etn}%</strong> (~{int(3045 * taxa_rev_etn / 100)} recursos deferidos)<br>
        • Reversão Perícia PCD: <strong>{taxa_rev_pcd}%</strong> (~{int(186 * taxa_rev_pcd / 100)} recursos deferidos)<br>
        • Reprovação no TAF: <strong>{taxa_taf}%</strong> de atrito nos testes físicos<br>
        • Base: <strong>Resultados Oficiais das Bancas de 23 de Outubro</strong>
        </div>
        """, unsafe_allow_html=True)

    df_simulada, res_sim, novos_ampla, novos_etnico, novos_pcd = executar_simulacao_pos_bancas(
        modo="real_bancas",
        taxa_reversao_etnico_pct=taxa_rev_etn,
        taxa_reversao_pcd_pct=taxa_rev_pcd,
        taxa_taf_pct=taxa_taf
    )

    st.write("---")
    st.markdown("#### 📊 Impacto nas Vagas e Linhas de Corte")
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-people-fill text-primary me-1"></i> Alcance Vagas Ampla (140 vagas)</div>
<div class="stat-value text-primary">Até o {res_sim['ultimo_ampla_orig']}º</div>
<div class="stat-sub text-success fw-bold">↑ Original: 140º (+{res_sim['ganho_ampla']} posições pós-TAF!)</div>
</div>""", unsafe_allow_html=True)
        
    with sc2:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-person-fill-check me-1" style="color: #6f42c1;"></i> Alcance Vagas Cota Étnica (40 vagas)</div>
<div class="stat-value" style="color: #6f42c1;">Até o {res_sim['ultimo_etnico_orig']}º</div>
<div class="stat-sub text-success fw-bold">↑ Original: 40º (+{res_sim['ganho_etnico']} cotistas beneficiados!)</div>
</div>""", unsafe_allow_html=True)

    with sc3:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-universal-access text-success me-1"></i> Alcance Vagas PCD (20 vagas)</div>
<div class="stat-value text-success">Até o {res_sim['ultimo_pcd_orig']}º</div>
<div class="stat-sub text-success fw-bold">↑ Original: 20º (+{res_sim['ganho_pcd']} PCDs beneficiados!)</div>
</div>""", unsafe_allow_html=True)

    with sc4:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-arrow-down-circle-fill text-primary me-1"></i> Linha de Corte TAF (Cota Étnica)</div>
<div class="stat-value">{res_sim['corte_etnico_taf']} pts</div>
<div class="stat-sub text-primary fw-bold">↓ Caiu de 115 para {res_sim['corte_etnico_taf']} pts pós-banca!</div>
</div>""", unsafe_allow_html=True)

    st.write("")

    fig_comp = go.Figure()
    modalidades_k = ['Ampla Concorrência', 'Cota Étnico-Racial', 'Cota PCD']
    valores_orig = [140, 40, 20]
    valores_sim = [res_sim['ultimo_ampla_orig'], res_sim['ultimo_etnico_orig'], res_sim['ultimo_pcd_orig']]
    
    fig_comp.add_trace(go.Bar(
        name='Oficial (Sem atrito de banca/TAF)',
        x=modalidades_k,
        y=valores_orig,
        marker_color='#6c757d',
        text=[f"{v}º" for v in valores_orig],
        textposition='auto',
        textfont=dict(weight=700, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif')
    ))
    fig_comp.add_trace(go.Bar(
        name=f'Simulação pós-Bancas Reais, Recursos ({taxa_rev_etn}%) e TAF ({taxa_taf}%)',
        x=modalidades_k,
        y=valores_sim,
        marker_color=['#0d6efd', '#6f42c1', '#198754'],
        text=[f"{v}º (+{v-orig})" for v, orig in zip(valores_sim, valores_orig)],
        textposition='auto',
        textfont=dict(weight=700, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif')
    ))
    fig_comp.update_layout(
        title=dict(text="Alcance Máximo de Convocação para as Vagas Imediatas (Oficial vs Simulado)", font=dict(color='#212529', size=14, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif')),
        barmode='group',
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(title="Última Colocação Alcançada", gridcolor='#dee2e6'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif')),
        margin=dict(l=10, r=20, t=50, b=30),
        height=350
    )
    st.plotly_chart(fig_comp, width="stretch")

    # Detalhamento
    st.markdown("#### 📋 Detalhamento dos Candidatos no Cenário Simulado")
    tab_sub1, tab_sub2, tab_sub3, tab_sub4 = st.tabs([
        f"🏆 Entram nas Vagas da Geral ({len(novos_ampla)} beneficiados)",
        f"🧑🏿 Entram nas Vagas da Cota Étnica ({len(novos_etnico)} beneficiados)",
        f"♿ Entram nas Vagas PCD ({len(novos_pcd)} beneficiados)",
        "🔍 Consultar Candidato na Simulação"
    ])
    
    with tab_sub1:
        st.write(f"Candidatos que estavam no **Cadastro de Reserva da Geral** (> 140º) e agora alcançam uma das **140 Vagas Imediatas**:")
        if len(novos_ampla) > 0:
            cols_show_ampla = ['Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Nota Objetiva', 'Execução Penal', 'Legislação Específica']
            st.dataframe(novos_ampla[cols_show_ampla], width="stretch", hide_index=True)
        else:
            st.info("Nenhum candidato além do 140º com a configuração atual.")

    with tab_sub2:
        st.write(f"Cotistas étnicos que estavam no **Cadastro de Reserva da Cota** (> 40º) e agora alcançam uma das **40 Vagas Imediatas Reservadas**:")
        if len(novos_etnico) > 0:
            cols_show_etnico = ['Pos_Lista_Etnico', 'Posição_Geral', 'Nome', 'Inscrição', 'Nota Objetiva', 'Execução Penal', 'Legislação Específica']
            st.dataframe(novos_etnico[cols_show_etnico], width="stretch", hide_index=True)
        else:
            st.info("Nenhum cotista além do 40º com a configuração atual.")

    with tab_sub3:
        st.write(f"Candidatos PCD que estavam além da 20ª colocação e agora alcançam uma das **20 Vagas Imediatas PCD**:")
        if len(novos_pcd) > 0:
            cols_show_pcd = ['Pos_Lista_PCD', 'Posição_Geral', 'Nome', 'Inscrição', 'Nota Objetiva']
            st.dataframe(novos_pcd[cols_show_pcd], width="stretch", hide_index=True)
        else:
            st.info("Nenhum candidato PCD além do 20º com a configuração atual.")

    with tab_sub4:
        st.write("Verifique a projeção de qualquer concorrente:")
        col_bs1, col_bs2 = st.columns([2, 1])
        with col_bs1:
            nome_busca_sim = st.text_input("Buscar por Nome ou Inscrição na Lista Simulada:", placeholder="Digite o nome ou número de inscrição...", key="input_busca_sim")
        
        if nome_busca_sim.strip():
            norm_bs = normalizar_texto(nome_busca_sim)
            if norm_bs.isdigit():
                filtro_sim = df_simulada[df_simulada['Inscrição_Str'].str.startswith(norm_bs)]
            else:
                filtro_sim = df_simulada[df_simulada['Nome_Busca'].str.contains(norm_bs, regex=False, na=False)]
            if len(filtro_sim) == 0:
                st.warning("Nenhum candidato encontrado com esse termo.")
            else:
                c_cand_sim = filtro_sim.iloc[0]
                st.markdown(f"""
                <div class="candidate-card" style="margin-top: 10px;">
                <h3 style="margin: 0 0 6px 0; color: #0F172A;">{c_cand_sim['Nome']}</h3>
                <div style="font-size: 0.9rem; color: #475569; margin-bottom: 12px;">Inscrição: <strong>{c_cand_sim['Inscrição']}</strong> | Modalidade: <strong>{c_cand_sim['Modalidade_Concorrencia']}</strong> | Nota: <strong>{c_cand_sim['Nota Objetiva']} pts</strong></div>
                <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                    <span class="sim-gain-pill">Posição Geral: {c_cand_sim['Posição_Geral']}º</span>
                    <span class="sim-gain-pill">Status TAF Simulado: {c_cand_sim['Status_TAF_Sim']}</span>
                    <span class="sim-gain-pill">Vagas: {c_cand_sim['Vaga_Imediata_Sim']}</span>
                </div>
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# ABA 3: AS LISTAS OFICIAIS & RESULTADOS DAS BANCAS (DOWNLOADS)
# ==============================================================================
with tab_listas:
    st.subheader("📋 Listas Oficiais Definitivas e Resultados das Bancas de Cotas (23/10)")
    st.write("""
    Acesse, filtre e faça o download de cada lista em formato Excel (.xlsx), incluindo as relações preliminares publicadas em **23 de outubro de 2026**:
    """)
    
    tipo_lista = st.radio(
        "Selecione a Lista que deseja visualizar e baixar:",
        [
            f"🧑🏿 1. Resultado Preliminar Heteroidentificação & Análise Doc (6.309 candidatos - 3.264 Deferidos / 3.045 Indeferidos)",
            f"♿ 2. Resultado Preliminar Perícia Médica PCD (659 candidatos - 473 Deferidos / 186 Indeferidos)",
            f"📈 3. Nova Lista Reclassificada da Cota Étnica (3.264 cotistas confirmados)",
            f"📈 4. Nova Lista Reclassificada da Cota PCD (473 PCDs confirmados)",
            f"🌐 5. Lista Geral Completa com Situação das Bancas (18.945 candidatos)",
            f"🏛️ 6. Lista Exclusiva de Não Cotistas (Ampla Concorrência Pura - {TOTAL_AMPLA_FMT} candidatos)"
        ],
        index=0
    )
    
    st.write("---")
    
    if "1. Resultado Preliminar Heteroidentificação" in tipo_lista:
        df_view = df_base[df_base['Cota_Etnico_Racial']].copy()
        pos_col = 'Pos_Lista_Etnico'
        nome_arquivo_excel = "LISTA_PRELIMINAR_HETEROIDENTIFICACAO_23_OUTUBRO.xlsx"
        titulo_lista = "Resultado Preliminar da Heteroidentificação & Análise Documental (23 de Outubro de 2026)"
        corte_taf_info = "3.264 Deferidos (51.7%) | 3.045 Indeferidos (48.3%)"
        cols_tabela = ['Pos_Lista_Etnico', 'Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Resultado_Hetero', 'Nova_Pos_Lista_Etnico', 'Nota Objetiva', 'Previsao_TAF_Preliminar']
        
    elif "2. Resultado Preliminar Perícia Médica PCD" in tipo_lista:
        df_view = df_base[df_base['Cota_PCD']].copy()
        pos_col = 'Pos_Lista_PCD'
        nome_arquivo_excel = "LISTA_PRELIMINAR_PERICIA_PCD_23_OUTUBRO.xlsx"
        titulo_lista = "Resultado Preliminar da Perícia Médica PCD (23 de Outubro de 2026)"
        corte_taf_info = "473 Deferidos (71.8%) | 186 Indeferidos (28.2%)"
        cols_tabela = ['Pos_Lista_PCD', 'Posição_Geral', 'Nome', 'Inscrição', 'Resultado_PCD', 'Nova_Pos_Lista_PCD', 'Nota Objetiva', 'Previsao_TAF_Preliminar']
        
    elif "3. Nova Lista Reclassificada da Cota Étnica" in tipo_lista:
        df_view = df_base[df_base['Cota_Etnico_Apta_Preliminar']].sort_values(by='Nova_Pos_Lista_Etnico').copy()
        pos_col = 'Nova_Pos_Lista_Etnico'
        nome_arquivo_excel = "LISTA_RECLASSIFICADA_COTA_ETNICA_PRELIMINAR.xlsx"
        titulo_lista = "Nova Lista Reclassificada da Reserva Étnico-Racial (Apenas Deferidos)"
        corte_taf_info = "Linha de corte para o TAF desceu de 115 para 113 pts!"
        cols_tabela = ['Nova_Pos_Lista_Etnico', 'Pos_Lista_Etnico', 'Ganho_Pos_Etnico', 'Posição_Geral', 'Nome', 'Inscrição', 'Nota Objetiva', 'Previsao_TAF_Preliminar', 'Previsao_Vagas_Preliminar']
        
    elif "4. Nova Lista Reclassificada da Cota PCD" in tipo_lista:
        df_view = df_base[df_base['Cota_PCD_Apta_Preliminar']].sort_values(by='Nova_Pos_Lista_PCD').copy()
        pos_col = 'Nova_Pos_Lista_PCD'
        nome_arquivo_excel = "LISTA_RECLASSIFICADA_PCD_PRELIMINAR.xlsx"
        titulo_lista = "Nova Lista Reclassificada da Reserva PCD (Apenas Laudos Deferidos)"
        corte_taf_info = "Todos os 473 PCDs deferidos vão para o TAF (Item 13.1.2)"
        cols_tabela = ['Nova_Pos_Lista_PCD', 'Pos_Lista_PCD', 'Ganho_Pos_PCD', 'Posição_Geral', 'Nome', 'Inscrição', 'Nota Objetiva', 'Previsao_TAF_Preliminar', 'Previsao_Vagas_Preliminar']
        
    elif "5. Lista Geral Completa" in tipo_lista:
        df_view = df_base.copy()
        pos_col = 'Posição_Geral'
        nome_arquivo_excel = "LISTA_DEFINITIVA_GERAL_PPRN.xlsx"
        titulo_lista = "Lista Geral Completa com Situação Atualizada das Bancas"
        corte_taf_info = "Top 960 (119 pts) + empates = 1.095 convocados na ampla"
        cols_tabela = ['Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Status_Cota_Preliminar', 'Nota Objetiva', 'Previsao_TAF_Preliminar', 'Previsao_Vagas_Preliminar']
        
    else:
        df_view = df_base[df_base['Ampla_Pura']].copy().sort_values(by="Pos_Lista_Ampla_Pura", ascending=True)
        pos_col = 'Pos_Lista_Ampla_Pura'
        nome_arquivo_excel = "LISTA_DEFINITIVA_AMPLA_CONCORRENCIA_PURA_PPRN.xlsx"
        titulo_lista = "Lista Exclusiva de Não Cotistas (Ampla Concorrência Pura)"
        corte_taf_info = "783 candidatos não cotistas dentro do corte de 119 pts"
        cols_tabela = ['Pos_Lista_Ampla_Pura', 'Posição_Geral', 'Nome', 'Inscrição', 'Nota Objetiva', 'Execução Penal', 'Legislação Específica', 'Previsao_TAF_Preliminar']

    st.markdown(f"### {titulo_lista}")
    
    total_view_fmt = f"{len(df_view):,}".replace(",", ".")
    col_l1, col_l2, col_l3, col_l4 = st.columns(4)
    with col_l1:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-list-columns-reverse text-primary me-1"></i> Total de Registros</div>
<div class="stat-value">{total_view_fmt}</div>
<div class="stat-sub">Candidatos nesta relação</div>
</div>""", unsafe_allow_html=True)
    with col_l2:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-star-fill text-warning me-1"></i> Maior Nota da Lista</div>
<div class="stat-value text-primary">{df_view['Nota Objetiva'].max()} pts</div>
<div class="stat-sub">Pontuação máxima atingida</div>
</div>""", unsafe_allow_html=True)
    with col_l3:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-calculator-fill text-primary me-1"></i> Média de Notas da Lista</div>
<div class="stat-value">{df_view['Nota Objetiva'].mean():.1f} pts</div>
<div class="stat-sub">Média dos classificados</div>
</div>""", unsafe_allow_html=True)
    with col_l4:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-trophy-fill text-warning me-1"></i> Destaque Oficial</div>
<div class="stat-value text-success" style="font-size: 1.1rem;">{corte_taf_info.split("(")[0]}</div>
<div class="stat-sub text-secondary fw-bold">{corte_taf_info}</div>
</div>""", unsafe_allow_html=True)
    
    st.write("")
    
    c_f1, c_f2 = st.columns([2, 1])
    with c_f1:
        busca_tab = st.text_input("Filtrar por nome ou inscrição nesta lista:", placeholder="Digite para filtrar instantaneamente...")
    with c_f2:
        qtd_exibir = st.selectbox("Exibir:", ["Top 50", "Top 100", "Top 250", "Top 500", "Todos"], index=1)
        
    if busca_tab.strip():
        norm_b = normalizar_texto(busca_tab)
        if norm_b.isdigit():
            df_view = df_view[df_view['Inscrição_Str'].str.startswith(norm_b)]
        else:
            df_view = df_view[df_view['Nome_Busca'].str.contains(norm_b, regex=False, na=False)]
        
    if qtd_exibir != "Todos":
        lim = int(qtd_exibir.replace("Top ", ""))
        df_view_show = df_view.head(lim)
    else:
        df_view_show = df_view
        
    st.dataframe(
        df_view_show[[c for c in cols_tabela if c in df_view_show.columns]],
        width="stretch",
        hide_index=True,
        height=480
    )
    
    st.write("")
    dados_excel_bytes = carregar_bytes_excel(nome_arquivo_excel)
    if dados_excel_bytes is not None:
        st.download_button(
            label=f"📥 Baixar Planilha Completa desta Lista em Excel (.xlsx)",
            data=dados_excel_bytes,
            file_name=nome_arquivo_excel,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Arquivo Excel sendo preparado.")

# ==============================================================================
# ABA 4: REGRAS DO EDITAL, RECURSOS & LINHAS DE CORTE
# ==============================================================================
with tab_regras:
    st.subheader("🎯 Entenda as Regras de Recursos, Convocação e Linhas de Corte")
    
    st.markdown("""<div class="card bg-success-subtle border-start border-4 border-success p-3 rounded-3 shadow-sm mb-3">
<div class="d-flex align-items-center gap-2 mb-1 fw-bold text-success text-uppercase" style="font-size: 0.85rem; letter-spacing: 0.04em;">
    <i class="bi bi-journal-text fs-5"></i> GUIA PRÁTICO PARA A FASE DE RECURSOS (26 E 27 DE OUTUBRO DE 2026)
</div>
<div style="font-size: 0.93rem; color: #212529; line-height: 1.6;">
    Se sua autodeclaração ou perícia PCD foi <strong>INDEFERIDA</strong> no resultado preliminar de 23/10:<br>
    <strong>1. Consulte a justificativa:</strong> Entre no site <a href="https://www.avalia.org.br" target="_blank" class="fw-bold text-primary">avalia.org.br</a> e acesse o link <em>"Boletim de Análise de Reserva de Vagas"</em> para ver a fundamentação da banca examinadora.<br>
    <strong>2. Período de envio do recurso:</strong> Da <strong>0h00 do dia 26/10/2026 até às 23h59 do dia 27/10/2026</strong> (horário de Brasília).<br>
    <strong>3. Como protocolar:</strong> Exclusivamente em formulário próprio no site <a href="https://www.avalia.org.br" target="_blank" class="fw-bold text-primary">avalia.org.br</a>.<br>
    <strong>4. Lembre-se:</strong> O indeferimento não o desclassifica do concurso — você continua na Ampla Concorrência (Art. 4º Hetero / Art. 3º PCD).
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("#### 📊 Estatísticas Oficiais da Heteroidentificação & Bancas de 23 de Outubro")
    st.caption("Dados consolidados com base nos Anexos I, II e Único publicados oficialmente pela banca Instituto Avalia:")
    
    col_h1, col_h2, col_h3, col_h4 = st.columns(4)
    with col_h1:
        st.markdown("""<div class="stat-card">
<div class="stat-label"><i class="bi bi-people-fill text-primary me-1"></i> Total Avaliado na Hetero</div>
<div class="stat-value">6.309</div>
<div class="stat-sub text-secondary fw-bold">100% dos cotistas étnicos</div>
</div>""", unsafe_allow_html=True)
    with col_h2:
        st.markdown("""<div class="stat-card">
<div class="stat-label"><i class="bi bi-check-circle-fill text-success me-1"></i> Deferidos na Hetero</div>
<div class="stat-value text-success">3.264</div>
<div class="stat-sub text-success fw-bold">✅ 51,74% de confirmação</div>
</div>""", unsafe_allow_html=True)
    with col_h3:
        st.markdown("""<div class="stat-card">
<div class="stat-label"><i class="bi bi-x-circle-fill text-warning me-1"></i> Indeferidos na Hetero</div>
<div class="stat-value text-warning">3.045</div>
<div class="stat-sub text-warning fw-bold">⚠️ 48,26% de indeferimento</div>
</div>""", unsafe_allow_html=True)
    with col_h4:
        st.markdown("""<div class="stat-card">
<div class="stat-label"><i class="bi bi-shield-check text-primary me-1"></i> Salvos pela Ampla (Art. 4º)</div>
<div class="stat-value text-primary">79</div>
<div class="stat-sub text-primary fw-bold">Nota ≥ 119 pts no TAF via Ampla</div>
</div>""", unsafe_allow_html=True)

    st.write("")
    
    # Tabela Analítica Segmentada
    st.markdown("**📋 Demonstrativo Analítico por Modalidade de Reserva de Vagas:**")
    tabela_hetero_dados = [
        {
            "Segmento de Reserva": "🧑🏿 Pretos e Pardos (Anexo I)",
            "Total Avaliados": "6.243",
            "Deferidos": "3.221",
            "Taxa Deferimento": "51,59%",
            "Indeferidos (Reprovações)": "3.022",
            "Taxa Reprovação": "48,41%",
            "Média Nota (Deferidos)": "97,4 pts",
            "Média Nota (Indeferidos)": "91,6 pts"
        },
        {
            "Segmento de Reserva": "🏹 Indígenas (Anexo II)",
            "Total Avaliados": "58",
            "Deferidos": "37",
            "Taxa Deferimento": "63,79%",
            "Indeferidos (Reprovações)": "21",
            "Taxa Reprovação": "36,21%",
            "Média Nota (Deferidos)": "92,6 pts",
            "Média Nota (Indeferidos)": "90,7 pts"
        },
        {
            "Segmento de Reserva": "🏺 Quilombolas (Anexo II)",
            "Total Avaliados": "29",
            "Deferidos": "18",
            "Taxa Deferimento": "62,07%",
            "Indeferidos (Reprovações)": "11",
            "Taxa Reprovação": "37,93%",
            "Média Nota (Deferidos)": "92,5 pts",
            "Média Nota (Indeferidos)": "82,7 pts"
        },
        {
            "Segmento de Reserva": "📊 TOTAL COTA ÉTNICO-RACIAL",
            "Total Avaliados": "6.309",
            "Deferidos": "3.264",
            "Taxa Deferimento": "51,74%",
            "Indeferidos (Reprovações)": "3.045",
            "Taxa Reprovação": "48,26%",
            "Média Nota (Deferidos)": "97,3 pts",
            "Média Nota (Indeferidos)": "91,6 pts"
        },
        {
            "Segmento de Reserva": "♿ Perícia Médica PCD (Anexo Único)",
            "Total Avaliados": "659",
            "Deferidos": "473",
            "Taxa Deferimento": "71,78%",
            "Indeferidos (Reprovações)": "186",
            "Taxa Reprovação": "28,22%",
            "Média Nota (Deferidos)": "94,9 pts",
            "Média Nota (Indeferidos)": "90,0 pts"
        }
    ]
    st.dataframe(pd.DataFrame(tabela_hetero_dados), width="stretch", hide_index=True)
    
    st.write("")
    
    # Gráfico Visual de Deferimento vs Indeferimento
    seg_names = ['Pretos/Pardos', 'Indígenas', 'Quilombolas', 'Total Étnico', 'Perícia PCD']
    def_vals = [51.59, 63.79, 62.07, 51.74, 71.78]
    ind_vals = [48.41, 36.21, 37.93, 48.26, 28.22]
    
    fig_hetero = go.Figure()
    fig_hetero.add_trace(go.Bar(
        y=seg_names,
        x=def_vals,
        name='Deferidos (Confirmados)',
        orientation='h',
        marker_color='#198754',
        text=[f"{v:.1f}%" for v in def_vals],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=11, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif', weight=700)
    ))
    fig_hetero.add_trace(go.Bar(
        y=seg_names,
        x=ind_vals,
        name='Indeferidos (Reprovados na Banca)',
        orientation='h',
        marker_color='#dc3545',
        text=[f"{v:.1f}%" for v in ind_vals],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=11, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif', weight=700)
    ))
    fig_hetero.update_layout(
        barmode='stack',
        title=dict(text="Proporção Visual: Confirmação vs. Reprovação nas Bancas", font=dict(color='#212529', size=13, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif')),
        xaxis=dict(range=[0, 100], title="Distribuição Percentual (%)", gridcolor='#dee2e6', tickfont=dict(color='#6c757d')),
        yaxis=dict(autorange="reversed", tickfont=dict(color='#212529')),
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=35, b=25),
        height=240,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(size=11, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif'))
    )
    st.plotly_chart(fig_hetero, width="stretch")
    
    st.write("")
    st.markdown("""<div class="card bg-light border-start border-4 border-primary p-3 rounded-3 shadow-sm mb-3">
<div class="d-flex align-items-center gap-2 mb-2 fw-bold text-primary text-uppercase" style="font-size: 0.85rem; letter-spacing: 0.04em;">
    <i class="bi bi-lightbulb-fill text-warning fs-5"></i> PRINCIPAIS CONCLUSÕES E IMPACTOS DA HETEROIDENTIFICAÇÃO
</div>
<div style="font-size: 0.9rem; color: #212529; line-height: 1.6;">
    • <strong>Atrito Elevado nas Cotas Étnicas:</strong> Quase metade dos cotistas (<strong>48,26%</strong>) foi indeferida na análise preliminar. Isso representa <strong>3.045 candidatos a menos</strong> na disputa da reserva.<br>
    • <strong>Efeito Positivo para Cotistas Deferidos:</strong> Como a fila da cota andou mais de 3.000 posições, os cotistas com laudo confirmado ganharam até centenas de posições na classificação.<br>
    • <strong>Candidatos de Cota com Alto Desempenho (Art. 4º):</strong> Exatamente <strong>79 cotistas indeferidos</strong> possuem nota ≥ 119 pontos (com pontuações que chegam até 136 pontos). Eles continuam <strong>100% convocados para o TAF</strong> pela Ampla Concorrência, sem qualquer prejuízo pelo indeferimento.<br>
    • <strong>Perícia PCD com Maior Índice de Homologação:</strong> A perícia médica teve <strong>71,78% de laudos deferidos</strong> (473 candidatos aptos de um total de 659 avaliados).
</div>
</div>""", unsafe_allow_html=True)
    
    st.write("")
    st.markdown("#### 🏃‍♂️ Linhas de Corte do TAF Atualizadas com as Bancas (23 de Outubro)")
    st.markdown("""
    Com o indeferimento preliminar de <strong>3.045 cotistas na Heteroidentificação</strong> e <strong>186 na Perícia PCD</strong>, a fila das cotas andou significativamente, gerando novos cortes para o TAF:
    """)
    
    quadro_taf = [
        {
            "Modalidade": "Ampla Concorrência (AC)",
            "Regra do Edital": "Até o 960º colocado geral + empatados",
            "Nota de Corte": "119 pontos",
            "Total Convocados": "1.095 candidatos",
            "Composição do Grupo": "783 Não Cotistas + 216 Cotistas Étnicos Confirmados + 17 PCDs + 79 Indeferidos que alcançaram a Ampla"
        },
        {
            "Modalidade": "Reserva Étnico-Racial",
            "Regra do Edital": "Até o 240º cotista apto fora da ampla + empatados",
            "Nota de Corte": "113 pontos (caiu 2 pontos!)",
            "Total Convocados": "376 cotistas adicionais via reserva",
            "Composição do Grupo": "Cotistas com notas entre 113 e 118 pontos convocados pela reserva de vagas"
        },
        {
            "Modalidade": "Reserva PCD",
            "Regra do Edital": "Sem linha de corte (Item 13.1.2)",
            "Nota de Corte": "73 pontos (nota mínima)",
            "Total Convocados": "473 candidatos com laudo deferido",
            "Composição do Grupo": "100% dos candidatos PCDs com laudo deferido preliminarmente na perícia médica"
        }
    ]
    st.dataframe(pd.DataFrame(quadro_taf), width="stretch", hide_index=True)
    
    st.write("")
    st.markdown("#### ❓ Perguntas Frequentes sobre os Resultados das Bancas")
    
    with st.expander("Fui indeferido na heteroidentificação. Fui eliminado do concurso?"):
        st.markdown("""
        **NÃO!** Conforme o **Art. 4º do Edital de Convocação**, o candidato que tiver a autodeclaração indeferida perde o direito às vagas reservadas da cota, **passando a concorrer apenas pela Ampla Concorrência**. Se a sua nota na prova objetiva for suficiente para o corte da Ampla (≥ 119 pontos), você será convocado normalmente para o TAF!
        Além disso, você tem o direito legal de interpor recurso nos dias **26 e 27 de outubro** no site `avalia.org.br`.
        """)
        
    with st.expander("Por que a linha de corte da cota étnica para o TAF caiu para 113 pontos?"):
        st.markdown("""
        No resultado definitivo de 09/10, o corte estimado da cota era 115 pontos porque havia mais de 6.300 cotistas na lista.
        Com a publicação do resultado preliminar de 23/10, **3.045 candidatos autodeclarados foram indeferidos** pela comissão de heteroidentificação.
        Ao retirar temporariamente os indeferidos da lista reservada de cotas, a fila andou e os 240 primeiros cotistas aptos fora da ampla atingiram a pontuação de **113 pontos**, beneficiando centenas de candidatos que agora alcançam a convocação do TAF!
        """)

    with st.expander("Quando sai o resultado definitivo das cotas e a convocação do TAF?"):
        st.markdown("""
        Conforme o cronograma oficial da banca, a data provável para a publicação do **Resultado Definitivo da Heteroidentificação e Perícia PCD (pós-recursos)** e a publicação da convocação oficial para o TAF é **04 de Novembro de 2026**.
        """)

# ==============================================================================
# ABA 5: CRONOGRAMA OFICIAL DO CONCURSO (TIMELINE FLAT)
# ==============================================================================
with tab_cronograma:
    st.subheader("📅 Cronograma Oficial do Concurso (Edital nº 002/2026)")
    st.write("""
    Acompanhe as principais datas e prazos atualizados do concurso de Policial Penal do RN:
    """)
    
    st.markdown("""<div class="card bg-success-subtle border-start border-4 border-success p-3 rounded-3 shadow-sm mb-4">
<div class="d-flex align-items-center gap-2 mb-1 fw-bold text-success text-uppercase" style="font-size: 0.82rem; letter-spacing: 0.04em;">
    <i class="bi bi-calendar-check-fill text-success fs-5"></i> FASE ATUAL CONCLUÍDA HOJE (23 DE OUTUBRO)
</div>
<div class="fw-bold text-dark fs-5 my-1">
    Publicação do Resultado Preliminar da Heteroidentificação e da Perícia Médica PCD
</div>
<div class="text-secondary" style="font-size: 0.88rem; line-height: 1.5;">
    Relações preliminares divulgadas em 23/10/2026 no site da banca Instituto Avalia (<a href="https://www.avalia.org.br" target="_blank" class="fw-bold text-primary">avalia.org.br</a>).
</div>
</div>""", unsafe_allow_html=True)

    marcos_cronograma = [
        {
            "data": "18 de Junho de 2026",
            "titulo": "Publicação do Edital de Abertura nº 002/2026",
            "descricao": "Publicação oficial do concurso com 260 vagas totais (200 para Policial Penal) e regras gerais.",
            "status": "Concluído",
            "tipo": "past"
        },
        {
            "data": "13 de Setembro de 2026",
            "titulo": "Aplicação da Prova Objetiva",
            "descricao": "Realização das provas objetivas no turno matutino para o cargo de Policial Penal do RN.",
            "status": "Concluído",
            "tipo": "past"
        },
        {
            "data": "09 de Outubro de 2026",
            "titulo": "Resultado Definitivo da Prova Objetiva & Convocação de Cotas",
            "descricao": "Divulgação da relação de 18.945 habilitados (≥ 73 pts) e convocação presencial de cotistas e PCDs.",
            "status": "Concluído",
            "tipo": "past"
        },
        {
            "data": "17 e 18 de Outubro de 2026",
            "titulo": "Realização das Bancas Presenciais de Cotas e Perícia PCD",
            "descricao": "Comparecimento presencial dos candidatos convocados em Natal/RN para heteroidentificação e perícia.",
            "status": "Concluído",
            "tipo": "past"
        },
        {
            "data": "23 de Outubro de 2026 (Hoje)",
            "titulo": "Publicação do Resultado Preliminar da Heteroidentificação e Perícia PCD",
            "descricao": "Divulgação dos Anexos I, II e Único com os candidatos deferidos e indeferidos nas bancas de cotas.",
            "status": "Marco de Hoje",
            "tipo": "active"
        },
        {
            "data": "26 e 27 de Outubro de 2026",
            "titulo": "Prazo para Interposição de Recursos contra o Resultado das Bancas",
            "descricao": "Abertura do formulário de recurso online no portal avalia.org.br (da 0h00 de 26/10 até às 23h59 de 27/10).",
            "status": "🚨 Próxima Etapa Crítica",
            "tipo": "next"
        },
        {
            "data": "04 de Novembro de 2026 (Data Provável)",
            "titulo": "Resultado Definitivo das Cotas & Convocação Oficial para o TAF",
            "descricao": "Julgamento dos recursos, homologação final das cotas e publicação da lista oficial de convocados para o TAF.",
            "status": "Próximo Marco Oficial",
            "tipo": "future"
        },
        {
            "data": "Novembro / Dezembro de 2026",
            "titulo": "Aplicação do Teste de Aptidão Física (TAF)",
            "descricao": "Realização dos testes de condicionamento físico (barra fixa, corrida, abdominal) em Natal/RN.",
            "status": "Etapa Subsequente",
            "tipo": "future"
        },
        {
            "data": "Fases Seguintes",
            "titulo": "Avaliação Psicológica, Exames Médicos, Investigação Social e CFP",
            "descricao": "Demais etapas eliminatórias até a homologação final e matrícula no Curso de Formação Profissional (CFP).",
            "status": "Etapas Finais",
            "tipo": "future"
        }
    ]

    for m in marcos_cronograma:
        card_class = f"timeline-card timeline-card-{m['tipo']}"
        badge_bg = "bg-success" if m['tipo'] == 'past' else ("bg-warning text-dark" if m['tipo'] == 'active' else ("bg-primary" if m['tipo'] == 'next' else "bg-secondary"))
        icon_m = '<i class="bi bi-check-circle-fill me-1"></i>' if m['tipo'] == 'past' else ('<i class="bi bi-stars me-1"></i>' if m['tipo'] == 'active' else ('<i class="bi bi-exclamation-circle-fill me-1"></i>' if m['tipo'] == 'next' else '<i class="bi bi-clock me-1"></i>'))
        
        st.markdown(f"""<div class="{card_class}">
<div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-1">
<div class="fw-bold text-primary text-uppercase" style="font-size: 0.82rem; letter-spacing: 0.04em;">
<i class="bi bi-calendar3 me-1"></i> {m['data']}
</div>
<span class="badge rounded-pill {badge_bg}" style="font-size: 0.75rem; text-transform: uppercase;">
{icon_m}{m['status']}
</span>
</div>
<div class="fw-bold text-dark my-1" style="font-size: 1.05rem;">
{m['titulo']}
</div>
<div class="text-secondary" style="font-size: 0.88rem; line-height: 1.5;">
{m['descricao']}
</div>
</div>""", unsafe_allow_html=True)

# ==============================================================================
# ABA 6: SOBRE O PORTAL, ORIGEM DOS DADOS E METODOLOGIA
# ==============================================================================
with tab_sobre:
    st.markdown("""<div class="sim-banner">
<span class="badge-pill-blue"><i class="bi bi-info-circle-fill text-primary me-1"></i> TRANSPARÊNCIA, METODOLOGIA & FONTES</span>
<h2 class="hero-title mt-1 mb-2" style="font-size: 1.75rem;"><i class="bi bi-patch-question-fill text-primary me-2"></i>Sobre o Portal de Resultados do PPRN</h2>
<p class="text-secondary mb-0" style="font-size: 0.95rem; line-height: 1.55;">
Conheça como esta aplicação foi desenvolvida, a proveniência dos dados, a metodologia aplicada nos desempates e simuladores, e a finalidade colaborativa do projeto.
</p>
</div>""", unsafe_allow_html=True)

    st.markdown("""<div class="card bg-warning-subtle border-start border-4 border-warning p-3 rounded-3 shadow-sm mb-4">
<div class="d-flex align-items-center gap-2 mb-1 fw-bold text-warning-emphasis text-uppercase" style="font-size: 0.85rem; letter-spacing: 0.04em;">
    <i class="bi bi-exclamation-triangle-fill text-warning fs-5"></i> AVISO LEGAL IMPORTANTE (DISCLAIMER DA BANCA)
</div>
<div style="font-size: 0.92rem; color: #212529; line-height: 1.55;">
Este portal é uma <strong>iniciativa independente</strong>, desenvolvida para auxiliar e orientar a comunidade de candidatos do Concurso de Policial Penal do Rio Grande do Norte (PPRN).<br>
<strong>NÃO se trata de uma plataforma oficial do Instituto Avalia nem do Governo do Estado do RN (SEAD/SEAP).</strong><br>
Todas as comunicações formais, convocações oficiais e atos com efeitos jurídicos devem ser obrigatoriamente consultados e confirmados no endereço oficial da banca examinadora: <a href="https://www.avalia.org.br" target="_blank" class="fw-bold text-primary">avalia.org.br</a>.
</div>
</div>""", unsafe_allow_html=True)

    col_sob1, col_sob2 = st.columns(2)
    
    with col_sob1:
        st.markdown("""<div class="stat-card mb-3">
<div class="stat-label"><i class="bi bi-folder-fill text-primary me-1"></i> Origem dos Dados</div>
<div class="fw-bold text-dark fs-5 my-1">100% Baseado em Documentos Públicos da Banca</div>
<div class="text-secondary" style="font-size: 0.88rem; line-height: 1.55;">
Todos os registros presentes neste painel foram extraídos diretamente dos editais e planilhas oficiais publicados pela banca <strong>Instituto Avalia</strong> em <strong>09 e 23 de outubro de 2026</strong>:
<ul class="my-2 ps-3">
<li>Edital de Publicação do Resultado Definitivo da Prova Objetiva;</li>
<li>Edital de Resultado Preliminar da Perícia Médica PCD (23/10);</li>
<li>Anexo I: Resultado Preliminar Heteroidentificação Preto e Pardo (23/10);</li>
<li>Anexo II: Resultado Preliminar Análise Documental Indígena e Quilombola (23/10);</li>
<li>Anexo Único: Resultado Preliminar Perícia Médica PCD (23/10).</li>
</ul>
</div>
</div>""", unsafe_allow_html=True)

        st.markdown("""<div class="stat-card">
<div class="stat-label"><i class="bi bi-cpu-fill text-primary me-1"></i> Inteligência Artificial Agêntica</div>
<div class="fw-bold text-dark fs-5 my-1">Engenharia Moderna com IA</div>
<div class="text-secondary" style="font-size: 0.88rem; line-height: 1.55;">
O desenvolvimento deste portal e o processamento dos dados contaram com o suporte de <strong>Inteligência Artificial Agêntica (Agentic AI)</strong> para:
<ul class="my-2 ps-3">
<li>Cruzamento e auditoria instantânea dos 6.309 cotistas étnicos e 659 PCDs com a base geral;</li>
<li>Implementação fiel dos 10 critérios oficiais de desempate do Edital (Item 21.2.1);</li>
<li>Modelagem matemática do motor de simulações pós-bancas e TAF;</li>
<li>Design visual institucional e arquitetura de carregamento em alta performance.</li>
</ul>
</div>
</div>""", unsafe_allow_html=True)

    with col_sob2:
        st.markdown("""<div class="stat-card mb-3">
<div class="stat-label"><i class="bi bi-shield-check text-success me-1"></i> Por que os Dados são Confiáveis?</div>
<div class="fw-bold text-dark fs-5 my-1">Rigor Matemático e Auditoria Cruzada</div>
<div class="text-secondary" style="font-size: 0.88rem; line-height: 1.55;">
A confiabilidade da aplicação fundamenta-se na fidelidade matemática aos documentos originais:
<ul class="my-2 ps-3">
<li><strong>Nenhum dado é inventado:</strong> notas e status preliminares (Deferido/Indeferido) são cópias exatas das relações oficiais;</li>
<li><strong>Regra do Art. 4º (Hetero) e Art. 3º (PCD):</strong> respeito estrito à norma editalícia que garante a concorrência na Ampla aos indeferidos;</li>
<li><strong>Classificação Concomitante (Item 7.3):</strong> os cotistas com nota para ampla são identificados conforme a legislação estadual e regras afirmativas.</li>
</ul>
</div>
</div>""", unsafe_allow_html=True)

        st.markdown("""<div class="stat-card">
<div class="stat-label"><i class="bi bi-graph-up text-primary me-1"></i> Natureza das Simulações</div>
<div class="fw-bold text-dark fs-5 my-1">Especulação Estatística para Auxílio</div>
<div class="text-secondary" style="font-size: 0.88rem; line-height: 1.55;">
Os recursos presentes no <strong>Simulador de Colocações</strong> e nas <strong>Projeções do Boletim</strong> são <strong>modelos especulativos de projeção</strong>:
<ul class="my-2 ps-3">
<li>Ajudam o candidato a entender o impacto da fase recursal de 26-27/10 e da reprovação típica do TAF;</li>
<li>Não representam resultado homologado futuro, mas servem como balizador estratégico para planejamento com antecedência.</li>
</ul>
</div>
</div>""", unsafe_allow_html=True)

    st.write("")
    
    st.markdown("""<div class="card border-start border-4 border-primary p-3 rounded-3 shadow-sm mb-4">
<div class="d-flex align-items-center gap-2 mb-1 fw-bold text-primary text-uppercase" style="font-size: 0.85rem;">
    <i class="bi bi-chat-heart-fill text-danger fs-5"></i> Mensagem aos Candidatos
</div>
<div style="font-size: 0.93rem; color: #212529; line-height: 1.6;">
Este portal nasceu com o propósito de oferecer clareza, transparência e conforto aos concurseiros que dedicaram meses de estudo para o certame de Policial Penal do RN. Acompanhar classificações em PDFs extensos de centenas de páginas é um processo exaustivo. Aqui, buscamos transformar dados públicos em informação acessível, rápida e compreensível.<br><br>
Para dúvidas, correções ou sugestões de novas análises, entre em contato diretamente com o criador do projeto: 
<a href="https://instagram.com/pedronildu" target="_blank" class="fw-bold text-primary text-decoration-none"><i class="bi bi-instagram text-danger me-1"></i>@pedronildu</a> no Instagram.
</div>
</div>""", unsafe_allow_html=True)

# ==============================================================================
# RODAPÉ COM CRÉDITOS DO CRIADOR @PEDRONILDU (BOOTSTRAP 5)
# ==============================================================================
st.markdown("""<div class="footer-container">
<div><i class="bi bi-shield-fill-check text-primary me-1"></i> <strong>Portal de Resultados PPRN</strong> • Dados oficiais atualizados com os Resultados Preliminares das Bancas de Heteroidentificação e Perícia PCD (23/10/2026).</div>
<div class="mt-2 text-secondary" style="font-size: 0.9rem;">
Desenvolvido com dedicação por <strong class="text-dark">Pedro Nildo</strong> • Instagram do Criador: <a href="https://instagram.com/pedronildu" target="_blank" class="fw-bold text-primary text-decoration-none"><i class="bi bi-instagram text-danger me-1"></i>@pedronildu</a>
</div>
</div>""", unsafe_allow_html=True)
