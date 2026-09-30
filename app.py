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
    page_title="PPRN - Resultado & Análise de Cotas",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# ESTILOS CSS CUSTOMIZADOS (DESIGN SYSTEM ELEGANTE & MODERNO)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Hero */
    .hero-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.98) 0%, rgba(30, 58, 138, 0.65) 50%, rgba(15, 23, 42, 0.98) 100%);
        border: 1px solid rgba(59, 130, 246, 0.35);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 20px rgba(59, 130, 246, 0.15);
    }
    
    .badge-pill {
        display: inline-block;
        background: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(96, 165, 250, 0.3);
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 12px;
    }
    
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0 0 8px 0;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        color: #94A3B8;
        font-size: 0.98rem;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Stat Cards */
    .stat-card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: rgba(96, 165, 250, 0.4);
    }
    
    .stat-label {
        color: #94A3B8;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 5px;
    }
    
    .stat-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
    }
    
    .stat-sub {
        font-size: 0.75rem;
        color: #64748B;
        margin-top: 4px;
    }
    
    /* Candidate Spotlight Card */
    .candidate-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
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
        font-size: 1.2rem;
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
    
    .card-previsao {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        margin-top: 15px;
    }
    
    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 10px 10px 0px 0px;
        gap: 8px;
        padding: 10px 18px;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(37, 99, 235, 0.2) !important;
        border-color: rgba(59, 130, 246, 0.5) !important;
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

@st.cache_data(show_spinner="Carregando base tratada com desempates e cotas do Edital...")
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

# Totais gerais
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

# ==============================================================================
# HEADER HERO & VISÃO GERAL
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <span class="badge-pill">🛡️ POLÍCIA PENAL DO RN (PPRN) • CONCURSO 002/2026</span>
    <h1 class="hero-title">Portal de Resultados • Classificação & Análise de Cotas</h1>
    <p class="hero-subtitle">
        Dados completos tratados conforme o <strong>Edital Geral</strong> e o <strong>Edital de Resultado Preliminar</strong>.
        Separação precisa entre <strong>Ampla Concorrência</strong>, <strong>Cotas Étnico-Raciais (Pretos, Pardos, Indígenas, Quilombolas)</strong> e <strong>PCD</strong>, com aplicação das regras oficiais de desempate e previsão de convocação do TAF.
    </p>
