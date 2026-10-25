"""
Injeção de Meta Tags Open Graph (SEO e Compartilhamento Rico no WhatsApp e Redes Sociais).
"""

import streamlit as st


def render_meta_tags():
    """Injeta meta tags HTML Open Graph e Twitter Cards para compartilhamento atraente."""
    meta_html = """
    <!-- Open Graph / WhatsApp / Facebook / Telegram -->
    <meta property="og:type" content="website" />
    <meta property="og:title" content="🛡️ Portal de Resultados • Policial Penal RN (PPRN)" />
    <meta property="og:description" content="Consulte seu boletim individual oficial, notas por disciplina, parecer das bancas de cotas (Heteroidentificação/PCD), avanço na fila e simuladores de convocação do TAF!" />
    <meta property="og:site_name" content="Portal de Resultados PPRN" />
    <meta property="og:locale" content="pt_BR" />
    
    <!-- Meta SEO Geral -->
    <meta name="description" content="Portal interativo de consulta individual de resultados, análise de notas e projeções do Concurso de Policial Penal do Rio Grande do Norte (PPRN - 2026)." />
    <meta name="keywords" content="PPRN, Policial Penal RN, Concurso RN, Instituto Avalia, Heteroidentificação, Perícia Médica PCD, TAF, Prova Objetiva, SEAD RN" />
    <meta name="author" content="Pedro Nildo (@pedronildu)" />
    <meta name="theme-color" content="#0D6EFD" />

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="🛡️ Portal de Resultados • Policial Penal RN (PPRN)" />
    <meta name="twitter:description" content="Boletim individual, parecer das bancas de cotas de 23/10, desempates e projeções do TAF do concurso PPRN." />
    """
    st.markdown(meta_html, unsafe_allow_html=True)
