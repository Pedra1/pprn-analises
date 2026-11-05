"""
Aba 3: As Listas Oficiais e Resultados das Bancas de Cotas (Downloads Excel).
Atualizado com as relações oficiais de 04 de novembro de 2026 (Convocação TAF).
"""

import pandas as pd
import streamlit as st
from src.config import TOTAL_AMPLA_FMT
from src.data_loader import normalizar_texto, carregar_bytes_excel


def render_tab_listas(df_base):
    """Renderiza a aba de listas oficiais definitivas e downloads das relações."""
    st.subheader("📋 Listas Oficiais Definitivas da Banca • Convocação para o TAF (04/11/2026)")
    st.write("""
    Acesse, filtre e faça o download de cada lista oficial em formato Excel (.xlsx), incluindo as relações homologadas publicadas em **04 de novembro de 2026**:
    """)

    tipo_lista = st.radio(
        "Selecione a Lista que deseja visualizar e baixar:",
        [
            "🏃 1. Relação Oficial de Convocados para o TAF (1.884 candidatos - Anexos I e IV)",
            "🧑🏿 2. Resultado Definitivo Heteroidentificação Pós-Recursos (3.586 Deferidos - Anexo I e II)",
            "♿ 3. Resultado Definitivo Perícia Médica PCD Pós-Recursos (534 Deferidos - Anexo Único)",
            "🏛️ 4. Classificação Oficial para Prosseguimento - Ampla Concorrência (1.074 convocados - Anexo I)",
            "📈 5. Classificação Oficial para Prosseguimento - Cota Étnico-Racial (276 convocados - Anexo II)",
            "🌐 6. Classificação Oficial para Prosseguimento - Cota PCD (534 convocados - Anexo III)",
            "📋 7. Lista Geral Completa com Situação Oficial Homologada (18.945 candidatos)"
        ],
        index=0
    )

    st.write("---")

    if "1. Relação Oficial de Convocados para o TAF" in tipo_lista:
        df_view = df_base[df_base['Convocado_TAF_Oficial']].sort_values(by='Posicao_Convocacao_TAF').copy()
        pos_col = 'Posicao_Convocacao_TAF'
        nome_arquivo_excel = "ANEXO IV - EDITAL DE CLASSIFICAÇÃO PARA PROSSEGUIMENTO NO CERTAME.xlsx"
        titulo_lista = "Relação Oficial dos Candidatos Convocados para o Teste de Aptidão Física (TAF)"
        corte_taf_info = "1.884 Convocados (1.074 Ampla | 276 Étnico | 534 PCD)"
        cols_tabela = ['Posicao_Convocacao_TAF', 'Posição_Geral', 'Nome', 'Inscrição', 'Nota Objetiva', 'Modalidade_Convocacao_TAF', 'Status_Oficial_TAF']

    elif "2. Resultado Definitivo Heteroidentificação" in tipo_lista:
        df_view = df_base[df_base['Cota_Etnico_Racial']].copy()
        pos_col = 'Nova_Pos_Lista_Etnico_Definitivo'
        nome_arquivo_excel = "ANEXO I - EDITAL DE RESULTADO DA HETEROIDENTIFICAÇÃO E ANÁLISE DOCUMENTAL PÓS-RECURSOS – PPP.xlsx"
        titulo_lista = "Resultado Definitivo da Heteroidentificação & Análise Documental Pós-Recursos (04/11)"
        corte_taf_info = "3.586 Deferidos (+322 recursos providos) | 2.723 Indeferidos"
        cols_tabela = ['Nova_Pos_Lista_Etnico_Definitivo', 'Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Resultado_Hetero_Definitivo', 'Recurso_Hetero_Deferido', 'Nota Objetiva', 'Convocado_TAF_Oficial']

    elif "3. Resultado Definitivo Perícia Médica PCD" in tipo_lista:
        df_view = df_base[df_base['Cota_PCD']].copy()
        pos_col = 'Nova_Pos_Lista_PCD_Definitivo'
        nome_arquivo_excel = "ANEXO ÚNICO - EDITAL DE RESULTADO DA PERÍCIA MÉDICA PÓS-RECURSOS – PESSOA COM DEFICIÊNCIA.xlsx"
        titulo_lista = "Resultado Definitivo da Perícia Médica PCD Pós-Recursos (04/11)"
        corte_taf_info = "534 Deferidos (+61 recursos providos) | 100% convocados no TAF"
        cols_tabela = ['Nova_Pos_Lista_PCD_Definitivo', 'Posição_Geral', 'Nome', 'Inscrição', 'Resultado_PCD_Definitivo', 'Recurso_PCD_Deferido', 'Nota Objetiva', 'Convocado_TAF_Oficial']

    elif "4. Classificação Oficial para Prosseguimento - Ampla" in tipo_lista:
        df_view = df_base[df_base['Modalidade_Convocacao_TAF'] == 'Ampla Concorrência (AC)'].sort_values(by='Posicao_Convocacao_TAF').copy()
        pos_col = 'Posicao_Convocacao_TAF'
        nome_arquivo_excel = "ANEXO I - EDITAL DE CLASSIFICAÇÃO PARA PROSSEGUIMENTO NO CERTAME.xlsx"
        titulo_lista = "Classificação Oficial para Prosseguimento • Ampla Concorrência (TAF)"
        corte_taf_info = "Linha de corte cravada em 119 pts (1.074 convocados)"
        cols_tabela = ['Posicao_Convocacao_TAF', 'Posição_Geral', 'Nome', 'Inscrição', 'Nota Objetiva', 'Status_Oficial_TAF']

    elif "5. Classificação Oficial para Prosseguimento - Cota Étnico" in tipo_lista:
        df_view = df_base[df_base['Modalidade_Convocacao_TAF'] == 'Cota Étnico-Racial (ÉT-R)'].sort_values(by='Posicao_Convocacao_TAF').copy()
        pos_col = 'Posicao_Convocacao_TAF'
        nome_arquivo_excel = "ANEXO II - EDITAL DE CLASSIFICAÇÃO PARA PROSSEGUIMENTO NO CERTAME PPPP.xlsx"
        titulo_lista = "Classificação Oficial para Prosseguimento • Reserva de Vagas Étnico-Racial (TAF)"
        corte_taf_info = "Linha de corte oficial em 114 pts (276 cotistas na reserva)"
        cols_tabela = ['Posicao_Convocacao_TAF', 'Nova_Pos_Lista_Etnico_Definitivo', 'Nome', 'Inscrição', 'Nota Objetiva', 'Status_Oficial_TAF']

    elif "6. Classificação Oficial para Prosseguimento - Cota PCD" in tipo_lista:
        df_view = df_base[df_base['Modalidade_Convocacao_TAF'] == 'Cota PCD (PCD)'].sort_values(by='Posicao_Convocacao_TAF').copy()
        pos_col = 'Posicao_Convocacao_TAF'
        nome_arquivo_excel = "ANEXO III - EDITAL DE CLASSIFICAÇÃO PARA PROSSEGUIMENTO NO CERTAME pcd.xlsx"
        titulo_lista = "Classificação Oficial para Prosseguimento • Reserva de Vagas PCD (TAF)"
        corte_taf_info = "100% dos laudos deferidos no TAF (534 convocados com nota >= 73 pts)"
        cols_tabela = ['Posicao_Convocacao_TAF', 'Nova_Pos_Lista_PCD_Definitivo', 'Nome', 'Inscrição', 'Nota Objetiva', 'Status_Oficial_TAF']

    else:
        df_view = df_base.copy()
        pos_col = 'Posição_Geral'
        nome_arquivo_excel = "ANEXO I - EDITAL DE CLASSIFICAÇÃO PARA PROSSEGUIMENTO NO CERTAME.xlsx"
        titulo_lista = "Lista Geral Completa Homologada com Situação Oficial das Bancas"
        corte_taf_info = "18.945 aprovados • 1.884 habilitados ao TAF"
        cols_tabela = ['Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Status_Cota_Definitivo', 'Nota Objetiva', 'Convocado_TAF_Oficial', 'Status_Oficial_TAF']

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
            label="📥 Baixar Planilha Oficial desta Lista em Excel (.xlsx)",
            data=dados_excel_bytes,
            file_name=nome_arquivo_excel,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Arquivo Excel sendo preparado.")
