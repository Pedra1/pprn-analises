import sys
import pandas as pd
import numpy as np

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_parquet('pprn_dados.parquet')

print("Colunas disponíveis no parquet:")
print(df.columns.tolist())

# Testar contagem de convocados para o TAF
print("\nDistribuição da Convocação TAF Preliminar:")
print(df['Previsao_TAF_Preliminar'].value_counts())

# Testar candidatos com cota étnica deferida
print("\nTop 5 Cotistas Étnicos com maior ganho de posições:")
top_ganho_etnico = df[df['Cota_Etnico_Apta_Preliminar']].sort_values(by='Ganho_Pos_Etnico', ascending=False)
print(top_ganho_etnico[['Pos_Lista_Etnico', 'Nova_Pos_Lista_Etnico', 'Ganho_Pos_Etnico', 'Nome', 'Nota Objetiva']].head(5))

# Testar candidatos PCD com cota deferida
print("\nTop 5 Candidatos PCD com maior ganho de posições:")
top_ganho_pcd = df[df['Cota_PCD_Apta_Preliminar']].sort_values(by='Ganho_Pos_PCD', ascending=False)
print(top_ganho_pcd[['Pos_Lista_PCD', 'Nova_Pos_Lista_PCD', 'Ganho_Pos_PCD', 'Nome', 'Nota Objetiva']].head(5))

# Testar distribuição de resultados das bancas
print("\nDistribuição Resultado Hetero:")
print(df['Resultado_Hetero'].value_counts())

print("\nDistribuição Resultado PCD:")
print(df['Resultado_PCD'].value_counts())
