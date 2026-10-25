"""
Motor de Simulação Preditiva Pós-Bancas de Heteroidentificação e TAF.
"""

import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner="Calculando simulação pós-bancas e TAF...")
def executar_simulacao_pos_bancas(
    _df_base,
    modo="real_bancas",
    taxa_reversao_etnico_pct=5,
    taxa_reversao_pcd_pct=5,
    taxa_taf_pct=20,
    sim_taxa_hetero_pct=48,
    sim_taxa_pcd_pct=28,
    regra_inaptos='migrar_ampla'
):
    df_sim = _df_base.copy()

    if modo == "real_bancas":
        rng_rev_etnico = np.random.RandomState(42)
        rng_rev_pcd = np.random.RandomState(123)

        idx_indef_etnico = df_sim[df_sim['Cota_Etnico_Racial'] & (~df_sim['Cota_Etnico_Apta_Preliminar'])].index
        scores_rev_etnico = pd.Series(rng_rev_etnico.rand(len(idx_indef_etnico)), index=idx_indef_etnico)
        revertidos_etnico = idx_indef_etnico[scores_rev_etnico < (taxa_reversao_etnico_pct / 100.0)]

        idx_indef_pcd = df_sim[df_sim['Cota_PCD'] & (~df_sim['Cota_PCD_Apta_Preliminar'])].index
        scores_rev_pcd = pd.Series(rng_rev_pcd.rand(len(idx_indef_pcd)), index=idx_indef_pcd)
        revertidos_pcd = idx_indef_pcd[scores_rev_pcd < (taxa_reversao_pcd_pct / 100.0)]

        df_sim['Cota_Etnico_Sim'] = df_sim['Cota_Etnico_Apta_Preliminar'].copy()
        df_sim.loc[revertidos_etnico, 'Cota_Etnico_Sim'] = True

        df_sim['Cota_PCD_Sim'] = df_sim['Cota_PCD_Apta_Preliminar'].copy()
        df_sim.loc[revertidos_pcd, 'Cota_PCD_Sim'] = True

        total_inaptos_etnico = len(df_sim[df_sim['Cota_Etnico_Racial'] & (~df_sim['Cota_Etnico_Sim'])])
        total_inaptos_pcd = len(df_sim[df_sim['Cota_PCD'] & (~df_sim['Cota_PCD_Sim'])])

    else:
        rng_etnico = np.random.RandomState(42)
        scores_etnico = pd.Series(rng_etnico.rand(len(df_sim)), index=df_sim.index)
        rng_pcd = np.random.RandomState(123)
        scores_pcd = pd.Series(rng_pcd.rand(len(df_sim)), index=df_sim.index)

        is_inapto_etnico = df_sim['Cota_Etnico_Racial'] & (scores_etnico < (sim_taxa_hetero_pct / 100.0))
        is_inapto_pcd = df_sim['Cota_PCD'] & (scores_pcd < (sim_taxa_pcd_pct / 100.0))

        df_sim['Cota_Etnico_Sim'] = df_sim['Cota_Etnico_Racial'] & (~is_inapto_etnico)
        df_sim['Cota_PCD_Sim'] = df_sim['Cota_PCD'] & (~is_inapto_pcd)
        total_inaptos_etnico = int(is_inapto_etnico.sum())
        total_inaptos_pcd = int(is_inapto_pcd.sum())

    idx_etnico_aptos = df_sim[df_sim['Cota_Etnico_Sim']].index
    df_sim['Pos_Etnico_Sim'] = np.nan
    df_sim.loc[idx_etnico_aptos, 'Pos_Etnico_Sim'] = range(1, len(idx_etnico_aptos) + 1)

    idx_pcd_aptos = df_sim[df_sim['Cota_PCD_Sim']].index
    df_sim['Pos_PCD_Sim'] = np.nan
    df_sim.loc[idx_pcd_aptos, 'Pos_PCD_Sim'] = range(1, len(idx_pcd_aptos) + 1)

    cand_960 = df_sim.iloc[959]
    corte_ampla_taf = int(cand_960['Nota Objetiva'])
    convocados_ampla_taf = df_sim['Nota Objetiva'] >= corte_ampla_taf

    cotistas_fora_ampla = df_sim[df_sim['Cota_Etnico_Sim'] & (~convocados_ampla_taf)]
    if len(cotistas_fora_ampla) >= 240:
        cand_240_cota = cotistas_fora_ampla.iloc[239]
        corte_etnico_taf = int(cand_240_cota['Nota Objetiva'])
        convocados_etnico_reserva = cotistas_fora_ampla['Nota Objetiva'] >= corte_etnico_taf
        idx_etnico_reserva = cotistas_fora_ampla[convocados_etnico_reserva].index
    else:
        corte_etnico_taf = int(cotistas_fora_ampla['Nota Objetiva'].min()) if len(cotistas_fora_ampla) > 0 else 73
        idx_etnico_reserva = cotistas_fora_ampla.index

    idx_pcd_taf = df_sim[df_sim['Cota_PCD_Sim']].index

    df_sim['Convocado_TAF_Sim'] = False
    df_sim.loc[df_sim[convocados_ampla_taf].index, 'Convocado_TAF_Sim'] = True
    df_sim.loc[idx_etnico_reserva, 'Convocado_TAF_Sim'] = True
    df_sim.loc[idx_pcd_taf, 'Convocado_TAF_Sim'] = True

    total_convocados_taf = int(df_sim['Convocado_TAF_Sim'].sum())

    rng_taf = np.random.RandomState(777)
    scores_taf = pd.Series(rng_taf.rand(len(df_sim)), index=df_sim.index)
    reprovados_taf = df_sim['Convocado_TAF_Sim'] & (scores_taf < (taxa_taf_pct / 100.0))
    total_reprovados_taf = int(reprovados_taf.sum())

    df_sim['Status_TAF_Sim'] = 'Não Convocado'
    df_sim.loc[df_sim['Convocado_TAF_Sim'], 'Status_TAF_Sim'] = 'Apto no TAF'
    df_sim.loc[reprovados_taf, 'Status_TAF_Sim'] = 'Reprovado / Ausente no TAF'

    aptos_taf = df_sim[df_sim['Status_TAF_Sim'] == 'Apto no TAF'].copy()
    aptos_taf['Pos_Final_Geral_Aptos'] = range(1, len(aptos_taf) + 1)

    vagas_ampla = aptos_taf.head(140)
    idx_vagas_ampla = vagas_ampla.index

    aptos_etnico_fora_ampla = aptos_taf[aptos_taf['Cota_Etnico_Sim'] & (~aptos_taf.index.isin(idx_vagas_ampla))]
    vagas_etnico = aptos_etnico_fora_ampla.head(40)
    idx_vagas_etnico = vagas_etnico.index

    aptos_pcd_fora_ampla = aptos_taf[aptos_taf['Cota_PCD_Sim'] & (~aptos_taf.index.isin(idx_vagas_ampla)) & (~aptos_taf.index.isin(idx_vagas_etnico))]
    vagas_pcd = aptos_pcd_fora_ampla.head(20)
    idx_vagas_pcd = vagas_pcd.index

    df_sim['Vaga_Imediata_Sim'] = '📋 Cadastro de Reserva'
    df_sim.loc[idx_vagas_ampla, 'Vaga_Imediata_Sim'] = '🏆 Vaga Imediata (Ampla Concorrência)'
    df_sim.loc[idx_vagas_etnico, 'Vaga_Imediata_Sim'] = '🏆 Vaga Imediata (Cota Étnico-Racial)'
    df_sim.loc[idx_vagas_pcd, 'Vaga_Imediata_Sim'] = '🏆 Vaga Imediata (Cota PCD)'

    ultimo_ampla_orig = int(vagas_ampla.iloc[-1]['Posição_Geral']) if len(vagas_ampla) > 0 else 140
    ultimo_etnico_orig = int(vagas_etnico.iloc[-1]['Pos_Lista_Etnico']) if len(vagas_etnico) > 0 else 40
    ultimo_pcd_orig = int(vagas_pcd.iloc[-1]['Pos_Lista_PCD']) if len(vagas_pcd) > 0 else 20

    novos_vagas_ampla = vagas_ampla[vagas_ampla['Posição_Geral'] > 140]
    novos_vagas_etnico = vagas_etnico[vagas_etnico['Pos_Lista_Etnico'] > 40]
    novos_vagas_pcd = vagas_pcd[vagas_pcd['Pos_Lista_PCD'] > 20]

    resumo = {
        'total_inaptos_etnico': total_inaptos_etnico,
        'total_inaptos_pcd': total_inaptos_pcd,
        'total_convocados_taf': total_convocados_taf,
        'total_reprovados_taf': total_reprovados_taf,
        'total_aptos_taf': len(aptos_taf),
        'corte_ampla_taf': corte_ampla_taf,
        'corte_etnico_taf': corte_etnico_taf,
        'ultimo_ampla_orig': ultimo_ampla_orig,
        'ganho_ampla': ultimo_ampla_orig - 140,
        'ultimo_etnico_orig': ultimo_etnico_orig,
        'ganho_etnico': ultimo_etnico_orig - 40,
        'ultimo_pcd_orig': ultimo_pcd_orig,
        'ganho_pcd': ultimo_pcd_orig - 20,
        'qtd_novos_vagas_ampla': len(novos_vagas_ampla),
        'qtd_novos_vagas_etnico': len(novos_vagas_etnico),
        'qtd_novos_vagas_pcd': len(novos_vagas_pcd),
    }

    return df_sim, resumo, novos_vagas_ampla, novos_vagas_etnico, novos_vagas_pcd
