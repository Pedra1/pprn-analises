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
    page_title="PPRN - Resultado Definitivo & Convocação de Cotas",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==============================================================================
# ESTILOS CSS CUSTOMIZADOS (DESIGN SYSTEM ELEGANTE & MODERNO)
# ==============================================================================
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Hero */
    .hero-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.98) 0%, rgba(30, 58, 138, 0.7) 50%, rgba(15, 23, 42, 0.98) 100%);
        border: 1px solid rgba(59, 130, 246, 0.4);
        border-radius: 16px;
        padding: 22px 28px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 20px rgba(59, 130, 246, 0.18);
    }
    
    .badge-pill {
        display: inline-block;
        background: rgba(16, 185, 129, 0.18);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
    }
    
    .hero-title {
        font-size: 2.05rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0 0 8px 0;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Stat Cards */
    .stat-card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: rgba(96, 165, 250, 0.4);
    }
    
    .stat-label {
        color: #94A3B8;
        font-size: 0.74rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 4px;
    }
    
    .stat-value {
        font-size: 1.55rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
    }
    
    .stat-sub {
        font-size: 0.72rem;
        color: #64748B;
        margin-top: 3px;
    }
    
    /* Candidate Spotlight Card */
    .candidate-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.92) 0%, rgba(15, 23, 42, 0.98) 100%);
        border: 1px solid rgba(59, 130, 246, 0.35);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    
    .pos-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 8px;
        font-size: 1.15rem;
        font-weight: 800;
    }
    
    .pos-top {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: #000;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
    }
    
    .pos-standard {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: #FFF;
        box-shadow: 0 0 15px rgba(37, 99, 235, 0.4);
    }
    
    .tag-cota {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 6px;
        margin-top: 4px;
    }
    
    .tag-ampla {
        background: rgba(59, 130, 246, 0.2);
        color: #93C5FD;
        border: 1px solid rgba(59, 130, 246, 0.4);
    }
    
    .tag-negro {
        background: rgba(168, 85, 247, 0.2);
        color: #D8B4FE;
        border: 1px solid rgba(168, 85, 247, 0.4);
    }
    
    .tag-pcd {
        background: rgba(16, 185, 129, 0.2);
        color: #6EE7B7;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    
    .tag-indigena {
        background: rgba(245, 158, 11, 0.2);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    
    .tag-quilombola {
        background: rgba(236, 72, 153, 0.2);
        color: #F472B6;
        border: 1px solid rgba(236, 72, 153, 0.4);
    }
    
    /* Notification Status Cards */
    .card-fase-presencial {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(30, 41, 59, 0.95) 100%);
        border: 1px solid rgba(245, 158, 11, 0.5);
        border-radius: 12px;
        padding: 16px 20px;
        margin-top: 14px;
    }

    .card-fase-ampla {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(30, 41, 59, 0.95) 100%);
        border: 1px solid rgba(59, 130, 246, 0.35);
        border-radius: 12px;
        padding: 16px 20px;
        margin-top: 14px;
    }
    
    .card-previsao {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 16px 20px;
        margin-top: 12px;
    }
    
    .card-previsao-ok {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(16, 185, 129, 0.45);
        border-radius: 12px;
        padding: 16px 20px;
        margin-top: 12px;
    }

    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: rgba(30, 41, 59, 0.6);
        border-radius: 10px 10px 0px 0px;
        gap: 8px;
        padding: 10px 22px;
        font-weight: 700;
        font-size: 0.95rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-bottom: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(37, 99, 235, 0.25) !important;
        border-color: rgba(59, 130, 246, 0.6) !important;
        color: #60A5FA !important;
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

@st.cache_data(show_spinner="Carregando base oficial definitiva pós-recursos...")
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

# Totais gerais definitivos
TOTAL_CANDIDATOS = len(df_base)
TOTAL_AMPLA_PURA = int(df_base['Ampla_Pura'].sum())
TOTAL_ETNICO = int(df_base['Cota_Etnico_Racial'].sum())
TOTAL_PCD = int(df_base['Cota_PCD'].sum())
TOTAL_NEGRO_PARDO = int(df_base['Cota_Negro_Pardo'].sum())
TOTAL_INDIGENA = int(df_base['Cota_Indigena'].sum())
TOTAL_QUILOMBOLA = int(df_base['Cota_Quilombola'].sum())
TOTAL_PCD_ETNICO = int((df_base['Cota_PCD'] & df_base['Cota_Etnico_Racial']).sum())

