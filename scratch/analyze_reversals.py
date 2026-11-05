import os
import pandas as pd

pasta = "Atualizacao 04 de novembro"
df_base = pd.read_parquet("pprn_dados.parquet")

# 1. Hetero PPP
f1 = os.path.join(pasta, "ANEXO I - EDITAL DE RESULTADO DA HETEROIDENTIFICAÇÃO E ANÁLISE DOCUMENTAL PÓS-RECURSOS – PPP.xlsx")
df1 = pd.read_excel(f1, header=None)
h1_dict = {}
for _, r in df1.iterrows():
    vals = [v for v in r.values if pd.notna(v)]
    insc = None; res = None
    for v in vals:
        s = str(v).strip()
        if s.isdigit() and len(s) >= 8:
            insc = int(s)
        elif s.upper() in ["DEFERIDO", "INDEFERIDO"]:
            res = s.upper()
    if insc and res:
        h1_dict[insc] = res

# 2. Hetero Ind/Qui
f2 = os.path.join(pasta, "ANEXO II - EDITAL DE RESULTADO DA HETEROIDENTIFICAÇÃO E ANÁLISE DOCUMENTAL PÓS-RECURSOS –  QUILOMBOLA E INDIGENA.xlsx")
df2 = pd.read_excel(f2, header=None)
h2_dict = {}
for _, r in df2.iterrows():
    vals = [v for v in r.values if pd.notna(v)]
    insc = None; res = None
    for v in vals:
        s = str(v).strip()
        if s.isdigit() and len(s) >= 8:
            insc = int(s)
        elif s.upper() in ["DEFERIDO", "INDEFERIDO"]:
            res = s.upper()
    if insc and res:
        h2_dict[insc] = res

# 3. PCD
f3 = os.path.join(pasta, "ANEXO ÚNICO - EDITAL DE RESULTADO DA PERÍCIA MÉDICA PÓS-RECURSOS – PESSOA COM DEFICIÊNCIA.xlsx")
df3 = pd.read_excel(f3, header=None)
pcd_dict = {}
for _, r in df3.iterrows():
    vals = [v for v in r.values if pd.notna(v)]
    insc = None; res = None
    for v in vals:
        s = str(v).strip()
        if s.isdigit() and len(s) >= 8:
            insc = int(s)
        elif s.upper() in ["DEFERIDO", "INDEFERIDO"]:
            res = s.upper()
    if insc and res:
        pcd_dict[insc] = res

print(f"Hetero PPP pós-recursos: {len(h1_dict)} registros. Deferidos: {sum(1 for v in h1_dict.values() if v=='DEFERIDO')}, Indeferidos: {sum(1 for v in h1_dict.values() if v=='INDEFERIDO')}")
print(f"Hetero Ind/Qui pós-recursos: {len(h2_dict)} registros. Deferidos: {sum(1 for v in h2_dict.values() if v=='DEFERIDO')}, Indeferidos: {sum(1 for v in h2_dict.values() if v=='INDEFERIDO')}")
print(f"Perícia PCD pós-recursos: {len(pcd_dict)} registros. Deferidos: {sum(1 for v in pcd_dict.values() if v=='DEFERIDO')}, Indeferidos: {sum(1 for v in pcd_dict.values() if v=='INDEFERIDO')}")

# Contar reversões
h_total_dict = {**h1_dict, **h2_dict}
revertidos_etnico = 0
for insc, novo_res in h_total_dict.items():
    cand = df_base[df_base['Inscrição'] == insc]
    if len(cand) > 0:
        velho_res = cand.iloc[0]['Resultado_Hetero']
        if velho_res == 'INDEFERIDO' and novo_res == 'DEFERIDO':
            revertidos_etnico += 1

revertidos_pcd = 0
for insc, novo_res in pcd_dict.items():
    cand = df_base[df_base['Inscrição'] == insc]
    if len(cand) > 0:
        velho_res = cand.iloc[0]['Resultado_PCD']
        if velho_res == 'INDEFERIDO' and novo_res == 'DEFERIDO':
            revertidos_pcd += 1

print(f"\nRecursos providos pela banca (reversões pós-recurso):")
print(f"Étnico-Racial: {revertidos_etnico} recursos providos (de INDEFERIDO para DEFERIDO)!")
print(f"Perícia PCD: {revertidos_pcd} recursos providos (de INDEFERIDO para DEFERIDO)!")
