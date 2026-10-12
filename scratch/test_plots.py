import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scratch.test_sim import executar_simulacao_completa

df = pd.read_parquet('pprn_dados.parquet')
df_sim, resumo, n_ampla, n_etnico, n_taf = executar_simulacao_completa(df, 15, 20, 'migrar_ampla', 20)

# Teste criação de gráfico
fig = go.Figure()
fig.add_trace(go.Bar(
    name='Oficial (Edital)',
    x=['Ampla Concorrência', 'Cota Étnico-Racial', 'Cota PCD'],
    y=[140, 40, 20],
    marker_color='#94A3B8',
    text=[140, 40, 20],
    textposition='auto'
))
fig.add_trace(go.Bar(
    name='Simulado (pós-Hetero/PCD e TAF)',
    x=['Ampla Concorrência', 'Cota Étnico-Racial', 'Cota PCD'],
    y=[resumo['ultimo_ampla_orig'], resumo['ultimo_etnico_orig'], resumo['ultimo_pcd_orig']],
    marker_color='#0284C7',
    text=[resumo['ultimo_ampla_orig'], resumo['ultimo_etnico_orig'], resumo['ultimo_pcd_orig']],
    textposition='auto'
))
fig.update_layout(barmode='group', height=350)
print('Gráfico criado com sucesso!')
print('Beneficiados ampla:', len(n_ampla))
