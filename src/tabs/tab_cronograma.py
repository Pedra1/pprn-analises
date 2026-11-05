"""
Aba 5: Cronograma Oficial de Execução do Concurso PPRN.
Com destaque automático em tempo real para a fase e eventos atuais.
"""

import datetime
import re
import pandas as pd
import streamlit as st
from src.data_loader import normalizar_texto

MESES_PT = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril", 5: "maio", 6: "junho",
    7: "julho", 8: "agosto", 9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
}


def parse_periodo(texto):
    """Extrai datas de início e fim a partir de descrições textuais do edital."""
    texto = texto.strip()
    m1 = re.search(r'(\d{2})/(\d{2}).*?(\d{2})/(\d{2})/(\d{4})', texto)
    if m1 and 'até' in texto:
        d1, m1_, d2, m2_, y = m1.groups()
        return datetime.date(int(y), int(m1_), int(d1)), datetime.date(int(y), int(m2_), int(d2))
    m2 = re.search(r'(\d{2})/(\d{2})\s*(?:a|e)\s*(\d{2})/(\d{2})/(\d{4})', texto)
    if m2:
        d1, m1_, d2, m2_, y = m2.groups()
        return datetime.date(int(y), int(m1_), int(d1)), datetime.date(int(y), int(m2_), int(d2))
    m3 = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)
    if m3:
        d, m, y = m3.groups()
        dt = datetime.date(int(y), int(m), int(d))
        return dt, dt
    return None, None


def processar_cronograma_com_status(dados_cronograma, data_base=None):
    """Processa o cronograma em tempo real, calculando a fase atual e status de cada evento."""
    if data_base is None:
        data_base = datetime.date.today()

    itens = []
    for idx, item in enumerate(dados_cronograma):
        ini, fim = parse_periodo(item['Período / Data'])
        itens.append({
            "idx": idx,
            "Etapa / Fase": item["Etapa / Fase"],
            "Evento / Atividade": item["Evento / Atividade"],
            "Período / Data": item["Período / Data"],
            "fase": item["Etapa / Fase"],
            "evento": item["Evento / Atividade"],
            "periodo": item["Período / Data"],
            "ini": ini,
            "fim": fim
        })

    em_andamento = [e for e in itens if e["ini"] and e["fim"] and e["ini"] <= data_base <= e["fim"]]
    passados = [e for e in itens if e["fim"] and e["fim"] < data_base]
    futuros = [e for e in itens if e["ini"] and e["ini"] > data_base]

    proximo_evento = futuros[0] if futuros else None
    ultimo_evento = passados[-1] if passados else None

    if em_andamento:
        fases_atuais = sorted(list(set(e["Etapa / Fase"] for e in em_andamento)))
        fase_principal = fases_atuais[0]
        status_fase = "Em Andamento Hoje"
        dias_proximo = (proximo_evento["ini"] - data_base).days if proximo_evento else None
    elif proximo_evento:
        fase_principal = proximo_evento["Etapa / Fase"]
        status_fase = "Fase Ativa (Preparação para Próxima Etapa)"
        fases_atuais = [fase_principal]
        dias_proximo = (proximo_evento["ini"] - data_base).days
    elif ultimo_evento:
        fase_principal = ultimo_evento["Etapa / Fase"]
        status_fase = "Concurso Concluído"
        fases_atuais = [fase_principal]
        dias_proximo = None
    else:
        fase_principal = "Aguardando Início"
        status_fase = "Aguardando Início"
        fases_atuais = []
        dias_proximo = None

    for e in itens:
        if e["ini"] and e["fim"] and e["ini"] <= data_base <= e["fim"]:
            e["Situação"] = "🟢 EM ANDAMENTO HOJE"
            e["tipo_status"] = "andamento"
        elif proximo_evento and e["idx"] == proximo_evento["idx"]:
            dias = (e["ini"] - data_base).days
            if dias == 0:
                e["Situação"] = "⏳ PRÓXIMA ETAPA (Hoje!)"
            elif dias == 1:
                e["Situação"] = "⏳ PRÓXIMA ETAPA (Amanhã!)"
            else:
                e["Situação"] = f"⏳ PRÓXIMA ETAPA (em {dias} dias)"
            e["tipo_status"] = "proximo"
        elif e["fim"] and e["fim"] < data_base:
            e["Situação"] = "✅ Concluído"
            e["tipo_status"] = "concluido"
        else:
            e["Situação"] = "📅 Previsto"
            e["tipo_status"] = "previsto"

    return {
        "hoje": data_base,
        "fase_principal": fase_principal,
        "fases_atuais": fases_atuais,
        "status_fase": status_fase,
        "em_andamento": em_andamento,
        "proximo_evento": proximo_evento,
        "ultimo_evento": ultimo_evento,
        "dias_proximo": dias_proximo,
        "itens": itens
    }


