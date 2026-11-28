"""
Módulo Isolado de Classificação Combinada e Simulador Exclusivo para Candidatos Sub Judice.
Todas as funções operam estritamente sobre cópias em memória, sem alterar df_base,
boletins individuais, acurácia global ou demais listas oficiais do portal.
"""

import numpy as np
import pandas as pd
import streamlit as st
from src.config import CORTE_TAF_AMPLA


def _classificar_condicao_subjudice(row):
    """Retorna rótulo descritivo do vínculo e objeto liminar na tabela combinada."""
    if not bool(row.get("Is_Sub_Judice", False)):
        mod_taf = str(row.get("Modalidade_Convocacao_TAF", "Não Convocado"))
        if mod_taf == "Não Convocado":
            return "✅ Cotista Regular (Cota Homologada)"
        return f"✅ Cotista Regular ({mod_taf})"

    if bool(row.get("Cota_PCD", False)):
        res_pcd = str(row.get("Resultado_PCD_Definitivo", ""))
        if res_pcd.startswith("DEFERIDO"):
            return "⚖️ SUB JUDICE (PCD Deferido + Liminar)"
        return "⚖️ SUB JUDICE (Liminar TAF • Perícia Indef.)"

    res_het = str(row.get("Resultado_Hetero_Definitivo", ""))
    if "Sub Judice" in res_het:
        return "⚖️ SUB JUDICE (Hetero + TAF por Liminar)"
    if res_het.startswith("DEFERIDO"):
        return "⚖️ SUB JUDICE (Liminar TAF • Cota Deferida)"
    return "⚖️ SUB JUDICE (Liminar TAF • Hetero Indef.)"


@st.cache_data(show_spinner=False)
def construir_classificacao_combinada(_df_base, modalidade="etnico", escopo_etnico="taf"):
    """
    Constrói a classificação combinada (somente cotistas convocados ao TAF + Sub Judice) para a aba Sub Judice.

    Parâmetros:
        _df_base: DataFrame base imutável (não é modificado).
        modalidade: 'etnico' ou 'pcd'.
        escopo_etnico:
            - 'taf': Todos os cotistas étnicos aptos convocados ao TAF (605) + 21 Sub Judice (626).
            - 'reserva_taf': Cotistas convocados na reserva ÉT-R do TAF (276) + 21 Sub Judice (297).
    """
    if modalidade == "pcd":
        mascara = (
            _df_base["Cota_PCD_Apta_Definitivo"].fillna(False)
            & _df_base["Convocado_TAF_Oficial"].fillna(False)
        ) | (
            _df_base["Is_Sub_Judice"].fillna(False) & _df_base["Cota_PCD"].fillna(False)
        )
        col_pos_oficial = "Nova_Pos_Lista_PCD_Definitivo"
    else:
        is_sj_etn = _df_base["Is_Sub_Judice"].fillna(False) & _df_base["Cota_Etnico_Racial"].fillna(False)
        if escopo_etnico == "reserva_taf":
            mascara = (_df_base["Modalidade_Convocacao_TAF"] == "Cota Étnico-Racial (ÉT-R)") | is_sj_etn
        else:
            mascara = (
                _df_base["Cota_Etnico_Apta_Definitivo"].fillna(False)
                & _df_base["Convocado_TAF_Oficial"].fillna(False)
            ) | is_sj_etn
        col_pos_oficial = "Nova_Pos_Lista_Etnico_Definitivo"

    df_comb = _df_base[mascara].sort_values(by="Posição_Geral", ascending=True).copy()
    df_comb["Class_Combinada"] = np.arange(1, len(df_comb) + 1)
    df_comb["Is_Sub_Judice"] = df_comb["Is_Sub_Judice"].fillna(False).astype(bool)

    # Quantos Sub Judice estão estritamente acima de cada candidato nesta lista
    sj_flags = df_comb["Is_Sub_Judice"].to_numpy(dtype=int)
    sj_acima = np.cumsum(sj_flags) - sj_flags
    df_comb["SJ_Acima"] = sj_acima

    def _fmt_pos_oficial(val, is_sj):
        if pd.notna(val):
            return f"{int(val)}º"
        return "— (Sub Judice)" if is_sj else "—"

    df_comb["Pos_Oficial_Display"] = [
        _fmt_pos_oficial(v, sj)
        for v, sj in zip(df_comb[col_pos_oficial], df_comb["Is_Sub_Judice"])
    ]

    def _fmt_impacto(is_sj, pos_comb, pos_of, n_sj_acima):
        if is_sj:
            return "⚖️ DESTAQUE SUB JUDICE"
        if modalidade == "pcd" and pd.notna(pos_of):
            diff = int(pos_comb) - int(pos_of)
            if diff > 0:
                return f"+{diff} pos. ({n_sj_acima} SJ acima)"
            return "Sem deslocamento"
        if n_sj_acima > 0:
            return f"{n_sj_acima} Sub Judice acima"
        return "Sem deslocamento"

    df_comb["Impacto_Display"] = [
        _fmt_impacto(sj, pc, po, sa)
        for sj, pc, po, sa in zip(
            df_comb["Is_Sub_Judice"],
            df_comb["Class_Combinada"],
            df_comb[col_pos_oficial],
            df_comb["SJ_Acima"],
        )
    ]

    df_comb["Condicao_Lista"] = df_comb.apply(_classificar_condicao_subjudice, axis=1)

    resumo = {
        "total": int(len(df_comb)),
        "total_sub_judice": int(df_comb["Is_Sub_Judice"].sum()),
        "total_regulares": int((~df_comb["Is_Sub_Judice"]).sum()),
        "maior_nota": int(df_comb["Nota Objetiva"].max()) if len(df_comb) else 0,
        "menor_nota_sj": int(df_comb.loc[df_comb["Is_Sub_Judice"], "Nota Objetiva"].min())
        if df_comb["Is_Sub_Judice"].any()
        else 0,
    }
    return df_comb, resumo


