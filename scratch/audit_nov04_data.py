import os
import sys
import pandas as pd
import numpy as np

def audit():
    pasta = "Atualizacao 04 de novembro"
    
    # 1. Carregar base do site
    df_base = pd.read_parquet("pprn_dados.parquet")
    print(f"Base do site carregada: {len(df_base)} candidatos")
    
    # 2. Ler Convocados TAF (Anexo I Convocação TAF)
    f_taf = os.path.join(pasta, "ANEXO I - EDITAL DE CONVOCAÇÃO PARA O TESTE DE APTIDÃO FÍSICA.xlsx")
    df_taf_raw = pd.read_excel(f_taf, header=None)
    # Encontrar linha de cabeçalho
    h_idx = None
    for i in range(10):
        row_str = " ".join([str(x) for x in df_taf_raw.iloc[i].dropna()])
        if "Inscrição" in row_str or "Inscricao" in row_str:
            h_idx = i
            break
            
    df_taf = df_taf_raw.iloc[h_idx+1:].copy()
    # Procurar colunas Nome e Inscrição
    col_nome = None
    col_insc = None
    for c in df_taf.columns:
        val = str(df_taf_raw.iloc[h_idx, c]).strip().lower()
        if "nome" in val:
            col_nome = c
        elif "inscri" in val:
            col_insc = c
            
    df_taf = df_taf[[col_nome, col_insc]].dropna()
    df_taf.columns = ["Nome", "Inscrição"]
    df_taf["Inscrição"] = df_taf["Inscrição"].astype(int)
    taf_inscricoes = set(df_taf["Inscrição"])
    print(f"Total convocados oficiais para o TAF (Anexo I Convocação): {len(taf_inscricoes)}")
    
    # 3. Ler Anexo IV (Classificação Geral dos Habilitados para Prosseguimento / TAF)
    f_anexo4 = os.path.join(pasta, "ANEXO IV - EDITAL DE CLASSIFICAÇÃO PARA PROSSEGUIMENTO NO CERTAME.xlsx")
    df_a4_raw = pd.read_excel(f_anexo4, header=None)
    h4_idx = None
    for i in range(10):
        row_str = " ".join([str(x) for x in df_a4_raw.iloc[i].dropna()])
        if "Inscrição" in row_str or "Inscricao" in row_str:
            h4_idx = i
            break
            
    # Mapear colunas do Anexo IV
    header_row = df_a4_raw.iloc[h4_idx]
    col_map = {}
    for c in df_a4_raw.columns:
        v = str(header_row[c]).strip().lower()
        if "nome" in v: col_map["Nome"] = c
        elif "inscri" in v: col_map["Inscrição"] = c
        elif "nota" in v: col_map["Nota"] = c
        elif "modalidade" in v: col_map["Modalidade"] = c
        elif "posi" in v: col_map["Posição"] = c
        elif "empate" in v: col_map["Empate"] = c
        
    df_a4 = df_a4_raw.iloc[h4_idx+1:][list(col_map.values())].dropna(subset=[col_map["Inscrição"]]).copy()
    df_a4.columns = list(col_map.keys())
    df_a4["Inscrição"] = df_a4["Inscrição"].astype(int)
    print(f"Total no Anexo IV (Habilitados Prosseguimento): {len(df_a4)}")
    print("Distribuição por modalidade no Anexo IV:")
    print(df_a4["Modalidade"].value_counts())
    
    # 4. Ler Hetero PPP pós-recursos
    f_ppp = os.path.join(pasta, "ANEXO I - EDITAL DE RESULTADO DA HETEROIDENTIFICAÇÃO E ANÁLISE DOCUMENTAL PÓS-RECURSOS – PPP.xlsx")
    df_ppp_raw = pd.read_excel(f_ppp, header=None)
    for i in range(10):
        if "Inscrição" in " ".join([str(x) for x in df_ppp_raw.iloc[i].dropna()]):
            h_ppp = i; break
    df_ppp = df_ppp_raw.iloc[h_ppp+1:].dropna(subset=[1, 2, 4 if 4 in df_ppp_raw.columns else 3])
    # colunas: Nome, Inscrição, Resultado
    ppp_dict = {}
    for _, r in df_ppp_raw.iloc[h_ppp+1:].iterrows():
        # r[1]: Nome, r[3]: Insc, r[5]: Res ou similar
        vals = [v for v in r.values if pd.notna(v)]
        if len(vals) >= 3:
            # encontrar qual valor é número de inscrição
            insc = None
            res = None
            for v in vals:
                if str(v).isdigit() and len(str(v)) >= 5:
                    insc = int(v)
                elif str(v).strip().upper() in ["DEFERIDO", "INDEFERIDO"]:
                    res = str(v).strip().upper()
            if insc and res:
                ppp_dict[insc] = res
    print(f"Hetero PPP pós-recursos lidos: {len(ppp_dict)} (Deferidos: {sum(1 for v in ppp_dict.values() if v=='DEFERIDO')}, Indeferidos: {sum(1 for v in ppp_dict.values() if v=='INDEFERIDO')})")

    # 5. Ler PCD pós-recursos
    f_pcd = os.path.join(pasta, "ANEXO ÚNICO - EDITAL DE RESULTADO DA PERÍCIA MÉDICA PÓS-RECURSOS – PESSOA COM DEFICIÊNCIA.xlsx")
    df_pcd_raw = pd.read_excel(f_pcd, header=None)
    for i in range(10):
        if "Inscrição" in " ".join([str(x) for x in df_pcd_raw.iloc[i].dropna()]):
            h_pcd = i; break
    pcd_dict = {}
    for _, r in df_pcd_raw.iloc[h_pcd+1:].iterrows():
        vals = [v for v in r.values if pd.notna(v)]
        if len(vals) >= 3:
            insc = None; res = None
            for v in vals:
                if str(v).isdigit() and len(str(v)) >= 5:
                    insc = int(v)
                elif str(v).strip().upper() in ["DEFERIDO", "INDEFERIDO"]:
                    res = str(v).strip().upper()
            if insc and res:
                pcd_dict[insc] = res
    print(f"Perícia PCD pós-recursos lidos: {len(pcd_dict)} (Deferidos: {sum(1 for v in pcd_dict.values() if v=='DEFERIDO')}, Indeferidos: {sum(1 for v in pcd_dict.values() if v=='INDEFERIDO')})")

    # 6. Comparar previsões do site com TAF oficial
    site_convocados = set(df_base[df_base["Convocado_TAF_Preliminar"]]["Inscrição"])
    print(f"\nSite previu convocados TAF: {len(site_convocados)}")
    print(f"Banca convocou oficialmente TAF: {len(taf_inscricoes)}")
    
    inter = site_convocados.intersection(taf_inscricoes)
    so_no_site = site_convocados - taf_inscricoes
    so_na_banca = taf_inscricoes - site_convocados
    
    print(f"Concordância exata (Verdadeiros Positivos): {len(inter)}")
    print(f"Previstos no site mas NÃO na banca de 04/11: {len(so_no_site)}")
    print(f"Convocados na banca de 04/11 mas NÃO previstos no site: {len(so_na_banca)}")
    
    total = len(df_base)
    vn = total - len(site_convocados.union(taf_inscricoes))
    acertos = len(inter) + vn
    acuracia = (acertos / total) * 100
    print(f"\nACURÁCIA GLOBAL TAF: {acuracia:.2f}% ({acertos}/{total} acertos)")
    print(f"Precisão: {len(inter)/len(site_convocados)*100:.2f}%")
    print(f"Sensibilidade (Recall): {len(inter)/len(taf_inscricoes)*100:.2f}%")
    
    if len(so_na_banca) > 0:
        print("\nExemplo de candidatos que entraram na banca pós-recurso:")
        ex_entraram = df_base[df_base["Inscrição"].isin(so_na_banca)].head(10)
        print(ex_entraram[["Nome", "Inscrição", "Nota Objetiva", "Modalidade_Concorrencia", "Resultado_Hetero", "Resultado_PCD"]])
        
    if len(so_no_site) > 0:
        print("\nExemplo de candidatos que não foram chamados pela banca:")
        ex_sairam = df_base[df_base["Inscrição"].isin(so_no_site)].head(10)
        print(ex_sairam[["Nome", "Inscrição", "Nota Objetiva", "Modalidade_Concorrencia", "Resultado_Hetero", "Resultado_PCD"]])

if __name__ == "__main__":
    audit()

