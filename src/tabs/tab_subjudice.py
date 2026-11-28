"""
Aba Especial: Painel Jurídico e Doutrinário dos Candidatos Sub Judice.
Análise jurídica estrita com base na Constituição Federal, CPC, Lei 12.016/2009,
jurisprudência vinculante do STF (Temas 376 e 476) e STJ, e regras do Edital nº 002/2026.
"""

import io
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from src.data_loader import normalizar_texto, carregar_bytes_excel
from src.subjudice_logic import (
    construir_classificacao_combinada,
    simular_cenario_subjudice,
)


def render_tab_subjudice(df_base):
    """Renderiza a aba dedicada aos candidatos com convocação ou deferimento Sub Judice."""

    # 1. Header Visual da Seção
    st.markdown("""<div class="sim-banner" style="border-left: 5px solid #4338ca;">
    <span class="badge-pill" style="background: #e0e7ff; color: #3730a3; border: 1px solid #c7d2fe;">
        <i class="bi bi-bank text-primary me-1"></i> PAINEL JURÍDICO & DOUTRINÁRIO OFICIAL
    </span>
    <h2 class="hero-title mt-1 mb-2" style="font-size: 1.75rem;">
        <i class="bi bi-scale text-primary me-2"></i>Candidatos Sub Judice • Regime Jurídico & Convocação às Próximas Fases
    </h2>
    <p class="text-secondary mb-0" style="font-size: 0.95rem; line-height: 1.6;">
        Esclarecimentos fundamentados na <strong>Constituição Federal</strong>, <strong>Código de Processo Civil (CPC/2015)</strong>, <strong>Lei do Mandado de Segurança (Lei nº 12.016/2009)</strong> e na <strong>jurisprudência vinculante do STF e do STJ</strong> acerca da eficácia das decisões liminares, notas de corte e prosseguimento nas etapas do concurso.
    </p>
    </div>""", unsafe_allow_html=True)

    # 2. Disclaimer Legal Expresso Obrigatório
    st.markdown("""<div class="card border-start border-4 border-warning p-3 rounded-3 shadow-sm mb-4" style="background-color: #fffbeb; border-color: #f59e0b !important;">
    <div class="d-flex align-items-center gap-2 mb-1 fw-bold text-dark text-uppercase" style="font-size: 0.88rem; letter-spacing: 0.04em;">
        <i class="bi bi-exclamation-triangle-fill text-warning fs-5"></i> AVISO LEGAL DE RESPONSABILIDADE & TRANSPARÊNCIA (DISCLAIMER)
    </div>
    <div style="font-size: 0.92rem; color: #92400e; line-height: 1.6;">
        <strong>Atenção candidato:</strong> As análises, interpretações e dados jurídicos consolidados nesta página possuem <strong>finalidade estritamente informativa, pedagógica e de auxílio aos concursandos</strong>.
        Elas <strong>não substituem</strong> as publicações oficiais no Diário Oficial do Estado do Rio Grande do Norte (DOE/RN), os atos formais da comissão do certame (SEAD/SEAP e Instituto Avalia), nem dispensam o acompanhamento técnico individual por <strong>advogado constituído ou Defensoria Pública</strong>. Cada ação judicial possui particularidades processuais e alcance delimitado pela respectiva decisão liminar. Consulte sempre as fontes oficiais e o andamento do seu processo no PJe do Tribunal de Justiça.
    </div>
    </div>""", unsafe_allow_html=True)

    # Filtrar candidatos sub judice no dataset
    df_sub = df_base[df_base.get('Is_Sub_Judice', False)].sort_values(by='Posição_Geral').copy()
    total_sub = len(df_sub)

    # 3. Estatísticas dos Casos Sub Judice no Concurso PPRN
    c_s1, c_s2, c_s3, c_s4 = st.columns(4)
    with c_s1:
        st.markdown(f"""<div class="stat-card">
        <div class="stat-label"><i class="bi bi-person-lines-fill text-primary me-1"></i> Total Sub Judice</div>
        <div class="stat-value" style="color: #4338ca;">{total_sub}</div>
        <div class="stat-sub">Cumprimento de liminares</div>
        </div>""", unsafe_allow_html=True)

    with c_s2:
        total_etn_sub = sum(df_sub['Modalidade_Concorrencia'].str.contains('Preto|Pardo|Cota', case=False, na=False))
        st.markdown(f"""<div class="stat-card">
        <div class="stat-label"><i class="bi bi-person-fill-check me-1" style="color: #6f42c1;"></i> Cota Étnico-Racial</div>
        <div class="stat-value" style="color: #6f42c1;">{total_etn_sub}</div>
        <div class="stat-sub">Convocados liminarmente</div>
        </div>""", unsafe_allow_html=True)

    with c_s3:
        total_pcd_sub = sum(df_sub['Modalidade_Concorrencia'].str.contains('PCD', case=False, na=False))
        st.markdown(f"""<div class="stat-card">
        <div class="stat-label"><i class="bi bi-universal-access text-success me-1"></i> Cota PCD</div>
        <div class="stat-value text-success">{total_pcd_sub}</div>
        <div class="stat-sub">Convocados liminarmente</div>
        </div>""", unsafe_allow_html=True)

    with c_s4:
        st.markdown("""<div class="stat-card">
        <div class="stat-label"><i class="bi bi-check2-all text-primary me-1"></i> Cota Homologada</div>
        <div class="stat-value text-primary">1</div>
        <div class="stat-sub">Bruno Celestino (Heteroidentificação)</div>
        </div>""", unsafe_allow_html=True)

    st.write("")

    # 4. Análise Jurídica Fundamentada
    st.markdown("### ⚖️ Como Funciona a Situação Sub Judice em Concursos Públicos?")
    st.markdown("""
A participação de um candidato sob a condição de *sub judice* decorre de uma **tutela de urgência** provisória (artigos 294 a 300 do CPC) ou **medida liminar** (artigo 7º, inciso III, da Lei nº 12.016/2009). Abaixo detalhamos como a ordem jurídica e as normas do edital regulam cada aspecto dessa situação:
""")

    # Quatro Pilares Jurídicos em Cartões Didáticos
    col_j1, col_j2 = st.columns(2)

    with col_j1:
        st.markdown("""<div class="card p-3 shadow-sm rounded-3 mb-3" style="background: #ffffff; border-left: 4px solid #0d6efd;">
<div class="fw-bold text-primary mb-2" style="font-size: 1.05rem;">
🏛️ 1. O Dever da Administração de Cumprir a Liminar
</div>
<div style="font-size: 0.92rem; color: #334155; line-height: 1.6;">
• <strong>Inafastabilidade da Jurisdição (Art. 5º, XXXV, CF/88):</strong> Nenhuma lesão ou ameaça a direito pode ser excluída da apreciação judicial.<br>
• <strong>Eficácia Mandamental (Art. 536 do CPC):</strong> Deferida a liminar pelo juiz ou desembargador, a comissão do concurso (SEAD/SEAP e Instituto Avalia) é obrigada por lei a cumpri-la de forma imediata, sob pena de crime de desobediência (art. 330 do Código Penal) e imposição de multa cominatória diária (*astreintes*).<br>
• <strong>Instrumento Formal:</strong> O cumprimento ocorre mediante publicação formal de <strong>Edital de Cumprimento Liminar</strong>, como o republicado pela SEAD/RN em 18 de novembro de 2026.
</div>
</div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card p-3 shadow-sm rounded-3 mb-3" style="background: #ffffff; border-left: 4px solid #f59e0b;">
<div class="fw-bold text-warning-emphasis mb-2" style="font-size: 1.05rem;">
⚠️ 2. A Precaridade da Decisão e a Súmula 405 do STF
</div>
<div style="font-size: 0.92rem; color: #334155; line-height: 1.6;">
• <strong>Natureza Provisória (Art. 4º do Edital Liminar):</strong> A decisão liminar é provisória e pode ser revogada ou reformada no decorrer do processo (ex: via Agravo de Instrumento ou na sentença de mérito). Ela <strong>não gera direito adquirido</strong>.<br>
• <strong>Súmula 405 do STF:</strong> <em>"Denegado o mandado de segurança pela sentença, ou no julgamento do agravo, dela interposto, fica sem efeito a liminar concedida, retroagindo os efeitos da decisão contrária."</em><br>
• Caso a decisão venha a ser cassada ou julgada improcedente, a convocação perde efeito automaticamente e o candidato é desclassificado do concurso.
</div>
</div>""", unsafe_allow_html=True)

    with col_j2:
        st.markdown("""<div class="card p-3 shadow-sm rounded-3 mb-3" style="background: #ffffff; border-left: 4px solid #198754;">
<div class="fw-bold text-success mb-2" style="font-size: 1.05rem;">
🎯 3. Podem Participar do TAF Mesmo com Nota Abaixo do Corte?
</div>
<div style="font-size: 0.92rem; color: #334155; line-height: 1.6;">
• <strong>SIM para a realização do TAF!</strong> A própria publicação da SEAD/RN comprova: candidatos com notas entre 74 e 113 pontos (cujo corte regular foi 114 na cota e 119 na ampla) foram convocados para realizar o teste nos dias <strong>19 e 20 de dezembro de 2026</strong>.<br>
• <strong>Por que isso ocorre?</strong> O Judiciário, ao identificar plausibilidade do direito (<em>fumus boni iuris</em>) e perigo da demora (<em>periculum in mora</em> da realização iminente da prova física), suspende a exclusão do candidato perante a cláusula de barreira a fim de evitar perecimento do direito.<br>
• A realização do teste físico em data oficial evita dano irreparável caso a ação venha a ser julgada procedente no mérito.
</div>
</div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card p-3 shadow-sm rounded-3 mb-3" style="background: #ffffff; border-left: 4px solid #dc3545;">
<div class="fw-bold text-danger mb-2" style="font-size: 1.05rem;">
🚫 4. Inaplicabilidade da Teoria do Fato Consumado (Tema 476/STF)
</div>
<div style="font-size: 0.92rem; color: #334155; line-height: 1.6;">
• <strong>Tese de Repercussão Geral (STF - RE 608.482 - Tema 476):</strong><br>
<em>"Não é compatível com o regime constitucional de acesso aos cargos públicos a manutenção no cargo, sob fundamento de fato consumado, de candidato não aprovado que nele tomou posse em decorrência de decisão judicial precária."</em><br>
• <strong>Significado Prático:</strong> Mesmo que o candidato participe do TAF, realize exame psicológico ou conclua o Curso de Formação, <strong>o decurso do tempo não valida sua permanência definitiva</strong> se a ação for julgada improcedente. O direito à vaga só se consolida com o trânsito em julgado favorável.
</div>
</div>""", unsafe_allow_html=True)

    st.write("---")

    # 5. A Grande Dúvida: Convocação para as Próximas Fases e Nomeação
    st.markdown("### ❓ O Candidato Sub Judice Será Convocado para as Fases Subsequentes?")
    st.markdown("##### 🔷 Entenda as Duas Situações Distintas Existentes no Concurso PPRN:")

    col_sit1, col_sit2 = st.columns(2)
    with col_sit1:
        st.markdown("""<div class="card p-3 shadow-sm rounded-3 mb-3" style="background: #f0fdf4; border: 1px solid #bbf7d0; height: 100%;">
<div class="fw-bold text-success mb-2" style="font-size: 1rem;">
🟢 Situação A: Candidato com Nota Suficiente cuja Cota foi Reconhecida Liminarmente
</div>
<div style="font-size: 0.9rem; color: #166534; line-height: 1.55;">
<strong>Exemplo Real no PPRN:</strong> Candidato <strong>Bruno De Medeiros Celestino</strong> (Inscrição 2320054913).<br><br>
• <strong>Nota Objetiva:</strong> 117 pontos.<br>
• <strong>Linha de Corte da Cota Étnica:</strong> 114 pontos.<br>
• <strong>O que aconteceu:</strong> Ele havia sido indeferido na heteroidentificação em 04/11. Em 12/11/2026, a SEAD/RN publicou cumprimento liminar (autos nº 0830487-85.2026.8.20.5106) deferindo provisoriamente sua condição de cotista.<br>
• <strong>Impacto nas Fases Seguintes:</strong> Como sua nota (117) é <strong>superior à nota de corte (114)</strong>, enquanto a condição de cotista estiver resguardada pela liminar, ele preenche tanto o requisito numérico quanto o requisito de cota, seguindo normalmente o fluxo do certame em caso de aprovação no TAF.
</div>
</div>""", unsafe_allow_html=True)

    with col_sit2:
        st.markdown("""<div class="card p-3 shadow-sm rounded-3 mb-3" style="background: #eff6ff; border: 1px solid #bfdbfe; height: 100%;">
<div class="fw-bold text-primary mb-2" style="font-size: 1rem;">
🔵 Situação B: Candidatos com Nota Objetiva Abaixo da Linha de Corte
</div>
<div style="font-size: 0.9rem; color: #1e40af; line-height: 1.55;">
<strong>Exemplo:</strong> Candidatos cotistas convocados com notas entre 74 e 113 pontos (abaixo do corte de 114 pontos).<br><br>
• <strong>Para o TAF:</strong> Foram convocados expressamente pelo Art. 1º do Edital de Cumprimento Liminar publicado em 18/11/2026.<br>
• <strong>Para as Fases Seguintes (Avaliação Psicológica, Curso de Formação):</strong> A convocação <strong>depende estritamente do teor do dispositivo da ordem judicial</strong> em cada processo:<br>
&nbsp;&nbsp;1. Se a liminar concedida determinar a participação <em>"no TAF e nas demais etapas subsequentes em caso de aptidão"</em>, a banca terá que convocá-los.<br>
&nbsp;&nbsp;2. Se a liminar tiver autorizado <em>apenas a realização do TAF</em>, o candidato necessitará requerer ao juiz ou relator a extensão da tutela para as fases vindouras.<br>
• <strong>Para a Nomeação Final:</strong> Conforme jurisprudência pacífica do STJ (AgInt no RMS 56.786/MS), a nomeação definitiva depende do trânsito em julgado favorável da ação ou de ordem judicial expressa transitada.
</div>
</div>""", unsafe_allow_html=True)

    # 6. Tabela Interativa de Todos os 23 Candidatos Sub Judice
    st.markdown("### 📋 Relação Oficial dos 23 Candidatos Sub Judice no Concurso PPRN")
    st.caption("Dados extraídos dos editais oficiais de cumprimento liminar republicados pela SEAD/RN em 12/11 e 18/11/2026:")

    # Busca rápida na tabela
    c_f1, c_f2 = st.columns([2, 1])
    with c_f1:
        busca_sub = st.text_input("Filtrar candidatos sub judice por nome, inscrição ou processo:", placeholder="Digite o nome ou número do processo...")
    with c_f2:
        filtro_modalidade = st.selectbox("Filtrar por modalidade:", ["Todas as modalidades", "Cota Preto/Pardo", "Cota PCD"])

    df_view_sub = df_sub.copy()

    if filtro_modalidade == "Cota Preto/Pardo":
        df_view_sub = df_view_sub[df_view_sub['Modalidade_Concorrencia'].str.contains('Preto|Pardo', case=False, na=False)]
    elif filtro_modalidade == "Cota PCD":
        df_view_sub = df_view_sub[df_view_sub['Modalidade_Concorrencia'].str.contains('PCD', case=False, na=False)]

    if busca_sub.strip():
        norm_s = normalizar_texto(busca_sub)
        df_view_sub = df_view_sub[
            df_view_sub['Nome_Busca'].str.contains(norm_s, regex=False, na=False) |
            df_view_sub['Inscrição_Str'].str.contains(norm_s, regex=False, na=False) |
            df_view_sub['Processo_Sub_Judice'].str.contains(busca_sub.strip(), regex=False, na=False)
        ]

    cols_exibir = [
        'Posição_Geral',
        'Nome',
        'Inscrição',
        'Nota Objetiva',
        'Modalidade_Concorrencia',
        'Processo_Sub_Judice',
        'Tipo_Sub_Judice',
        'Status_Oficial_TAF'
    ]

    st.dataframe(
        df_view_sub[[c for c in cols_exibir if c in df_view_sub.columns]].rename(columns={
            'Posição_Geral': 'Classificação Geral',
            'Inscrição': 'Inscrição',
            'Nota Objetiva': 'Nota',
            'Modalidade_Concorrencia': 'Modalidade',
            'Processo_Sub_Judice': 'Nº do Processo Judicial (TJRN)',
            'Tipo_Sub_Judice': 'Objeto da Decisão',
            'Status_Oficial_TAF': 'Situação Oficial'
        }),
        width="stretch",
        hide_index=True,
        height=380
    )

    st.write("")

    # 7. Downloads e Consulta Processual no TJRN
    c_dw1, c_dw2 = st.columns([1, 1])

    with c_dw1:
        st.markdown("""<div class="fw-bold text-primary mb-1" style="font-size: 1rem;">
📥 Baixar Documentos Oficiais em PDF & Excel
</div>
<div style="font-size: 0.88rem; color: #475569; margin-bottom: 12px;">
Baixe as publicações oficiais da SEAD/RN e a planilha com os 23 candidatos:
</div>""", unsafe_allow_html=True)

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            bytes_sub_rep = carregar_bytes_excel("REPUBLICAÇÃO - EDITAL DE CUMPRIMENTO LIMINAR – CONVOCAÇÃO PARA O TESTE DE APTIDÃO FÍSICA.pdf")
            if bytes_sub_rep:
                st.download_button(
                    "📄 Convocação TAF (PDF)",
                    data=bytes_sub_rep,
                    file_name="REPUBLICAÇÃO - EDITAL DE CUMPRIMENTO LIMINAR – CONVOCAÇÃO PARA O TESTE DE APTIDÃO FÍSICA.pdf",
                    mime="application/pdf",
                    width="stretch"
                )
        with col_b2:
            bytes_sub_xl = carregar_bytes_excel("RELAÇÃO OFICIAL - CANDIDATOS CONVOCADOS SUB JUDICE.xlsx")
            if bytes_sub_xl:
                st.download_button(
                    "📊 Planilha Completa (Excel)",
                    data=bytes_sub_xl,
                    file_name="RELAÇÃO OFICIAL - CANDIDATOS CONVOCADOS SUB JUDICE.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    width="stretch"
                )

        bytes_sub_het = carregar_bytes_excel("EDITAL DE CUMPRIMENTO LIMINAR – ALTERAÇÃO DE RESULTADO NA HETEROIDENTIFICAÇÃO.pdf")
        if bytes_sub_het:
            st.download_button(
                "📄 Edital Heteroidentificação Liminar (Bruno Celestino)",
                data=bytes_sub_het,
                file_name="EDITAL DE CUMPRIMENTO LIMINAR – ALTERAÇÃO DE RESULTADO NA HETEROIDENTIFICAÇÃO.pdf",
                mime="application/pdf",
                width="stretch"
            )

    with c_dw2:
        st.markdown("""<div class="card p-3 shadow-sm rounded-3 h-100" style="background: #ffffff; border-left: 4px solid #10b981;">
<div class="fw-bold text-success mb-2" style="font-size: 1rem;">
    🔍 Como Acompanhar os Processos no PJe do TJRN
</div>
<div style="font-size: 0.88rem; color: #334155; line-height: 1.55;">
    Os números de processo no padrão CNJ (ex: <code>0826153-97.2026.8.20.0000</code>) tramitam no <strong>Tribunal de Justiça do Estado do Rio Grande do Norte (TJRN)</strong>:<br><br>
    • Processos terminados em <code>.0000</code>: Tramitam originariamente no <strong>2º Grau / Tribunal Pleno do TJRN</strong> (Mandados de Segurança contra o Secretário de Estado da Administração).<br>
    • Processos terminados em <code>.5001</code>: Comarca de Natal (Varas da Fazenda Pública).<br>
    • Processos terminados em <code>.5106</code>: Comarca de Mossoró.<br><br>
    • <strong>Portal Oficial de Consulta Pública:</strong> Acesse o PJe do TJRN em <a href="https://pje.tjrn.jus.br" target="_blank" rel="noopener noreferrer">pje.tjrn.jus.br</a> para verificar despachos, petições e certidões.
</div>
</div>""", unsafe_allow_html=True)

    st.write("---")

    # 8. Área Combinada: Sub Judice Integrados às Respectivas Cotas (Exclusivo desta aba)
    _render_classificacao_combinada(df_base)

    st.write("---")

    # 9. Simulador Exclusivo para Candidatos Sub Judice (Exclusivo desta aba)
    _render_simulador_subjudice(df_base)

    st.write("---")

    # 10. FAQ Doutrinário e Jurisprudencial
    st.markdown("### 💡 Perguntas Frequentes sobre Candidatos Sub Judice")

    with st.expander("1. O candidato convocado sub judice 'tira' a vaga de outro candidato convocado regularmente?"):
        st.markdown("""
**Não.** No regime constitucional dos concursos públicos e na jurisprudência do STJ:
- A vaga disputada pelo candidato sub judice é tratada sob o regime de **reserva de vaga** ou **vaga suplementar** provisória decorrente de mandado judicial.
- A Administração Pública não pode desconvocar um candidato que atingiu a nota de corte regular para dar lugar ao candidato sub judice.
- A participação do candidato sub judice ocorre em acréscimo provisório à lista regular (tanto que o número de convocados para o TAF subiu de 1.884 para 1.907).
""")

    with st.expander("2. Se o candidato for aprovado no TAF e no Psicológico, ele pode ser nomeado e tomar posse apenas com a liminar?"):
        st.markdown("""
**Em regra, não.** O Superior Tribunal de Justiça (STJ) firmou jurisprudência pacífica no sentido de que:
> *"O candidato que concorre a cargo público sob a condição 'sub judice' não tem direito à nomeação e posse antes do trânsito em julgado da decisão que lhe foi favorável, salvo se houver expressa determinação judicial de antecipação de posse em casos excepcionalíssimos."* (STJ, AgInt no RMS 56.786/MS, Rel. Min. Mauro Campbell Marques; RMS 51.520/MG).

Portanto, o candidato tem direito a participar das etapas de capacitação e avaliação, garantindo sua classificação e reserva de vaga, mas a posse definitiva é condicionada ao trânsito em julgado.
""")

    with st.expander("3. O que acontece se a liminar for suspensa ou revogada pelo Tribunal em grau de recurso (Agravo de Instrumento)?"):
        st.markdown("""
Caso o Estado do Rio Grande do Norte (PGE/RN) interponha **Agravo de Instrumento** ou ingresse com pedido de **Suspensão de Liminar** e obtenha efeito suspensivo ou reforma da decisão:
- Cessa imediatamente a eficácia da convocação.
- Pelo efeito retroativo da **Súmula 405 do STF**, a decisão contrária retroage (*ex tunc*), fazendo com que o candidato deixe de figurar entre os habilitados do concurso, sem qualquer direito à indenização pelos testes realizados.
""")

    with st.expander("4. O que a banca Instituto Avalia exige do candidato sub judice para o dia do TAF?"):
        st.markdown("""
Conforme estabelecido no Artigo 3º do Edital de Cumprimento Liminar (republicado em 18/11/2026):
1. O candidato deve observar **todas as regras do Item 14 do Edital de Abertura nº 02/2026** e da republicação do edital de convocação de 17/11/2026.
2. Apresentar **atestado médico original** emitido nos termos do subitem 14.4 "c" (são válidos atestados emitidos desde **15 de outubro de 2026**).
3. Consultar o **Cartão de Informação** com local e horário exatos, disponível no site da banca ([avalia.org.br](https://www.avalia.org.br)) a partir das **15h do dia 14 de dezembro de 2026**.
4. Comparecer com documento oficial de identificação com foto e trajes esportivos adequados na data designada (19 ou 20 de dezembro de 2026).
""")


