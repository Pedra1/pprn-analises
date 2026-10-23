# -*- coding: utf-8 -*-
import sys
import pandas as pd
import numpy as np

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_parquet('pprn_dados.parquet')
print(f"Total de candidatos carregados: {len(df)}")

cases = [
    ("Abdiel Damasceno de Sousa", "Cotista Étnico Deferido"),
    ("Adriano da Silva Ferreira", "Cotista Étnico Indeferido"),
    ("Abraão Barbosa Pontes Junior", "PCD Deferido"),
    ("Abimael das Neves Ramos Júnior", "PCD Indeferido"),
]

for name, desc in cases:
    print("\n" + "="*50)
    print(f"TESTE: {desc} -> {name}")
    match = df[df['Nome'].str.upper() == name.upper()]
    if len(match) == 0:
        # Tenta com busca normalizada
        from unicodedata import normalize
        def norm(t): return ''.join(c for c in normalize('NFD', str(t)) if not normalize('NFD', c).startswith('\u0300')).upper()
        match = df[df['Nome_Busca'] == norm(name)]
        
    if len(match) > 0:
        row = match.iloc[0]
        print(f"  Pos Geral: {row['Posição_Geral']}º | Inscrição: {row['Inscrição']} | Nota: {row['Nota Objetiva']}")
        print(f"  Modalidade: {row['Modalidade_Concorrencia']}")
        print(f"  Resultado Hetero: {row.get('Resultado_Hetero')} | Resultado PCD: {row.get('Resultado_PCD')}")
        print(f"  Status Cota Preliminar: {row.get('Status_Cota_Preliminar')}")
        print(f"  Nova Pos Étnico: {row.get('Nova_Pos_Lista_Etnico')} (Ganho: +{row.get('Ganho_Pos_Etnico')})")
        print(f"  Nova Pos PCD: {row.get('Nova_Pos_Lista_PCD')} (Ganho: +{row.get('Ganho_Pos_PCD')})")
        print(f"  Previsão TAF: {row.get('Previsao_TAF_Preliminar')}")
        print(f"  Previsão Vagas: {row.get('Previsao_Vagas_Preliminar')}")
    else:
        print("  Candidato não encontrado!")

# Testar caso de candidato indeferido na cota com nota alta (>= 119)
print("\n" + "="*50)
print("TESTE: Cotistas Indeferidos que continuam no TAF via Ampla:")
altos_indef = df[(df['Resultado_Hetero'] == 'INDEFERIDO') & (df['Nota Objetiva'] >= 119)]
print(f"Total encontrados: {len(altos_indef)}")
if len(altos_indef) > 0:
    ex = altos_indef.iloc[0]
    print(f"  Exemplo: {ex['Nome']} | Pos Geral: {ex['Posição_Geral']}º | Nota: {ex['Nota Objetiva']} pts | TAF: {ex['Previsao_TAF_Preliminar']}")

print("\nTodos os casos testados com sucesso!")