MAIOR_NOTA = int(df_base['Nota Objetiva'].max())
MENOR_NOTA = int(df_base['Nota Objetiva'].min())
MEDIA_NOTA = float(df_base['Nota Objetiva'].mean())
MEDIANA_NOTA = float(df_base['Nota Objetiva'].median())

TOTAL_CANDIDATOS_FMT = f"{TOTAL_CANDIDATOS:,}".replace(",", ".")
TOTAL_AMPLA_FMT = f"{TOTAL_AMPLA_PURA:,}".replace(",", ".")
TOTAL_ETNICO_FMT = f"{TOTAL_ETNICO:,}".replace(",", ".")
TOTAL_PCD_FMT = f"{TOTAL_PCD:,}".replace(",", ".")

# ==============================================================================
# HEADER HERO & VISÃO GERAL
# ==============================================================================
st.markdown("""<div class="hero-container">
<span class="badge-pill">✅ RESULTADO DEFINITIVO PÓS-RECURSOS • ATUALIZADO EM 09/10/2026</span>
<h1 class="hero-title">Portal de Resultados Definitivos • Concurso Policial Penal RN</h1>
<p class="hero-subtitle">
Classificação oficial definitiva com todos os critérios de desempate do edital (Item 21.2.1), convocação para as etapas presenciais de 17-18 de outubro e previsão oficial do TAF.
</p>
</div>""", unsafe_allow_html=True)

# 4 Métricas Principais Objetivas
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""<div class="stat-card">
<div class="stat-label">👥 Total Aprovados</div>
<div class="stat-value">{TOTAL_CANDIDATOS_FMT}</div>
<div class="stat-sub">100% da lista definitiva oficial</div>
</div>""", unsafe_allow_html=True)

with m2:
    st.markdown(f"""<div class="stat-card">
<div class="stat-label">🏛️ Não Cotistas (Ampla)</div>
<div class="stat-value">{TOTAL_AMPLA_FMT}</div>
<div class="stat-sub">{(TOTAL_AMPLA_PURA/TOTAL_CANDIDATOS)*100:.1f}% concorrendo exclusivamente na Ampla</div>
</div>""", unsafe_allow_html=True)

with m3:
    st.markdown(f"""<div class="stat-card">
<div class="stat-label">🧑🏿 Étnico-Racial</div>
<div class="stat-value">{TOTAL_ETNICO_FMT}</div>
<div class="stat-sub">{(TOTAL_ETNICO/TOTAL_CANDIDATOS)*100:.1f}% convocados hetero/análise doc</div>
</div>""", unsafe_allow_html=True)

with m4:
    st.markdown(f"""<div class="stat-card">
<div class="stat-label">♿ PCD</div>
<div class="stat-value">{TOTAL_PCD_FMT}</div>
<div class="stat-sub">{(TOTAL_PCD/TOTAL_CANDIDATOS)*100:.1f}% convocados para perícia ({TOTAL_PCD_ETNICO} dupla cota)</div>
</div>""", unsafe_allow_html=True)

st.write("")

# ==============================================================================
# NAVEGAÇÃO PRINCIPAL EM 3 ABAS LIMPAS & DIRETAS
# ==============================================================================
tab_busca, tab_listas, tab_regras = st.tabs([
    "🔍 Meu Boletim (Consulta Rápida)",
    "📋 As 4 Listas Oficiais & Downloads",
    "🎯 Entenda as Regras & Previsão TAF"
])

# ==============================================================================
# ABA 1: CONSULTA INDIVIDUAL (BOLETIM DO CANDIDATO COM CONVOCAÇÃO PRESENCIAL)
# ==============================================================================
with tab_busca:
    st.subheader("🔍 Localize seu Desempenho e Convocação Oficial")
    st.write("Digite seu **Nome Completo** (ou parte dele) ou seu número de **Inscrição** para conferir seu boletim oficial:")
    
    col_search, col_action = st.columns([3, 1])
    with col_search:
        termo_busca = st.text_input(
            "Buscar por Nome ou Inscrição",
            placeholder="Exemplo: Pedro Nildo, Liliane Pequeno, Herbert Ryan ou 2320000136...",
            label_visibility="collapsed"
        )
    with col_action:
        st.write("")
        st.caption("💡 Busca flexível (ignora maiúsculas e acentos)")
    
    candidato_selecionado = None
    
    if termo_busca.strip():
        termo_norm = normalizar_texto(termo_busca)
        mascara = (
            df_base['Nome_Busca'].str.contains(termo_norm, na=False) |
            df_base['Inscrição_Str'].str.contains(termo_norm, na=False)
        )
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
        st.info("💡 **Faça sua busca acima:** Digite seu nome ou número de inscrição para carregar seu boletim oficial completo. Como exemplo inicial, exibindo o 1º colocado geral:")
        candidato_selecionado = df_base.iloc[0]

    # Exibição do Perfil do Candidato
    if candidato_selecionado is not None:
        pos_geral = int(candidato_selecionado['Posição_Geral'])
        pos_orig = int(candidato_selecionado.get('Posição_Original_Definitiva', pos_geral))
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
        
        # Bloco de Convocação Presencial (17-18 de Outubro)
        convocacao_texto = str(candidato_selecionado['Convocacao_Fase_Presencial'])
        if "Convocado" in convocacao_texto:
            presencial_html = f"""<div class="card-fase-presencial">