</div>
""", unsafe_allow_html=True)

# 5 Métricas Principais
m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">👥 Total Aprovados</div>
        <div class="stat-value">{TOTAL_CANDIDATOS:,}</div>
        <div class="stat-sub">100% da lista objetiva</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">🏛️ Não Cotistas (Ampla)</div>
        <div class="stat-value">{TOTAL_AMPLA_PURA:,}</div>
        <div class="stat-sub">{(TOTAL_AMPLA_PURA/TOTAL_CANDIDATOS)*100:.1f}% dos candidatos</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">🧑🏿 Étnico-Racial</div>
        <div class="stat-value">{TOTAL_ETNICO:,}</div>
        <div class="stat-sub">{(TOTAL_ETNICO/TOTAL_CANDIDATOS)*100:.1f}% (Preto/Pardo/Ind/Quil)</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">♿ PCD</div>
        <div class="stat-value">{TOTAL_PCD:,}</div>
        <div class="stat-sub">{(TOTAL_PCD/TOTAL_CANDIDATOS)*100:.1f}% ({TOTAL_PCD_ETNICO} com dupla cota)</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

with m5:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">🏆 Maior Nota</div>
        <div class="stat-value">{MAIOR_NOTA} <span style="font-size: 0.9rem; color: #94A3B8;">/ {NOTA_MAXIMA_PROVA}</span></div>
        <div class="stat-sub">Média geral: {MEDIA_NOTA:.1f} pts</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==============================================================================
# NAVEGAÇÃO PRINCIPAL EM ABAS
# ==============================================================================
tab_busca, tab_listas, tab_stats, tab_simulador, tab_comparador, tab_deploy = st.tabs([
    "🔍 Consulta Individual",
    "📋 As 4 Listas Oficiais do Edital",
    "📊 Raio-X & Análise por Cotas",
    "🎯 Previsão TAF & Simulador de Vagas",
    "⚔️ Comparador de Candidatos",
    "🚀 Publicar no Streamlit Cloud"
])

# ==============================================================================
# ABA 1: CONSULTA INDIVIDUAL (BOLETIM DO CANDIDATO COM COTAS)
# ==============================================================================
with tab_busca:
    st.subheader("🔍 Localize seu Desempenho e Situação nas Cotas")
    st.write("Digite o seu **Nome** (ou parte dele) ou o número da sua **Inscrição**:")
    
    col_search, col_action = st.columns([3, 1])
    with col_search:
        termo_busca = st.text_input(
            "Buscar por Nome ou Inscrição",
            placeholder="Exemplo: Liliane Pequeno, Herbert Ryan ou 2320012112...",
            label_visibility="collapsed"
        )
    with col_action:
        st.write("")
        st.caption("💡 Busca flexível (ignora acentos e maiúsculas)")
    
    candidato_selecionado = None
    
    if termo_busca.strip():
        termo_norm = normalizar_texto(termo_busca)
        mascara = (
            df_base['Nome_Busca'].str.contains(termo_norm, na=False) |
            df_base['Inscrição_Str'].str.contains(termo_norm, na=False)
        )
        resultados_busca = df_base[mascara]
        
        if len(resultados_busca) == 0:
            st.warning("⚠️ Nenhum candidato encontrado com o termo informado. Verifique a grafia ou o número da inscrição.")
        elif len(resultados_busca) == 1:
            candidato_selecionado = resultados_busca.iloc[0]
        else:
            st.info(f"🔎 Encontrados **{len(resultados_busca)}** candidatos. Selecione o seu abaixo:")
            opcoes = [
                f"{row['Posição_Geral']}º Geral - {row['Nome']} (Inscrição: {row['Inscrição']} | {row['Modalidade_Concorrencia']} | Nota: {row['Nota Objetiva']} pts)"
                for _, row in resultados_busca.head(50).iterrows()
            ]
            escolha = st.selectbox("Selecione o candidato:", opcoes)
            idx_geral = int(escolha.split("º")[0]) - 1
            candidato_selecionado = df_base.iloc[idx_geral]
    else:
        st.caption("Dica: Experimente buscar seu nome. Como demonstração, exibindo o 1º colocado geral abaixo:")
        candidato_selecionado = df_base.iloc[0]

    # Exibição do Perfil do Candidato
    if candidato_selecionado is not None:
        pos_geral = int(candidato_selecionado['Posição_Geral'])
        pos_orig = int(candidato_selecionado.get('Posição_Original', pos_geral))
        nome = candidato_selecionado['Nome']
        inscricao = candidato_selecionado['Inscrição']
        nota_total = int(candidato_selecionado['Nota Objetiva'])
        aproveitamento_total = (nota_total / NOTA_MAXIMA_PROVA) * 100
        percentil = ((TOTAL_CANDIDATOS - pos_geral + 1) / TOTAL_CANDIDATOS) * 100
        top_pct = 100 - percentil
        
        modalidade = candidato_selecionado['Modalidade_Concorrencia']
        is_pcd = candidato_selecionado['Cota_PCD']
        is_etnico = candidato_selecionado['Cota_Etnico_Racial']
        is_ampla_pura = candidato_selecionado['Ampla_Pura']
        
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
        
        st.markdown(f"""
        <div class="candidate-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
                <div>
                    <span class="badge-pill">BOLETIM OFICIAL INDIVIDUAL</span>
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
                        Top {top_pct:.2f}% de todos os 18.944 candidatos
                    </div>
                </div>
            </div>
            
            <div class="card-previsao">
                <div style="font-size: 0.82rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; margin-bottom: 8px;">
                    🎯 PREVISÃO OFICIAL CONFORME REGRAS DO EDITAL (PROVA OBJETIVA)
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 20px; font-size: 0.95rem; color: #F1F5F9;">
                    <div><strong>🏃‍♂️ Status Convocação TAF:</strong> {candidato_selecionado['Previsao_TAF']}</div>
                    <div><strong>🏆 Vagas Imediatas:</strong> {candidato_selecionado['Previsao_Vagas_Imediatas']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Posições Específicas em Cada Lista
        col_pos1, col_pos2, col_pos3, col_pos4 = st.columns(4)
        with col_pos1:
            st.metric("Posição Geral Oficial", f"{pos_geral}º", f"De 18.944 (Desempate Edital)")
        with col_pos2:
            if is_etnico and pd.notnull(candidato_selecionado['Pos_Lista_Etnico']):
                st.metric("Posição Cota Étnica", f"{int(candidato_selecionado['Pos_Lista_Etnico'])}º", f"De {TOTAL_ETNICO} cotistas étnicos")
            else:
                st.metric("Posição Cota Étnica", "N/A", "Não optou por cota étnica")
        with col_pos3:
            if is_pcd and pd.notnull(candidato_selecionado['Pos_Lista_PCD']):
                st.metric("Posição Cota PCD", f"{int(candidato_selecionado['Pos_Lista_PCD'])}º", f"De {TOTAL_PCD} cotistas PCD")
            else:
                st.metric("Posição Cota PCD", "N/A", "Não optou por PCD")
        with col_pos4:
            if is_ampla_pura and pd.notnull(candidato_selecionado['Pos_Lista_Ampla_Pura']):
                st.metric("Posição Não Cotista", f"{int(candidato_selecionado['Pos_Lista_Ampla_Pura'])}º", f"De {TOTAL_AMPLA_PURA} da Ampla Pura")
            else:
                st.metric("Posição na Ampla", f"{pos_geral}º Geral", "Concorre concomitantemente")
                
        st.write("")
        
        # Gráficos de Análise Individual
        col_radar, col_bar = st.columns(2)
        
        with col_radar:
            st.markdown("#### 🕸️ Desempenho vs. Média da Prova")
            medias_disciplinas = [df_base[d].mean() for d in DISCIPLINAS]
            notas_candidato = [candidato_selecionado[d] for d in DISCIPLINAS]
            nomes_curtos = [
                d.replace("História do RN e Aspectos Geoeconômicos do RN", "História RN")
                 .replace("Ética no Serviço Público", "Ética")
                 .replace("Direito Penal e Processo Penal", "Penal / Proc.")
                 .replace("Legislação Específica", "Leg. Específica")
                for d in DISCIPLINAS
            ]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=notas_candidato,
                theta=nomes_curtos,
                fill='toself',
                name='Candidato',
                line_color='#3B82F6',
                fillcolor='rgba(59, 130, 246, 0.35)'
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=medias_disciplinas,
                theta=nomes_curtos,
                fill='toself',
                name='Média Geral (18.944)',
                line_color='#94A3B8',
                fillcolor='rgba(148, 163, 184, 0.15)',
                line_dash='dot'
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, showticklabels=True, gridcolor='rgba(255, 255, 255, 0.1)'),
                    angularaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
                ),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=20, b=40),
                height=380
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
        with col_bar:
            st.markdown("#### 📊 Aproveitamento (%) por Disciplina")
            pct_candidato = [
                (candidato_selecionado[d] / PONTOS_MAXIMOS[d]) * 100 for d in DISCIPLINAS
            ]
            cores = [
                '#10B981' if p >= 80 else ('#F59E0B' if p >= 60 else '#EF4444')
                for p in pct_candidato
            ]
            
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
                xaxis=dict(range=[0, 105], title="Aproveitamento (%)", gridcolor='rgba(255, 255, 255, 0.1)'),
                yaxis=dict(autorange="reversed"),
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=20, t=20, b=40),
                height=380
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Detalhamento Matéria por Matéria
        st.markdown("#### 📋 Detalhamento Ponto a Ponto das Disciplinas")
        dados_detalhamento = []
        for d in DISCIPLINAS:
            nota_cand = int(candidato_selecionado[d])
            max_p = PONTOS_MAXIMOS[d]
            aprov = (nota_cand / max_p) * 100
            media_disc = df_base[d].mean()
            diff_media = nota_cand - media_disc
            dados_detalhamento.append({
                "Disciplina": d,
                "Sua Nota": f"{nota_cand} pts",
                "Pontos Máximos": f"{max_p} pts",
                "Aproveitamento": f"{aprov:.1f}%",
                "Média Geral da Prova": f"{media_disc:.2f} pts",
                "Desempenho Relativo": f"{diff_media:+.2f} pts" + (" 🟢 Acima" if diff_media > 0 else " 🔴 Abaixo")
            })
        st.dataframe(pd.DataFrame(dados_detalhamento), use_container_width=True, hide_index=True)
        
        # Vizinhança de Classificação (+/- 5 concorrentes ao redor)
        st.markdown("#### 👥 Candidatos Próximos na Classificação Geral")
        st.caption("Veja os candidatos imediatamente antes e depois da sua posição:")
        start_idx = max(0, pos_geral - 6)
        end_idx = min(TOTAL_CANDIDATOS, pos_geral + 5)
        vizinhos = df_base.iloc[start_idx:end_idx][['Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Nota Objetiva', 'Execução Penal', 'Legislação Específica', 'Direito Penal e Processo Penal', 'Língua Portuguesa']]
        
        def destacar_linha(row):
            if row['Posição_Geral'] == pos_geral:
                return ['background-color: rgba(59, 130, 246, 0.35); font-weight: bold;'] * len(row)
            return [''] * len(row)
            
        st.dataframe(
            vizinhos.style.apply(destacar_linha, axis=1),
            use_container_width=True,
            hide_index=True
        )