@st.cache_data(show_spinner=False)
def _gerar_excel_combinado(_df_export):
    """Gera bytes Excel (.xlsx) sob demanda para a lista combinada exibida na aba Sub Judice."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        _df_export.to_excel(writer, index=False, sheet_name="Classificacao_Combinada")
    return buf.getvalue()


def _render_painel_cota_combinada(df_base, modalidade, key_prefix):
    """Renderiza a tabela classificatória unindo os Sub Judice aos cotistas regulares respectivos."""
    escopo = "taf"
    if modalidade == "etnico":
        escopo_label = st.radio(
            "Recorte dos cotistas étnico-raciais convocados ao TAF para unir aos 21 Sub Judice:",
            [
                "🏃 Todos os Cotistas Étnicos Convocados ao TAF + Sub Judice (626)",
                "🎯 Apenas Reserva ÉT-R do TAF (114–118 pts) + Sub Judice (297)",
            ],
            horizontal=True,
            key=f"sj_escopo_{key_prefix}",
        )
        escopo = "reserva_taf" if "Apenas Reserva ÉT-R" in escopo_label else "taf"
    else:
        st.caption(
            "Na Cota PCD, todos os 534 candidatos deferidos na perícia médica foram convocados ao TAF; "
            "unidos aos 2 candidatos PCD Sub Judice, formam 536 convocados ao TAF."
        )

    df_comb, resumo = construir_classificacao_combinada(df_base, modalidade=modalidade, escopo_etnico=escopo)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        total_fmt = f"{resumo['total']:,}".replace(",", ".")
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-people-fill text-primary me-1"></i> Total Combinado</div>
<div class="stat-value">{total_fmt}</div>
<div class="stat-sub">Regulares + Sub Judice</div>
</div>""", unsafe_allow_html=True)
    with c2:
        reg_fmt = f"{resumo['total_regulares']:,}".replace(",", ".")
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-person-check-fill text-success me-1"></i> Cotistas Regulares</div>
<div class="stat-value text-success">{reg_fmt}</div>
<div class="stat-sub">Posição oficial preservada</div>
</div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-scale me-1" style="color: #4338ca;"></i> Sub Judice na Lista</div>
<div class="stat-value" style="color: #4338ca;">{resumo['total_sub_judice']}</div>
<div class="stat-sub">Destacados em azul índigo</div>
</div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-bar-chart-fill text-warning me-1"></i> Faixa de Notas</div>
<div class="stat-value text-dark">{resumo['menor_nota_sj']}–{resumo['maior_nota']} pts</div>
<div class="stat-sub">Menor Sub Judice a maior da cota</div>
</div>""", unsafe_allow_html=True)

    st.write("")

    col_f1, col_f2, col_f3 = st.columns([1.4, 1.4, 1.0])
    with col_f1:
        busca_comb = st.text_input(
            "Localizar candidato na lista combinada:",
            placeholder="Nome, inscrição ou nº do processo...",
            key=f"sj_comb_busca_{key_prefix}",
        )
    with col_f2:
        modo_viz = st.selectbox(
            "Modo de visualização:",
            [
                "📋 Lista Combinada Completa (Sub Judice destacados)",
                "⚖️ Somente Candidatos Sub Judice (com posição combinada)",
                "🔎 Janela ±5 posições ao redor de um Sub Judice",
            ],
            key=f"sj_comb_viz_{key_prefix}",
        )

    df_filtrado = df_comb.copy()

    if "Janela ±5" in modo_viz:
        sj_opcoes = df_comb[df_comb["Is_Sub_Judice"]].copy()
        with col_f3:
            idx_sj_escolhido = st.selectbox(
                "Centralizar em:",
                options=sj_opcoes.index.tolist(),
                format_func=lambda idx: (
                    f"{int(sj_opcoes.loc[idx, 'Class_Combinada'])}º - "
                    f"{sj_opcoes.loc[idx, 'Nome']} ({int(sj_opcoes.loc[idx, 'Nota Objetiva'])} pts)"
                ),
                key=f"sj_comb_foco_{key_prefix}",
            )
        pos_central = int(df_comb.loc[idx_sj_escolhido, "Class_Combinada"])
        df_filtrado = df_comb[
            (df_comb["Class_Combinada"] >= pos_central - 5)
            & (df_comb["Class_Combinada"] <= pos_central + 5)
        ].copy()
    elif "Somente Candidatos Sub Judice" in modo_viz:
        df_filtrado = df_comb[df_comb["Is_Sub_Judice"]].copy()
        with col_f3:
            st.caption("Exibindo apenas os Sub Judice com sua classificação na cota combinada.")
    else:
        with col_f3:
            opcoes_qtd = ["Todos", "Top 100", "Top 300", "Top 700"]
            qtd_exibir = st.selectbox("Quantidade exibida:", opcoes_qtd, key=f"sj_comb_qtd_{key_prefix}")

    if busca_comb.strip():
        norm_q = normalizar_texto(busca_comb)
        df_filtrado = df_filtrado[
            df_filtrado["Nome_Busca"].str.contains(norm_q, regex=False, na=False)
            | df_filtrado["Inscrição_Str"].str.contains(norm_q, regex=False, na=False)
            | df_filtrado["Processo_Sub_Judice"].fillna("").astype(str).str.contains(busca_comb.strip(), regex=False, na=False)
        ]
    elif "Lista Combinada Completa" in modo_viz and qtd_exibir != "Todos":
        limite = int(qtd_exibir.replace("Top ", ""))
        df_filtrado = df_filtrado.head(limite)

    sj_indices = set(df_filtrado[df_filtrado["Is_Sub_Judice"]].index.tolist())

    df_exibir = pd.DataFrame(index=df_filtrado.index)
    df_exibir["Class. Combinada"] = df_filtrado["Class_Combinada"].astype(int)
    df_exibir["Pos. Geral"] = df_filtrado["Posição_Geral"].astype(int)
    df_exibir["Pos. Oficial Cota (04/11)"] = df_filtrado["Pos_Oficial_Display"]
    df_exibir["Nome"] = df_filtrado["Nome"]
    df_exibir["Inscrição"] = df_filtrado["Inscrição"].astype(str)
    df_exibir["Nota"] = df_filtrado["Nota Objetiva"].astype(int)
    df_exibir["Condição / Vínculo"] = df_filtrado["Condicao_Lista"]
    df_exibir["Impacto (Simulação)"] = df_filtrado["Impacto_Display"]
    df_exibir["Processo TJRN"] = (
        df_filtrado["Processo_Sub_Judice"]
        .fillna("—")
        .astype(str)
        .replace({"": "—", "None": "—", "nan": "—"})
    )

    def _destacar_subjudice(row):
        if row.name in sj_indices:
            return ["background-color: #e0e7ff; color: #312e81; font-weight: 700;"] * len(row)
        return [""] * len(row)

    if len(df_filtrado) == 0:
        st.info("Nenhum candidato encontrado com os filtros aplicados.")
    else:
        st.dataframe(
            df_exibir.style.apply(_destacar_subjudice, axis=1),
            width="stretch",
            hide_index=True,
            height=460,
            column_config={
                "Class. Combinada": st.column_config.NumberColumn("Class. Combinada", format="%dº"),
                "Pos. Geral": st.column_config.NumberColumn("Class. Geral", format="%dº"),
                "Nota": st.column_config.NumberColumn("Nota", format="%d pts"),
            },
        )

    col_dl1, col_dl2 = st.columns([1, 2])
    with col_dl1:
        df_export = pd.DataFrame({
            "Classificacao_Combinada": df_comb["Class_Combinada"].astype(int),
            "Classificacao_Geral": df_comb["Posição_Geral"].astype(int),
            "Posicao_Oficial_Cota_04_11": df_comb["Pos_Oficial_Display"],
            "Nome": df_comb["Nome"],
            "Inscricao": df_comb["Inscrição"].astype(str),
            "Nota_Objetiva": df_comb["Nota Objetiva"].astype(int),
            "Sub_Judice": df_comb["Is_Sub_Judice"].map({True: "SIM", False: "NÃO"}),
            "Condicao_Vinculo": df_comb["Condicao_Lista"],
            "Impacto_Simulacao": df_comb["Impacto_Display"],
            "Processo_TJRN": df_comb["Processo_Sub_Judice"].fillna("").astype(str),
        })
        st.download_button(
            "📥 Baixar Classificação Combinada (.xlsx)",
            data=_gerar_excel_combinado(df_export),
            file_name=f"classificacao_combinada_subjudice_{modalidade}_{escopo}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch",
            key=f"sj_comb_dl_{key_prefix}_{escopo}",
        )
    with col_dl2:
        st.caption(
            "ℹ️ Esta visualização simula exclusivamente a ordenação conjunta (Nota Objetiva + critérios de desempate do Item 21.2.1) "
            "para fins comparativos na área Sub Judice, sem alterar as posições oficiais do Boletim ou das Listas Oficiais."
        )


def _render_classificacao_combinada(df_base):
    """Renderiza a seção de união dos candidatos Sub Judice com as respectivas cotas."""
    st.markdown("""<div class="sim-banner" style="border-left: 5px solid #4338ca;">
    <span class="badge-pill" style="background: #e0e7ff; color: #3730a3; border: 1px solid #c7d2fe;">
        <i class="bi bi-layers-fill me-1"></i> CLASSIFICAÇÃO COMBINADA • EXCLUSIVO ÁREA SUB JUDICE
    </span>
    <h3 class="hero-title mt-1 mb-2" style="font-size: 1.55rem;">
        <i class="bi bi-list-ol text-primary me-2"></i>Convocados ao TAF: Sub Judice Integrados às Respectivas Cotas
    </h3>
    <p class="text-secondary mb-0" style="font-size: 0.93rem; line-height: 1.55;">
        Veja onde cada candidato <strong>Sub Judice</strong> se posiciona quando reunido <strong>exclusivamente aos cotistas regulares convocados para o TAF</strong> da sua respectiva modalidade, respeitando rigorosamente a ordem de <strong>Nota Objetiva e desempates do Edital</strong>. As linhas em destaque índigo identificam os candidatos Sub Judice. <em>Nenhuma classificação oficial do Boletim ou das Listas Oficiais é modificada.</em>
    </p>
    </div>""", unsafe_allow_html=True)

    tab_comb_etn, tab_comb_pcd = st.tabs([
        "🧑🏿 Cota Étnico-Racial + 21 Sub Judice",
        "♿ Cota PCD + 2 Sub Judice",
    ])

    with tab_comb_etn:
        _render_painel_cota_combinada(df_base, modalidade="etnico", key_prefix="etn")

    with tab_comb_pcd:
        _render_painel_cota_combinada(df_base, modalidade="pcd", key_prefix="pcd")


def _render_simulador_subjudice(df_base):
    """Renderiza o simulador exclusivo para candidatos Sub Judice."""
    st.markdown("""<div class="sim-banner" style="border-left: 5px solid #6f42c1;">
    <span class="sim-badge">
        <i class="bi bi-cpu-fill me-1"></i> SIMULADOR EXCLUSIVO • CANDIDATOS SUB JUDICE
    </span>
    <h3 class="hero-title mt-1 mb-2" style="font-size: 1.55rem;">
        <i class="bi bi-graph-up-arrow me-2" style="color: #6f42c1;"></i>Simulador Preditivo Exclusivo para Candidatos Sub Judice
    </h3>
    <p class="text-secondary mb-0" style="font-size: 0.93rem; line-height: 1.55;">
        Simule suas chances reais nas etapas seguintes e na validade de 4 anos considerando o grupo ativo de habilitados ao TAF (<strong>1.884 regulares + 23 Sub Judice</strong>), o atrito do TAF/fases subsequentes, a absorção de cotistas na Ampla Concorrência e a taxa de êxito das liminares. <em>Uso exclusivo desta área, sem impacto nas análises oficiais do portal.</em>
    </p>
    </div>""", unsafe_allow_html=True)

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        total_nomeacoes = st.slider(
            "Total estimado de nomeações no concurso (validade 2+2 anos):",
            min_value=200,
            max_value=1800,
            value=600,
            step=25,
            key="sj_sim_total_nomeacoes",
            help="Projeção total de chamados (70% Ampla, 20% Cota Étnico-Racial, 10% Cota PCD).",
        )
        taxa_taf_pct = st.slider(
            "Atrito / Reprovação estimada no TAF (19 e 20/Dez):",
            min_value=0,
            max_value=45,
            value=20,
            step=1,
            format="%d%%",
            key="sj_sim_taxa_taf",
        )
    with col_p2:
        taxa_demais_pct = st.slider(
            "Atrito nas demais etapas (Psico, Toxicológico, IS, CFP e desistências):",
            min_value=0,
            max_value=40,
            value=15,
            step=1,
            format="%d%%",
            key="sj_sim_taxa_demais",
        )
        taxa_exito_sj_pct = st.slider(
            "Manutenção / Êxito no mérito dos demais Sub Judice:",
            min_value=0,
            max_value=100,
            value=100,
            step=5,
            format="%d%%",
            key="sj_sim_taxa_sj",
            help="100% considera todos os demais Sub Judice ativos à sua frente; 0% simula como se apenas o seu processo permanecesse.",
        )

    incluir_indef_cota = st.checkbox(
        "Considerar reconhecimento de cota na simulação para os 3 Sub Judice atualmente indeferidos na banca (Pablo, Cícero G. e Anna Beatriz)",
        value=True,
        key="sj_sim_incluir_indef",
    )

    df_res, meta = simular_cenario_subjudice(
        df_base,
        total_nomeacoes=total_nomeacoes,
        taxa_taf_pct=taxa_taf_pct,
        taxa_demais_pct=taxa_demais_pct,
        taxa_exito_sj_pct=taxa_exito_sj_pct,
        incluir_indef_cota=incluir_indef_cota,
    )

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-diagram-3-fill text-primary me-1"></i> Vagas do Cenário</div>
<div class="stat-value text-primary">{total_nomeacoes:,}</div>
<div class="stat-sub">{meta['vagas_ac']} AC • {meta['vagas_etn']} Étnico • {meta['vagas_pcd']} PCD</div>
</div>""".replace(",", "."), unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-shield-check text-success me-1"></i> Retenção Pós-Etapas</div>
<div class="stat-value text-success">{meta['taxa_retencao_pct']:.1f}%</div>
<div class="stat-sub">~{meta['sobreviventes_totais']:,} aptos finais de {meta['total_pool']:,}</div>
</div>""".replace(",", "."), unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-scale me-1" style="color: #4338ca;"></i> Sub Judice Alcançados</div>
<div class="stat-value" style="color: #4338ca;">{meta['total_alcancados']} / 23</div>
<div class="stat-sub">No cenário de {total_nomeacoes:,} chamados</div>
</div>""".replace(",", "."), unsafe_allow_html=True)
    with m4:
        ac_txt = "AC Esgotada" if meta["ac_esgotada"] else "AC Com Saldo"
        ac_cor = "#d97706" if meta["ac_esgotada"] else "#198754"
        ac_sub = (
            f"Faltam {meta['rem_ac']:.0f} na AC (≥119: ~{meta['sobreviventes_ac']} aptos)"
            if meta["ac_esgotada"]
            else f"Absorve {meta['vagas_ac']} de ~{meta['sobreviventes_ac']} aptos ≥119"
        )
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-award-fill text-warning me-1"></i> Ampla Concorrência</div>
<div class="stat-value" style="color: {ac_cor}; font-size: 1.35rem;">{ac_txt}</div>
<div class="stat-sub">{ac_sub}</div>
</div>""", unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 🎯 Análise Individual do Candidato Sub Judice")

    idx_sel = st.selectbox(
        "Selecione o candidato Sub Judice para simular sua projeção individual:",
        options=list(range(len(df_res))),
        format_func=lambda idx: (
            f"{int(df_res.loc[idx, 'Posição_Geral'])}º Geral • {df_res.loc[idx, 'Nome']} "
            f"({int(df_res.loc[idx, 'Nota Objetiva'])} pts | Cota {df_res.loc[idx, 'Cota_Grupo']})"
        ),
        key="sj_sim_candidato_sel",
    )

    cand = df_res.loc[idx_sel]
    cota_banca = (
        cand["Resultado_PCD_Definitivo"]
        if cand["Cota_Grupo"] == "PCD"
        else cand["Resultado_Hetero_Definitivo"]
    )

    if cand["Alcancado"]:
        box_cls = "bg-success-subtle border-success"
        tit_cor = "text-success"
        tit_txt = f"🏆 PROJEÇÃO FAVORÁVEL! ALCANÇADO VIA {cand['Vaga_Tipo'].upper()} NESTE CENÁRIO!"
        det_txt = (
            f"Considerando aprovação no TAF e etapas subsequentes, o cenário de <strong>{total_nomeacoes:,} chamados</strong> "
            f"(com {taxa_taf_pct}% de atrito no TAF e {taxa_demais_pct}% nas demais fases) alcança sua posição na cota."
        ).replace(",", ".")
    else:
        box_cls = "bg-warning-subtle border-warning"
        tit_cor = "text-warning-emphasis"
        tit_txt = f"⏳ {cand['Status_Cenario']}"
        det_txt = (
            f"Com os parâmetros atuais, seriam necessárias aproximadamente <strong>{cand['Min_Nomeacoes_Display']}</strong> no concurso "
            f"(cerca de <strong>{cand['Vagas_Cota_Necessarias'] if cand['Vagas_Cota_Necessarias'] is not None else '-'} vagas na cota</strong>) "
            f"para alcançar sua colocação."
        )

    st.markdown(f"""<div class="candidate-card" style="border-left: 5px solid #4338ca; margin-top: 8px;">
