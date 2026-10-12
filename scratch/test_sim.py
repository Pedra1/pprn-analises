import time
import pandas as pd
import numpy as np

def executar_simulacao_completa(df, taxa_hetero_pct=15, taxa_pcd_pct=20, regra_inaptos='migrar_ampla', taxa_taf_pct=20):
    t0 = time.time()
    taxa_hetero = taxa_hetero_pct / 100.0
    taxa_pcd = taxa_pcd_pct / 100.0
    taxa_taf = taxa_taf_pct / 100.0
    
    # Sementes determinísticas para reproducibilidade progressiva
    rng_etnico = np.random.RandomState(42)
    scores_etnico = pd.Series(rng_etnico.rand(len(df)), index=df.index)

    rng_pcd = np.random.RandomState(123)
    scores_pcd = pd.Series(rng_pcd.rand(len(df)), index=df.index)

    rng_taf = np.random.RandomState(777)
    scores_taf = pd.Series(rng_taf.rand(len(df)), index=df.index)

    # 1. Identificação de Inaptos nas Bancas de Cotas
    is_inapto_etnico = df['Cota_Etnico_Racial'] & (scores_etnico < taxa_hetero)
    is_inapto_pcd = df['Cota_PCD'] & (scores_pcd < taxa_pcd)
    
    df_sim = df.copy()
    df_sim['Inapto_Hetero_Sim'] = is_inapto_etnico
    df_sim['Inapto_PCD_Sim'] = is_inapto_pcd
    
    total_inaptos_etnico = int(is_inapto_etnico.sum())
    total_inaptos_pcd = int(is_inapto_pcd.sum())
    
    if regra_inaptos == 'migrar_ampla':
        # Conforme Art. 4º Hetero e Art. 3º PCD: perdem a cota e concorrem apenas na Ampla
        df_sim['Cota_Etnico_Sim'] = df_sim['Cota_Etnico_Racial'] & (~is_inapto_etnico)
        df_sim['Cota_PCD_Sim'] = df_sim['Cota_PCD'] & (~is_inapto_pcd)
        df_sim['Eliminado_Cota_Sim'] = False
        df_sim['Posicao_Geral_Sim'] = df_sim['Posição_Geral']
    else:
        # Cenário Severo: Eliminados sumariamente do certame
        df_sim['Cota_Etnico_Sim'] = df_sim['Cota_Etnico_Racial'] & (~is_inapto_etnico)
        df_sim['Cota_PCD_Sim'] = df_sim['Cota_PCD'] & (~is_inapto_pcd)
        df_sim['Eliminado_Cota_Sim'] = is_inapto_etnico | is_inapto_pcd
        # Mantém apenas não eliminados e recalcula geral
        df_sim = df_sim[~df_sim['Eliminado_Cota_Sim']].copy()
        df_sim['Posicao_Geral_Sim'] = range(1, len(df_sim) + 1)
        
    df_sim['Ampla_Pura_Sim'] = (~df_sim['Cota_Etnico_Sim']) & (~df_sim['Cota_PCD_Sim'])
    
    # Reclassificação na Cota Étnica
    idx_etnico_aptos = df_sim[df_sim['Cota_Etnico_Sim']].index
    df_sim['Pos_Etnico_Sim'] = np.nan
    df_sim.loc[idx_etnico_aptos, 'Pos_Etnico_Sim'] = range(1, len(idx_etnico_aptos) + 1)
    
    # Reclassificação PCD
    idx_pcd_aptos = df_sim[df_sim['Cota_PCD_Sim']].index
    df_sim['Pos_PCD_Sim'] = np.nan
    df_sim.loc[idx_pcd_aptos, 'Pos_PCD_Sim'] = range(1, len(idx_pcd_aptos) + 1)
    
    # 2. Convocação TAF Simulada
    # Ampla: Top 960 da Geral + Empatados na última nota
    idx_960 = min(959, len(df_sim) - 1)
    candidato_960 = df_sim.iloc[idx_960]
    nota_corte_ampla_taf = int(candidato_960['Nota Objetiva'])
    convocados_ampla_taf = df_sim['Nota Objetiva'] >= nota_corte_ampla_taf
    
    # Cota Étnica: Primeiros 240 cotistas que NÃO estão no corte da Ampla + empatados
    cotistas_fora_ampla = df_sim[df_sim['Cota_Etnico_Sim'] & (~convocados_ampla_taf)]
    if len(cotistas_fora_ampla) >= 240:
        cand_240_cota = cotistas_fora_ampla.iloc[239]
        nota_corte_etnico_taf = int(cand_240_cota['Nota Objetiva'])
        convocados_etnico_reserva = cotistas_fora_ampla['Nota Objetiva'] >= nota_corte_etnico_taf
        idx_etnico_reserva = cotistas_fora_ampla[convocados_etnico_reserva].index
    else:
        nota_corte_etnico_taf = int(cotistas_fora_ampla['Nota Objetiva'].min()) if len(cotistas_fora_ampla) > 0 else 73
        idx_etnico_reserva = cotistas_fora_ampla.index
        
    # PCD: Todos os habilitados com cota PCD confirmada
    idx_pcd_taf = df_sim[df_sim['Cota_PCD_Sim']].index
    
    # Marcação de Convocados TAF
    df_sim['Convocado_TAF_Sim'] = False
    df_sim.loc[df_sim[convocados_ampla_taf].index, 'Convocado_TAF_Sim'] = True
    df_sim.loc[idx_etnico_reserva, 'Convocado_TAF_Sim'] = True
    df_sim.loc[idx_pcd_taf, 'Convocado_TAF_Sim'] = True
    
    total_convocados_taf = int(df_sim['Convocado_TAF_Sim'].sum())
    
    # Novos cotistas étnicos que ganharam convocação para o TAF graças à inaptidão dos anteriores
    # Eram convocados originalmente na reserva ou ampla?
    novos_convocados_taf_etnico = df_sim[
        df_sim['Cota_Etnico_Sim'] & 
        df_sim['Convocado_TAF_Sim'] & 
        (df['Previsao_TAF'].str.contains('Não Convocado', na=False))
    ]
    
    # 3. Simulação de Desempenho no TAF
    # Quem reprova no TAF
    reprovados_taf = df_sim['Convocado_TAF_Sim'] & (scores_taf < taxa_taf)
    total_reprovados_taf = int(reprovados_taf.sum())
    
    df_sim['Status_TAF_Sim'] = 'Não Convocado'
    df_sim.loc[df_sim['Convocado_TAF_Sim'], 'Status_TAF_Sim'] = 'Apto no TAF'
    df_sim.loc[reprovados_taf, 'Status_TAF_Sim'] = 'Reprovado / Ausente no TAF'
    
    # 4. Distribuição das Vagas Imediatas pós-TAF
    aptos_taf = df_sim[df_sim['Status_TAF_Sim'] == 'Apto no TAF'].copy()
    aptos_taf['Pos_Final_Geral_Aptos'] = range(1, len(aptos_taf) + 1)
    
    # 140 vagas Ampla Concorrência (Top 140 da Geral entre aptos no TAF)
    vagas_ampla = aptos_taf.head(140)
    idx_vagas_ampla = vagas_ampla.index
    
    # 40 vagas Cota Étnica (próximos cotistas étnicos aptos no TAF que não ocuparam a Ampla)
    cotistas_restantes = aptos_taf[(~aptos_taf.index.isin(idx_vagas_ampla)) & aptos_taf['Cota_Etnico_Sim']]
    vagas_etnico = cotistas_restantes.head(40)
    idx_vagas_etnico = vagas_etnico.index
    
    # 20 vagas PCD (próximos PCDs aptos no TAF que não ocuparam Ampla nem cota étnica)
    pcds_restantes = aptos_taf[(~aptos_taf.index.isin(idx_vagas_ampla)) & (~aptos_taf.index.isin(idx_vagas_etnico)) & aptos_taf['Cota_PCD_Sim']]
    vagas_pcd = pcds_restantes.head(20)
    idx_vagas_pcd = vagas_pcd.index
    
    # Marcador de vaga imediata simulada
    df_sim['Vaga_Imediata_Sim'] = 'Cadastro de Reserva'
    df_sim.loc[idx_vagas_ampla, 'Vaga_Imediata_Sim'] = '🏆 Vaga Imediata (Ampla Concorrência)'
    df_sim.loc[idx_vagas_etnico, 'Vaga_Imediata_Sim'] = '🏆 Vaga Imediata (Cota Étnico-Racial)'
    df_sim.loc[idx_vagas_pcd, 'Vaga_Imediata_Sim'] = '🏆 Vaga Imediata (Cota PCD)'
    
    ultimo_ampla_orig = int(vagas_ampla.iloc[-1]['Posição_Geral']) if len(vagas_ampla) > 0 else 140
    ultimo_etnico_orig = int(vagas_etnico.iloc[-1]['Pos_Lista_Etnico']) if len(vagas_etnico) > 0 else 40
    ultimo_pcd_orig = int(vagas_pcd.iloc[-1]['Pos_Lista_PCD']) if len(vagas_pcd) > 0 else 20
    
    # Candidatos que originalmente estavam no CR e entraram nas vagas imediatas da Geral
    novos_vagas_ampla = vagas_ampla[vagas_ampla['Posição_Geral'] > 140]
    
    # Candidatos que originalmente estavam no CR da cota e entraram nas vagas da cota
    novos_vagas_etnico = vagas_etnico[vagas_etnico['Pos_Lista_Etnico'] > 40]
    
    # Candidatos PCD que entraram nas vagas PCD além do 20º
    novos_vagas_pcd = vagas_pcd[vagas_pcd['Pos_Lista_PCD'] > 20]
    
    resumo = {
        'total_inaptos_etnico': total_inaptos_etnico,
        'total_inaptos_pcd': total_inaptos_pcd,
        'total_convocados_taf': total_convocados_taf,
        'total_reprovados_taf': total_reprovados_taf,
        'total_aptos_taf': len(aptos_taf),
        'nota_corte_ampla_taf': nota_corte_ampla_taf,
        'nota_corte_etnico_taf': nota_corte_etnico_taf,
        'ultimo_ampla_orig': ultimo_ampla_orig,
        'ganho_ampla': ultimo_ampla_orig - 140,
        'ultimo_etnico_orig': ultimo_etnico_orig,
        'ganho_etnico': ultimo_etnico_orig - 40,
        'ultimo_pcd_orig': ultimo_pcd_orig,
        'ganho_pcd': ultimo_pcd_orig - 20,
        'qtd_novos_vagas_ampla': len(novos_vagas_ampla),
        'qtd_novos_vagas_etnico': len(novos_vagas_etnico),
        'qtd_novos_vagas_pcd': len(novos_vagas_pcd),
        'qtd_novos_taf_etnico': len(novos_convocados_taf_etnico),
        'tempo_ms': round((time.time() - t0) * 1000, 1)
    }
    
    return df_sim, resumo, novos_vagas_ampla, novos_vagas_etnico, novos_convocados_taf_etnico

df = pd.read_parquet('pprn_dados.parquet')
df_sim, resumo, n_ampla, n_etnico, n_taf = executar_simulacao_completa(df, 15, 20, 'migrar_ampla', 20)
print('Resumo do teste:')
for k, v in resumo.items():
    print(f"  {k}: {v}")
print(f'Novos vagas ampla: {len(n_ampla)}')
print(f'Novos vagas etnico: {len(n_etnico)}')
print(f'Novos TAF etnico: {len(n_taf)}')
