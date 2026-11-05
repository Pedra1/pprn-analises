"""
Aba 4: Regras do Edital, Resultados Definitivos e Linhas de Corte do TAF.
Atualizado com as publicações oficiais de 04 de novembro de 2026.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from src.config import (
    TOTAL_ETNICO_APTOS,
    TOTAL_ETNICO_INAPTOS,
    PCT_ETNICO_APTOS,
    PCT_ETNICO_INAPTOS,
    TOTAL_PCD_APTOS,
    TOTAL_PCD_INAPTOS,
    PCT_PCD_APTOS,
    PCT_PCD_INAPTOS,
    TOTAL_CONVOCADOS_TAF_OFICIAL,
    TOTAL_CONVOCADOS_AMPLA_OFICIAL,
    TOTAL_CONVOCADOS_ETNICO_OFICIAL,
    TOTAL_CONVOCADOS_PCD_OFICIAL,
    CORTE_TAF_AMPLA,
    CORTE_TAF_ETNICO,
    CORTE_TAF_PCD,
    RECURSOS_ETNICO_PROVIDOS,
    RECURSOS_PCD_PROVIDOS
)


def render_tab_regras():
    """Renderiza a aba de regras do edital, resultados definitivos e cortes do TAF."""
    st.subheader("🎯 Regras Oficiais do Edital, Resultados Definitivos e Cortes do TAF (04/11/2026)")

    st.markdown(f"""<div class="card bg-success-subtle border-start border-4 border-success p-3 rounded-3 shadow-sm mb-3">
    <div class="d-flex align-items-center gap-2 mb-1 fw-bold text-success-emphasis text-uppercase" style="font-size: 0.85rem; letter-spacing: 0.04em;">
        <i class="bi bi-patch-check-fill text-success fs-5"></i> RESULTADOS DEFINITIVOS DAS BANCAS DE COTAS & CONVOCAÇÃO DO TAF (04/11/2026)
    </div>
    <div style="font-size: 0.93rem; color: #0f5132; line-height: 1.6;">
        A banca <strong>Instituto Avalia</strong> divulgou os pareceres dos recursos e homologou o <strong>resultado definitivo</strong> das bancas de cotas em <strong>04 de novembro de 2026</strong>:<br>
        • <strong>Recursos Deferidos:</strong> Foram acolhidos <strong>{RECURSOS_ETNICO_PROVIDOS} recursos</strong> na Cota Étnico-Racial e <strong>{RECURSOS_PCD_PROVIDOS} recursos</strong> na Perícia PCD, totalizando <strong>383 candidatos reclassificados</strong>.<br>
        • <strong>Convocação Oficial para o TAF:</strong> Foram convocados oficialmente <strong>{TOTAL_CONVOCADOS_TAF_OFICIAL:,} candidatos</strong> (Anexos I e IV do Edital nº 002/2026).<br>
        • <strong>Próxima Fase do Concurso:</strong> Realização presencial do <strong>Teste de Aptidão Física (TAF)</strong> nos dias <strong>14 e 15 de novembro de 2026</strong>.
    </div>
    </div>""".replace(",", "."), unsafe_allow_html=True)

    st.markdown("#### 📊 Estatísticas Definitivas da Heteroidentificação & Perícia PCD (Pós-Recursos)")
    st.caption("Dados oficiais consolidados a partir dos Anexos I, II e Único publicados em 04 de novembro de 2026:")

    col_h1, col_h2, col_h3, col_h4 = st.columns(4)
    with col_h1:
        st.markdown("""<div class="stat-card">
<div class="stat-label"><i class="bi bi-people-fill text-primary me-1"></i> Total Cotistas Étnicos</div>
<div class="stat-value">6.309</div>
<div class="stat-sub text-secondary fw-bold">100% dos inscritos na reserva</div>
</div>""", unsafe_allow_html=True)
    with col_h2:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-check-circle-fill text-success me-1"></i> Deferidos Definitivos</div>
<div class="stat-value text-success">{TOTAL_ETNICO_APTOS:,}</div>
<div class="stat-sub text-success fw-bold">+{RECURSOS_ETNICO_PROVIDOS} recursos acolhidos ({PCT_ETNICO_APTOS:.1f}%)</div>
</div>""".replace(",", "."), unsafe_allow_html=True)
    with col_h3:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-universal-access text-success me-1"></i> PCDs Deferidos Definitivo</div>