<div style="font-size: 0.85rem; font-weight: 800; color: #F59E0B; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.04em;">
📢 CONVOCAÇÃO PARA ETAPA PRESENCIAL (EDITAIS DE 09 DE OUTUBRO)
</div>
<div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC;">
{convocacao_texto}
</div>
<div style="font-size: 0.84rem; color: #CBD5E1; margin-top: 8px; line-height: 1.4;">
📅 <strong>Data da Etapa:</strong> 17 e 18 de outubro de 2026 em Natal/RN.<br>
🎫 <strong>Cartão de Informação:</strong> Acesse <a href="https://www.avalia.org.br" target="_blank" style="color: #60A5FA; font-weight: 600;">avalia.org.br</a> a partir das 15h de 13/10 para consultar seu local, sala e horário exato.
</div>
</div>"""
        else:
            presencial_html = """<div class="card-fase-ampla">
<div style="font-size: 0.85rem; font-weight: 800; color: #60A5FA; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.04em;">
ℹ️ ETAPA PRESENCIAL DE 17-18/10 NÃO SE APLICA (AMPLA CONCORRÊNCIA)
</div>
<div style="font-size: 1.02rem; font-weight: 700; color: #F8FAFC;">
⚪ Não Convocado para Avaliações de Cotas (Candidato de Ampla Concorrência)
</div>
<div style="font-size: 0.84rem; color: #94A3B8; margin-top: 6px; line-height: 1.4;">
As bancas de 17 e 18 de outubro são exclusivas para heteroidentificação de cotas étnicas e perícia médica PCD. Como candidato de Ampla Concorrência, você não realiza esta etapa — sua próxima fase avaliativa é diretamente a convocação do TAF (conforme classificação).
</div>
</div>"""

        # Bloco de Previsão TAF & Vagas
        status_taf = str(candidato_selecionado['Previsao_TAF'])
        is_taf_convocado = "Convocado" in status_taf
        taf_class = "card-previsao-ok" if is_taf_convocado else "card-previsao"
        taf_title_color = "#34D399" if is_taf_convocado else "#94A3B8"
        taf_badge_text = "🟢 PREVISÃO OFICIAL: DENTRO DO LIMITE DE CONVOCAÇÃO DO TAF!" if is_taf_convocado else "⚪ PREVISÃO OFICIAL: FORA DO CORTE PRELIMINAR DO TAF"

        taf_html = f"""<div class="{taf_class}">
<div style="font-size: 0.85rem; font-weight: 800; color: {taf_title_color}; text-transform: uppercase; margin-bottom: 8px;">
🎯 {taf_badge_text}
</div>
<div style="display: flex; flex-wrap: wrap; gap: 20px; font-size: 0.95rem; color: #F1F5F9; margin-bottom: 4px;">
<div><strong>🏃‍♂️ Status no TAF:</strong> {status_taf}</div>
<div><strong>🏆 Vagas Imediatas:</strong> {candidato_selecionado['Previsao_Vagas_Imediatas']}</div>
</div>
</div>"""

        # Montagem do Cartão Principal sem nenhuma indentação de Markdown
        card_html = f"""<div class="candidate-card">
