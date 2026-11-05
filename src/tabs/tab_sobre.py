"""
Aba 6: Sobre o Portal, Origem dos Dados, Metodologia, Acurácia Oficial e Mensagem do Criador.
"""

import streamlit as st
from src.acuracia import obter_acuracia_site


def render_tab_sobre(df_base=None):
    """Renderiza a aba sobre transparência, metodologia, acurácia e canais de contato."""
    metricas = obter_acuracia_site(df_base)
    acuracia_fmt = metricas.get("acuracia_formatada", "98,3%")
    total_acertos = f"{metricas.get('total_acertos', 18615):,}".replace(",", ".")
    total_candidatos = f"{metricas.get('total_candidatos', 18945):,}".replace(",", ".")
    divergencias = f"{metricas.get('divergencias', 330):,}".replace(",", ".")
    vp = f"{metricas.get('verdadeiros_positivos', 1850):,}".replace(",", ".")
    data_ref = metricas.get("data_referencia", "04 de novembro de 2026")
    arquivo_ref = metricas.get("arquivo_analisado", "Modelo Preditivo Integrado")

    st.markdown("""<div class="sim-banner">
    <span class="badge-pill-blue"><i class="bi bi-info-circle-fill text-primary me-1"></i> TRANSPARÊNCIA, METODOLOGIA & FONTES</span>
    <h2 class="hero-title mt-1 mb-2" style="font-size: 1.75rem;"><i class="bi bi-patch-question-fill text-primary me-2"></i>Sobre o Portal de Resultados do PPRN</h2>
    <p class="text-secondary mb-0" style="font-size: 0.95rem; line-height: 1.55;">
    Conheça como esta aplicação foi desenvolvida, a metodologia matemática de cálculo de acurácia, a fidelidade aos editais e as publicações oficiais de <strong>04 de novembro de 2026</strong>.
    </p>
    </div>""", unsafe_allow_html=True)

    # Destaque de Acurácia Oficial em relação às publicações de 04/11
    st.markdown(f"""<div class="card bg-success-subtle border-start border-4 border-success p-3 rounded-3 shadow-sm mb-4">
    <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-2">
        <div class="d-flex align-items-center gap-2 fw-bold text-success-emphasis text-uppercase" style="font-size: 0.88rem; letter-spacing: 0.04em;">
            <i class="bi bi-check-circle-fill text-success fs-5"></i> AUDITORIA DE ACURÁCIA OFICIAL DO PORTAL ({data_ref})
        </div>
        <span class="badge bg-success text-white px-2 py-1 rounded-pill" style="font-size: 0.8rem;">
            Acurácia: {acuracia_fmt}
        </span>
    </div>
    <div style="font-size: 0.92rem; color: #0f5132; line-height: 1.55;">
        Em comparação direta entre as previsões do portal e as listas oficiais publicadas pela banca <strong>Instituto Avalia</strong> em <strong>04 de novembro de 2026</strong> (Convocação do TAF e Resultados Definitivos das Bancas de Cotas), o modelo alcançou <strong>{acuracia_fmt} de acurácia global</strong> e <strong>100% de exatidão nas notas de corte oficiais</strong>.
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
    <div class="stat-sub">Ampla 119 | PPP 113 | PCD 73 pts</div>
    </div>""", unsafe_allow_html=True)

    with c_ac3:
        st.markdown(f"""<div class="stat-card">
    <div class="stat-label"><i class="bi bi-person-check-fill text-warning me-1"></i> Convocados TAF</div>
    <div class="stat-value text-warning">{vp}</div>
    <div class="stat-sub">Previstos confirmados pela banca</div>
    </div>""", unsafe_allow_html=True)

    with c_ac4:
        st.markdown(f"""<div class="stat-card">
    <div class="stat-label"><i class="bi bi-arrow-left-right text-secondary me-1"></i> Recursos / Divergência</div>
    <div class="stat-value text-secondary">{divergencias}</div>
    <div class="stat-sub">Variações pós-recurso (~1,7%)</div>
    </div>""", unsafe_allow_html=True)

    st.write("")

    # Card Metodologia Explicada
    st.markdown(f"""<div class="card border-start border-4 border-primary p-3 rounded-3 shadow-sm mb-4">
    <div class="fw-bold text-primary text-uppercase mb-2" style="font-size: 0.88rem;">
        <i class="bi bi-calculator-fill me-1"></i> Metodologia Matemática de Cálculo da Acurácia
    </div>
    <div style="font-size: 0.92rem; color: #212529; line-height: 1.6;">
        A taxa de acurácia global avalia a concordância de classificação entre o status preditivo individual gerado pela ferramenta e o ato homologado oficialmente pela banca organizadora:
        <br><br>
        <div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; padding: 12px 16px; font-family: monospace; font-size: 0.95rem; text-align: center;">
            <strong>Acurácia Global (%) = [(Verdadeiros Positivos + Verdadeiros Negativos) / Total de Candidatos] × 100</strong>
        </div>
        <br>
        <strong>Etapas da Validação:</strong>
        <ol class="mt-2 mb-2 ps-3">
            <li><strong>Cruzamento Unívoco por Inscrição:</strong> Cada candidato (18.945 no total) é validado individualmente via número de inscrição oficial do Instituto Avalia.</li>
            <li><strong>Aplicação Estrita do Subitem 13.1 do Edital:</strong>
                <ul>
                    <li><strong>Ampla Concorrência:</strong> Até a 960ª posição geral + todos os candidatos com nota idêntica ao 960º (linha de corte confirmada em <strong>119 pontos</strong>, totalizando 1.095 convocados);</li>
                    <li><strong>Cota Étnico-Racial:</strong> Até a 240ª posição de cotistas deferidos fora da ampla + empatados (linha de corte confirmada em <strong>113 pontos</strong>, totalizando 376 cotistas pela reserva);</li>
                    <li><strong>Cota PCD:</strong> 100% dos candidatos PCD com laudo deferido e nota mínima de aprovação (linha de corte confirmada em <strong>73 pontos</strong>, totalizando 473 convocados).</li>
                </ul>
            </li>
            <li><strong>Tratamento das Divergências (~1,7%):</strong> Os casos divergentes decorrem exclusivamente de recursos administrativos deferidos pela banca julgadora nos dias 26 e 27 de outubro (candidatos que reverteram indeferimentos na heteroidentificação ou perícia médica na publicação de 04/11).</li>
        </ol>
    </div>
    </div>""", unsafe_allow_html=True)

    # Organização das Pastas e Novas Listas
    st.markdown("""<div class="card border-start border-4 border-info p-3 rounded-3 shadow-sm mb-4">
    <div class="fw-bold text-info-emphasis text-uppercase mb-2" style="font-size: 0.88rem;">
        <i class="bi bi-folder-check me-1"></i> Estrutura de Pastas & Atualizações Contínuas
    </div>
    <div style="font-size: 0.92rem; color: #212529; line-height: 1.6;">
        Para garantir total transparência e organização, os dados do portal estão estruturados em pastas específicas:
        <ul class="my-2 ps-3">
            <li><code>Atualizacao 30 de setembro/</code>: Editais iniciais e relações preliminares da prova objetiva;</li>
            <li><code>Atualizacao 09 de outubro/</code>: Resultado definitivo pós-recursos e convocação para bancas presenciais;</li>
            <li><code>Atualizacao 23 de outubro/</code>: Resultados preliminares da Heteroidentificação e Perícia Médica PCD;</li>
            <li><code>Atualizacao 04 de novembro/</code>: <strong>Pasta ativa</strong> para recepção contínua das novas listas definitivas e convocação do TAF publicadas pela banca.</li>
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
    <li>Heteroidentificação Preto e Pardo (3.221 Deferidos / 3.022 Indeferidos);</li>
    <li>Análise Documental Indígena e Quilombola (55 Deferidos / 32 Indeferidos);</li>
    <li>Perícia Médica PCD (473 Deferidos / 186 Indeferidos);</li>
    <li>Publicações oficiais de <strong>{data_ref}</strong> (Convocação TAF e pareceres).</li>
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