@st.cache_data(show_spinner=False)
def obter_posicoes_combinadas_subjudice(_df_base):
    """Mapeia as posições combinadas dos 23 candidatos Sub Judice entre os convocados para o TAF."""
    df_etn_taf, _ = construir_classificacao_combinada(_df_base, "etnico", "taf")
    df_etn_res, _ = construir_classificacao_combinada(_df_base, "etnico", "reserva_taf")
    df_pcd, _ = construir_classificacao_combinada(_df_base, "pcd", "taf")

    map_taf = df_etn_taf.set_index("Inscrição")["Class_Combinada"].to_dict()
    map_res = df_etn_res.set_index("Inscrição")["Class_Combinada"].to_dict()
    map_pcd = df_pcd.set_index("Inscrição")["Class_Combinada"].to_dict()

    posicoes = {}
    sj_df = _df_base[_df_base["Is_Sub_Judice"].fillna(False)].sort_values("Posição_Geral")
    for _, row in sj_df.iterrows():
        insc = int(row["Inscrição"])
        is_pcd = bool(row.get("Cota_PCD", False))
        posicoes[insc] = {
            "cota": "PCD" if is_pcd else "Étnico-Racial",
            "pos_comb_taf": int(map_pcd[insc]) if is_pcd else int(map_taf[insc]),
            "total_comb_taf": int(len(df_pcd)) if is_pcd else int(len(df_etn_taf)),
            "pos_comb_reserva": int(map_pcd[insc]) if is_pcd else int(map_res[insc]),
            "total_comb_reserva": int(len(df_pcd)) if is_pcd else int(len(df_etn_res)),
        }
    return posicoes


def _extrair_arrays_pool(_df_base):
    """Extrai listas nativas do pool ativo (1.884 regulares TAF + 23 Sub Judice) para simulação rápida."""
    pool = _df_base[
        _df_base["Convocado_TAF_Oficial"].fillna(False) | _df_base["Is_Sub_Judice"].fillna(False)
    ].sort_values("Posição_Geral", ascending=True)

    return {
        "inscs": pool["Inscrição"].astype(int).tolist(),
        "nomes": pool["Nome"].astype(str).tolist(),
        "pos_geral": pool["Posição_Geral"].astype(int).tolist(),
        "notas": pool["Nota Objetiva"].astype(int).tolist(),
        "is_sj": pool["Is_Sub_Judice"].fillna(False).astype(bool).tolist(),
        "cota_etn": pool["Cota_Etnico_Racial"].fillna(False).astype(bool).tolist(),
        "cota_pcd": pool["Cota_PCD"].fillna(False).astype(bool).tolist(),
        "apta_etn": pool["Cota_Etnico_Apta_Definitivo"].fillna(False).astype(bool).tolist(),
        "apta_pcd": pool["Cota_PCD_Apta_Definitivo"].fillna(False).astype(bool).tolist(),
        "res_het": pool["Resultado_Hetero_Definitivo"].astype(str).tolist(),
        "res_pcd": pool["Resultado_PCD_Definitivo"].astype(str).tolist(),
        "processos": pool["Processo_Sub_Judice"].fillna("").astype(str).tolist(),
        "tipos_sj": pool["Tipo_Sub_Judice"].fillna("").astype(str).tolist(),
        "modalidades": pool["Modalidade_Concorrencia"].astype(str).tolist(),
    }


