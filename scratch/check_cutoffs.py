import os
import pandas as pd

pasta = "Atualizacao 04 de novembro"
f_a4 = os.path.join(pasta, "ANEXO IV - EDITAL DE CLASSIFICAÇÃO PARA PROSSEGUIMENTO NO CERTAME.xlsx")
df_a4_raw = pd.read_excel(f_a4, header=None)

cands = []
for idx, row in df_a4_raw.iterrows():
    vals = [v for v in row.values if pd.notna(v)]
    if not vals: continue
    insc = None; nome = None; nota = None; mod = None; pos = None
    for v in vals:
        s = str(v).strip()
        if (s.isdigit() or isinstance(v, (int, float))) and float(v) > 2000000000:
            insc = int(v)
        elif s.upper() in ["AC", "ÉT-R", "ET-R", "PCD"]:
            mod = s.upper()
    if insc:
        # pegar nota e posição
        # no anexo IV: Col 1: Nome, Col 4: Insc, Col 7: Nota, Col 10: Modalidade, Col 13: Pos, Col 16: Empate
        # Vamos achar o float/int que corresponde à nota (entre 50 e 150)
        num_vals = []
        for v in vals:
            try:
                fn = float(v)
                if 50 <= fn <= 145:
                    num_vals.append(fn)
            except:
                pass
        nota = num_vals[0] if num_vals else None
        cands.append({"Inscrição": insc, "Modalidade": mod, "Nota": nota})

df_a4 = pd.DataFrame(cands)
print(f"Total de registros analisados no Anexo IV: {len(df_a4)}")
for mod in ["AC", "ÉT-R", "PCD"]:
    sub = df_a4[df_a4["Modalidade"] == mod]
    print(f"\nModalidade {mod}: {len(sub)} candidatos")
    if len(sub) > 0 and sub["Nota"].notna().any():
        print(f"  Maior nota: {sub['Nota'].max()}")
        print(f"  Menor nota (Linha de Corte Oficial): {sub['Nota'].min()}")
        print(f"  Qtd na nota de corte: {sum(sub['Nota'] == sub['Nota'].min())}")

