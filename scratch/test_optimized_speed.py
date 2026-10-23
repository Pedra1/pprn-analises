import time
import pandas as pd
import numpy as np

t0 = time.time()
df = pd.read_parquet('pprn_dados.parquet')
t1 = time.time()

# Test fast lookup by inscription
insc_map = {str(insc): i for i, insc in enumerate(df['Inscrição'])}
t2 = time.time()

# Lookup test
test_insc = '2320045431'
idx = insc_map.get(test_insc)
cand = df.iloc[idx]
t3 = time.time()

print(f"Parquet load: {t1-t0:.4f}s")
print(f"Insc map build: {t2-t1:.4f}s")
print(f"Insc lookup time: {(t3-t2)*1000:.4f}ms -> Cand: {cand['Nome']}")
print(f"Precomputed sim fields: Pos Etnico={cand.get('Pos_Etnico_Sim_Padrao')}, TAF={cand.get('Convocado_TAF_Sim_Padrao')}")