def _simular_uma_rodada(arrays, total_nomeacoes, r, p_sj, incluir_indef_cota):
    """Executa uma passagem determinística sobre o pool TAF+Sub Judice para um total N de nomeações."""
    vagas_ac = float(round(total_nomeacoes * 0.70))
    vagas_etn = float(round(total_nomeacoes * 0.20))
    vagas_pcd = float(round(total_nomeacoes * 0.10))

    rem_ac = vagas_ac
    rem_etn = vagas_etn
    rem_pcd = vagas_pcd

    etn_demanda_acum = 0.0
    pcd_demanda_acum = 0.0
    ac_demanda_acum = 0.0

    inscs = arrays["inscs"]
    notas = arrays["notas"]
    is_sj_arr = arrays["is_sj"]
    cota_etn_arr = arrays["cota_etn"]
    cota_pcd_arr = arrays["cota_pcd"]
    apta_etn_arr = arrays["apta_etn"]
    apta_pcd_arr = arrays["apta_pcd"]

    sj_status = {}

    for i in range(len(inscs)):
        is_sj = is_sj_arr[i]
        w = r * p_sj if is_sj else r
        is_ac_elig = notas[i] >= CORTE_TAF_AMPLA

        if is_sj:
            elig_etn = cota_etn_arr[i] if (incluir_indef_cota or apta_etn_arr[i]) else False
            elig_pcd = cota_pcd_arr[i] if (incluir_indef_cota or apta_pcd_arr[i]) else False
        else:
            elig_etn = apta_etn_arr[i]
            elig_pcd = apta_pcd_arr[i]

        if is_sj:
            # Avalia se há vaga quando a fila alcança este candidato (assumindo o próprio candidato apto)
            if is_ac_elig and rem_ac >= 0.5:
                vaga_tipo = "Ampla Concorrência (AC)"
                alcancado = True
                fila_a_frente = ac_demanda_acum
                vagas_alvo = vagas_ac
            elif elig_etn:
                alcancado = rem_etn >= 0.5
                vaga_tipo = "Cota Étnico-Racial" if alcancado else "Fora (Cadastro de Reserva)"
                fila_a_frente = etn_demanda_acum
                vagas_alvo = vagas_etn
            elif elig_pcd:
                alcancado = rem_pcd >= 0.5
                vaga_tipo = "Cota PCD" if alcancado else "Fora (Cadastro de Reserva)"
                fila_a_frente = pcd_demanda_acum
                vagas_alvo = vagas_pcd
            else:
                alcancado = False
                vaga_tipo = "Sem Cota Deferida (Abaixo Corte AC)"
                fila_a_frente = ac_demanda_acum
                vagas_alvo = vagas_ac

            sj_status[inscs[i]] = {
                "alcancado": alcancado,
                "vaga_tipo": vaga_tipo,
                "sobreviventes_a_frente": fila_a_frente,
                "vagas_alvo_cota": vagas_alvo,
                "elig_etn": elig_etn,
                "elig_pcd": elig_pcd,
            }

        # Consome a vaga correspondente em ordem estrita de Posição_Geral
        # Nota >= 119: Ampla primeiro; 114 <= Nota < 119: Étnico antes de PCD; Nota < 114: PCD antes de Étnico
        if is_ac_elig and rem_ac > 0:
            rem_ac = max(0.0, rem_ac - w)
            ac_demanda_acum += w
        elif notas[i] < 114 and elig_pcd:
            pcd_demanda_acum += w
            if rem_pcd > 0:
                rem_pcd = max(0.0, rem_pcd - w)
            elif elig_etn:
                etn_demanda_acum += w
                if rem_etn > 0:
                    rem_etn = max(0.0, rem_etn - w)
        elif elig_etn:
            etn_demanda_acum += w
            if rem_etn > 0:
                rem_etn = max(0.0, rem_etn - w)
            elif elig_pcd:
                pcd_demanda_acum += w
                if rem_pcd > 0:
                    rem_pcd = max(0.0, rem_pcd - w)
        elif elig_pcd:
            pcd_demanda_acum += w
            if rem_pcd > 0:
                rem_pcd = max(0.0, rem_pcd - w)

    return sj_status, rem_ac, rem_etn, rem_pcd


