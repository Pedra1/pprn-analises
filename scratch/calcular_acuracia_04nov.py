"""
Script de Linha de Comando para Auditoria e Cálculo de Acurácia das Listas de 04/11.
Uso:
    python scratch/calcular_acuracia_04nov.py
ou
    python scratch/calcular_acuracia_04nov.py "caminho/para/lista_oficial.xlsx"
"""

import sys
import os
import pandas as pd

# Garantir UTF-8 no terminal Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.acuracia import obter_acuracia_site, calcular_acuracia_com_arquivo_oficial, PASTA_04_NOVEMBRO

def main():
    print("=" * 70)
    print("AUDITORIA DE ACURÁCIA • PORTAL PPRN vs BANCA AVALIA (04/11/2026)")
    print("=" * 70)

    # 1. Carregar base do portal
    parquet_path = "pprn_dados.parquet"
    if not os.path.exists(parquet_path):
        print(f"Erro: Arquivo {parquet_path} não encontrado.")
        return

    print("Carregando base de dados do portal...")
    df_base = pd.read_parquet(parquet_path)
    print(f"Base carregada: {len(df_base):,} candidatos.")

    # 2. Verificar se foi passado arquivo como argumento
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        caminho_arquivo = sys.argv[1]
        print(f"\nCalculando acurácia contra arquivo especificado: {caminho_arquivo}")
        metricas = calcular_acuracia_com_arquivo_oficial(df_base, caminho_arquivo)
    else:
        print(f"\nVerificando arquivos na pasta '{PASTA_04_NOVEMBRO}'...")
        metricas = obter_acuracia_site(df_base)

    if not metricas:
        print("Erro: Não foi possível calcular a acurácia.")
        return

    print("\n" + "-" * 70)
    print(f"STATUS DO CÁLCULO    : {metricas.get('status', 'OK').upper()}")
    print(f"ARQUIVO ANALISADO    : {metricas.get('arquivo_analisado')}")
    print(f"DATA DE REFERÊNCIA   : {metricas.get('data_referencia')}")
    print("-" * 70)
    print(f"ACURÁCIA GLOBAL      : {metricas.get('acuracia_formatada')} ({metricas.get('total_acertos', 0):,} acertos em {metricas.get('total_candidatos', 0):,} avaliados)")
    print(f"PRECISÃO DOS CORTES  : {metricas.get('precisao_cortes_pct', 100):.1f}%")
    print(f"  • Corte Ampla      : {metricas.get('corte_ampla')} pts")
    print(f"  • Corte Cota Étnica: {metricas.get('corte_etnico')} pts")
    print(f"  • Corte Cota PCD   : {metricas.get('corte_pcd')} pts")
    print(f"DIVERGÊNCIAS (RECURSO): {metricas.get('divergencias', 0):,} candidatos")
    if 'verdadeiros_positivos' in metricas:
        print(f"VERDADEIROS POSITIVOS: {metricas.get('verdadeiros_positivos', 0):,} (Convocados confirmados)")
        print(f"VERDADEIROS NEGATIVOS: {metricas.get('verdadeiros_negativos', 0):,} (Não convocados confirmados)")
    print("-" * 70)
    print(f"MENSAGEM: {metricas.get('mensagem')}")
    print("=" * 70)

if __name__ == "__main__":
    main()

