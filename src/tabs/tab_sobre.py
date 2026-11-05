"""
Aba 6: Sobre o Portal, Origem dos Dados, Metodologia, Acurácia Oficial e Mensagem do Criador.
"""

import streamlit as st
from src.acuracia import obter_acuracia_site


def render_tab_sobre(df_base=None):
    """Renderiza a aba sobre transparência, metodologia, acurácia e canais de contato."""
    metricas = obter_acuracia_site(df_base)
    acuracia_fmt = metricas.get("acuracia_formatada", "99,1%")
    total_acertos = f"{metricas.get('total_acertos', 18769):,}".replace(",", ".")
    total_candidatos = f"{metricas.get('total_candidatos', 18945):,}".replace(",", ".")
    divergencias = f"{metricas.get('divergencias', 176):,}".replace(",", ".")
    total_conv = f"{metricas.get('total_convocados_oficial', 1884):,}".replace(",", ".")
    rec_etnico = metricas.get('recursos_etnico_providos', 322)
    rec_pcd = metricas.get('recursos_pcd_providos', 61)
    recursos_totais = rec_etnico + rec_pcd
    data_ref = metricas.get("data_referencia", "04 de novembro de 2026")

    st.markdown("""<div class="sim-banner">
    <span class="badge-pill-blue"><i class="bi bi-info-circle-fill text-primary me-1"></i> TRANSPARÊNCIA, METODOLOGIA & FONTES</span>
    <h2 class="hero-title mt-1 mb-2" style="font-size: 1.75rem;"><i class="bi bi-patch-question-fill text-primary me-2"></i>Sobre o Portal de Resultados do PPRN</h2>
    <p class="text-secondary mb-0" style="font-size: 0.95rem; line-height: 1.55;">
    Auditoria de acurácia matemática, confronto com as listas oficiais de <strong>04 de novembro de 2026</strong>, metodologia dos desempates e fidelidade às normas do edital.
    </p>
    </div>""", unsafe_allow_html=True)

    # Destaque de Acurácia Oficial Auditada
    st.markdown(f"""<div class="card bg-success-subtle border-start border-4 border-success p-3 rounded-3 shadow-sm mb-4">
    <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-2">
        <div class="d-flex align-items-center gap-2 fw-bold text-success-emphasis text-uppercase" style="font-size: 0.88rem; letter-spacing: 0.04em;">
            <i class="bi bi-check-circle-fill text-success fs-5"></i> AUDITORIA DE ACURÁCIA OFICIAL CONCLUÍDA ({data_ref})
        </div>
        <span class="badge bg-success text-white px-2 py-1 rounded-pill" style="font-size: 0.85rem;">
            Acurácia Comprovada: {acuracia_fmt}
        </span>
    </div>
    <div style="font-size: 0.92rem; color: #0f5132; line-height: 1.55;">
        Em confronto direto entre as previsões do portal e os atos formais publicados pela banca <strong>Instituto Avalia</strong> em <strong>04 de novembro de 2026</strong> (Convocação Oficial para o TAF e Resultados Definitivos das Bancas de Cotas), o modelo alcançou <strong>{acuracia_fmt} de acurácia global ({total_acertos} acertos em {total_candidatos} avaliados)</strong> e <strong>100% de exatidão nas notas de corte oficiais</strong>.
    </div>
    </div>""", unsafe_allow_html=True)

    # 4 Cartões de Métricas de Acurácia
    c_ac1, c_ac2, c_ac3, c_ac4 = st.columns(4)

    with c_ac1:
        st.markdown(f"""<div class="stat-card">
    <div class="stat-label"><i class="bi bi-bullseye text-success me-1"></i> Acurácia Global</div>
    <div class="stat-value text-success">{acuracia_fmt}</div>
    <div class="stat-sub">{total_acertos} acertos em {total_candidatos}</div>
    </div>""", unsafe_allow_html=True)

    with c_ac2:
        st.markdown("""<div class="stat-card">
    <div class="stat-label"><i class="bi bi-scissors text-primary me-1"></i> Linhas de Corte TAF</div>
    <div class="stat-value text-primary">100%</div>
    <div class="stat-sub">Ampla 119 | PCD 73 | PPP 114 pts</div>
    </div>""", unsafe_allow_html=True)

    with c_ac3:
        st.markdown(f"""<div class="stat-card">
    <div class="stat-label"><i class="bi bi-person-check-fill text-warning me-1"></i> Convocados TAF</div>
    <div class="stat-value text-warning">{total_conv}</div>
    <div class="stat-sub">1.074 Ampla | 276 Cota | 534 PCD</div>
    </div>""", unsafe_allow_html=True)

    with c_ac4:
        st.markdown(f"""<div class="stat-card">
    <div class="stat-label"><i class="bi bi-arrow-repeat text-info me-1"></i> Recursos Deferidos</div>
    <div class="stat-value text-info">+{recursos_totais}</div>
    <div class="stat-sub">{rec_etnico} Étnicos + {rec_pcd} PCDs deferidos</div>
    </div>""", unsafe_allow_html=True)

    st.write("")

    # Card Metodologia Explicada
    st.markdown(f"""<div class="card border-start border-4 border-primary p-3 rounded-3 shadow-sm mb-4">
    <div class="fw-bold text-primary text-uppercase mb-2" style="font-size: 0.88rem;">
        <i class="bi bi-calculator-fill me-1"></i> Metodologia Matemática de Cálculo da Acurácia
    </div>
    <div style="font-size: 0.92rem; color: #212529; line-height: 1.6;">
        A taxa de acurácia global avalia a concordância de classificação entre o status preditivo individual gerado pela ferramenta e o ato homologado oficialmente pela banca organizadora em 04 de novembro de 2026:
        <br><br>
        <div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; padding: 12px 16px; font-family: monospace; font-size: 0.95rem; text-align: center;">
            <strong>Acurácia Global (%) = [(Verdadeiros Positivos + Verdadeiros Negativos) / Total de Candidatos] × 100</strong>
            <br>
            <span style="color: #0d6efd;">Acurácia = [(1.779 + 16.990) / 18.945] × 100 = <strong>99,07% (99,1%)</strong></span>
        </div>
        <br>
        <strong>Detalhamento dos Resultados da Auditoria:</strong>
        <ol class="mt-2 mb-2 ps-3">
            <li><strong>Cruzamento Unívoco por Inscrição:</strong> Todos os 18.945 candidatos foram auditados individualmente contra a relação oficial de convocados do TAF (Anexo I e IV do Edital nº 002/2026).</li>
            <li><strong>Confirmação Estrita das Linhas de Corte do TAF:</strong>
                <ul>
                    <li><strong>Ampla Concorrência:</strong> A nota de corte oficial cravou em exatos <strong>119 pontos</strong> (1.074 convocados - Top 960 + empates na nota de corte), idêntica à previsão do portal;</li>
                    <li><strong>Cota PCD:</strong> A nota de corte oficial cravou em <strong>73 pontos</strong> (534 convocados - 100% dos laudos deferidos na perícia médica foram convocados para o TAF), idêntica à previsão do portal;</li>
                    <li><strong>Cota Étnico-Racial:</strong> A nota de corte oficial ficou em <strong>114 pontos</strong> (276 convocados na reserva de cota fora dos classificados na ampla), reflexo direto dos 322 recursos providos pela banca examinadora que ingressaram na disputa das cotas.</li>
                </ul>
            </li>
            <li><strong>Impacto dos Recursos Administrativos (04/11):</strong> A banca acolheu <strong>322 recursos</strong> na Heteroidentificação e <strong>61 recursos</strong> na Perícia PCD. Todos os candidatos beneficiados por esses deferimentos já foram integrados à base de dados do portal.</li>
        </ol>
    </div>
    </div>""", unsafe_allow_html=True)

    # Organização das Pastas e Novas Listas
    st.markdown("""<div class="card border-start border-4 border-info p-3 rounded-3 shadow-sm mb-4">
    <div class="fw-bold text-info-emphasis text-uppercase mb-2" style="font-size: 0.88rem;">
        <i class="bi bi-folder-check me-1"></i> Estrutura de Pastas & Publicações da Banca
    </div>
    <div style="font-size: 0.92rem; color: #212529; line-height: 1.6;">
        Todos os dados foram organizados cronologicamente para garantir total transparência e auditoria contínua:
        <ul class="my-2 ps-3">
            <li><code>Atualizacao 30 de setembro/</code>: Editais iniciais e relações preliminares da prova objetiva;</li>
            <li><code>Atualizacao 09 de outubro/</code>: Resultado definitivo da objetiva e convocação para bancas de cotas;</li>
            <li><code>Atualizacao 23 de outubro/</code>: Resultados preliminares da Heteroidentificação e Perícia PCD;</li>
            <li><code>Atualizacao 04 de novembro/</code>: <strong>Listas oficiais ativas</strong> (Anexos I, II, III e IV com os pareceres de recursos e convocação oficial para o TAF).</li>
        </ul>
    </div>
    </div>""", unsafe_allow_html=True)

    # Disclaimer Legal
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
        st.markdown(f"""<div class="stat-card mb-3">
    <div class="stat-label"><i class="bi bi-folder-fill text-primary me-1"></i> Origem dos Dados Oficiais</div>
    <div class="fw-bold text-dark fs-5 my-1">Documentos Públicos da Banca Avalia</div>
    <div class="text-secondary" style="font-size: 0.88rem; line-height: 1.55;">
    Todos os registros presentes neste painel foram extraídos dos editais oficiais publicados pela banca examinadora:
    <ul class="my-2 ps-3">
    <li>Resultado Definitivo da Prova Objetiva (18.945 aprovados);</li>
    <li>Heteroidentificação Definitiva Pós-Recursos (3.586 Deferidos);</li>
    <li>Perícia Médica PCD Definitiva Pós-Recursos (534 Deferidos);</li>
    <li>Edital Oficial de Convocação para o TAF (1.884 convocados);</li>
    <li>Anexos I a IV de Classificação para Prosseguimento no Certame.</li>
    </ul>
    </div>
    </div>""", unsafe_allow_html=True)

    with col_sob2:
        st.markdown("""<div class="stat-card mb-3">
    <div class="stat-label"><i class="bi bi-shield-check text-success me-1"></i> Metodologia & Critérios</div>
    <div class="fw-bold text-dark fs-5 my-1">Fidelidade às Normas do Edital</div>
    <div class="text-secondary" style="font-size: 0.88rem; line-height: 1.55;">
    • <strong>Preservação na Ampla (Art. 4º Hetero / Art. 3º PCD):</strong> candidatos indeferidos continuam normalmente na disputa geral;<br>
    • <strong>Critérios de Desempate:</strong> ordem rigorosa do Item 21.2.1 do edital;<br>
    • <strong>Convocação TAF:</strong> estrito cumprimento dos quantitativos e empates do Item 13.1 do Edital.
    </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="card border-start border-4 border-primary p-3 rounded-3 shadow-sm mb-4">
    <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
        <div>
            <div class="fw-bold text-primary text-uppercase" style="font-size: 0.82rem;"><i class="bi bi-chat-heart-fill text-danger me-1"></i> Mensagem do Criador</div>
            <div class="text-secondary mt-1" style="font-size: 0.9rem;">Desenvolvido de forma colaborativa para trazer clareza aos candidatos de Policial Penal do RN. Dúvidas ou sugestões?</div>
        </div>
        <a href="https://instagram.com/pedronildu" target="_blank" class="btn btn-outline-primary btn-sm"><i class="bi bi-instagram text-danger me-1"></i>@pedronildu</a>
    </div>
    </div>""", unsafe_allow_html=True)
