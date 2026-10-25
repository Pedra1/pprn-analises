"""
Componente de Cabeçalho (Hero Banner e Métricas Principais).
"""

import streamlit as st
from src.config import (
    TOTAL_CANDIDATOS,
    TOTAL_CANDIDATOS_FMT,
    TOTAL_AMPLA_FMT,
    TOTAL_AMPLA_PURA,
    TOTAL_ETNICO_APTOS,
    TOTAL_ETNICO_INAPTOS,
    PCT_ETNICO_APTOS,
    PCT_ETNICO_INAPTOS,
    TOTAL_PCD_APTOS,
    TOTAL_PCD_INAPTOS,
    PCT_PCD_APTOS,
    PCT_PCD_INAPTOS
)


def render_header():
    """Renderiza o Hero Banner institucional e os 4 cartões com métricas oficiais."""
    st.markdown("""<div class="hero-container">
    <div class="mb-2">
        <span class="badge-pill-amber"><i class="bi bi-lightning-charge-fill text-warning me-1"></i> ATUALIZAÇÃO 23 DE OUTUBRO DE 2026 • RESULTADO PRELIMINAR DAS BANCAS</span>
    </div>
    <h1 class="hero-title"><i class="bi bi-shield-fill-check text-primary me-2"></i>Portal de Resultados • Concurso Policial Penal RN</h1>
    <p class="hero-subtitle mb-0">
    Boletim individual com resultados oficiais preliminares da <strong>Heteroidentificação Étnico-Racial</strong> e <strong>Perícia Médica PCD</strong>, reclassificação pós-banca e simuladores.
    </p>
    </div>""", unsafe_allow_html=True)

    # 4 Métricas Principais Bootstrap
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""<div class="stat-card">
    <div class="stat-label"><i class="bi bi-people-fill text-primary me-1"></i> Total Aprovados</div>
    <div class="stat-value">{TOTAL_CANDIDATOS_FMT}</div>
    <div class="stat-sub">100% da lista objetiva oficial</div>
    </div>""", unsafe_allow_html=True)

    with m2:
        st.markdown(f"""<div class="stat-card">
    <div class="stat-label"><i class="bi bi-person-fill-check me-1" style="color: #6f42c1;"></i> Heteroidentificação Étnica</div>
    <div class="stat-value" style="color: #6f42c1;">{TOTAL_ETNICO_APTOS:,} Aprovados</div>
    <div class="stat-sub text-warning fw-bold">{TOTAL_ETNICO_APTOS:,} Deferidos ({PCT_ETNICO_APTOS:.1f}%) | {TOTAL_ETNICO_INAPTOS:,} Indeferidos ({PCT_ETNICO_INAPTOS:.1f}%)</div>
    </div>""".replace(",", "."), unsafe_allow_html=True)

    with m3:
        st.markdown(f"""<div class="stat-card">
    <div class="stat-label"><i class="bi bi-universal-access text-success me-1"></i> Perícia Médica PCD</div>
    <div class="stat-value text-success">{TOTAL_PCD_APTOS} Aprovados</div>
    <div class="stat-sub text-success fw-bold">{TOTAL_PCD_APTOS} Deferidos ({PCT_PCD_APTOS:.1f}%) | {TOTAL_PCD_INAPTOS} Indeferidos ({PCT_PCD_INAPTOS:.1f}%)</div>
    </div>""", unsafe_allow_html=True)

    with m4:
        st.markdown(f"""<div class="stat-card">
    <div class="stat-label"><i class="bi bi-award-fill text-primary me-1"></i> Não Cotistas (Ampla)</div>
    <div class="stat-value text-primary">{TOTAL_AMPLA_FMT}</div>
    <div class="stat-sub">{(TOTAL_AMPLA_PURA/TOTAL_CANDIDATOS)*100:.1f}% concorrendo exclusivamente na Ampla</div>
    </div>""", unsafe_allow_html=True)

    st.write("")

    # Linhas de Corte do TAF em Destaque na Página Inicial (Ampla, PPP e PCD)
    c_corte1, c_corte2, c_corte3 = st.columns(3)

    with c_corte1:
        st.markdown("""<div class="stat-card" style="border-top: 3px solid #0d6efd;">
    <div class="stat-label"><i class="bi bi-award-fill text-primary me-1"></i> Linha de Corte TAF • Ampla Concorrência</div>
    <div class="stat-value text-primary">119 pts</div>
    <div class="stat-sub text-secondary fw-bold">Top 960 + empates (1.095 convocados)</div>
    </div>""", unsafe_allow_html=True)

    with c_corte2:
        st.markdown("""<div class="stat-card" style="border-top: 3px solid #6f42c1;">
    <div class="stat-label"><i class="bi bi-person-fill-check me-1" style="color: #6f42c1;"></i> Linha de Corte TAF • Cota Étnica (PPP)</div>
    <div class="stat-value" style="color: #6f42c1;">113 pts</div>
    <div class="stat-sub text-success fw-bold">↓ Desceu 2 pontos (376 cotistas na reserva)</div>
    </div>""", unsafe_allow_html=True)

    with c_corte3:
        st.markdown("""<div class="stat-card" style="border-top: 3px solid #198754;">
    <div class="stat-label"><i class="bi bi-universal-access text-success me-1"></i> Linha de Corte TAF • Cota PCD</div>
    <div class="stat-value text-success">73 pts</div>
    <div class="stat-sub text-success fw-bold">100% dos laudos deferidos vão ao TAF (473 aptos)</div>
    </div>""", unsafe_allow_html=True)

    st.write("")