# ==============================================================================
# ABA 2: AS 4 LISTAS OFICIAIS DO EDITAL (ITEM 21.3)
# ==============================================================================
with tab_listas:
    st.subheader("📋 As 4 Listas Oficiais do Concurso (Item 21.3 do Edital)")
    st.write("""
    Conforme o **Item 21.3 do Edital**, o resultado é publicado em listas oficiais separadas.
    Aqui você pode visualizar, filtrar e baixar cada uma das listas individualmente em formato Excel oficial:
    """)
    
    tipo_lista = st.radio(
        "Selecione a Lista que deseja visualizar e baixar:",
        [
            f"🌐 1. Lista Geral Oficial (AC Universal - {TOTAL_CANDIDATOS:,} candidatos)",
            f"🧑🏿 2. Lista Étnico-Racial (Pretos, Pardos, Indígenas, Quilombolas - {TOTAL_ETNICO:,} candidatos)",
            f"♿ 3. Lista de Pessoas com Deficiência - PCD ({TOTAL_PCD:,} candidatos)",
            f"🏛️ 4. Lista Ampla Concorrência (Apenas Não Cotistas - {TOTAL_AMPLA_PURA:,} candidatos)"
        ],
        index=0
    )
    
    st.write("---")
    
    if "1. Lista Geral Oficial" in tipo_lista:
        df_view = df_base.copy()
        pos_col = 'Posição_Geral'
        nome_arquivo_excel = "LISTA_OFICIAL_GERAL_PPRN.xlsx"
        titulo_lista = "Lista Geral (AC Universal) - Todos os Candidatos Aprovados"
        corte_taf_info = "Top 960 (119 pts) + empates = 1.095 convocados"
        
    elif "2. Lista Étnico-Racial" in tipo_lista:
        df_view = df_base[df_base['Cota_Etnico_Racial']].copy().sort_values(by="Pos_Lista_Etnico", ascending=True)
        pos_col = 'Pos_Lista_Etnico'
        nome_arquivo_excel = "LISTA_OFICIAL_ETNICO_RACIAL_PPRN.xlsx"
        titulo_lista = "Lista de Reserva Étnico-Racial (Pretos, Pardos, Indígenas e Quilombolas)"
        corte_taf_info = "Top 240 na cota (120 pts direto / 115 pts com aproveitamento da ampla)"
        
    elif "3. Lista de Pessoas com Deficiência" in tipo_lista:
        df_view = df_base[df_base['Cota_PCD']].copy().sort_values(by="Pos_Lista_PCD", ascending=True)
        pos_col = 'Pos_Lista_PCD'
        nome_arquivo_excel = "LISTA_OFICIAL_PCD_PPRN.xlsx"
        titulo_lista = "Lista de Pessoas com Deficiência (PCD)"
        corte_taf_info = "Sem linha de corte! Todos os 659 PCDs habilitados vão para o TAF (Item 13.1.2)"
        
    else:
        df_view = df_base[df_base['Ampla_Pura']].copy().sort_values(by="Pos_Lista_Ampla_Pura", ascending=True)
        pos_col = 'Pos_Lista_Ampla_Pura'
        nome_arquivo_excel = "LISTA_OFICIAL_AMPLA_CONCORRENCIA_PURA_PPRN.xlsx"
        titulo_lista = "Lista Exclusiva de Candidatos Não Cotistas (Ampla Concorrência Pura)"
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
        
    cols_tabela = [pos_col, 'Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Nota Objetiva', 'Execução Penal', 'Legislação Específica', 'Direito Penal e Processo Penal', 'Língua Portuguesa', 'Previsao_TAF', 'Previsao_Vagas_Imediatas']
    
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
# ABA 3: RAIO-X & ANÁLISE POR COTAS
# ==============================================================================
with tab_stats:
    st.subheader("📊 Raio-X & Comparativo entre Ampla e Cotas")
    st.write("Análise detalhada de distribuição de notas, médias comparativas e comportamento das notas por cota:")
    
    # Médias comparativas
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    with col_c1:
        st.metric("Média Ampla Concorrência", f"{df_base[df_base['Ampla_Pura']]['Nota Objetiva'].mean():.2f} pts", "12.134 candidatos")
    with col_c2:
        st.metric("Média Étnico-Racial", f"{df_base[df_base['Cota_Etnico_Racial']]['Nota Objetiva'].mean():.2f} pts", "6.309 candidatos")
    with col_c3:
        st.metric("Média PCD", f"{df_base[df_base['Cota_PCD']]['Nota Objetiva'].mean():.2f} pts", "659 candidatos")
    with col_c4:
        st.metric("Média Geral da Prova", f"{MEDIA_NOTA:.2f} pts", "18.944 candidatos")
        
    st.write("")
    
    # Gráfico de Boxplot / Distribuição comparativa
    st.markdown("#### 📦 Distribuição das Notas por Modalidade de Concorrência")
    fig_box = px.box(
        df_base,
        x="Modalidade_Concorrencia",
        y="Nota Objetiva",
        color="Modalidade_Concorrencia",
        title="Dispersão de Notas por Modalidade",
        points="outliers"
    )
    fig_box.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        showlegend=False,
        xaxis_tickangle=-15
    )
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Histograma Geral de Notas com Linha de Corte
    st.markdown("#### 📈 Histograma de Notas com Marcos de Convocação")
    fig_hist = px.histogram(
        df_base,
        x="Nota Objetiva",
        color="Cota_Etnico_Racial",
        nbins=65,
        title="Frequência de Candidatos (Azul = Ampla | Laranja = Étnico-Racial)",
        labels={"Cota_Etnico_Racial": "Étnico-Racial"}
    )
    fig_hist.add_vline(x=128, line_dash="dash", line_color="#10B981", annotation_text="Corte Vagas Imediatas (128 pts)", annotation_position="top left")
    fig_hist.add_vline(x=119, line_dash="dash", line_color="#F59E0B", annotation_text="Corte TAF Ampla (119 pts)", annotation_position="top right")
    fig_hist.add_vline(x=115, line_dash="dot", line_color="#8B5CF6", annotation_text="Corte TAF Étnico Real (115 pts)", annotation_position="bottom left")
    
    fig_hist.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=380,
        yaxis_title="Quantidade de Candidatos"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# ==============================================================================