<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
<div>
<span class="badge-pill">BOLETIM OFICIAL DEFINITIVO PÓS-RECURSOS</span>
<h2 style="color: #FFF; margin: 4px 0 6px 0; font-size: 1.8rem;">{nome}</h2>
<p style="color: #94A3B8; margin: 0 0 10px 0; font-size: 0.95rem;">
Inscrição: <strong>{inscricao}</strong> &nbsp;•&nbsp; Cargo: <strong>401 - Policial Penal RN</strong>
</p>
<div>{tags_html}</div>
</div>
<div style="text-align: right;">
<div class="pos-badge {pos_class}">
{medalha}{pos_geral}º LUGAR GERAL
</div>
<div style="color: #60A5FA; font-size: 0.85rem; margin-top: 6px; font-weight: 600;">
Top {top_pct_fmt} de todos os {TOTAL_CANDIDATOS_FMT} candidatos
</div>
</div>
</div>
{presencial_html}
{taf_html}
</div>"""

        st.markdown(card_html, unsafe_allow_html=True)
        
        # 4 Indicadores Principais de Classificação
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Classificação Geral Oficial", f"{pos_geral}º", f"De {TOTAL_CANDIDATOS_FMT} candidatos")
        with c2:
            if is_etnico and pd.notnull(candidato_selecionado['Pos_Lista_Etnico']):
                st.metric("Posição na Cota Étnica", f"{int(candidato_selecionado['Pos_Lista_Etnico'])}º", f"De {TOTAL_ETNICO_FMT} cotistas étnicos")
            elif is_pcd and pd.notnull(candidato_selecionado['Pos_Lista_PCD']):
                st.metric("Posição na Cota PCD", f"{int(candidato_selecionado['Pos_Lista_PCD'])}º", f"De {TOTAL_PCD_FMT} cotistas PCD")
            else:
                st.metric("Posição Não Cotista", f"{int(candidato_selecionado['Pos_Lista_Ampla_Pura'])}º", f"De {TOTAL_AMPLA_FMT} da Ampla Pura")
        with c3:
            st.metric("Nota Objetiva", f"{nota_total} pts", f"{aproveitamento_total:.1f}% de aproveitamento (Máx {NOTA_MAXIMA_PROVA})")
        with c4:
            if pos_geral <= 140 or "Vagas Imediatas" in str(candidato_selecionado['Previsao_Vagas_Imediatas']):
                st.metric("Situação de Vagas", "Vagas Imediatas 🏆", "Dentro das 140 vagas")
            else:
                st.metric("Situação de Vagas", "Cadastro Reserva 📋", "Classificado no CR")
                
        st.write("")
        
        # Detalhamento de Disciplinas
        st.markdown("#### 📋 Detalhamento do seu Aproveitamento por Disciplina")
        dados_detalhamento = []
        for d in DISCIPLINAS:
            nota_cand = int(candidato_selecionado[d])
            max_p = PONTOS_MAXIMOS[d]
            aprov = (nota_cand / max_p) * 100
            media_disc = df_base[d].mean()
            diff_media = nota_cand - media_disc
            dados_detalhamento.append({
                "Disciplina": d,
                "Sua Nota": f"{nota_cand} / {max_p} pts",
                "Aproveitamento": f"{aprov:.1f}%",
                "Média Geral da Prova": f"{media_disc:.2f} pts",
                "Comparativo com a Média": f"{diff_media:+.2f} pts" + (" 🟢 Acima" if diff_media > 0 else " 🔴 Abaixo")
            })
        st.dataframe(pd.DataFrame(dados_detalhamento), use_container_width=True, hide_index=True)
        
        # Gráfico de barras horizontal limpo de aproveitamento
        pct_candidato = [(candidato_selecionado[d] / PONTOS_MAXIMOS[d]) * 100 for d in DISCIPLINAS]
        nomes_curtos = [
            d.replace("História do RN e Aspectos Geoeconômicos do RN", "História RN")
             .replace("Ética no Serviço Público", "Ética")
             .replace("Direito Penal e Processo Penal", "Penal / Processo")
             .replace("Legislação Específica", "Leg. Específica")
            for d in DISCIPLINAS
        ]
        cores = ['#10B981' if p >= 80 else ('#F59E0B' if p >= 60 else '#EF4444') for p in pct_candidato]

        fig_bar = go.Figure(go.Bar(
            x=pct_candidato,
            y=nomes_curtos,
            orientation='h',
            marker_color=cores,
            text=[f"{p:.1f}% ({candidato_selecionado[d]}/{PONTOS_MAXIMOS[d]} pts)" for p, d in zip(pct_candidato, DISCIPLINAS)],
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(color='white', size=11, family='Inter')
        ))
        fig_bar.update_layout(
            title="Aproveitamento Percentual por Disciplina",
            xaxis=dict(range=[0, 105], title="Aproveitamento (%)", gridcolor='rgba(255, 255, 255, 0.1)'),
            yaxis=dict(autorange="reversed"),
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=20, t=35, b=30),
            height=340
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Expanders Retráteis (informação sem poluição visual)
        with st.expander("👥 Candidatos Próximos na Classificação Geral (+/- 5 concorrentes ao redor)"):
            st.caption("Veja os candidatos imediatamente antes e depois da sua posição para entender os empates na nota e critérios de desempate:")
            start_idx = max(0, pos_geral - 6)
            end_idx = min(TOTAL_CANDIDATOS, pos_geral + 5)
            vizinhos = df_base.iloc[start_idx:end_idx][['Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Nota Objetiva', 'Execução Penal', 'Legislação Específica', 'Direito Penal e Processo Penal', 'Língua Portuguesa', 'Convocacao_Fase_Presencial']]
            
            def destacar_linha(row):
                if row['Posição_Geral'] == pos_geral:
                    return ['background-color: rgba(59, 130, 246, 0.35); font-weight: bold;'] * len(row)
                return [''] * len(row)
                
            st.dataframe(
                vizinhos.style.apply(destacar_linha, axis=1),
                use_container_width=True,
                hide_index=True
            )

        with st.expander("⚔️ Comparar Meu Resultado com Outro Candidato"):
            st.caption("Compare seu boletim de notas matéria por matéria com qualquer concorrente da lista:")
            col_comp_busca, col_comp_sel = st.columns([1, 1])
            with col_comp_busca:
                termo_outro = st.text_input("Buscar Concorrente (Nome ou Inscrição):", placeholder="Digite o nome do concorrente...", key="busca_outro")
            
            if termo_outro.strip():
                filtro_outro = df_base[
                    df_base['Nome_Busca'].str.contains(normalizar_texto(termo_outro), na=False) |
                    df_base['Inscrição_Str'].str.contains(normalizar_texto(termo_outro), na=False)
                ]
                if len(filtro_outro) > 0:
                    opcoes_outro = [
                        f"{row['Posição_Geral']}º - {row['Nome']} (Nota: {row['Nota Objetiva']} pts | {row['Modalidade_Concorrencia']})"
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
                    st.dataframe(pd.DataFrame(confronto_rows), use_container_width=True, hide_index=True)
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
            6. **Maior pontuação em Criminologia** (se aplicável);
            7. **Maior pontuação em Raciocínio Lógico Matemático**;
            8. **Maior pontuação em Noções de Informática**;
            9. **Maior pontuação em História do RN**;
            10. **Maior idade cronológica geral**.
            """)

