"""
Módulo de Carregamento, Cache e Processamento de Dados do PPRN.
"""

import os
import unicodedata
import pandas as pd
import streamlit as st


def normalizar_texto(texto):
    """Normaliza strings removendo acentuações e caracteres especiais para busca."""
    if not isinstance(texto, str):
        texto = str(texto)
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn').upper().strip()


@st.cache_data(show_spinner=False)
def carregar_dados():
    """Carrega o dataframe base otimizado em formato parquet."""
    parquet_path = "pprn_dados.parquet"
    if not os.path.exists(parquet_path):
        # Fallback para o arquivo completo caso necessário
        if os.path.exists("pprn_dados_completos.parquet"):
            parquet_path = "pprn_dados_completos.parquet"
        else:
            st.error("⚠️ Arquivo de dados pprn_dados.parquet não foi encontrado.")
            return None

    df = pd.read_parquet(parquet_path)

    if 'Posição_Geral' not in df.columns:
        df['Posição_Geral'] = range(1, len(df) + 1)
    if 'Nome_Busca' not in df.columns:
        df['Nome_Busca'] = df['Nome'].apply(normalizar_texto)
    if 'Inscrição_Str' not in df.columns:
        df['Inscrição_Str'] = df['Inscrição'].astype(str)

    return df


@st.cache_data(show_spinner=False)
def get_mapa_inscricoes(_df):
    """Cria um dicionário O(1) de acesso direto por número de inscrição."""
    return {str(insc): i for i, insc in enumerate(_df['Inscrição'])}


@st.cache_data(show_spinner=False)
def carregar_bytes_excel(caminho):
    """Carrega arquivos binários Excel para download sob demanda."""
    if os.path.exists(caminho):
        with open(caminho, "rb") as f:
            return f.read()
    return None