CRONOGRAMA_OFICIAL_DADOS = [
    {"Etapa / Fase": "ISENÇÃO DA TAXA DE INSCRIÇÃO", "Evento / Atividade": "Período para solicitação de isenção da Taxa de Inscrição", "Período / Data": "22/06 até às 23h59min do dia 24/06/2026"},
    {"Etapa / Fase": "ISENÇÃO DA TAXA DE INSCRIÇÃO", "Evento / Atividade": "Prazo para envio da documentação referente a isenção da Taxa de Inscrição", "Período / Data": "22/06 até às 23h59min do dia 25/06/2026"},
    {"Etapa / Fase": "ISENÇÃO DA TAXA DE INSCRIÇÃO", "Evento / Atividade": "Divulgação do deferimento das solicitações de isenção da Taxa de Inscrição", "Período / Data": "03/07/2026"},
    {"Etapa / Fase": "ISENÇÃO DA TAXA DE INSCRIÇÃO", "Evento / Atividade": "Período para recurso contra o indeferimento da solicitação de isenção", "Período / Data": "06/07 a 07/07/2026"},
    {"Etapa / Fase": "ISENÇÃO DA TAXA DE INSCRIÇÃO", "Evento / Atividade": "Divulgação do deferimento da solicitação de isenção pós-recursos", "Período / Data": "14/07/2026"},
    {"Etapa / Fase": "SOLICITAÇÃO DE INSCRIÇÃO", "Evento / Atividade": "Período para solicitação de Inscrição", "Período / Data": "22/06 até às 23h59min do dia 05/08/2026"},
    {"Etapa / Fase": "SOLICITAÇÃO DE INSCRIÇÃO", "Evento / Atividade": "Período para envio de laudo médico (apenas nos casos de solicitação de condições especiais)", "Período / Data": "22/06 até às 23h59min do dia 07/08/2026"},
    {"Etapa / Fase": "SOLICITAÇÃO DE INSCRIÇÃO", "Evento / Atividade": "Período para emissão do boleto bancário e pagamento da Taxa de Inscrição", "Período / Data": "22/06 até às 23h59min do dia 07/08/2026"},
    {"Etapa / Fase": "SOLICITAÇÃO DE INSCRIÇÃO", "Evento / Atividade": "Divulgação do deferimento das inscrições", "Período / Data": "12/08/2026"},
    {"Etapa / Fase": "SOLICITAÇÃO DE INSCRIÇÃO", "Evento / Atividade": "Período para recurso contra o indeferimento da inscrição", "Período / Data": "13/08 a 14/08/2026"},
    {"Etapa / Fase": "SOLICITAÇÃO DE INSCRIÇÃO", "Evento / Atividade": "Divulgação do deferimento da inscrição pós-recurso", "Período / Data": "20/08/2026"},
    {"Etapa / Fase": "PROVA OBJETIVA", "Evento / Atividade": "Divulgação do horário e local de realização da prova", "Período / Data": "04/09/2026"},
    {"Etapa / Fase": "PROVA OBJETIVA", "Evento / Atividade": "APLICAÇÃO DA PROVA OBJETIVA", "Período / Data": "13/09/2026"},
    {"Etapa / Fase": "PROVA OBJETIVA", "Evento / Atividade": "Divulgação do Gabarito Preliminar e do(s) Caderno(s) de questões", "Período / Data": "14/09/2026"},
    {"Etapa / Fase": "PROVA OBJETIVA", "Evento / Atividade": "Período para recurso contra o Gabarito Preliminar", "Período / Data": "15/09 a 16/09/2026"},
    {"Etapa / Fase": "PROVA OBJETIVA", "Evento / Atividade": "Divulgação do edital de pareceres dos recursos contra o Gabarito Preliminar, do Gabarito pós-recursos, das folhas de respostas e do resultado preliminar da Prova Objetiva", "Período / Data": "30/09/2026"},
    {"Etapa / Fase": "PROVA OBJETIVA", "Evento / Atividade": "Período para recurso contra o resultado preliminar da Prova Objetiva", "Período / Data": "01/10 a 02/10/2026"},
    {"Etapa / Fase": "PROVA OBJETIVA", "Evento / Atividade": "Divulgação do resultado da Prova Objetiva pós-recursos", "Período / Data": "09/10/2026"},
    {"Etapa / Fase": "PERÍCIA MÉDICA (PcD)", "Evento / Atividade": "Convocação dos candidatos inscritos às vagas PcD para a perícia médica", "Período / Data": "09/10/2026"},
    {"Etapa / Fase": "PERÍCIA MÉDICA (PcD)", "Evento / Atividade": "APLICAÇÃO DA PERÍCIA MÉDICA PRESENCIAL PARA PcD", "Período / Data": "18/10/2026"},
    {"Etapa / Fase": "PERÍCIA MÉDICA (PcD)", "Evento / Atividade": "Divulgação do resultado preliminar da perícia médica", "Período / Data": "23/10/2026"},
    {"Etapa / Fase": "PERÍCIA MÉDICA (PcD)", "Evento / Atividade": "Período para recurso contra o resultado da perícia médica", "Período / Data": "26/10 a 27/10/2026"},
    {"Etapa / Fase": "PERÍCIA MÉDICA (PcD)", "Evento / Atividade": "Divulgação do parecer do recurso contra o resultado da perícia médica e do resultado da perícia médica pós-recurso", "Período / Data": "04/11/2026"},
    {"Etapa / Fase": "PROCEDIMENTO DE HETEROIDENTIFICAÇÃO", "Evento / Atividade": "Convocação dos candidatos inscritos às vagas étnico-raciais para o procedimento de heteroidentificação e análise documental", "Período / Data": "09/10/2026"},
    {"Etapa / Fase": "PROCEDIMENTO DE HETEROIDENTIFICAÇÃO", "Evento / Atividade": "APLICAÇÃO DA HETEROIDENTIFICAÇÃO PRESENCIAL E ANÁLISE DOCUMENTAL", "Período / Data": "17/10 e 18/10/2026"},
    {"Etapa / Fase": "PROCEDIMENTO DE HETEROIDENTIFICAÇÃO", "Evento / Atividade": "Divulgação do resultado preliminar da heteroidentificação e análise documental", "Período / Data": "23/10/2026"},
    {"Etapa / Fase": "PROCEDIMENTO DE HETEROIDENTIFICAÇÃO", "Evento / Atividade": "Período para recurso contra o resultado provisório da heteroidentificação e análise documental", "Período / Data": "26/10 a 27/10/2026"},
    {"Etapa / Fase": "PROCEDIMENTO DE HETEROIDENTIFICAÇÃO", "Evento / Atividade": "Divulgação do parecer do recurso contra o resultado da heteroidentificação e análise documental e resultado definitivo da heteroidentificação", "Período / Data": "04/11/2026"},
    {"Etapa / Fase": "DO TESTE DE APTIDÃO FÍSICA", "Evento / Atividade": "Convocação para o teste de aptidão física", "Período / Data": "04/11/2026"},
    {"Etapa / Fase": "DO TESTE DE APTIDÃO FÍSICA", "Evento / Atividade": "APLICAÇÃO DO TESTE DE APTIDÃO FÍSICA", "Período / Data": "14/11 e 15/11/2026"},
    {"Etapa / Fase": "DO TESTE DE APTIDÃO FÍSICA", "Evento / Atividade": "Divulgação do resultado preliminar do teste de aptidão física", "Período / Data": "23/11/2026"},
    {"Etapa / Fase": "DO TESTE DE APTIDÃO FÍSICA", "Evento / Atividade": "Período para recurso contra o resultado provisório do teste de aptidão física", "Período / Data": "24/11 a 25/11/2026"},
    {"Etapa / Fase": "DO TESTE DE APTIDÃO FÍSICA", "Evento / Atividade": "Divulgação do parecer do recurso contra o resultado do teste de aptidão física e resultado definitivo", "Período / Data": "03/12/2026"},
    {"Etapa / Fase": "DA AVALIAÇÃO PSICOLÓGICA", "Evento / Atividade": "Convocação para a avaliação psicológica", "Período / Data": "03/12/2026"},
    {"Etapa / Fase": "DA AVALIAÇÃO PSICOLÓGICA", "Evento / Atividade": "APLICAÇÃO DA AVALIAÇÃO PSICOLÓGICA", "Período / Data": "20/12/2026"},
    {"Etapa / Fase": "DA AVALIAÇÃO PSICOLÓGICA", "Evento / Atividade": "Divulgação do resultado preliminar da avaliação psicológica", "Período / Data": "05/01/2027"},
    {"Etapa / Fase": "DA AVALIAÇÃO PSICOLÓGICA", "Evento / Atividade": "Entrevista devolutiva", "Período / Data": "10/01/2027"},
    {"Etapa / Fase": "DA AVALIAÇÃO PSICOLÓGICA", "Evento / Atividade": "Período para recurso contra o resultado preliminar da avaliação psicológica", "Período / Data": "11/01 a 12/01/2027"},
    {"Etapa / Fase": "DA AVALIAÇÃO PSICOLÓGICA", "Evento / Atividade": "Divulgação do parecer do recurso contra o resultado da avaliação psicológica e resultado definitivo", "Período / Data": "19/01/2027"},
    {"Etapa / Fase": "DO EXAME TOXICOLÓGICO", "Evento / Atividade": "Convocação para a entrega do exame toxicológico", "Período / Data": "03/12/2026"},
    {"Etapa / Fase": "DO EXAME TOXICOLÓGICO", "Evento / Atividade": "ENTREGA DO EXAME TOXICOLÓGICO (no mesmo dia da avaliação psicológica)", "Período / Data": "20/12/2026"},
    {"Etapa / Fase": "DO EXAME TOXICOLÓGICO", "Evento / Atividade": "Divulgação do resultado preliminar do exame toxicológico", "Período / Data": "19/01/2027"},
    {"Etapa / Fase": "DO EXAME TOXICOLÓGICO", "Evento / Atividade": "Período para recurso contra o resultado provisório do exame toxicológico", "Período / Data": "20/01 a 21/01/2027"},
    {"Etapa / Fase": "DO EXAME TOXICOLÓGICO", "Evento / Atividade": "Divulgação do parecer do recurso contra o resultado do exame toxicológico e resultado definitivo", "Período / Data": "28/01/2027"},
    {"Etapa / Fase": "DA INVESTIGAÇÃO SOCIAL", "Evento / Atividade": "Convocação para a investigação social", "Período / Data": "28/01/2027"},
    {"Etapa / Fase": "DA INVESTIGAÇÃO SOCIAL", "Evento / Atividade": "PREENCHIMENTO DO FORMULÁRIO DE INFORMAÇÕES PARA INVESTIGAÇÃO SOCIAL", "Período / Data": "28/01 a 17/02/2027"},
    {"Etapa / Fase": "DA INVESTIGAÇÃO SOCIAL", "Evento / Atividade": "Divulgação do resultado preliminar da investigação social", "Período / Data": "26/02/2027"},
    {"Etapa / Fase": "DA INVESTIGAÇÃO SOCIAL", "Evento / Atividade": "Período para recurso contra o resultado provisório da investigação social", "Período / Data": "01/03 a 02/03/2027"},
    {"Etapa / Fase": "DA INVESTIGAÇÃO SOCIAL", "Evento / Atividade": "Divulgação do parecer do recurso contra o resultado da investigação social e resultado definitivo", "Período / Data": "10/03/2027"},
    {"Etapa / Fase": "DO CURSO DE FORMAÇÃO", "Evento / Atividade": "Convocação dos candidatos habilitados para matrícula no curso de formação", "Período / Data": "10/03/2027"},
    {"Etapa / Fase": "DO CURSO DE FORMAÇÃO", "Evento / Atividade": "PERÍODO PARA MATRÍCULA", "Período / Data": "10/03 a 12/03/2027"},
    {"Etapa / Fase": "DO CURSO DE FORMAÇÃO", "Evento / Atividade": "Aula inaugural do curso de formação", "Período / Data": "22/03/2027"},
    {"Etapa / Fase": "DO CURSO DE FORMAÇÃO", "Evento / Atividade": "Período de realização do curso de formação", "Período / Data": "22/03 a 22/06/2027"},
    {"Etapa / Fase": "DO CURSO DE FORMAÇÃO", "Evento / Atividade": "AVALIAÇÃO DO CURSO DE FORMAÇÃO", "Período / Data": "04/07/2027"},
    {"Etapa / Fase": "DO CURSO DE FORMAÇÃO", "Evento / Atividade": "Divulgação do resultado preliminar do curso de formação", "Período / Data": "16/07/2027"},
    {"Etapa / Fase": "DO CURSO DE FORMAÇÃO", "Evento / Atividade": "Período para recurso contra o resultado do curso de formação", "Período / Data": "19/07 a 20/07/2027"},
    {"Etapa / Fase": "DO CURSO DE FORMAÇÃO", "Evento / Atividade": "Divulgação do resultado do curso de formação pós-recurso", "Período / Data": "27/07/2027"},
    {"Etapa / Fase": "RESULTADO FINAL E HOMOLOGAÇÃO", "Evento / Atividade": "Divulgação do resultado preliminar e classificação dos candidatos", "Período / Data": "27/07/2027"},
    {"Etapa / Fase": "RESULTADO FINAL E HOMOLOGAÇÃO", "Evento / Atividade": "Período para recurso contra o resultado e classificação", "Período / Data": "28/07 a 29/07/2027"},
    {"Etapa / Fase": "RESULTADO FINAL E HOMOLOGAÇÃO", "Evento / Atividade": "Divulgação do resultado final e classificação pós-recurso", "Período / Data": "05/08/2027"},
    {"Etapa / Fase": "RESULTADO FINAL E HOMOLOGAÇÃO", "Evento / Atividade": "DIVULGAÇÃO DA HOMOLOGAÇÃO DO RESULTADO FINAL E CLASSIFICAÇÃO", "Período / Data": "05/08/2027"}
]