# ABA 4: PREVISÃO TAF & SIMULADOR DE VAGAS DO EDITAL
# ==============================================================================
with tab_simulador:
    st.subheader("🎯 Previsão Oficial de Convocação para o TAF (Tabela 13.1)")
    st.markdown("""
    O **Item 13 do Edital** estabelece os limites máximos de classificação para convocação ao Teste de Aptidão Física (TAF):
    - **Ampla Concorrência:** até o **960º colocado** + todos os empatados na última nota.
    - **Reserva Étnico-Racial:** até o **240º colocado** + todos os empatados na última nota.
    - **PCD:** **Sem linha de corte!** Todos os aprovados com nota mínima (≥ 73 pts) são convocados (Item 13.1.2).
    """)
    
    st.markdown("#### 📊 Quadro Resumo da Previsão Oficial do TAF")
    quadro_taf = [
        {
            "Modalidade": "Ampla Concorrência (AC)",
            "Vagas no Edital (Tab 13.1)": "Até 960º",
            "Corte Estimado": "119 pontos",
            "Convocados Reais (com empates)": "1.095 candidatos",
            "Composição do Grupo": "783 Não Cotistas + 295 Étnico-Raciais + 17 PCDs no Top 960"
        },
        {
            "Modalidade": "Reserva Étnico-Racial",
            "Vagas no Edital (Tab 13.1)": "Até 240º",
            "Corte Estimado": "115 pontos (com desocupação)",
            "Convocados Reais (com empates)": "608 cotistas étnicos no total",
            "Composição do Grupo": "295 convocados via Ampla + 313 convocados pela cota"
        },
        {
            "Modalidade": "PCD (Pessoa com Deficiência)",
            "Vagas no Edital (Tab 13.1)": "Todos os habilitados",
            "Corte Estimado": "73 pontos (nota mínima)",
            "Convocados Reais (com empates)": "659 candidatos",
            "Composição do Grupo": "100% dos candidatos PCD aprovados (sem linha de corte)"
        }
    ]
    st.dataframe(pd.DataFrame(quadro_taf), use_container_width=True, hide_index=True)
    
    st.write("---")
    st.markdown("#### 🧮 Simulador Personalizado de Chamadas")
    st.write("Simule um número arbitrário de convocações gerais para ver a linha de corte e a distribuição de cotas:")
    
    vagas_sim = st.slider("Simular Quantidade de Vagas Convocadas:", min_value=50, max_value=3000, value=960, step=50)
    cand_sim = df_base.iloc[vagas_sim - 1]
    nota_sim = int(cand_sim['Nota Objetiva'])
    empatados_sim = (df_base['Nota Objetiva'] >= nota_sim).sum()
    
    grupo_sim = df_base.head(vagas_sim)
    qtd_ac_sim = (grupo_sim['Ampla_Pura']).sum()
    qtd_etnico_sim = (grupo_sim['Cota_Etnico_Racial']).sum()
    qtd_pcd_sim = (grupo_sim['Cota_PCD']).sum()
    
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Nota de Corte na Simulação", f"{nota_sim} pts", f"{vagas_sim}º colocado")
    s2.metric("Total com Empates na Nota", f"{empatados_sim} pessoas", f"Empatados em {nota_sim} pts")
    s3.metric("Não Cotistas no Grupo", f"{qtd_ac_sim} ({qtd_ac_sim/vagas_sim*100:.1f}%)")
    s4.metric("Cotistas no Grupo", f"{qtd_etnico_sim} Étnicos | {qtd_pcd_sim} PCD")
    
    st.dataframe(
        grupo_sim[['Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Nota Objetiva', 'Execução Penal', 'Legislação Específica', 'Previsao_TAF']].head(100),
        use_container_width=True,
        hide_index=True
    )