<div class="d-flex justify-content-between align-items-start flex-wrap gap-2">
    <div>
        <span class="badge-pill" style="background:#e0e7ff; color:#3730a3; border:1px solid #c7d2fe;">
            ⚖️ SIMULAÇÃO INDIVIDUAL SUB JUDICE • {cand['Cota_Grupo'].upper()}
        </span>
        <h4 class="mt-1 mb-1">{cand['Nome']}</h4>
        <div style="font-size: 0.9rem; color: #475569;">
            Inscrição: <strong>{cand['Inscrição']}</strong> • Nota: <strong>{cand['Nota Objetiva']} pts</strong> •
            Geral: <strong>{cand['Posição_Geral']}º</strong> • Processo: <strong>{cand['Processo_Sub_Judice']}</strong><br>
            Objeto Liminar: <strong>{cand['Tipo_Sub_Judice']}</strong> • Parecer Banca na Cota: <strong>{cota_banca}</strong>
        </div>
    </div>
</div>
<div class="card {box_cls} border-start border-4 p-3 rounded-3 mt-3 mb-0">
    <div class="fw-bold {tit_cor}" style="font-size: 1.02rem;">{tit_txt}</div>
    <div class="text-dark mt-1" style="font-size: 0.9rem; line-height: 1.5;">{det_txt}</div>