def render_tab_cronograma():
    """Renderiza a aba de cronograma com busca interativa, filtro dinâmico e destaque em tempo real da fase atual."""
    hoje = datetime.date.today()
    info_crono = processar_cronograma_com_status(CRONOGRAMA_OFICIAL_DADOS, hoje)

    fase_ativa = info_crono["fase_principal"]
    hoje_extenso = f"{hoje.day} de {MESES_PT.get(hoje.month, '')} de {hoje.year}"
    prox = info_crono["proximo_evento"]
    ult = info_crono["ultimo_evento"]
    dias_prox = info_crono["dias_proximo"]
    status_fase = info_crono["status_fase"]

    st.subheader("📅 Cronograma Oficial de Execução do Concurso")
    st.caption("Tabela 2.1 – Policial Penal • Anexo III do Edital nº 002/2026 (Governo do Estado do RN • SEAD/SEAP)")

    # Destaque em Tempo Real da Fase Atual
    if prox and dias_prox is not None:
        if dias_prox == 0:
            regressiva_txt = "Acontecendo Hoje!"
            regressiva_sub = "Dia oficial de realização da etapa"
            badge_cor = "#15803D"
        elif dias_prox == 1:
            regressiva_txt = "É Amanhã!"
            regressiva_sub = f"Data: {prox['periodo']}"
            badge_cor = "#D97706"
        else:
            regressiva_txt = f"Faltam {dias_prox} dias!"
            regressiva_sub = f"Data prevista: {prox['periodo']}"
            badge_cor = "#2563EB"
    elif ult:
        regressiva_txt = "Certame Concluído"
        regressiva_sub = "Todas as etapas do cronograma foram finalizadas"
        badge_cor = "#475569"
    else:
        regressiva_txt = "Aguardando Início"
        regressiva_sub = "Cronograma em fase preliminar"
        badge_cor = "#475569"

    ult_evento_txt = ult["evento"] if ult else "Início do Concurso"
    ult_evento_data = ult["periodo"] if ult else "-"
    prox_evento_txt = prox["evento"] if prox else "Homologação Final"
    prox_evento_data = prox["periodo"] if prox else "-"

    st.markdown(f"""<div class="card bg-success-subtle border-start border-4 border-success p-3 rounded-3 shadow-sm mb-3">
<div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-2">
<span class="badge bg-success text-white px-2 py-1 rounded-pill fw-bold" style="font-size: 0.82rem;">
<i class="bi bi-broadcast me-1"></i> FASE ATUAL EM TEMPO REAL: {fase_ativa}
</span>
<span class="badge bg-light text-secondary border px-2 py-1 rounded-pill" style="font-size: 0.8rem;">
<i class="bi bi-calendar-event me-1"></i> Data Real do Sistema: {hoje_extenso}
</span>
</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #064E3B; margin-bottom: 4px;">
🎯 Status do Concurso: {status_fase}
</div>
<div style="font-size: 0.92rem; color: #1E293B; line-height: 1.55;">
O concurso encontra-se oficialmente na etapa de <strong>{fase_ativa}</strong>. O cronograma abaixo é atualizado automaticamente todos os dias com base no calendário oficial do Edital nº 002/2026.
</div>
</div>""", unsafe_allow_html=True)

    # 3 Métricas Rápidas dos Marcos
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-check-circle-fill text-success me-1"></i> Último Marco Concluído</div>
<div class="stat-value text-success" style="font-size: 1.15rem;">{ult_evento_data}</div>
<div class="stat-sub text-dark fw-bold">{ult_evento_txt}</div>
</div>""", unsafe_allow_html=True)

    with mc2:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-flag-fill text-primary me-1"></i> Próximo Marco Oficial</div>
<div class="stat-value text-primary" style="font-size: 1.15rem;">{prox_evento_data}</div>
<div class="stat-sub text-dark fw-bold">{prox_evento_txt}</div>
</div>""", unsafe_allow_html=True)

    with mc3:
        st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-hourglass-split text-warning me-1"></i> Contagem Regressiva</div>