# ==============================================================================
# ABA 5: COMPARADOR DE CANDIDATOS
# ==============================================================================
with tab_comparador:
    st.subheader("⚔️ Confronto Direto entre Candidatos")
    st.write("Compare dois candidatos quaisquer da lista geral ou de cotas matéria a matéria:")
    
    col_comp1, col_comp2 = st.columns(2)
    with col_comp1:
        st.markdown("##### 👤 1º Candidato")
        termo_c1 = st.text_input("Buscar Nome ou Inscrição:", value="Liliane", key="busca_c1")
        filtro_c1 = df_base[
            df_base['Nome_Busca'].str.contains(normalizar_texto(termo_c1), na=False) |
            df_base['Inscrição_Str'].str.contains(normalizar_texto(termo_c1), na=False)
        ]
        if len(filtro_c1) > 0:
            opcoes_c1 = [
                f"{row['Posição_Geral']}º - {row['Nome']} (Nota: {row['Nota Objetiva']} pts | {row['Modalidade_Concorrencia']})"
                for _, row in filtro_c1.head(30).iterrows()
            ]
            escolha_c1 = st.selectbox("Selecione o 1º candidato:", opcoes_c1, key="sel_c1")
            pos_c1 = int(escolha_c1.split("º")[0]) - 1
            c1_dados = df_base.iloc[pos_c1]
        else:
            st.warning("Nenhum candidato encontrado para o 1º campo.")
            c1_dados = df_base.iloc[0]

    with col_comp2:
        st.markdown("##### 👤 2º Candidato")
        termo_c2 = st.text_input("Buscar Nome ou Inscrição:", value="Herbert", key="busca_c2")
        filtro_c2 = df_base[
            df_base['Nome_Busca'].str.contains(normalizar_texto(termo_c2), na=False) |
            df_base['Inscrição_Str'].str.contains(normalizar_texto(termo_c2), na=False)
        ]
        if len(filtro_c2) > 0:
            opcoes_c2 = [
                f"{row['Posição_Geral']}º - {row['Nome']} (Nota: {row['Nota Objetiva']} pts | {row['Modalidade_Concorrencia']})"
                for _, row in filtro_c2.head(30).iterrows()
            ]
            escolha_c2 = st.selectbox("Selecione o 2º candidato:", opcoes_c2, key="sel_c2")
            pos_c2 = int(escolha_c2.split("º")[0]) - 1
            c2_dados = df_base.iloc[pos_c2]
        else:
            st.warning("Nenhum candidato encontrado para o 2º campo.")
            c2_dados = df_base.iloc[1]
    
    diff_total = int(c1_dados['Nota Objetiva']) - int(c2_dados['Nota Objetiva'])
    
    if diff_total > 0:
        st.success(f"🏆 **{c1_dados['Nome']}** ({c1_dados['Posição_Geral']}º) está à frente por **+{diff_total} pontos** ({c1_dados['Nota Objetiva']} vs. {c2_dados['Nota Objetiva']} pts).")
    elif diff_total < 0:
        st.success(f"🏆 **{c2_dados['Nome']}** ({c2_dados['Posição_Geral']}º) está à frente por **+{abs(diff_total)} pontos** ({c2_dados['Nota Objetiva']} vs. {c1_dados['Nota Objetiva']} pts).")
    else:
        st.info(f"🤝 **Empate em {c1_dados['Nota Objetiva']} pontos!** Desempate do edital: {c1_dados['Nome']} ({c1_dados['Posição_Geral']}º) vs {c2_dados['Nome']} ({c2_dados['Posição_Geral']}º).")
        
    # Gráfico comparativo de barras
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name=f"{c1_dados['Nome']} ({c1_dados['Posição_Geral']}º)",
        x=DISCIPLINAS,
        y=[c1_dados[d] for d in DISCIPLINAS],
        marker_color='#3B82F6'
    ))
    fig_comp.add_trace(go.Bar(
        name=f"{c2_dados['Nome']} ({c2_dados['Posição_Geral']}º)",
        x=DISCIPLINAS,
        y=[c2_dados[d] for d in DISCIPLINAS],
        marker_color='#10B981'
    ))
    fig_comp.update_layout(
        barmode='group',
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Pontos",
        xaxis_tickangle=-30,
        height=380,
        margin=dict(l=20, r=20, t=30, b=80),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_comp, use_container_width=True)
    
    # Tabela de confronto
    confronto_rows = []
    for d in DISCIPLINAS:
        n1 = int(c1_dados[d])
        n2 = int(c2_dados[d])
        if n1 > n2:
            vantagem = f"🟢 +{n1 - n2} pts ({c1_dados['Nome'].split()[0]})"
        elif n2 > n1:
            vantagem = f"🔵 +{n2 - n1} pts ({c2_dados['Nome'].split()[0]})"
        else:
            vantagem = "⚪ Empate"
        confronto_rows.append({
            "Disciplina": d,
            f"{c1_dados['Nome']}": f"{n1} pts",
            f"{c2_dados['Nome']}": f"{n2} pts",
            "Vantagem": vantagem
        })
    st.dataframe(pd.DataFrame(confronto_rows), use_container_width=True, hide_index=True)

