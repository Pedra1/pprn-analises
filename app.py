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
    page_title="PPRN - Resultado Policial Penal RN",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# ESTILOS CSS CUSTOMIZADOS (DESIGN SYSTEM ELEGANTE & MODERNO)
# ==============================================================================
st.markdown("""
<style>
    /* Tipografia e Fundo */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Hero */
    .hero-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 58, 138, 0.6) 50%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 15px rgba(59, 130, 246, 0.15);
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
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0 0 8px 0;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.02rem;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Stat Cards */
    .stat-card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: rgba(96, 165, 250, 0.4);
    }
    
    .stat-label {
        color: #94A3B8;
        font-size: 0.82rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 6px;
    }
    
    .stat-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
    }
    
    .stat-sub {
        font-size: 0.78rem;
        color: #64748B;
        margin-top: 5px;
    }
    
    /* Candidate Spotlight Card */
    .candidate-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(59, 130, 246, 0.35);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    
    .pos-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 8px;
        font-size: 1.25rem;
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
        padding: 10px 20px;
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
# CARREGAMENTO E PROCESSAMENTO DOS DADOS (COM CACHE ULTRA-RÁPIDO)
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
    """Remove acentos e coloca em caixa alta para busca flexível."""
    if not isinstance(texto, str):
        texto = str(texto)
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn').upper().strip()

@st.cache_data(show_spinner="Carregando dados da lista oficial do PPRN...")
def carregar_dados():
    parquet_path = "pprn_dados.parquet"
    excel_path = "LISTA PPRN POLICIAL PENAL ORGANIZADA NOTA DECRESCENTE.xlsx"
    
    df = None
    if os.path.exists(parquet_path):
        try:
            df = pd.read_parquet(parquet_path)
        except Exception:
            df = None
            
    if df is None:
        if os.path.exists(excel_path):
            df = pd.read_excel(excel_path, skiprows=4)
            standard_columns = [
                'Nome',
                'Inscrição',
                'Língua Portuguesa',
                'História do RN',
                'Ética no Serviço Público',
                'Direito Constitucional',
                'Direito Administrativo',
                'Direitos Humanos',
                'Execução Penal',
                'Legislação Específica',
                'Direito Penal e Processo Penal',
                'Nota Objetiva'
            ]
            df.columns = standard_columns
            df.insert(0, 'Posição', range(1, len(df) + 1))
            df['Nome_Busca'] = df['Nome'].apply(normalizar_texto)
            df['Inscrição_Str'] = df['Inscrição'].astype(str)
            try:
                df.to_parquet(parquet_path, index=False)
            except Exception:
                pass
        else:
            return None

    # Garantir colunas essenciais
    if 'Posição' not in df.columns:
        df.insert(0, 'Posição', range(1, len(df) + 1))
    if 'Nome_Busca' not in df.columns:
        df['Nome_Busca'] = df['Nome'].apply(normalizar_texto)
    if 'Inscrição_Str' not in df.columns:
        df['Inscrição_Str'] = df['Inscrição'].astype(str)
        
    return df

df_base = carregar_dados()

if df_base is None:
    st.error("⚠️ O arquivo da planilha não foi encontrado. Por favor, certifique-se de que `LISTA PPRN POLICIAL PENAL ORGANIZADA NOTA DECRESCENTE.xlsx` ou `pprn_dados.parquet` estão na pasta da aplicação.")
    st.stop()

# Estatísticas Gerais Pré-calculadas
TOTAL_CANDIDATOS = len(df_base)
MAIOR_NOTA = int(df_base['Nota Objetiva'].max())
MENOR_NOTA = int(df_base['Nota Objetiva'].min())
MEDIA_NOTA = float(df_base['Nota Objetiva'].mean())
MEDIANA_NOTA = float(df_base['Nota Objetiva'].median())

# ==============================================================================
# HEADER HERO & VISÃO GERAL
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <span class="badge-pill">🛡️ SEAP / GOVERNO DO ESTADO DO RN • EDITAL PRELIMINAR</span>
    <h1 class="hero-title">Portal de Resultados • Policial Penal RN</h1>
    <p class="hero-subtitle">
        Consulta completa dos <strong>18.944</strong> candidatos classificados na prova objetiva.
        Busca individual com raio-x de desempenho, ranking completo, simulador de corte e estatísticas detalhadas.
    </p>
</div>
""", unsafe_allow_html=True)

