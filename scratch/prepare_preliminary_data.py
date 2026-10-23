import os
import pandas as pd
import numpy as np

def main():
    print("Iniciando processamento dos Resultados Preliminares de 23/10/2026...")
    
    # 1. Carregar base original
    df_base = pd.read_parquet('pprn_dados.parquet')
    print(f"Base carregada: {len(df_base)} candidatos")
    
    # 2. Carregar Anexo I (Preto e Pardo)
    f1 = 'ANEXO I - EDITAL DE RESULTADO PRELIMINAR DA HETEROIDENTIFICAÇÃO E ANÁLISE DOCUMENTAL –  preto e pardo (1) (1).xlsx'
    df1 = pd.read_excel(f1, header=None)
    f1_dict = {}
    for idx, row in df1.iterrows():
        val0, val2, val3, val4 = row[0], row[2], row[3], row[4]
        if pd.isna(val0) or str(val0).startswith('ANEXO') or str(val0).startswith('401') or str(val0) == 'Nome':
            continue
        res = val3 if pd.notna(val3) else val4
        f1_dict[int(val2)] = str(res).strip().upper()
    print(f"Anexo I (Preto/Pardo): {len(f1_dict)} registros. Deferidos: {sum(1 for v in f1_dict.values() if v=='DEFERIDO')}, Indeferidos: {sum(1 for v in f1_dict.values() if v=='INDEFERIDO')}")

    # 3. Carregar Anexo II (Indígena e Quilombola)
    f2 = 'ANEXO II - EDITAL DE RESULTADO PRELIMINAR DA HETEROIDENTIFICAÇÃO E ANÁLISE DOCUMENTAL – indigena e quilombola (1).xlsx'
    df2 = pd.read_excel(f2, header=None)
    f2_dict_ind = {}
    f2_dict_qui = {}
    current_sec = None
    for idx, row in df2.iterrows():
        r_str = ' '.join([str(v) for v in row.values if pd.notna(v)])
        if 'INDÍGENAS:' in r_str.upper() or 'INDIGENAS:' in r_str.upper():
            current_sec = 'INDIGENA'
            continue
        elif 'QUILOMBOLAS:' in r_str.upper():
            current_sec = 'QUILOMBOLA'
            continue
        if any(k in r_str.upper() for k in ['401', 'ANEXO', 'NOME']):
            continue
        if pd.notna(row[1]) and pd.notna(row[3]) and pd.notna(row[5]):
            insc = int(row[3])
            res = str(row[5]).strip().upper()
        elif pd.notna(row[0]) and pd.notna(row[2]) and pd.notna(row[4]):
            insc = int(row[2])
            res = str(row[4]).strip().upper()
        else:
            continue
            
        if current_sec == 'INDIGENA':
            f2_dict_ind[insc] = res
        else:
            f2_dict_qui[insc] = res
            
    print(f"Anexo II (Indígenas): {len(f2_dict_ind)} registros. Deferidos: {sum(1 for v in f2_dict_ind.values() if v=='DEFERIDO')}, Indeferidos: {sum(1 for v in f2_dict_ind.values() if v=='INDEFERIDO')}")
    print(f"Anexo II (Quilombolas): {len(f2_dict_qui)} registros. Deferidos: {sum(1 for v in f2_dict_qui.values() if v=='DEFERIDO')}, Indeferidos: {sum(1 for v in f2_dict_qui.values() if v=='INDEFERIDO')}")

    # 4. Carregar Anexo Único (PCD)
    f3 = 'ANEXO ÚNICO - EDITAL DE RESULTADO PRELIMINAR DA PERÍCIA MÉDICA (1).xlsx'
    df3 = pd.read_excel(f3, header=None)
    f3_dict = {}
    for idx, row in df3.iterrows():
        val0, val2, val4 = row[0], row[2], row[4]
        if pd.isna(val0) or str(val0).startswith('ANEXO') or str(val0).startswith('401') or str(val0) == 'Nome':
            continue
        f3_dict[int(val2)] = str(val4).strip().upper()
    print(f"Anexo Único (PCD): {len(f3_dict)} registros. Deferidos: {sum(1 for v in f3_dict.values() if v=='DEFERIDO')}, Indeferidos: {sum(1 for v in f3_dict.values() if v=='INDEFERIDO')}")

    # 5. Adicionar colunas de resultado individual ao DataFrame base
    df = df_base.copy()
    
    # Status individual por banca
    df['Resultado_PPP'] = df['Inscrição'].map(f1_dict).fillna('Não se Aplica')
    df['Resultado_Indigena'] = df['Inscrição'].map(f2_dict_ind).fillna('Não se Aplica')
    df['Resultado_Quilombola'] = df['Inscrição'].map(f2_dict_qui).fillna('Não se Aplica')
    df['Resultado_PCD'] = df['Inscrição'].map(f3_dict).fillna('Não se Aplica')
    
    # Resultado Étnico Consolidado:
    # Se o candidato foi DEFERIDO em qualquer uma das categorias étnicas que concorreu, considera DEFERIDO.
    # Se participou de banca étnica e foi INDEFERIDO (e em nenhuma DEFERIDO), considera INDEFERIDO.
    def calc_res_etnico(row):
        r_ppp = row['Resultado_PPP']
        r_ind = row['Resultado_Indigena']
        r_qui = row['Resultado_Quilombola']
        
        status_list = [s for s in [r_ppp, r_ind, r_qui] if s != 'Não se Aplica']
        if not status_list:
            return 'Não se Aplica'
        if 'DEFERIDO' in status_list:
            return 'DEFERIDO'
        return 'INDEFERIDO'
        
    df['Resultado_Hetero'] = df.apply(calc_res_etnico, axis=1)
    
    # Aptidão oficial preliminar nas cotas
    df['Cota_Etnico_Apta_Preliminar'] = df['Cota_Etnico_Racial'] & (df['Resultado_Hetero'] == 'DEFERIDO')
    df['Cota_PCD_Apta_Preliminar'] = df['Cota_PCD'] & (df['Resultado_PCD'] == 'DEFERIDO')
    
    # Status Cota Consolidado Descritivo
    def get_status_cota_desc(row):
        etnico_apto = row['Cota_Etnico_Apta_Preliminar']
        pcd_apto = row['Cota_PCD_Apta_Preliminar']
        is_etnico = row['Cota_Etnico_Racial']
        is_pcd = row['Cota_PCD']
        
        if is_etnico and is_pcd:
            if etnico_apto and pcd_apto:
                return '✅ Confirmado em Ambas as Cotas (Étnico e PCD)'
            elif etnico_apto and not pcd_apto:
                return '✅ Confirmado em Cota Étnica | ⚠️ PCD Indeferido'
            elif not etnico_apto and pcd_apto:
                return '⚠️ Cota Étnica Indeferida | ✅ Confirmado em Cota PCD'
            else:
                return '⚠️ Ambas as Cotas Indeferidas (Concorre na Ampla)'
        elif is_etnico:
            if etnico_apto:
                return '✅ Deferido na Cota Étnico-Racial (Preliminar)'
            else:
                return '⚠️ Indeferido na Cota Étnica (Concorre na Ampla)'
        elif is_pcd:
            if pcd_apto:
                return '✅ Deferido na Perícia Médica PCD (Preliminar)'
            else:
                return '⚠️ Indeferido na Perícia PCD (Concorre na Ampla)'
        else:
            return '🏛️ Não Cotista (Ampla Concorrência Direta)'
            
    df['Status_Cota_Preliminar'] = df.apply(get_status_cota_desc, axis=1)
    
    # 6. Recálculo das Colocações Preliminares Reais
    # Apenas cotistas deferidos permanecem na lista de reserva de cota
    # Cota Étnica
    idx_etnico_aptos = df[df['Cota_Etnico_Apta_Preliminar']].index
    df['Nova_Pos_Lista_Etnico'] = np.nan
    df.loc[idx_etnico_aptos, 'Nova_Pos_Lista_Etnico'] = range(1, len(idx_etnico_aptos) + 1)
    df['Ganho_Pos_Etnico'] = df['Pos_Lista_Etnico'] - df['Nova_Pos_Lista_Etnico']
    
    # Cota PCD
    idx_pcd_aptos = df[df['Cota_PCD_Apta_Preliminar']].index
    df['Nova_Pos_Lista_PCD'] = np.nan
    df.loc[idx_pcd_aptos, 'Nova_Pos_Lista_PCD'] = range(1, len(idx_pcd_aptos) + 1)
    df['Ganho_Pos_PCD'] = df['Pos_Lista_PCD'] - df['Nova_Pos_Lista_PCD']

    # 7. Recálculo Oficial Preliminar da Linha de Corte do TAF (com bancas reais!)
    # Ampla Concorrência: Top 960 geral + todos com nota igual ao 960º colocado geral
    cand_960 = df.iloc[959]
    corte_ampla_taf = int(cand_960['Nota Objetiva'])
    convocados_ampla_taf = df['Nota Objetiva'] >= corte_ampla_taf
    
    # Cotistas Étnicos Aptos chamados pela reserva da cota (fora dos convocados na ampla):
    # Conforme o edital: até o 240º cotista fora da ampla + empatados
    cotistas_aptos_fora_ampla = df[df['Cota_Etnico_Apta_Preliminar'] & (~convocados_ampla_taf)]
    if len(cotistas_aptos_fora_ampla) >= 240:
        cand_240_cota = cotistas_aptos_fora_ampla.iloc[239]
        corte_etnico_taf = int(cand_240_cota['Nota Objetiva'])
        convocados_etnico_reserva = cotistas_aptos_fora_ampla['Nota Objetiva'] >= corte_etnico_taf
        idx_etnico_taf_reserva = cotistas_aptos_fora_ampla[convocados_etnico_reserva].index
    else:
        corte_etnico_taf = int(cotistas_aptos_fora_ampla['Nota Objetiva'].min()) if len(cotistas_aptos_fora_ampla) > 0 else 73
        idx_etnico_taf_reserva = cotistas_aptos_fora_ampla.index
        
    # PCDs Aptos: Todos com nota >= 73 (sem corte)
    idx_pcd_taf = df[df['Cota_PCD_Apta_Preliminar']].index
    
    df['Convocado_TAF_Preliminar'] = False
    df.loc[df[convocados_ampla_taf].index, 'Convocado_TAF_Preliminar'] = True
    df.loc[idx_etnico_taf_reserva, 'Convocado_TAF_Preliminar'] = True
    df.loc[idx_pcd_taf, 'Convocado_TAF_Preliminar'] = True
    
    def get_previsao_taf_preliminar(row):
        is_convocado = row['Convocado_TAF_Preliminar']
        if not is_convocado:
            if row['Cota_Etnico_Apta_Preliminar']:
                return '⚪ Fora da Linha de Corte do TAF (Pontuação na Cota Étnica abaixo de 113 pts)'
            elif row['Cota_PCD_Apta_Preliminar']:
                return '⚪ Fora da Linha de Corte do TAF (Pontuação PCD abaixo de 73 pts)'
            elif row['Cota_Etnico_Racial'] and row['Resultado_Hetero'] == 'INDEFERIDO':
                return '⚪ Fora do Corte do TAF (Cota Étnica Indeferida preliminarmente, nota abaixo do corte de Ampla)'
            elif row['Cota_PCD'] and row['Resultado_PCD'] == 'INDEFERIDO':
                return '⚪ Fora do Corte do TAF (Laudo PCD Indeferido preliminarmente, nota abaixo do corte de Ampla)'
            else:
                return '⚪ Fora da Linha de Corte do TAF (Ampla Concorrência abaixo de 119 pts)'
        else:
            if row['Posição_Geral'] <= 960 or row['Nota Objetiva'] >= corte_ampla_taf:
                if row['Cota_Etnico_Apta_Preliminar']:
                    return '🟢 Convocado para o TAF (Classificado dentro da Ampla Concorrência - Cota Confirmada)'
                elif row['Cota_PCD_Apta_Preliminar']:
                    return '🟢 Convocado para o TAF (Classificado dentro da Ampla Concorrência - PCD Confirmado)'
                elif row['Resultado_Hetero'] == 'INDEFERIDO' or row['Resultado_PCD'] == 'INDEFERIDO':
                    return '🟢 Convocado para o TAF via Ampla Concorrência (Mesmo com indeferimento na cota, nota alcançou a Ampla!)'
                else:
                    return '🟢 Convocado para o TAF (Ampla Concorrência)'
            elif row['Cota_Etnico_Apta_Preliminar']:
                return '🟣 Convocado para o TAF (Reserva de Vagas da Cota Étnica)'
            elif row['Cota_PCD_Apta_Preliminar']:
                return '♿ Convocado para o TAF (Reserva de Vagas PCD)'
            return '🟢 Convocado para o TAF'
            
    df['Previsao_TAF_Preliminar'] = df.apply(get_previsao_taf_preliminar, axis=1)

    # 8. Previsão Preliminar de Vagas Imediatas pós-bancas
    # Ampla: Top 140 geral
    # Étnica: Top 40 cotistas aptos fora dos 140 da ampla
    # PCD: Top 20 PCDs aptos fora dos 140 da ampla
    top_140 = df.head(140)
    cotistas_aptos_fora_140 = df[df['Cota_Etnico_Apta_Preliminar'] & (~df.index.isin(top_140.index))]
    top_40_etnico = cotistas_aptos_fora_140.head(40)
    
    pcd_aptos_fora_140 = df[df['Cota_PCD_Apta_Preliminar'] & (~df.index.isin(top_140.index)) & (~df.index.isin(top_40_etnico.index))]
    top_20_pcd = pcd_aptos_fora_140.head(20)
    
    df['Previsao_Vagas_Preliminar'] = '📋 Cadastro de Reserva'
    df.loc[top_140.index, 'Previsao_Vagas_Preliminar'] = '🏆 Vaga Imediata (Ampla Concorrência)'
    df.loc[top_40_etnico.index, 'Previsao_Vagas_Preliminar'] = '🏆 Vaga Imediata (Cota Étnico-Racial)'
    df.loc[top_20_pcd.index, 'Previsao_Vagas_Preliminar'] = '🏆 Vaga Imediata (Cota PCD)'
    
    print("\n=== RESUMO GERAL DAS BANCAS DE 23/10 ===")
    print(f"Candidatos Étnicos Convocados: {df['Cota_Etnico_Racial'].sum()}")
    print(f"Étnicos DEFERIDOS: {df['Cota_Etnico_Apta_Preliminar'].sum()} ({df['Cota_Etnico_Apta_Preliminar'].sum() / df['Cota_Etnico_Racial'].sum() * 100:.1f}%)")
    print(f"Étnicos INDEFERIDOS: {df['Cota_Etnico_Racial'].sum() - df['Cota_Etnico_Apta_Preliminar'].sum()} ({(df['Cota_Etnico_Racial'].sum() - df['Cota_Etnico_Apta_Preliminar'].sum()) / df['Cota_Etnico_Racial'].sum() * 100:.1f}%)")
    
    print(f"\nCandidatos PCD Convocados: {df['Cota_PCD'].sum()}")
    print(f"PCDs DEFERIDOS: {df['Cota_PCD_Apta_Preliminar'].sum()} ({df['Cota_PCD_Apta_Preliminar'].sum() / df['Cota_PCD'].sum() * 100:.1f}%)")
    print(f"PCDs INDEFERIDOS: {df['Cota_PCD'].sum() - df['Cota_PCD_Apta_Preliminar'].sum()} ({(df['Cota_PCD'].sum() - df['Cota_PCD_Apta_Preliminar'].sum()) / df['Cota_PCD'].sum() * 100:.1f}%)")

    print(f"\nLinha de Corte TAF Ampla: {corte_ampla_taf} pts (Total convocados Ampla: {convocados_ampla_taf.sum()})")
    print(f"Linha de Corte TAF Cota Étnica: {corte_etnico_taf} pts (Total convocados na cota reserva: {len(idx_etnico_taf_reserva)})")
    print(f"Total PCDs Convocados TAF: {len(idx_pcd_taf)}")
    print(f"TOTAL GERAL CONVOCADOS TAF PÓS-BANCAS: {df['Convocado_TAF_Preliminar'].sum()}")
    
    # Salvar novo arquivo parquet enriquecido
    df.to_parquet('pprn_dados.parquet', index=False)
    print("\nArquivo pprn_dados.parquet atualizado com sucesso!")
    
    # Também vamos salvar os novos Excels oficiais para download!
    # 1. Lista Deferidos e Indeferidos Heteroidentificação & Análise Documental
    df_hetero_export = df[df['Cota_Etnico_Racial']][['Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Nota Objetiva', 'Resultado_Hetero', 'Nova_Pos_Lista_Etnico', 'Previsao_TAF_Preliminar']].copy()
    df_hetero_export.rename(columns={
        'Resultado_Hetero': 'Resultado Preliminar da Banca (23/10)',
        'Nova_Pos_Lista_Etnico': 'Nova Posição na Cota (Recalculada)',
        'Previsao_TAF_Preliminar': 'Situação para o TAF'
    }, inplace=True)
    df_hetero_export.to_excel("LISTA_PRELIMINAR_HETEROIDENTIFICACAO_23_OUTUBRO.xlsx", index=False)
    print("Salvo: LISTA_PRELIMINAR_HETEROIDENTIFICACAO_23_OUTUBRO.xlsx")
    
    # 2. Lista Deferidos e Indeferidos Perícia Médica PCD
    df_pcd_export = df[df['Cota_PCD']][['Posição_Geral', 'Nome', 'Inscrição', 'Nota Objetiva', 'Resultado_PCD', 'Nova_Pos_Lista_PCD', 'Previsao_TAF_Preliminar']].copy()
    df_pcd_export.rename(columns={
        'Resultado_PCD': 'Resultado Preliminar Perícia PCD (23/10)',
        'Nova_Pos_Lista_PCD': 'Nova Posição PCD (Recalculada)',
        'Previsao_TAF_Preliminar': 'Situação para o TAF'
    }, inplace=True)
    df_pcd_export.to_excel("LISTA_PRELIMINAR_PERICIA_PCD_23_OUTUBRO.xlsx", index=False)
    print("Salvo: LISTA_PRELIMINAR_PERICIA_PCD_23_OUTUBRO.xlsx")

    # 3. Lista Reclassificada das Cotas Étnicas Preliminar
    df_etnico_reclass = df[df['Cota_Etnico_Apta_Preliminar']].sort_values(by='Nova_Pos_Lista_Etnico').copy()
    df_etnico_reclass_export = df_etnico_reclass[['Nova_Pos_Lista_Etnico', 'Pos_Lista_Etnico', 'Ganho_Pos_Etnico', 'Posição_Geral', 'Nome', 'Inscrição', 'Nota Objetiva', 'Previsao_TAF_Preliminar', 'Previsao_Vagas_Preliminar']].copy()
    df_etnico_reclass_export.rename(columns={
        'Nova_Pos_Lista_Etnico': 'Posição Preliminar Pós-Banca',
        'Pos_Lista_Etnico': 'Posição Original (09/10)',
        'Ganho_Pos_Etnico': 'Posições Ganhas (+)',
        'Previsao_TAF_Preliminar': 'Situação TAF',
        'Previsao_Vagas_Preliminar': 'Situação Vagas'
    }, inplace=True)
    df_etnico_reclass_export.to_excel("LISTA_RECLASSIFICADA_COTA_ETNICA_PRELIMINAR.xlsx", index=False)
    print("Salvo: LISTA_RECLASSIFICADA_COTA_ETNICA_PRELIMINAR.xlsx")

    # 4. Lista Reclassificada PCD Preliminar
    df_pcd_reclass = df[df['Cota_PCD_Apta_Preliminar']].sort_values(by='Nova_Pos_Lista_PCD').copy()
    df_pcd_reclass_export = df_pcd_reclass[['Nova_Pos_Lista_PCD', 'Pos_Lista_PCD', 'Ganho_Pos_PCD', 'Posição_Geral', 'Nome', 'Inscrição', 'Nota Objetiva', 'Previsao_TAF_Preliminar', 'Previsao_Vagas_Preliminar']].copy()
    df_pcd_reclass_export.rename(columns={
        'Nova_Pos_Lista_PCD': 'Posição Preliminar Pós-Perícia',
        'Pos_Lista_PCD': 'Posição Original (09/10)',
        'Ganho_Pos_PCD': 'Posições Ganhas (+)',
        'Previsao_TAF_Preliminar': 'Situação TAF',
        'Previsao_Vagas_Preliminar': 'Situação Vagas'
    }, inplace=True)
    df_pcd_reclass_export.to_excel("LISTA_RECLASSIFICADA_PCD_PRELIMINAR.xlsx", index=False)
    print("Salvo: LISTA_RECLASSIFICADA_PCD_PRELIMINAR.xlsx")

if __name__ == '__main__':
    main()