</div>
</div>""", unsafe_allow_html=True)

    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label">Posição Combinada (Cotistas TAF)</div>
<div class="stat-value" style="color: #4338ca;">{cand['Pos_Comb_TAF']}º</div>
<div class="stat-sub">De {cand['Total_Comb_TAF']} convocados na cota</div>
</div>""", unsafe_allow_html=True)
    with sc2:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label">Posição na Reserva (TAF)</div>
<div class="stat-value text-primary">{cand['Pos_Comb_Reserva']}º</div>
<div class="stat-sub">De {cand['Total_Comb_Reserva']} na reserva TAF + SJ</div>
</div>""", unsafe_allow_html=True)
    with sc3:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label">Aptos Estimados à Frente</div>
<div class="stat-value text-dark">~{cand['Sobreviventes_Frente']:.0f}</div>
<div class="stat-sub">Na cota (pós-atrito e pós-AC)</div>
</div>""", unsafe_allow_html=True)
    with sc4:
        vagas_nec_txt = f"~{cand['Vagas_Cota_Necessarias']} vagas na cota" if cand["Vagas_Cota_Necessarias"] is not None else "Requer deferimento cota"
        st.markdown(f"""<div class="stat-card">
<div class="stat-label">Alcance Estimado</div>
<div class="stat-value text-success" style="font-size: 1.25rem;">{cand['Min_Nomeacoes_Display']}</div>
<div class="stat-sub">{vagas_nec_txt}</div>
</div>""", unsafe_allow_html=True)

    if int(cand["Nota Objetiva"]) >= 114 and cand["Cota_Grupo"] == "Étnico-Racial":
        st.info(
            "⚖️ **Nota acima da linha de corte regular (114 pts):** Este candidato atingiu pontuação superior ao corte da cota étnico-racial. "
            "Sua permanência até a nomeação depende essencialmente do êxito no mérito quanto à validade da cota/liminar (e aprovação nas demais fases)."
        )
    else:
        st.info(
            "⚖️ **Nota abaixo da linha de corte regular da modalidade:** Além do aproveitamento do Cadastro de Reserva e aprovação em todas as etapas, "
            "a consolidação da vaga depende do provimento definitivo de mérito sobre a cláusula de barreira (e da condição de cotista, se aplicável), nos termos do Tema 476/STF."
        )

    st.write("")
    st.markdown("#### 📊 Panorama Comparativo dos 23 Candidatos Sub Judice")

    df_plot = df_res.copy()
    df_plot["Nome_Curto"] = df_plot.apply(
        lambda r: f"{r['Nome'].split()[0]} {r['Nome'].split()[-1]} ({int(r['Nota Objetiva'])} pts • {r['Cota_Grupo']})",
        axis=1,
    )
    df_plot["Alcance_Plot"] = df_plot["Min_Nomeacoes_Alcance"].fillna(3500)
    df_plot["Cor_Plot"] = ["#198754" if alc else "#4338ca" for alc in df_plot["Alcancado"]]
    df_plot["Texto_Plot"] = [
        f"{int(v):,} chamados".replace(",", ".") if pd.notna(v) else "> 3.500 chamados"
        for v in df_plot["Min_Nomeacoes_Alcance"]
    ]

    fig_sj = go.Figure(
        go.Bar(
            y=df_plot["Nome_Curto"],
            x=df_plot["Alcance_Plot"],
            orientation="h",
            marker_color=df_plot["Cor_Plot"],
            text=df_plot["Texto_Plot"],
            textposition="auto",
            textfont=dict(size=11, weight=700, family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif"),
        )
    )
    fig_sj.add_vline(
        x=total_nomeacoes,
        line_dash="dash",
        line_color="#dc3545",
        line_width=2,
        annotation_text=f"Cenário Atual: {total_nomeacoes} chamados",
        annotation_position="top right",
    )
    fig_sj.update_layout(
        title=dict(
            text="Estimativa de Chamados Totais Necessários para Alcançar Cada Candidato Sub Judice",
            font=dict(color="#212529", size=14, family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif"),
        ),
        font=dict(color="#212529", family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif"),
        xaxis=dict(
            title="Total Estimado de Nomeações no Concurso",
            gridcolor="#dee2e6",
            tickfont=dict(color="#495057"),
            title_font=dict(color="#212529"),
        ),
        yaxis=dict(autorange="reversed", tickfont=dict(color="#212529")),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=20, t=50, b=30),
        height=620,
    )
    st.plotly_chart(fig_sj, width="stretch")

    df_tab_sim = pd.DataFrame(index=df_res.index)
    df_tab_sim["Geral"] = df_res["Posição_Geral"].astype(int)
    df_tab_sim["Nome"] = df_res["Nome"]
    df_tab_sim["Nota"] = df_res["Nota Objetiva"].astype(int)
    df_tab_sim["Cota"] = df_res["Cota_Grupo"]
    df_tab_sim["Pos. Cotistas (TAF)"] = [f"{int(r['Pos_Comb_TAF'])}º / {int(r['Total_Comb_TAF'])}" for _, r in df_res.iterrows()]
    df_tab_sim["Pos. Reserva (TAF)"] = [f"{int(r['Pos_Comb_Reserva'])}º / {int(r['Total_Comb_Reserva'])}" for _, r in df_res.iterrows()]
    df_tab_sim["Aptos à Frente"] = df_res["Sobreviventes_Frente"].round(0).astype(int)
    df_tab_sim["Vagas Cota Nec."] = [
        f"{int(v)} vagas" if pd.notna(v) else "—" for v in df_res["Vagas_Cota_Necessarias"]
    ]
    df_tab_sim["Mín. Chamados Est."] = df_res["Min_Nomeacoes_Display"]
    df_tab_sim["Projeção no Cenário"] = df_res["Status_Cenario"]

    alc_indices = set(df_res[df_res["Alcancado"]].index.tolist())

    def _colorir_sim_sj(row):
        if row.name in alc_indices:
            return ["background-color: #dcfce7; color: #166534; font-weight: 700;"] * len(row)
        return [""] * len(row)

    st.dataframe(
        df_tab_sim.style.apply(_colorir_sim_sj, axis=1),
        width="stretch",
        hide_index=True,
        height=520,
        column_config={
            "Geral": st.column_config.NumberColumn("Pos. Geral", format="%dº"),
            "Nota": st.column_config.NumberColumn("Nota", format="%d pts"),
            "Aptos à Frente": st.column_config.NumberColumn("Aptos à Frente (Est.)", format="~%d"),
        },
    )