# Linha de métricas principais
m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">👥 Candidatos</div>
        <div class="stat-value">{TOTAL_CANDIDATOS:,}</div>
        <div class="stat-sub">Classificados na lista</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">🏆 Maior Nota</div>
        <div class="stat-value">{MAIOR_NOTA} <span style="font-size: 1rem; color: #94A3B8;">/ {NOTA_MAXIMA_PROVA}</span></div>
        <div class="stat-sub">Aproveitamento de {(MAIOR_NOTA/NOTA_MAXIMA_PROVA)*100:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">📊 Média Geral</div>
        <div class="stat-value">{MEDIA_NOTA:.1f}</div>
        <div class="stat-sub">{(MEDIA_NOTA/NOTA_MAXIMA_PROVA)*100:.1f}% de aproveitamento</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">🎯 Mediana</div>
        <div class="stat-value">{MEDIANA_NOTA:.0f}</div>
        <div class="stat-sub">50% pontuaram ≥ {MEDIANA_NOTA:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with m5:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">🚪 Corte Mínimo</div>
        <div class="stat-value">{MENOR_NOTA}</div>
        <div class="stat-sub">Nota do 18.944º colocado</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==============================================================================
# NAVEGAÇÃO PRINCIPAL EM ABAS
# ==============================================================================
tab_busca, tab_ranking, tab_stats, tab_simulador, tab_comparador, tab_deploy = st.tabs([
    "🔍 Consulta Individual",
    "🏆 Classificação Geral",
    "📊 Raio-X & Estatísticas",
    "🎯 Simulador de Vagas",
    "⚔️ Comparador de Candidatos",
    "🚀 Publicar no Streamlit Cloud"
])

# ==============================================================================
# ABA 1: CONSULTA INDIVIDUAL (BOLETIM DO CANDIDATO)
# ==============================================================================
with tab_busca:
    st.subheader("🔍 Localize seu Desempenho")
    st.write("Digite o seu **Nome** (ou parte dele) ou o número da sua **Inscrição** para consultar seu cartão de resultado:")
    
    col_search, col_action = st.columns([3, 1])
    with col_search:
        termo_busca = st.text_input(
            "Buscar por Nome ou Inscrição",
            placeholder="Exemplo: Liliane Pequeno ou 2320012112...",
            label_visibility="collapsed"
        )
    with col_action:
        st.write("")
        st.caption("💡 Busca flexível (ignora acentos e maiúsculas)")
    
    candidato_selecionado = None
    
    if termo_busca.strip():
        termo_norm = normalizar_texto(termo_busca)
        
        # Filtro em memória
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
            st.info(f"🔎 Encontrados **{len(resultados_busca)}** candidatos. Selecione um abaixo para detalhar:")
            opcoes = [
                f"{row['Posição']}º - {row['Nome']} (Inscrição: {row['Inscrição']} | Nota: {row['Nota Objetiva']} pts)"
                for _, row in resultados_busca.head(50).iterrows()
            ]
            escolha = st.selectbox("Selecione o candidato:", opcoes)
            idx_escolhido = int(escolha.split("º")[0]) - 1
            candidato_selecionado = df_base.iloc[idx_escolhido]
    else:
        # Se nada foi digitado, sugerir o 1º colocado como exemplo
        st.caption("Dica: Experimente buscar seu nome. Como demonstração, exibindo o 1º colocado abaixo:")
        candidato_selecionado = df_base.iloc[0]

    # Exibição do Perfil do Candidato
    if candidato_selecionado is not None:
        pos = int(candidato_selecionado['Posição'])
        nome = candidato_selecionado['Nome']
        inscricao = candidato_selecionado['Inscrição']
        nota_total = int(candidato_selecionado['Nota Objetiva'])
        aproveitamento_total = (nota_total / NOTA_MAXIMA_PROVA) * 100
        percentil = ((TOTAL_CANDIDATOS - pos + 1) / TOTAL_CANDIDATOS) * 100
        top_pct = 100 - percentil
        
        # Estilo do badge da posição
        pos_class = "pos-top" if pos <= 100 else "pos-standard"
        medalha = "🥇 " if pos == 1 else ("🥈 " if pos == 2 else ("🥉 " if pos == 3 else "🎖️ "))
        
        st.markdown(f"""
        <div class="candidate-card">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                <div>
                    <span class="badge-pill">BOLETIM INDIVIDUAL DO CANDIDATO</span>
                    <h2 style="color: #FFF; margin: 4px 0 6px 0; font-size: 1.8rem;">{nome}</h2>
                    <p style="color: #94A3B8; margin: 0; font-size: 0.95rem;">
                        Inscrição: <strong>{inscricao}</strong> &nbsp;•&nbsp; Cargo: <strong>401 - Policial Penal RN</strong>
                    </p>
                </div>
                <div style="text-align: right;">
                    <div class="pos-badge {pos_class}">
                        {medalha}{pos}º LUGAR
                    </div>
                    <div style="color: #60A5FA; font-size: 0.85rem; margin-top: 6px; font-weight: 600;">
                        Top {top_pct:.2f}% de todos os 18.944 candidatos
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas de Desempenho do Candidato
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Nota Objetiva", f"{nota_total} pts", f"{aproveitamento_total:.1f}% de acertos")
        c2.metric("Distância do 1º Lugar", f"{nota_total - MAIOR_NOTA} pts" if pos > 1 else "Líder", "Pontos atrás do líder")
        c3.metric("Distância da Média", f"{nota_total - MEDIA_NOTA:+.1f} pts", "Comparado a todos")
        c4.metric("Margem sobre o Corte", f"+{nota_total - MENOR_NOTA} pts", f"Corte mínimo: {MENOR_NOTA} pts")
        
        st.write("")
        
        # Gráficos de Análise Individual
        col_radar, col_bar = st.columns(2)
        
        with col_radar:
            st.markdown("#### 🕸️ Desempenho vs. Média da Concorrência")
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

        # Tabela Detalhada com os Pontos por Matéria
        st.markdown("#### 📋 Detalhamento Ponto a Ponto")
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
                "Pontos Possíveis": f"{max_p} pts",
                "Aproveitamento": f"{aprov:.1f}%",
                "Média Geral": f"{media_disc:.2f} pts",
                "Desempenho Relativo": f"{diff_media:+.2f} pts" + (" 🟢 Acima" if diff_media > 0 else " 🔴 Abaixo")
            })
        st.dataframe(pd.DataFrame(dados_detalhamento), use_container_width=True, hide_index=True)
        
        # Vizinhança de Classificação (+/- 5 candidatos ao redor)
        st.markdown("#### 👥 Candidatos Próximos na Classificação")
        st.caption("Veja os candidatos imediatamente antes e depois da sua posição:")
        start_idx = max(0, pos - 6)
        end_idx = min(TOTAL_CANDIDATOS, pos + 5)
        vizinhos = df_base.iloc[start_idx:end_idx][['Posição', 'Nome', 'Inscrição', 'Nota Objetiva'] + DISCIPLINAS]
        
        # Destacar a linha do candidato
        def destacar_candidato(row):
            if row['Posição'] == pos:
                return ['background-color: rgba(59, 130, 246, 0.35); font-weight: bold;'] * len(row)
            return [''] * len(row)
            
        st.dataframe(
            vizinhos.style.apply(destacar_candidato, axis=1),
            use_container_width=True,
            hide_index=True
        )

# ==============================================================================
# ABA 2: CLASSIFICAÇÃO GERAL & TABELA INTERATIVA
# ==============================================================================
with tab_ranking:
    st.subheader("🏆 Classificação Geral Oficial")
    st.write("Filtre, ordene e exporte a lista completa dos 18.944 candidatos:")
    
    col_f1, col_f2, col_f3 = st.columns([1.5, 1.5, 1])
    
    with col_f1:
        faixa_nota = st.slider(
            "Filtrar por Faixa de Nota Objetiva:",
            min_value=MENOR_NOTA,
            max_value=MAIOR_NOTA,
            value=(MENOR_NOTA, MAIOR_NOTA),
            step=1
        )
        
    with col_f2:
        top_n_opcoes = ["Todos (18.944)", "Top 50", "Top 100", "Top 250", "Top 500", "Top 1000", "Top 2000", "Top 5000"]
        top_n_escolha = st.selectbox("Exibir grupo:", top_n_opcoes, index=1)
        
    with col_f3:
        ordem_col = st.selectbox(
            "Ordenar por:",
            ["Posição (Crescente)", "Nota Objetiva (Decrescente)"] + [f"{d} (Decrescente)" for d in DISCIPLINAS]
        )
        
    # Aplicar Filtros
    df_filtrado = df_base[
        (df_base['Nota Objetiva'] >= faixa_nota[0]) &
        (df_base['Nota Objetiva'] <= faixa_nota[1])
    ]
    
    # Ordenação
    if ordem_col == "Posição (Crescente)":
        df_filtrado = df_filtrado.sort_values(by="Posição", ascending=True)
    elif ordem_col == "Nota Objetiva (Decrescente)":
        df_filtrado = df_filtrado.sort_values(by="Nota Objetiva", ascending=False)
    else:
        disc_nome = ordem_col.replace(" (Decrescente)", "")
        df_filtrado = df_filtrado.sort_values(by=disc_nome, ascending=False)
        
    # Aplicar Top N
    if top_n_escolha != "Todos (18.944)":
        limite = int(top_n_escolha.replace("Top ", ""))
        df_filtrado = df_filtrado.head(limite)
        
    st.info(f"📋 Exibindo **{len(df_filtrado):,}** candidatos selecionados | Média deste grupo: **{df_filtrado['Nota Objetiva'].mean():.1f} pts** | Maior: **{df_filtrado['Nota Objetiva'].max()}** | Menor: **{df_filtrado['Nota Objetiva'].min()}**".replace(",", "."))
    
    # Colunas visíveis na tabela
    colunas_exibir = ['Posição', 'Nome', 'Inscrição', 'Nota Objetiva'] + DISCIPLINAS
    st.dataframe(
        df_filtrado[colunas_exibir],
        use_container_width=True,
        hide_index=True,
        height=500
    )
    
    # Opções de Download
    st.write("---")
    st.markdown("#### 📥 Exportar Resultados Filtrados")
    c_dl1, c_dl2 = st.columns(2)
    
    with c_dl1:
        csv_buffer = io.StringIO()
        df_filtrado[colunas_exibir].to_csv(csv_buffer, index=False, sep=";", encoding="utf-8-sig")
        st.download_button(
            label="📄 Baixar em CSV (Excel Brasil com acentos)",
            data=csv_buffer.getvalue().encode("utf-8-sig"),
            file_name="pprn_classificacao_filtrada.csv",
            mime="text/csv"
        )
        
    with c_dl2:
        st.caption("Você pode abrir o arquivo CSV diretamente no Excel, Google Planilhas ou Power BI.")

# ==============================================================================
# ABA 3: RAIO-X & ESTATÍSTICAS DO CONCURSO
# ==============================================================================
with tab_stats:
    st.subheader("📊 Raio-X Estatístico da Prova Objetiva")
    st.write("Análise aprofundada de distribuição, dificuldade das matérias e pontos de corte:")
    
    # Histograma de Distribuição de Notas
    st.markdown("#### 📈 Distribuição Geral de Notas")
    fig_hist = px.histogram(
        df_base,
        x="Nota Objetiva",
        nbins=65,
        color_discrete_sequence=['#3B82F6'],
        title="Frequência de Candidatos por Faixa de Pontuação",
        labels={"Nota Objetiva": "Pontuação Obtida", "count": "Quantidade de Candidatos"}
    )
    fig_hist.add_vline(x=MEDIA_NOTA, line_dash="dash", line_color="#F59E0B", annotation_text=f"Média: {MEDIA_NOTA:.1f}", annotation_position="top left")
    fig_hist.add_vline(x=MEDIANA_NOTA, line_dash="dot", line_color="#10B981", annotation_text=f"Mediana: {MEDIANA_NOTA:.0f}", annotation_position="top right")
    
    # Adicionar percentis chave
    p90 = np.percentile(df_base['Nota Objetiva'], 90)
    p99 = np.percentile(df_base['Nota Objetiva'], 99)
    fig_hist.add_vline(x=p90, line_dash="dashdot", line_color="#EC4899", annotation_text=f"Top 10% ({p90:.0f} pts)", annotation_position="bottom left")
    fig_hist.add_vline(x=p99, line_dash="dashdot", line_color="#8B5CF6", annotation_text=f"Top 1% ({p99:.0f} pts)", annotation_position="bottom right")

    fig_hist.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        height=380,
        yaxis_title="Quantidade de Candidatos"
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Dificuldade Relativa das Matérias
    col_dif1, col_dif2 = st.columns(2)
    
    with col_dif1:
        st.markdown("#### 🎯 Qual matéria foi mais difícil? (% Médio de Acertos)")
        aprov_medio = []
        for d in DISCIPLINAS:
            media = df_base[d].mean()
            max_p = PONTOS_MAXIMOS[d]
            pct = (media / max_p) * 100
            aprov_medio.append({"Disciplina": d, "Aproveitamento_Medio": pct, "Media": media, "Maximo": max_p})
            
        df_aprov = pd.DataFrame(aprov_medio).sort_values(by="Aproveitamento_Medio", ascending=True)
        
        fig_dif = px.bar(
            df_aprov,
            x="Aproveitamento_Medio",
            y="Disciplina",
            orientation='h',
            color="Aproveitamento_Medio",
            color_continuous_scale="Viridis",
            labels={"Aproveitamento_Medio": "Média de Acertos (%)"},
            text=df_aprov["Aproveitamento_Medio"].apply(lambda x: f"{x:.1f}%")
        )
        fig_dif.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=380,
            showlegend=False
        )
        st.plotly_chart(fig_dif, use_container_width=True)
        st.caption("📌 Quanto menor a porcentagem, mais exigente foi a disciplina para o conjunto dos candidatos.")

    with col_dif2:
        st.markdown("#### 🏆 Marcos de Classificação e Notas de Corte")
        marcos = [1, 10, 50, 100, 200, 500, 1000, 2000, 3000, 5000, 10000, TOTAL_CANDIDATOS]
        dados_marcos = []
        for m in marcos:
            if m <= TOTAL_CANDIDATOS:
                row_m = df_base.iloc[m - 1]
                dados_marcos.append({
                    "Posição": f"{m}º Colocado",
                    "Nota Necessária": f"{int(row_m['Nota Objetiva'])} pts",
                    "Aproveitamento": f"{(row_m['Nota Objetiva'] / NOTA_MAXIMA_PROVA)*100:.1f}%",
                    "Candidato": row_m['Nome']
                })
        st.dataframe(pd.DataFrame(dados_marcos), use_container_width=True, hide_index=True)

# ==============================================================================
# ABA 4: SIMULADOR DE VAGAS E CORTE
# ==============================================================================
with tab_simulador:
    st.subheader("🎯 Simulador de Chamadas & Nota de Corte")
    st.write("Selecione o número de vagas previsto para Ampla Concorrência ou fases posteriores (como TAF) para calcular a nota de corte instantaneamente:")
    
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        num_vagas = st.slider(
            "Quantidade de Vagas / Convocados:",
            min_value=10,
            max_value=min(5000, TOTAL_CANDIDATOS),
            value=500,
            step=50
        )
    with col_s2:
        num_custom = st.number_input("Ou digite um número exato:", min_value=1, max_value=TOTAL_CANDIDATOS, value=num_vagas)
        if num_custom != num_vagas:
            num_vagas = int(num_custom)
            
    candidato_corte = df_base.iloc[num_vagas - 1]
    nota_corte = int(candidato_corte['Nota Objetiva'])
    
    # Empatados na nota de corte
    empatados = df_base[df_base['Nota Objetiva'] == nota_corte]
    qtd_empatados = len(empatados)
    
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Nota de Corte Estimada", f"{nota_corte} pts", f"{(nota_corte/NOTA_MAXIMA_PROVA)*100:.1f}% de aproveitamento")
    sc2.metric("Último Convocado no Limite", f"{num_vagas}º Lugar", f"{candidato_corte['Nome']}")
    sc3.metric("Candidatos Empatados nesta Nota", f"{qtd_empatados} candidatos", f"Nota {nota_corte} exata")
    
    st.write("")
    st.markdown(f"#### 👥 Lista dos {num_vagas} Primeiros Convocados na Simulação")
    st.dataframe(
        df_base.head(num_vagas)[['Posição', 'Nome', 'Inscrição', 'Nota Objetiva'] + DISCIPLINAS],
        use_container_width=True,
        hide_index=True,
        height=400
    )

# ==============================================================================
# ABA 5: COMPARADOR DE CANDIDATOS
# ==============================================================================
with tab_comparador:
    st.subheader("⚔️ Confronto Direto entre Candidatos")
    st.write("Selecione dois candidatos para comparar o desempenho matéria a matéria:")
    
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
                f"{row['Posição']}º - {row['Nome']} (Nota: {row['Nota Objetiva']} pts | Inscrição: {row['Inscrição']})"
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
                f"{row['Posição']}º - {row['Nome']} (Nota: {row['Nota Objetiva']} pts | Inscrição: {row['Inscrição']})"
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
        st.success(f"🏆 **{c1_dados['Nome']}** está à frente por **+{diff_total} pontos** ({c1_dados['Nota Objetiva']} vs. {c2_dados['Nota Objetiva']} pts).")
    elif diff_total < 0:
        st.success(f"🏆 **{c2_dados['Nome']}** está à frente por **+{abs(diff_total)} pontos** ({c2_dados['Nota Objetiva']} vs. {c1_dados['Nota Objetiva']} pts).")
    else:
        st.info(f"🤝 **Empate absoluto** em {c1_dados['Nota Objetiva']} pontos!")
        
    # Gráfico comparativo de barras lado a lado
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name=f"{c1_dados['Nome']} ({c1_dados['Posição']}º)",
        x=DISCIPLINAS,
        y=[c1_dados[d] for d in DISCIPLINAS],
        marker_color='#3B82F6'
    ))
    fig_comp.add_trace(go.Bar(
        name=f"{c2_dados['Nome']} ({c2_dados['Posição']}º)",
        x=DISCIPLINAS,
        y=[c2_dados[d] for d in DISCIPLINAS],
        marker_color='#10B981'
    ))
    fig_comp.update_layout(
        barmode='group',
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Pontos Obtidos",
        xaxis_tickangle=-30,
        height=400,
        margin=dict(l=20, r=20, t=30, b=80),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_comp, use_container_width=True)
    
    # Tabela detalhada de confronto
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
    st.subheader("🚀 Como Hospedar este Site Gratuitamente no Streamlit Cloud")
    st.write("""
    O Streamlit oferece **hospedagem gratuita e ilimitada** na nuvem (*Streamlit Community Cloud*). 
    Com o passo a passo abaixo, seu site ficará acessível na internet com um link público (exemplo: `https://pprn-analises.streamlit.app`) para qualquer pessoa acessar no computador ou celular!
    """)
    
    col_d1, col_d2 = st.columns([1, 1])
    
    with col_d1:
        st.markdown("""
        ### 📌 Passo 1: Criar um Repositório no GitHub
        1. Acesse **[github.com](https://github.com)** e faça login na sua conta (crie uma gratuita se não tiver).
        2. Clique no botão verde **"New"** (Novo Repositório).
        3. Dê um nome ao repositório, por exemplo: `pprn-analises`.
        4. Deixe como **Public** (Público) e clique em **"Create repository"**.
        
        ### 📌 Passo 2: Subir os Arquivos desta Pasta
        Abra o terminal na pasta deste projeto e execute estes 4 comandos:
        ```bash
        git init
        git add .
        git commit -m "Site de Análise PPRN Oficial"
        git branch -M main
        git remote add origin https://github.com/SEU_USUARIO/pprn-analises.git
        git push -u origin main
        ```
        *(Substitua `SEU_USUARIO` pelo seu usuário do GitHub)*
        """)
        
    with col_d2:
        st.markdown("""
        ### 📌 Passo 3: Ativar no Streamlit Cloud
        1. Acesse **[share.streamlit.io](https://share.streamlit.io)** e faça login com a sua conta do GitHub.
        2. Clique em **"Create app"** (ou "New app").
        3. Preencha os 3 campos:
           - **Repository:** `SEU_USUARIO/pprn-analises`
           - **Branch:** `main`
           - **Main file path:** `app.py`
        4. Clique em **"Deploy!"**.
        
        🎉 **Pronto!** Em 1 a 2 minutos o Streamlit irá instalar as dependências e seu site estará no ar na nuvem com certificado SSL (HTTPS) seguro e link compartilhável!
        """)
        
    st.success("💡 **Dica importante:** Todos os arquivos necessários (`app.py`, `requirements.txt`, `.streamlit/config.toml` e a planilha otimizada) já estão criados e prontos nesta pasta!")

# ==============================================================================
# RODAPÉ
# ==============================================================================
st.write("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 10px 0;">
    🛡️ <strong>Portal de Análises Independentes PPRN</strong> • Dados extraídos do Edital de Resultado Preliminar Oficial da Prova Objetiva.<br>
    Construído com Python & Streamlit • Hospedagem Streamlit Community Cloud
</div>
""", unsafe_allow_html=True)
