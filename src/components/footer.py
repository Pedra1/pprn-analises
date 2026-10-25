"""
Componente de Rodapé Institucional e Créditos.
"""

import streamlit as st


def render_footer():
    """Renderiza o rodapé com informações de transparência e créditos do criador."""
    st.markdown("""<div class="footer-container">
    <div><i class="bi bi-shield-fill-check text-primary me-1"></i> <strong>Portal de Resultados PPRN</strong> • Dados oficiais atualizados com os Resultados Preliminares das Bancas de Heteroidentificação e Perícia PCD (23/10/2026).</div>
    <div class="mt-2 text-secondary" style="font-size: 0.9rem;">
    Desenvolvido com dedicação por <strong class="text-dark">Pedro Nildo</strong> • Instagram do Criador: <a href="https://instagram.com/pedronildu" target="_blank" class="fw-bold text-primary text-decoration-none"><i class="bi bi-instagram text-danger me-1"></i>@pedronildu</a>
    </div>
    </div>""", unsafe_allow_html=True)
