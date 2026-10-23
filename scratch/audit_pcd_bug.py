# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

df = pd.read_parquet('pprn_dados.parquet')

# Candidatos que são PCD E Étnico ao mesmo tempo
dupla = df[df['Cota_PCD'] & df['Cota_Etnico_Racial']]
print(f"Total PCD+Étnico: {len(dupla)}")

# Desses, quais têm PCD deferido E étnico deferido
dupla_ambos_def = dupla[(dupla['Resultado_PCD'] == 'DEFERIDO') & (dupla['Resultado_Hetero'] == 'DEFERIDO')]
print(f"Ambos deferidos: {len(dupla_ambos_def)}")

pcd_def_etn_ind = dupla[(dupla['Resultado_PCD'] == 'DEFERIDO') & (dupla['Resultado_Hetero'] == 'INDEFERIDO')]
print(f"PCD deferido + Étnico indeferido: {len(pcd_def_etn_ind)}")

etn_def_pcd_ind = dupla[(dupla['Resultado_Hetero'] == 'DEFERIDO') & (dupla['Resultado_PCD'] == 'INDEFERIDO')]
print(f"Étnico deferido + PCD indeferido: {len(etn_def_pcd_ind)}")

ambos_ind = dupla[(dupla['Resultado_Hetero'] == 'INDEFERIDO') & (dupla['Resultado_PCD'] == 'INDEFERIDO')]
print(f"Ambos indeferidos: {len(ambos_ind)}")

# PCDs aptos que também são cotistas étnicos
pcd_aptos = df[df['Cota_PCD_Apta_Preliminar']]
pcd_aptos_etnicos = pcd_aptos[pcd_aptos['Cota_Etnico_Racial']]
print(f"\nPCDs aptos que também são cotistas étnicos: {len(pcd_aptos_etnicos)}")
etn_apta_count = pcd_aptos_etnicos['Cota_Etnico_Apta_Preliminar'].sum()
print(f"Desses, com Cota Étnica Apta: {etn_apta_count}")

low_pcd_etn = pcd_aptos_etnicos[pcd_aptos_etnicos['Nota Objetiva'] < 113]
print(f"Desses, com nota < 113 (abaixo do corte étnico TAF): {len(low_pcd_etn)}")

print("\nExemplos de PCDs aptos + étnico com nota baixa e sua previsão TAF:")
for _, r in low_pcd_etn.head(8).iterrows():
    print(f"  {r['Nome']} | Nota: {r['Nota Objetiva']} | Previsao TAF: {r['Previsao_TAF_Preliminar']}")

# Verificar o problema: candidatos PCD aptos (nota baixa) aparecendo como convocados pela cota étnica
print("\n=== CANDIDATOS COM PROBLEMA (PCD apto, nota < 113, mostrando como cota étnica) ===")
problematicos = pcd_aptos_etnicos[
    (pcd_aptos_etnicos['Nota Objetiva'] < 113) & 
    (pcd_aptos_etnicos['Cota_Etnico_Apta_Preliminar']) &
    pcd_aptos_etnicos['Previsao_TAF_Preliminar'].str.contains('Cota Étnica', na=False)
]
print(f"Total com problema: {len(problematicos)}")
for _, r in problematicos.head(10).iterrows():
    print(f"  {r['Nome']} | Nota: {r['Nota Objetiva']} | TAF: {r['Previsao_TAF_Preliminar']}")

# Candidatos PCD aptos com nota baixa mostrando como convocados por qualquer cota que não PCD
print("\n=== TODOS OS PCD APTOS COM NOTA BAIXA E PREVISÃO TAF ===")
all_pcd_low = df[df['Cota_PCD_Apta_Preliminar'] & (df['Nota Objetiva'] < 100)]
for _, r in all_pcd_low.head(10).iterrows():
    print(f"  {r['Nome']} | Nota: {r['Nota Objetiva']} | Etn: {r['Cota_Etnico_Racial']} | Hetero: {r['Resultado_Hetero']} | TAF: {r['Previsao_TAF_Preliminar']}")
