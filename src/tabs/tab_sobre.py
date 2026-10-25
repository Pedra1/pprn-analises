"""
Aba 6: Sobre o Portal, Origem dos Dados, Metodologia e Mensagem do Criador.
"""

import streamlit as st


def render_tab_sobre():
    """Renderiza a aba sobre transparência, metodologia e canais de contato."""
    st.markdown("""<div class="sim-banner">
    <span class="badge-pill-blue"><i class="bi bi-info-circle-fill text-primary me-1"></i> TRANSPARÊNCIA, METODOLOGIA & FONTES</span>
    <h2 class="hero-title mt-1 mb-2" style="font-size: 1.75rem;"><i class="bi bi-patch-question-fill text-primary me-2"></i>Sobre o Portal de Resultados do PPRN</h2>
    <p class="text-secondary mb-0" style="font-size: 0.95rem; line-height: 1.55;">
    Conheça como esta aplicação foi desenvolvida, a proveniência dos dados, a metodologia aplicada nos desempates e simuladores, e a finalidade colaborativa do projeto.
    </p>
    </div>""", unsafe_allow_html=True)

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
        st.markdown("""<div class="stat-card mb-3">
    <div class="stat-label"><i class="bi bi-folder-fill text-primary me-1"></i> Origem dos Dados Oficiais</div>
    <div class="fw-bold text-dark fs-5 my-1">Documentos Públicos da Banca Avalia</div>
    <div class="text-secondary" style="font-size: 0.88rem; line-height: 1.55;">
    Todos os registros presentes neste painel foram extraídos dos editais oficiais publicados em <strong>09 e 23 de outubro de 2026</strong>:
    <ul class="my-2 ps-3">
    <li>Resultado Definitivo da Prova Objetiva (18.945 aprovados);</li>
    <li>Anexo I: Heteroidentificação Preto e Pardo (3.221 Deferidos / 3.022 Indeferidos);</li>
    <li>Anexo II: Análise Documental Indígena e Quilombola (55 Deferidos / 32 Indeferidos);</li>
    <li>Anexo Único: Perícia Médica PCD (473 Deferidos / 186 Indeferidos).</li>
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
    • <strong>Simuladores:</strong> modelos preditivos baseados em médias históricas de carreiras policiais para auxílio ao candidato.
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