# ==============================================================================
# ABA 2: AS 4 LISTAS OFICIAIS DEFINITIVAS (ITEM 21.3 DO EDITAL)
# ==============================================================================
with tab_listas:
    st.subheader("📋 As 4 Listas Oficiais Definitivas do Concurso (Pós-Recursos)")
    st.write("""
    Conforme o **Item 21.3 do Edital** e os resultados definitivos divulgados em **09 de outubro de 2026**:
    Visualize, filtre e faça o download de cada lista oficial definitiva em formato Excel (.xlsx):
    """)
    
    tipo_lista = st.radio(
        "Selecione a Lista Definitiva que deseja visualizar e baixar:",
        [
            f"🌐 1. Lista Definitiva Geral (AC Universal - {TOTAL_CANDIDATOS_FMT} candidatos)",
            f"🧑🏿 2. Lista Definitiva Étnico-Racial (Pretos, Pardos, Indígenas, Quilombolas - {TOTAL_ETNICO_FMT} candidatos)",
            f"♿ 3. Lista Definitiva PCD (Pessoas com Deficiência - {TOTAL_PCD_FMT} candidatos)",
            f"🏛️ 4. Lista Definitiva Ampla Concorrência (Apenas Não Cotistas - {TOTAL_AMPLA_FMT} candidatos)"
        ],
        index=0
    )
    
    st.write("---")
    
    if "1. Lista Definitiva Geral" in tipo_lista:
        df_view = df_base.copy()
        pos_col = 'Posição_Geral'
        nome_arquivo_excel = "LISTA_DEFINITIVA_GERAL_PPRN.xlsx"
        titulo_lista = "Lista Definitiva Geral (AC Universal) - Todos os Candidatos Aprovados Pós-Recursos"
        corte_taf_info = "Top 960 (119 pts) + empates = 1.095 convocados"
        
    elif "2. Lista Definitiva Étnico-Racial" in tipo_lista:
        df_view = df_base[df_base['Cota_Etnico_Racial']].copy().sort_values(by="Pos_Lista_Etnico", ascending=True)
        pos_col = 'Pos_Lista_Etnico'
        nome_arquivo_excel = "LISTA_DEFINITIVA_ETNICO_RACIAL_PPRN.xlsx"
        titulo_lista = "Lista Definitiva de Reserva Étnico-Racial (Pretos, Pardos, Indígenas e Quilombolas)"
        corte_taf_info = "Top 240 na cota (120 pts direto / 115 pts com aproveitamento da ampla)"
        
    elif "3. Lista Definitiva PCD" in tipo_lista:
        df_view = df_base[df_base['Cota_PCD']].copy().sort_values(by="Pos_Lista_PCD", ascending=True)
        pos_col = 'Pos_Lista_PCD'
        nome_arquivo_excel = "LISTA_DEFINITIVA_PCD_PPRN.xlsx"
        titulo_lista = "Lista Definitiva de Pessoas com Deficiência (PCD) Convocadas para Perícia"
        corte_taf_info = "Sem linha de corte! Todos os 659 PCDs habilitados vão para o TAF (Item 13.1.2)"
        
    else:
        df_view = df_base[df_base['Ampla_Pura']].copy().sort_values(by="Pos_Lista_Ampla_Pura", ascending=True)
        pos_col = 'Pos_Lista_Ampla_Pura'
        nome_arquivo_excel = "LISTA_DEFINITIVA_AMPLA_CONCORRENCIA_PURA_PPRN.xlsx"
        titulo_lista = "Lista Definitiva Exclusiva de Não Cotistas (Ampla Concorrência Pura)"
        corte_taf_info = "783 candidatos não cotistas classificados dentro do Top 960 da Geral"

    # Métricas da Lista Selecionada
    st.markdown(f"### {titulo_lista}")
    
    col_l1, col_l2, col_l3, col_l4 = st.columns(4)
    col_l1.metric("Total de Candidatos", f"{len(df_view):,}".replace(",", "."))
    col_l2.metric("Maior Nota da Lista", f"{df_view['Nota Objetiva'].max()} pts")
    col_l3.metric("Média de Notas da Lista", f"{df_view['Nota Objetiva'].mean():.1f} pts")
    col_l4.metric("Regra TAF do Edital", corte_taf_info.split("(")[0])
    
    # Filtros da Lista
    c_f1, c_f2 = st.columns([2, 1])
    with c_f1:
        busca_tab = st.text_input("Filtrar por nome ou inscrição nesta lista:", placeholder="Digite para filtrar instantaneamente...")
    with c_f2:
        qtd_exibir = st.selectbox("Exibir:", ["Top 50", "Top 100", "Top 250", "Top 500", "Todos"], index=1)
        
    if busca_tab.strip():
        norm_b = normalizar_texto(busca_tab)
        df_view = df_view[
            df_view['Nome_Busca'].str.contains(norm_b, na=False) |
            df_view['Inscrição_Str'].str.contains(norm_b, na=False)
        ]
        
    if qtd_exibir != "Todos":
        lim = int(qtd_exibir.replace("Top ", ""))
        df_view_show = df_view.head(lim)
    else:
        df_view_show = df_view
        
    colunas_padrao = ['Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Convocacao_Fase_Presencial', 'Nota Objetiva', 'Execução Penal', 'Legislação Específica', 'Direito Penal e Processo Penal', 'Língua Portuguesa', 'Previsao_TAF', 'Previsao_Vagas_Imediatas']
    if pos_col == 'Posição_Geral':
        cols_tabela = colunas_padrao
    else:
        cols_tabela = [pos_col] + [c for c in colunas_padrao if c != pos_col]
    
    st.dataframe(
        df_view_show[cols_tabela],
        use_container_width=True,
        hide_index=True,
        height=480
    )
    
    # Botão de Download do Excel Oficial
    st.write("")
    if os.path.exists(nome_arquivo_excel):
        with open(nome_arquivo_excel, "rb") as f_excel:
            st.download_button(
                label=f"📥 Baixar Planilha Completa desta Lista em Excel (.xlsx)",
                data=f_excel.read(),
                file_name=nome_arquivo_excel,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("Arquivo Excel sendo preparado.")

# ==============================================================================
# ABA 3: REGRAS DO EDITAL, LINHAS DE CORTE & PREVISÃO TAF
# ==============================================================================
with tab_regras:
    st.subheader("🎯 Entenda as Regras de Convocação, Vagas e TAF")
    
    # Cronograma Oficial em Cards
    st.markdown("#### 📅 Cronograma Oficial dos Próximos Passos (Editais de 09/10/2026)")
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.markdown("""<div class="stat-card" style="border-left: 4px solid #10B981;">
<div class="stat-label">09 DE OUTUBRO</div>
<div style="font-weight: 700; color: #FFF; font-size: 0.95rem;">Resultado Definitivo</div>
<div class="stat-sub">Publicação das listas definitivas e convocação presencial.</div>
</div>""", unsafe_allow_html=True)
    with t2:
        st.markdown("""<div class="stat-card" style="border-left: 4px solid #3B82F6;">
<div class="stat-label">13 DE OUTUBRO (15H)</div>
<div style="font-weight: 700; color: #FFF; font-size: 0.95rem;">Cartão de Confirmação</div>
<div class="stat-sub">Horário, local e sala no site avalia.org.br para os convocados.</div>
</div>""", unsafe_allow_html=True)
    with t3:
        st.markdown("""<div class="stat-card" style="border-left: 4px solid #F59E0B;">
<div class="stat-label">17 E 18 DE OUTUBRO</div>
<div style="font-weight: 700; color: #FFF; font-size: 0.95rem;">Bancas Presenciais</div>
<div class="stat-sub">Heteroidentificação (Pretos/Pardos) e Perícia PCD em Natal/RN.</div>
</div>""", unsafe_allow_html=True)
    with t4:
        st.markdown("""<div class="stat-card" style="border-left: 4px solid #8B5CF6;">
<div class="stat-label">PRÓXIMA ETAPA GERAL</div>
<div style="font-weight: 700; color: #FFF; font-size: 0.95rem;">Convocação do TAF</div>
<div class="stat-sub">Teste de Aptidão Física após a homologação das cotas.</div>
</div>""", unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 🏃‍♂️ Como Funciona a Linha de Corte do TAF (Tabela 13.1 do Edital)")
    st.markdown("""
    O **Item 13 do Edital** estabelece o número máximo de candidatos habilitados para realizar o Teste de Aptidão Física (TAF):
    - **Ampla Concorrência:** até o **960º colocado** + todos os empatados na última nota.
    - **Reserva Étnico-Racial:** até o **240º colocado na cota** + todos os empatados na última nota.
    - **Reserva PCD:** **Sem linha de corte!** Todos os habilitados com a nota mínima (≥ 73 pts) vão para o TAF (Item 13.1.2).
    """)
    
    quadro_taf = [
        {
            "Modalidade": "Ampla Concorrência (AC)",
            "Previsão no Edital": "Até o 960º colocado + empatados",
            "Nota de Corte": "119 pontos",
            "Total de Convocados": "1.095 candidatos",
            "Quem compõe esse grupo": "783 Não Cotistas + 295 Étnico-Raciais + 17 PCDs (todos no Top 960)"
        },
        {
            "Modalidade": "Reserva Étnico-Racial",
            "Previsão no Edital": "Até o 240º colocado na cota + empatados",
            "Nota de Corte": "115 pontos (com desocupação)",
            "Total de Convocados": "608 cotistas étnicos",
            "Quem compõe esse grupo": "295 chamados via Ampla + 313 chamados pela reserva da cota"
        },
        {
            "Modalidade": "Reserva PCD",
            "Previsão no Edital": "Sem linha de corte (Item 13.1.2)",
            "Nota de Corte": "73 pontos (nota mínima da prova)",
            "Total de Convocados": "659 candidatos",
            "Quem compõe esse grupo": "100% dos candidatos PCDs habilitados com a pontuação mínima"
        }
    ]
    st.dataframe(pd.DataFrame(quadro_taf), use_container_width=True, hide_index=True)
    
    st.write("")
    st.markdown("#### 🧮 Simulador Personalizado de Chamadas")
    st.write("Arraste o seletor para simular qualquer número de convocações gerais e veja a linha de corte estimada:")
    
    vagas_sim = st.slider("Simular Quantidade de Candidatos Chamados:", min_value=50, max_value=3000, value=960, step=50)
    cand_sim = df_base.iloc[vagas_sim - 1]
    nota_sim = int(cand_sim['Nota Objetiva'])
    empatados_sim = int((df_base['Nota Objetiva'] >= nota_sim).sum())
    
    grupo_sim = df_base.head(vagas_sim)
    qtd_ac_sim = int((grupo_sim['Ampla_Pura']).sum())
    qtd_etnico_sim = int((grupo_sim['Cota_Etnico_Racial']).sum())
    qtd_pcd_sim = int((grupo_sim['Cota_PCD']).sum())
    
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Nota de Corte na Simulação", f"{nota_sim} pts", f"{vagas_sim}º colocado geral")
    s2.metric("Total com Empates na Nota", f"{empatados_sim} candidatos", f"Empatados em {nota_sim} pts")
    s3.metric("Não Cotistas no Grupo", f"{qtd_ac_sim}", f"{(qtd_ac_sim/vagas_sim)*100:.1f}% do total")
    s4.metric("Cotistas no Grupo", f"{qtd_etnico_sim + qtd_pcd_sim}", f"{qtd_etnico_sim} Étnicos | {qtd_pcd_sim} PCD")

    st.write("")
    st.markdown("#### ❓ Perguntas Frequentes (FAQ Rápido)")
    with st.expander("Por que candidatos cotistas aparecem na convocação da Ampla Concorrência?"):
        st.markdown("""
        Conforme a **Lei Estadual de Cotas** e o **Item 7.3 do Edital**, os candidatos inscritos para vagas reservadas concorrem concomitantemente às vagas destinadas à Ampla Concorrência.
        
        Se a nota do cotista for suficiente para colocá-lo dentro do Top 960 da Geral, **ele é convocado pela Ampla Concorrência**. Isso é fundamental para a política afirmativa, pois a vaga reservada da cota fica livre para convocar outro candidato cotista que esteja mais atrás na pontuação!
        """)
        
    with st.expander("Quem precisa viajar para Natal nos dias 17 e 18 de outubro?"):
        st.markdown("""
        **Apenas** os candidatos expressamente convocados para:
        - **Heteroidentificação** (Pretos e Pardos);
        - **Análise Documental Presencial** (Indígenas e Quilombolas);
        - **Perícia Médica** (PCD).
        
        Os candidatos da **Ampla Concorrência pura (não cotistas)** NÃO participam das etapas de 17 e 18 de outubro. A próxima etapa para a Ampla será a convocação para o TAF.
        """)
        
    with st.expander("O que levar no dia da heteroidentificação ou perícia PCD?"):
        st.markdown("""
        - Documento oficial de identidade original com foto;
        - Comprovante/Cartão de Informação impresso com local e horário (emitido no site da banca `avalia.org.br` a partir de 13/10);
        - Para candidatos PCD: laudos médicos originais com CID e exames comprobatórios;
        - Para Indígenas e Quilombolas: documentação original comprobatória exigida no edital.
        """)

# ==============================================================================
# RODAPÉ
# ==============================================================================
st.write("---")
st.markdown("""<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 10px 0;">
🛡️ <strong>Portal de Resultados Definitivos PPRN</strong> • Dados extraídos do Edital de Resultado Definitivo Pós-Recursos e Editais de Convocação de Cotas (09/10/2026).<br>
Construído com Python & Streamlit • Hospedagem Streamlit Community Cloud
</div>""", unsafe_allow_html=True)
