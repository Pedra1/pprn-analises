"""
Aba 3: As Listas Oficiais e Resultados das Bancas de Cotas (Downloads Excel).
"""

import pandas as pd
import streamlit as st
from src.config import TOTAL_AMPLA_FMT
from src.data_loader import normalizar_texto, carregar_bytes_excel


def render_tab_listas(df_base):
    """Renderiza a aba de listas oficiais definitivas e downloads das relações."""
    st.subheader("📋 Listas Oficiais Definitivas e Resultados das Bancas de Cotas (23/10)")
    st.write("""
    Acesse, filtre e faça o download de cada lista em formato Excel (.xlsx), incluindo as relações preliminares publicadas em **23 de outubro de 2026**:
    """)

    tipo_lista = st.radio(
        "Selecione a Lista que deseja visualizar e baixar:",
        [
            "🧑🏿 1. Resultado Preliminar Heteroidentificação & Análise Doc (6.309 candidatos - 3.264 Deferidos / 3.045 Indeferidos)",
            "♿ 2. Resultado Preliminar Perícia Médica PCD (659 candidatos - 473 Deferidos / 186 Indeferidos)",
            "📈 3. Nova Lista Reclassificada da Cota Étnica (3.264 cotistas confirmados)",
            "📈 4. Nova Lista Reclassificada da Cota PCD (473 PCDs confirmados)",
            "🌐 5. Lista Geral Completa com Situação das Bancas (18.945 candidatos)",
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
            label="📥 Baixar Planilha Completa desta Lista em Excel (.xlsx)",
            data=dados_excel_bytes,
            file_name=nome_arquivo_excel,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Arquivo Excel sendo preparado.")