@st.cache_data(show_spinner=False)
def simular_cenario_subjudice(
    _df_base,
    total_nomeacoes=600,
    taxa_taf_pct=20,
    taxa_demais_pct=15,
    taxa_exito_sj_pct=100,
    incluir_indef_cota=True,
):
    """
    Executa a simulação exclusiva para os 23 candidatos Sub Judice.
    Retorna um DataFrame detalhado com projeção para cada um dos 23 e métricas globais do cenário.
    """
    arrays = _extrair_arrays_pool(_df_base)
    pos_map = obter_posicoes_combinadas_subjudice(_df_base)

    r = (1.0 - taxa_taf_pct / 100.0) * (1.0 - taxa_demais_pct / 100.0)
    p_sj = taxa_exito_sj_pct / 100.0

    sj_atual, rem_ac, rem_etn, rem_pcd = _simular_uma_rodada(
        arrays, total_nomeacoes, r, p_sj, incluir_indef_cota
    )

    # Varredura rápida para estimar o mínimo de nomeações totais (N) que alcança cada Sub Judice
    min_n_alcance = {}
    max_scan = 3500
    for n_scan in range(200, max_scan + 1, 25):
        res_scan, _, _, _ = _simular_uma_rodada(arrays, n_scan, r, p_sj, incluir_indef_cota)
        for insc, st_info in res_scan.items():
            if st_info["alcancado"] and insc not in min_n_alcance:
                min_n_alcance[insc] = n_scan
        if len(min_n_alcance) == len(sj_atual):
            break

    # Estimativa de quantos sobreviventes no pool geral existem
    total_pool = len(arrays["inscs"])
    total_ac_pool = sum(1 for n in arrays["notas"] if n >= CORTE_TAF_AMPLA)
    sobreviventes_ac_pool = total_ac_pool * r
    sobreviventes_totais = sum(
        (r * p_sj if sj else r) for sj in arrays["is_sj"]
    )

    linhas = []
    for i, insc in enumerate(arrays["inscs"]):
        if not arrays["is_sj"][i]:
            continue
        info_atual = sj_atual[insc]
        pos_info = pos_map[insc]
        n_min = min_n_alcance.get(insc)

        sobrev_frente = info_atual["sobreviventes_a_frente"]
        vagas_cota_nec = int(np.ceil(sobrev_frente + 0.5)) if (info_atual["elig_etn"] or info_atual["elig_pcd"]) else None

        if info_atual["alcancado"]:
            status_cenario = f"🏆 Alcançado ({info_atual['vaga_tipo']})"
        elif not info_atual["elig_etn"] and not info_atual["elig_pcd"]:
            status_cenario = "⚠️ Depende de deferimento da cota"
        else:
            faltam = max(1, int(np.ceil(sobrev_frente + 0.5 - info_atual["vagas_alvo_cota"])))
            status_cenario = f"⏳ Fora por ~{faltam} vagas na cota"

        linhas.append({
            "Inscrição": insc,
            "Nome": arrays["nomes"][i],
            "Posição_Geral": arrays["pos_geral"][i],
            "Nota Objetiva": arrays["notas"][i],
            "Modalidade": arrays["modalidades"][i],
            "Cota_Grupo": pos_info["cota"],
            "Processo_Sub_Judice": arrays["processos"][i],
            "Tipo_Sub_Judice": arrays["tipos_sj"][i],
            "Resultado_Hetero_Definitivo": arrays["res_het"][i],
            "Resultado_PCD_Definitivo": arrays["res_pcd"][i],
            "Pos_Comb_TAF": pos_info["pos_comb_taf"],
            "Total_Comb_TAF": pos_info["total_comb_taf"],
            "Pos_Comb_Reserva": pos_info["pos_comb_reserva"],
            "Total_Comb_Reserva": pos_info["total_comb_reserva"],
            "Sobreviventes_Frente": round(sobrev_frente, 1),
            "Vagas_Cota_Alvo": int(info_atual["vagas_alvo_cota"]),
            "Vagas_Cota_Necessarias": vagas_cota_nec,
            "Alcancado": bool(info_atual["alcancado"]),
            "Vaga_Tipo": info_atual["vaga_tipo"],
            "Status_Cenario": status_cenario,
            "Min_Nomeacoes_Alcance": n_min,
            "Min_Nomeacoes_Display": f"{n_min:,} chamados".replace(",", ".") if n_min else f"> {max_scan:,} chamados".replace(",", "."),
        })

    df_resultado = pd.DataFrame(linhas)
    meta = {
        "taxa_retencao_pct": round(r * 100.0, 1),
        "vagas_ac": int(round(total_nomeacoes * 0.70)),
        "vagas_etn": int(round(total_nomeacoes * 0.20)),
        "vagas_pcd": int(round(total_nomeacoes * 0.10)),
        "total_alcancados": int(df_resultado["Alcancado"].sum()) if len(df_resultado) else 0,
        "total_pool": total_pool,
        "sobreviventes_totais": int(round(sobreviventes_totais)),
        "sobreviventes_ac": int(round(sobreviventes_ac_pool)),
        "ac_esgotada": rem_ac > 0.5,
        "rem_ac": round(rem_ac, 1),
        "rem_etn": round(rem_etn, 1),
        "rem_pcd": round(rem_pcd, 1),
    }
    return df_resultado, meta
