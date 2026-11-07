"""
Componente de Cabeçalho (Hero Banner e Métricas Oficiais de 04/11/2026).
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
    PCT_PCD_INAPTOS,
    TOTAL_CONVOCADOS_TAF_OFICIAL,
    TOTAL_CONVOCADOS_AMPLA_OFICIAL,
    TOTAL_CONVOCADOS_ETNICO_OFICIAL,
    TOTAL_CONVOCADOS_PCD_OFICIAL,
    CORTE_TAF_AMPLA,
    CORTE_TAF_ETNICO,
    CORTE_TAF_PCD,
    ACURACIA_GLOBAL_OFICIAL,
    TOTAL_ACERTOS_OFICIAL,
    RECURSOS_ETNICO_PROVIDOS,
    RECURSOS_PCD_PROVIDOS
)


def render_header():
    """Renderiza o Hero Banner institucional e os cartões com métricas oficiais de 04/11."""
    st.markdown("""<div class="hero-container">
    <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
        <span class="badge-pill-amber">
            <i class="bi bi-patch-check-fill text-success me-1"></i> ATUALIZAÇÃO OFICIAL 04 DE NOVEMBRO DE 2026 • CONVOCAÇÃO DO TAF & BANCAS DEFINITIVAS
        </span>
        <span class="badge bg-success text-white px-2 py-1 rounded-pill fw-bold" style="font-size: 0.8rem;">
            <i class="bi bi-shield-check me-1"></i> Acurácia Comprovada: 99,1%
        </span>
    </div>
    <h1 class="hero-title"><i class="bi bi-shield-fill-check text-primary me-2"></i>Portal de Resultados • Concurso Policial Penal RN</h1>
    <p class="hero-subtitle mb-0">
    Boletim individual sincronizado com a <strong>Convocação Oficial para o Teste de Aptidão Física (TAF)</strong> e os resultados definitivos pós-recursos da <strong>Heteroidentificação Étnico-Racial</strong> e <strong>Perícia Médica PCD</strong>.
    </p>
    </div>""", unsafe_allow_html=True)

    # 4 Métricas Principais Bootstrap
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""<div class="stat-card header-stat-card">
    <div class="stat-label"><i class="bi bi-people-fill text-primary me-1"></i> Total Aprovados</div>
    <div class="stat-value">{TOTAL_CANDIDATOS_FMT}</div>
    <div class="stat-sub">100% da lista objetiva homologada</div>
    </div>""", unsafe_allow_html=True)

    with m2:
        st.markdown(f"""<div class="stat-card header-stat-card">
    <div class="stat-label"><i class="bi bi-person-fill-check me-1" style="color: #6f42c1;"></i> Heteroidentificação Étnica</div>
    <div class="stat-value" style="color: #6f42c1;">{TOTAL_ETNICO_APTOS:,} Aprovados</div>
    <div class="stat-sub text-success fw-bold">+{RECURSOS_ETNICO_PROVIDOS} recursos deferidos em 04/11</div>
    </div>""".replace(",", "."), unsafe_allow_html=True)

    with m3:
        st.markdown(f"""<div class="stat-card header-stat-card">
    <div class="stat-label"><i class="bi bi-universal-access text-success me-1"></i> Perícia Médica PCD</div>
    <div class="stat-value text-success">{TOTAL_PCD_APTOS} Aprovados</div>
    <div class="stat-sub text-success fw-bold">+{RECURSOS_PCD_PROVIDOS} recursos deferidos em 04/11</div>
    </div>""", unsafe_allow_html=True)

    with m4:
        st.markdown(f"""<div class="stat-card header-stat-card">
    <div class="stat-label"><i class="bi bi-award-fill text-warning me-1"></i> Convocados TAF (Oficial)</div>
    <div class="stat-value text-warning">{TOTAL_CONVOCADOS_TAF_OFICIAL:,}</div>
    <div class="stat-sub text-secondary fw-bold">1.074 Ampla | 276 Cota | 534 PCD</div>
    </div>""".replace(",", "."), unsafe_allow_html=True)

    st.write("")

    # Linhas de Corte do TAF Oficiais em Destaque (Ampla, PPP e PCD)
    c_corte1, c_corte2, c_corte3 = st.columns(3)

    with c_corte1:
        st.markdown(f"""<div class="stat-card header-stat-card" style="border-top: 3px solid #0d6efd;">
    <div class="stat-label"><i class="bi bi-award-fill text-primary me-1"></i> Linha de Corte TAF • Ampla Concorrência</div>
    <div class="stat-value text-primary">{CORTE_TAF_AMPLA} pts</div>
    <div class="stat-sub text-success fw-bold">1.074 convocados oficiais (Top 960 + empates)</div>
    </div>""", unsafe_allow_html=True)

    with c_corte2:
        st.markdown(f"""<div class="stat-card header-stat-card" style="border-top: 3px solid #6f42c1;">
    <div class="stat-label"><i class="bi bi-person-fill-check me-1" style="color: #6f42c1;"></i> Linha de Corte TAF • Cota Étnica (PPP)</div>
    <div class="stat-value" style="color: #6f42c1;">{CORTE_TAF_ETNICO} pts</div>
    <div class="stat-sub text-secondary fw-bold">276 convocados oficiais na reserva de cota</div>
    </div>""", unsafe_allow_html=True)

    with c_corte3:
        st.markdown(f"""<div class="stat-card header-stat-card" style="border-top: 3px solid #198754;">
    <div class="stat-label"><i class="bi bi-universal-access text-success me-1"></i> Linha de Corte TAF • Cota PCD</div>
    <div class="stat-value text-success">{CORTE_TAF_PCD} pts</div>
    <div class="stat-sub text-success fw-bold">100% dos laudos deferidos vão ao TAF (534 aptos)</div>
    </div>""", unsafe_allow_html=True)

    st.write("")
