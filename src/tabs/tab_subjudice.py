"""
Aba Especial: Painel Jurídico e Doutrinário dos Candidatos Sub Judice.
Análise jurídica estrita com base na Constituição Federal, CPC, Lei 12.016/2009,
jurisprudência vinculante do STF (Temas 376 e 476) e STJ, e regras do Edital nº 002/2026.
"""

import pandas as pd
import streamlit as st
from src.data_loader import normalizar_texto, carregar_bytes_excel


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

    st.markdown("""<div class="card p-4 shadow-sm rounded-3 mb-4" style="background: #ffffff; border: 1px solid #e2e8f0;">
    <h5 class="fw-bold text-primary mb-3">
        <i class="bi bi-question-diamond-fill me-2"></i>Entenda as Duas Situações Distintas Existentes no Concurso PPRN:
    </h5>

    <div class="row g-3">
        <div class="col-md-6">
            <div class="p-3 rounded-3" style="background: #f0fdf4; border: 1px solid #bbf7d0; height: 100%;">
                <div class="fw-bold text-success mb-2" style="font-size: 1rem;">
                    🟢 Situação A: Candidato com Nota Suficiente cuja Cota foi Reconhecida Liminarmente
                </div>
                <div style="font-size: 0.9rem; color: #166534; line-height: 1.55;">
                    <strong>Exemplo Real no PPRN:</strong> Candidato <strong>Bruno De Medeiros Celestino</strong> (Inscrição 2320054913).<br>
                    • <strong>Nota Objetiva:</strong> 117 pontos.<br>
                    • <strong>Linha de Corte da Cota Étnica:</strong> 114 pontos.<br>
                    • <strong>O que aconteceu:</strong> Ele havia sido indeferido na heteroidentificação em 04/11. Em 12/11/2026, a SEAD/RN publicou cumprimento liminar (autos nº 0830487-85.2026.8.20.5106) deferindo provisoriamente sua condição de cotista.<br>
                    • <strong>Impacto nas Fases Seguintes:</strong> Como sua nota (117) é <strong>superior à nota de corte (114)</strong>, enquanto a condição de cotista estiver resguardada pela liminar, ele preenche tanto o requisito numérico quanto o requisito de cota, seguindo normalmente o fluxo do certame em caso de aprovação no TAF.
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="p-3 rounded-3" style="background: #eff6ff; border: 1px solid #bfdbfe; height: 100%;">
                <div class="fw-bold text-primary mb-2" style="font-size: 1rem;">
                    🔵 Situação B: Candidatos com Nota Objetiva Abaixo da Linha de Corte
                </div>
                <div style="font-size: 0.9rem; color: #1e40af; line-height: 1.55;">
                    <strong>Exemplo:</strong> Candidatos cotistas convocados com notas entre 74 e 113 pontos (abaixo do corte de 114 pontos).<br>
                    • <strong>Para o TAF:</strong> Foram convocados expressamente pelo Art. 1º do Edital de Cumprimento Liminar publicado em 18/11/2026.<br>
                    • <strong>Para as Fases Seguintes (Avaliação Psicológica, Curso de Formação):</strong> A convocação <strong>depende estritamente do teor do dispositivo da ordem judicial</strong> em cada processo:<br>
                    &nbsp;&nbsp;1. Se a liminar concedida determinar a participação <em>"no TAF e nas demais etapas subsequentes em caso de aptidão"</em>, a banca terá que convocá-los.<br>
                    &nbsp;&nbsp;2. Se a liminar tiver autorizado <em>apenas a realização do TAF</em>, o candidato necessitará requerer ao juiz ou relator a extensão da tutela para as fases vindouras.<br>
                    • <strong>Para a Nomeação Final:</strong> Conforme jurisprudência pacífica do STJ (AgInt no RMS 56.786/MS), a nomeação definitiva depende do trânsito em julgado favorável da ação ou de ordem judicial expressa transitada.
                </div>
            </div>
        </div>
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
        st.markdown("""<div class="card p-3 shadow-sm rounded-3 h-100" style="background: #ffffff; border-left: 4px solid #0d6efd;">
        <div class="fw-bold text-primary mb-2" style="font-size: 1rem;">
            📥 Baixar Documentos Oficiais em PDF & Excel
        </div>
        <div style="font-size: 0.88rem; color: #475569; margin-bottom: 10px;">
            Baixe as publicações originais da SEAD/RN e a planilha com os 23 candidatos:
        </div>
        """, unsafe_allow_html=True)

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
        st.markdown("</div>", unsafe_allow_html=True)

    with c_dw2:
        st.markdown("""<div class="card p-3 shadow-sm rounded-3 h-100" style="background: #ffffff; border-left: 4px solid #10b981;">
        <div class="fw-bold text-success mb-2" style="font-size: 1rem;">
            🔍 Como Acompanhar os Processos no PJe do TJRN
        </div>
        <div style="font-size: 0.88rem; color: #334155; line-height: 1.55;">
            Os números de processo no padrão CNJ (ex: <code>0826153-97.2026.8.20.0000</code>) tramitam no <strong>Tribunal de Justiça do Estado do Rio Grande do Norte (TJRN)</strong>:<br>
            • Processos terminados em <code>.0000</code>: Tramitam originariamente no <strong>2º Grau / Tribunal Pleno do TJRN</strong> (Mandados de Segurança contra o Secretário de Estado da Administração).<br>
            • Processos terminados em <code>.5001</code>: Comarca de Natal (Varas da Fazenda Pública).<br>
            • Processos terminados em <code>.5106</code>: Comarca de Mossoró.<br>
            • <strong>Portal Oficial de Consulta Pública:</strong> Acesse o PJe do TJRN em <a href="https://pje.tjrn.jus.br" target="_blank" rel="noopener noreferrer">pje.tjrn.jus.br</a> para verificar despachos, petições e certidões.
        </div>
        </div>""", unsafe_allow_html=True)

    st.write("---")

    # 8. FAQ Doutrinário e Jurisprudencial
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
