# -*- coding: utf-8 -*-
"""
Corrigir bug: candidatos PCD+Étnico com nota < corte étnico TAF (113)
mostrando como 'Convocado pela Cota Étnica' quando deveriam mostrar 'Reserva PCD'.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np

df = pd.read_parquet('pprn_dados.parquet')
print(f"Parquet carregado: {len(df)} candidatos, {len(df.columns)} colunas")

# Parâmetros do corte
corte_ampla_taf = 119
corte_etnico_taf = 113

# Fix: Recalcular Previsao_TAF_Preliminar com prioridade PCD sobre Étnico
def get_previsao_taf_corrigida(row):
    is_convocado = row['Convocado_TAF_Preliminar']
    is_pcd_apto = row['Cota_PCD_Apta_Preliminar']
    is_etnico_apto = row['Cota_Etnico_Apta_Preliminar']
    nota = row['Nota Objetiva']
    
    if not is_convocado:
        # Fora do TAF
        if is_etnico_apto:
            return '⚪ Fora da Linha de Corte do TAF (Pontuação na Cota Étnica abaixo de 113 pts)'
        elif is_pcd_apto:
            return '⚪ Fora da Linha de Corte do TAF (Pontuação PCD abaixo de 73 pts)'
        elif row['Cota_Etnico_Racial'] and row['Resultado_Hetero'] == 'INDEFERIDO':
            return '⚪ Fora do Corte do TAF (Cota Étnica Indeferida preliminarmente, nota abaixo do corte de Ampla)'
        elif row['Cota_PCD'] and row['Resultado_PCD'] == 'INDEFERIDO':
            return '⚪ Fora do Corte do TAF (Laudo PCD Indeferido preliminarmente, nota abaixo do corte de Ampla)'
        else:
            return '⚪ Fora da Linha de Corte do TAF (Ampla Concorrência abaixo de 119 pts)'
    else:
        # Dentro do TAF
        if row['Posição_Geral'] <= 960 or nota >= corte_ampla_taf:
            # Convocado pela Ampla
            if is_etnico_apto:
                return '🟢 Convocado para o TAF (Classificado dentro da Ampla Concorrência - Cota Confirmada)'
            elif is_pcd_apto:
                return '🟢 Convocado para o TAF (Classificado dentro da Ampla Concorrência - PCD Confirmado)'
            elif row['Resultado_Hetero'] == 'INDEFERIDO' or row['Resultado_PCD'] == 'INDEFERIDO':
                return '🟢 Convocado para o TAF via Ampla Concorrência (Mesmo com indeferimento na cota, nota alcançou a Ampla!)'
            else:
                return '🟢 Convocado para o TAF (Ampla Concorrência)'
        else:
            # Convocado pela reserva de vagas (fora da ampla)
            # CORREÇÃO: Priorizar PCD sobre étnico quando nota está abaixo do corte étnico
            # Candidato PCD apto SEMPRE entra por PCD (sem corte), independente de ser étnico
            if is_pcd_apto:
                return '♿ Convocado para o TAF (Reserva de Vagas PCD)'
            elif is_etnico_apto:
                return '🟣 Convocado para o TAF (Reserva de Vagas da Cota Étnica)'
            return '🟢 Convocado para o TAF'

# Contar problemas antes da correção
antes = df['Previsao_TAF_Preliminar'].value_counts()
print("\n=== ANTES DA CORREÇÃO ===")
for k, v in antes.items():
    print(f"  {k}: {v}")

# Aplicar correção
df['Previsao_TAF_Preliminar'] = df.apply(get_previsao_taf_corrigida, axis=1)

# Contar após correção
depois = df['Previsao_TAF_Preliminar'].value_counts()
print("\n=== DEPOIS DA CORREÇÃO ===")
for k, v in depois.items():
    print(f"  {k}: {v}")

# Verificar se ainda existem problemas
pcd_aptos_etnicos = df[df['Cota_PCD_Apta_Preliminar'] & df['Cota_Etnico_Racial']]
problematicos = pcd_aptos_etnicos[
    (pcd_aptos_etnicos['Nota Objetiva'] < corte_etnico_taf) & 
    pcd_aptos_etnicos['Previsao_TAF_Preliminar'].str.contains('Cota Étnica', na=False)
]
print(f"\nProblemas restantes após correção: {len(problematicos)}")

# Salvar parquet corrigido
df.to_parquet('pprn_dados.parquet', index=False)
df.to_parquet('pprn_dados_completos.parquet', index=False)
print("\n✅ Parquets salvos com correção!")

# Verificar exemplos corrigidos
print("\n=== EXEMPLOS CORRIGIDOS ===")
exemplos = df[df['Cota_PCD_Apta_Preliminar'] & df['Cota_Etnico_Racial'] & (df['Nota Objetiva'] < 113)]
for _, r in exemplos.head(8).iterrows():
    print(f"  {r['Nome']} | Nota: {r['Nota Objetiva']} | TAF: {r['Previsao_TAF_Preliminar']}")