<div class="stat-value text-success">{TOTAL_PCD_APTOS}</div>
<div class="stat-sub text-success fw-bold">+{RECURSOS_PCD_PROVIDOS} recursos acolhidos ({PCT_PCD_APTOS:.1f}%)</div>
</div>""", unsafe_allow_html=True)
    with col_h4:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-award-fill text-warning me-1"></i> Total Habilitados no TAF</div>
<div class="stat-value text-warning">{TOTAL_CONVOCADOS_TAF_OFICIAL:,}</div>
<div class="stat-sub text-secondary fw-bold">Convocação oficial homologada</div>
</div>""".replace(",", "."), unsafe_allow_html=True)

    st.write("")

    # Tabela Analítica Definitiva por Modalidade
    st.markdown("**📋 Demonstrativo Analítico Definitivo Pós-Recursos (04/11/2026):**")
    tabela_hetero_dados = [
        {
            "Segmento de Reserva": "🧑🏿 Pretos e Pardos (Anexo I)",
            "Total Avaliados": "6.243",
            "Deferidos Definitivo": "3.538",
            "Recursos Acolhidos": "+317",
            "Taxa Deferimento": "56,67%",
            "Indeferidos Definitivo": "2.705",
            "Taxa Indeferimento": "43,33%"
        },
        {
            "Segmento de Reserva": "🏹 Indígenas (Anexo II)",
            "Total Avaliados": "58",
            "Deferidos Definitivo": "38",
            "Recursos Acolhidos": "+1",
            "Taxa Deferimento": "65,52%",
            "Indeferidos Definitivo": "20",
            "Taxa Indeferimento": "34,48%"
        },
        {
            "Segmento de Reserva": "🏺 Quilombolas (Anexo II)",
            "Total Avaliados": "29",
            "Deferidos Definitivo": "16",
            "Recursos Acolhidos": "+4",
            "Taxa Deferimento": "55,17%",
            "Indeferidos Definitivo": "13",
            "Taxa Indeferimento": "44,83%"
        },
        {
            "Segmento de Reserva": "📊 TOTAL COTA ÉTNICO-RACIAL",
            "Total Avaliados": "6.309",
            "Deferidos Definitivo": f"{TOTAL_ETNICO_APTOS:,}".replace(",", "."),
            "Recursos Acolhidos": f"+{RECURSOS_ETNICO_PROVIDOS}",
            "Taxa Deferimento": f"{PCT_ETNICO_APTOS:.2f}%",
            "Indeferidos Definitivo": f"{TOTAL_ETNICO_INAPTOS:,}".replace(",", "."),
            "Taxa Indeferimento": f"{PCT_ETNICO_INAPTOS:.2f}%"
        },
        {
            "Segmento de Reserva": "♿ Perícia Médica PCD (Anexo Único)",
            "Total Avaliados": "659",
            "Deferidos Definitivo": f"{TOTAL_PCD_APTOS}",
            "Recursos Acolhidos": f"+{RECURSOS_PCD_PROVIDOS}",
            "Taxa Deferimento": f"{PCT_PCD_APTOS:.2f}%",
            "Indeferidos Definitivo": f"{TOTAL_PCD_INAPTOS}",
            "Taxa Indeferimento": f"{PCT_PCD_INAPTOS:.2f}%"
        }
    ]
    st.dataframe(pd.DataFrame(tabela_hetero_dados), width="stretch", hide_index=True)

    st.write("")

    # Gráfico Visual Definitivo de Deferimento vs Indeferimento
    seg_names = ['Pretos/Pardos', 'Indígenas', 'Quilombolas', 'Total Étnico', 'Perícia PCD']
    def_vals = [56.67, 65.52, 55.17, PCT_ETNICO_APTOS, PCT_PCD_APTOS]
    ind_vals = [43.33, 34.48, 44.83, PCT_ETNICO_INAPTOS, PCT_PCD_INAPTOS]

    fig_hetero = go.Figure()
    fig_hetero.add_trace(go.Bar(
        y=seg_names,
        x=def_vals,
        name='Deferidos Definitivos (Homologados)',
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
        name='Indeferidos Definitivos (Concorrem Ampla)',
        orientation='h',
        marker_color='#dc3545',
        text=[f"{v:.1f}%" for v in ind_vals],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=11, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif', weight=700)
    ))
    fig_hetero.update_layout(
        barmode='stack',
        title=dict(text="Proporção Definitiva Pós-Recursos: Confirmação vs. Indeferimento nas Bancas (04/11/2026)", font=dict(color='#212529', size=13, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif')),
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
        <i class="bi bi-lightbulb-fill text-warning fs-5"></i> PRINCIPAIS CONCLUSÕES DOS RESULTADOS DEFINITIVOS (04/11/2026)
    </div>
    <div style="font-size: 0.9rem; color: #212529; line-height: 1.6;">
        • <strong>Reversão Expressiva via Recursos:</strong> A comissão da banca deferiu <strong>322 recursos étnicos</strong> e <strong>61 recursos na perícia PCD</strong>, reconduzindo 383 candidatos aptos à disputa das cotas.<br>
        • <strong>Impacto Direto na Nota de Corte Étnica:</strong> Com a entrada dos 322 cotistas deferidos pós-recursos, a concorrência na reserva se intensificou e a linha de corte do TAF subiu de 113 para <strong>114 pontos</strong>.<br>
        • <strong>Ampla Concorrência Inalterada:</strong> A linha de corte da Ampla Concorrência cravou em exatos <strong>119 pontos</strong> (1.074 convocados - Top 960 + empates).<br>
        • <strong>100% dos Laudos PCDs Convocados:</strong> Todos os <strong>534 candidatos PCD deferidos</strong> foram convocados para o TAF (conforme Item 13.1.2 do edital).
    </div>
    </div>""", unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 🏃‍♂️ Quadro Oficial de Convocação para o TAF (04 de Novembro de 2026)")
    st.write(
        "Conforme o Edital de Convocação e Anexo IV publicados oficialmente pela banca examinadora, "
        "o quantitativo final homologado de convocados para o TAF é de **1.884 candidatos**:"
    )

    quadro_taf = [
        {
            "Modalidade": "Ampla Concorrência (AC)",
            "Regra do Edital": "Até o 960º colocado geral + empatados",
            "Nota de Corte": f"{CORTE_TAF_AMPLA} pontos",
            "Total Convocados": f"{TOTAL_CONVOCADOS_AMPLA_OFICIAL:,} candidatos".replace(",", "."),
            "Composição do Grupo": "Classificados na Ampla (Não cotistas + Cotistas com nota de Ampla + Indeferidos que alcançaram o corte de 119 pts)"
        },
        {
            "Modalidade": "Reserva Étnico-Racial (ÉT-R)",
            "Regra do Edital": "Até o 240º cotista apto fora da ampla + empatados",
            "Nota de Corte": f"{CORTE_TAF_ETNICO} pontos",
            "Total Convocados": f"{TOTAL_CONVOCADOS_ETNICO_OFICIAL:,} candidatos".replace(",", "."),
            "Composição do Grupo": "Cotistas deferidos definitivamente com notas entre 114 e 118 pontos na reserva"
        },
        {
            "Modalidade": "Reserva PCD (PCD)",
            "Regra do Edital": "Sem linha de corte numérico (Item 13.1.2)",
            "Nota de Corte": f"{CORTE_TAF_PCD} pontos (nota mínima)",
            "Total Convocados": f"{TOTAL_CONVOCADOS_PCD_OFICIAL:,} candidatos".replace(",", "."),
            "Composição do Grupo": "100% dos candidatos PCD com laudo deferido definitivamente na perícia médica"
        }
    ]
    st.dataframe(
        pd.DataFrame(quadro_taf),
        width="stretch",
        hide_index=True,
        column_config={
            "Modalidade": st.column_config.TextColumn("Modalidade", width="medium"),
            "Regra do Edital": st.column_config.TextColumn("Regra do Edital", width="medium"),
            "Nota de Corte": st.column_config.TextColumn("Nota de Corte", width="small"),
            "Total Convocados": st.column_config.TextColumn("Total Convocados", width="medium"),
            "Composição do Grupo": st.column_config.TextColumn("Composição do Grupo", width="large"),
        }
    )

    st.write("")
    st.markdown("#### ❓ Perguntas Frequentes sobre a Publicação de 04 de Novembro")

    with st.expander("Fui indeferido definitivamente na heteroidentificação. Fui eliminado do concurso?"):
        st.markdown("""
        **NÃO!** Conforme o **Art. 4º do Edital de Convocação**, o candidato que teve a autodeclaração indeferida perde apenas o direito à reserva de vagas de cotas, **continuando a concorrer normalmente pela Ampla Concorrência**. Se a sua nota na prova objetiva for igual ou superior à linha de corte da Ampla (≥ 119 pontos), você está convocado para o TAF!
        """)

    with st.expander("Por que a linha de corte da cota étnica fechou em 114 pontos no TAF oficial?"):
        st.markdown("""
        Na publicação preliminar de 23/10, o corte estimado da cota era 113 pontos. Contudo, na publicação definitiva de 04/11, **a banca acolheu 322 recursos administrativos** de candidatos que reverteram o indeferimento. Com mais 322 cotistas deferidos disputando as 240 vagas de reserva fora da ampla, a linha de corte subiu naturalmente 1 ponto, fixando-se oficialmente em **114 pontos**.
        """)

    with st.expander("Quais são as datas de realização do TAF?"):
        st.markdown("""
        Conforme o edital oficial de convocação de 04 de novembro de 2026, o Teste de Aptidão Física (TAF) será aplicado nos dias **14 e 15 de novembro de 2026**. O resultado preliminar do TAF tem previsão de publicação em **23 de novembro de 2026**.
        """)
