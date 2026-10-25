"""
Aba 4: Regras do Edital, Recursos e Linhas de Corte do TAF.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_tab_regras():
    """Renderiza a aba de regras do edital, recursos administrativos e cortes do TAF."""
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
