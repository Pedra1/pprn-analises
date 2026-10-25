"""
Aba 5: Cronograma Oficial de Execução do Concurso PPRN.
"""

import pandas as pd
import streamlit as st
from src.data_loader import normalizar_texto


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
    """Renderiza a aba de cronograma com busca interativa e filtro por fase."""
    st.subheader("📅 Cronograma Oficial de Execução do Concurso")
    st.caption("Tabela 2.1 – Policial Penal • Anexo III do Edital nº 002/2026 (Governo do Estado do RN • SEAD/SEAP)")

    df_crono = pd.DataFrame(CRONOGRAMA_OFICIAL_DADOS)

    col_cr1, col_cr2 = st.columns([2, 1])
    with col_cr1:
        busca_crono = st.text_input("Filtrar etapas ou datas:", placeholder="Digite para filtrar etapas do edital...", key="busca_crono_edital")
    with col_cr2:
        filtro_etapa = st.selectbox("Filtrar por Fase:", ["Todas as Fases"] + list(df_crono["Etapa / Fase"].unique()), key="filtro_fase_crono")

    df_crono_show = df_crono.copy()
    if filtro_etapa != "Todas as Fases":
        df_crono_show = df_crono_show[df_crono_show["Etapa / Fase"] == filtro_etapa]

    if busca_crono.strip():
        norm_cr = normalizar_texto(busca_crono)
        df_crono_show = df_crono_show[
            df_crono_show["Evento / Atividade"].apply(normalizar_texto).str.contains(norm_cr, na=False) |
            df_crono_show["Etapa / Fase"].apply(normalizar_texto).str.contains(norm_cr, na=False) |
            df_crono_show["Período / Data"].str.contains(busca_crono, case=False, na=False)
        ]

    st.dataframe(df_crono_show, width="stretch", hide_index=True, height=520)