# ==============================================================================
# ABA 6: GUIA COMPLETO DE HOSPEDAGEM NO STREAMLIT CLOUD (GRÁTIS)
# ==============================================================================
with tab_deploy:
    st.subheader("🚀 Como Hospedar no Streamlit Community Cloud")
    st.markdown("""
    O site já está configurado e pronto para a nuvem! Todas as 4 planilhas oficiais, os dados tratados e os arquivos de configuração estão no repositório.
    
    👉 **Link do Repositório no GitHub:** [https://github.com/Pedra1/pprn-analises](https://github.com/Pedra1/pprn-analises)
    
    Para publicar em 1 clique:
    1. Acesse: **[share.streamlit.io](https://share.streamlit.io)**
    2. Clique em **"Create app"**
    3. Selecione o repositório `Pedra1/pprn-analises`, branch `main` e arquivo `app.py`.
    4. Clique em **"Deploy!"**.
    """)

# ==============================================================================
# RODAPÉ
# ==============================================================================
st.write("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 10px 0;">
    🛡️ <strong>Portal de Análises Independentes PPRN</strong> • Dados extraídos do Edital de Resultado Preliminar e Editais de Deferimento de Cotas.<br>
    Construído com Python & Streamlit • Hospedagem Streamlit Community Cloud
</div>
""", unsafe_allow_html=True)