<div class="stat-value" style="color: {badge_cor}; font-size: 1.25rem;">{regressiva_txt}</div>
<div class="stat-sub text-secondary fw-bold">{regressiva_sub}</div>
</div>""", unsafe_allow_html=True)

    st.write("")

    # Orientações Específicas se estiver na Fase do TAF
    if "TESTE DE APTIDÃO FÍSICA" in fase_ativa.upper():
        st.markdown("""<div class="card bg-warning-subtle border-start border-4 border-warning p-3 rounded-3 shadow-sm mb-3">
<div class="d-flex align-items-center gap-2 mb-1 fw-bold text-warning-emphasis text-uppercase" style="font-size: 0.85rem; letter-spacing: 0.04em;">
<i class="bi bi-exclamation-triangle-fill text-warning fs-5"></i> ORIENTAÇÕES ESSENCIAIS PARA O TAF (14 E 15 DE NOVEMBRO DE 2026)
</div>
<div style="font-size: 0.9rem; color: #212529; line-height: 1.55;">
<div>• <strong>Atestado Médico Obrigatório:</strong> Deve conter expressamente a autorização para submissão a esforços físicos intensos, emitido com antecedência máxima de 30 dias.</div>
<div style="margin-top: 3px;">• <strong>Documento de Identificação:</strong> Apresentar documento oficial original com foto no dia e turno designados no Anexo IV.</div>
<div style="margin-top: 3px;">• <strong>Traje Adequado:</strong> Camiseta, calção ou bermuda apropriada para prática esportiva e calçado esportivo (tênis).</div>
</div>
</div>""", unsafe_allow_html=True)

    # Filtros da Tabela
    df_crono_base = pd.DataFrame(info_crono["itens"])

    col_cr1, col_cr2, col_cr3 = st.columns([1.5, 1.2, 1.3])
    with col_cr1:
        busca_crono = st.text_input("Filtrar etapas ou datas:", placeholder="Digite para filtrar etapas...", key="busca_crono_edital")
    with col_cr2:
        filtro_etapa = st.selectbox("Filtrar por Fase:", ["Todas as Fases"] + list(df_crono_base["Etapa / Fase"].unique()), key="filtro_fase_crono")
    with col_cr3:
        filtro_status = st.selectbox(
            "Visualização Rápida:",
            [
                "Todas as Etapas (61)",
                "🔥 Fase Atual & Próximas Etapas",
                "⏳ Somente Etapas Futuras",
                "✅ Somente Etapas Concluídas"
            ],
            key="filtro_status_crono"
        )

    df_crono_show = df_crono_base.copy()

    if filtro_etapa != "Todas as Fases":
        df_crono_show = df_crono_show[df_crono_show["Etapa / Fase"] == filtro_etapa]

    if filtro_status == "🔥 Fase Atual & Próximas Etapas":
        df_crono_show = df_crono_show[(df_crono_show["Etapa / Fase"] == fase_ativa) | (df_crono_show["tipo_status"].isin(["andamento", "proximo", "previsto"]))]
    elif filtro_status == "⏳ Somente Etapas Futuras":
        df_crono_show = df_crono_show[df_crono_show["tipo_status"].isin(["proximo", "previsto"])]
    elif filtro_status == "✅ Somente Etapas Concluídas":
        df_crono_show = df_crono_show[df_crono_show["tipo_status"] == "concluido"]

    if busca_crono.strip():
        norm_cr = normalizar_texto(busca_crono)
        df_crono_show = df_crono_show[
            df_crono_show["Evento / Atividade"].apply(normalizar_texto).str.contains(norm_cr, na=False) |
            df_crono_show["Etapa / Fase"].apply(normalizar_texto).str.contains(norm_cr, na=False) |
            df_crono_show["Período / Data"].str.contains(busca_crono, case=False, na=False)
        ]

    # Styler de Destaque Visual
    def colorir_linhas_cronograma(row):
        sit = str(row.get('Situação', ''))
        fase = str(row.get('Etapa / Fase', ''))
        if 'EM ANDAMENTO' in sit:
            return ['background-color: #DCFCE7; color: #166534; font-weight: bold;'] * len(row)
        elif 'PRÓXIMA ETAPA' in sit:
            return ['background-color: #FEF9C3; color: #854D0E; font-weight: bold;'] * len(row)
        elif fase == fase_ativa:
            return ['background-color: #F0FDF4; color: #0F172A; font-weight: 600;'] * len(row)
        elif 'Concluído' in sit:
            return ['color: #64748B;'] * len(row)
        return [''] * len(row)

    colunas_exibir = ['Situação', 'Etapa / Fase', 'Evento / Atividade', 'Período / Data']
    df_final_view = df_crono_show[colunas_exibir]

    st.dataframe(
        df_final_view.style.apply(colorir_linhas_cronograma, axis=1),
        width="stretch",
        hide_index=True,
        height=520,
        column_config={
            "Situação": st.column_config.TextColumn("Situação Atual", width="medium"),
            "Etapa / Fase": st.column_config.TextColumn("Etapa / Fase", width="medium"),
            "Evento / Atividade": st.column_config.TextColumn("Evento / Atividade", width="large"),
            "Período / Data": st.column_config.TextColumn("Período / Data", width="medium"),
        }
    )
