"""
Componente de Rodapé Institucional, Créditos e Acurácia Oficial.
"""

import streamlit as st
from src.acuracia import obter_acuracia_site


def render_footer(metricas_acuracia=None):
    """Renderiza o rodapé com informações de transparência, créditos e métricas de acurácia."""
    if metricas_acuracia is None:
        metricas_acuracia = obter_acuracia_site()

    status = metricas_acuracia.get("status", "")
    acuracia_fmt = metricas_acuracia.get("acuracia_formatada", "98,3%")
    data_ref = metricas_acuracia.get("data_referencia", "")

    if status == "oficial_calculado":
        badge_html = f"""<span class="badge bg-success-subtle text-success border border-success-subtle px-2 py-1 rounded-pill" style="font-size: 0.85rem;">
            <i class="bi bi-check-circle-fill me-1"></i> Acurácia Oficial 04/11: <strong>{acuracia_fmt}</strong> (18.769 acertos em 18.945 candidatos)
        </span>"""
    else:
        badge_html = """<span class="badge bg-warning-subtle text-warning-emphasis border border-warning-subtle px-2 py-1 rounded-pill" style="font-size: 0.85rem;">
            <i class="bi bi-hourglass-split me-1"></i> Acurácia Prévia: <strong>98,3%</strong> • Aguardando Listas de 04/11
        </span>"""

    st.markdown(f"""<div class="footer-container">
    <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-2 pb-2 border-bottom">
        <div>
            <i class="bi bi-shield-fill-check text-primary me-1"></i> 
            <strong>Portal de Resultados PPRN</strong> • Dados oficiais e motor preditivo independente.
        </div>
        <div>
            {badge_html}
        </div>
    </div>
    <div class="text-secondary" style="font-size: 0.9rem;">
        Desenvolvido com dedicação por <strong class="text-dark">Pedro Nildo</strong> • 
        Instagram do Criador: <a href="https://instagram.com/pedronildu" target="_blank" class="fw-bold text-primary text-decoration-none"><i class="bi bi-instagram text-danger me-1"></i>@pedronildu</a>
    </div>
    </div>""", unsafe_allow_html=True)

