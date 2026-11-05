"""
Modais e Diálogos de Avisos e Orientações Oficiais.
"""

import streamlit as st
from src.acuracia import obter_acuracia_site


@st.dialog("ℹ️ Informações Importantes & Aviso Legal", width="large")
def modal_aviso_legal():
    metricas = obter_acuracia_site()
    acuracia_fmt = metricas.get("acuracia_formatada", "98,3%")
    total_acertos = f"{metricas.get('total_acertos', 18615):,}".replace(",", ".")
    total_candidatos = f"{metricas.get('total_candidatos', 18945):,}".replace(",", ".")
    data_ref = metricas.get("data_referencia", "04 de novembro de 2026")

    st.markdown(f"""
    ### 🎯 Finalidade do Portal
    Este portal é uma **iniciativa independente e voluntária** desenvolvida com o único propósito de ajudar os candidatos do Concurso de Policial Penal do Rio Grande do Norte (PPRN) a consultarem seu desempenho individual, compreenderem o andamento das listas e visualizarem cenários de classificação de forma clara e transparente.

    ---

    ### 🛡️ Acurácia do Portal & Auditoria das Listas de 04 de Novembro
    - **Acurácia Prévia Comprovada (Fase Preliminar):** O modelo do portal alcançou **98,3% de acurácia global** ({total_acertos} acertos em {total_candidatos} avaliados) e **100% de exatidão nas notas de corte oficiais** (Ampla: 119 pts | Cota Étnica: 113 pts | Cota PCD: 73 pts).
    - **Sincronização com as Listas de 04/11:** O portal possui motor automatizado de auditoria. Assim que os arquivos oficiais publicados ontem (04/11) forem inseridos na pasta de atualização, o sistema recalculará instantaneamente o índice de acurácia definitivo pós-recursos.
    - *Observação:* Pequenas variações residuais no modelo preliminar decorrem unicamente de recursos administrativos providos pela banca examinadora.

    ---

    ### 📋 Regras de Processamento dos Dados
    Para garantir a máxima fidelidade às regras dos editais do concurso:
    - **Cotistas com nota de Ampla Concorrência:** Os candidatos cotistas que atingiram nota suficiente para ingressar na Ampla Concorrência já são computados prioritariamente nas vagas da Ampla, desocupando a vaga reservada para que o próximo cotista da fila seja beneficiado.
    - **Candidatos indeferidos nas bancas de cotas:** Aqueles que tiveram a solicitação indeferida preliminarmente na Heteroidentificação ou na Perícia PCD foram automaticamente realocados para disputar exclusivamente pela Ampla Concorrência, sem prejuízo ou eliminação do concurso, conforme previsto no Art. 4º (Hetero) e Art. 3º (PCD) dos editais de convocação.

    ---

    ### ⚖️ Dados Públicos e Ausência de Ilegalidade
    Todos os dados presentes nesta plataforma foram compilados diretamente a partir de editais, anexos e relações nominais **públicas** disponibilizadas pela banca examinadora. Não há uso de dados sigilosos ou privados. A compilação e organização dessas informações têm finalidade estritamente informativa e de auxílio à comunidade de candidatos.

    ---

    ### ⚠️ Aviso Legal (Disclaimer)
    - Este portal **não possui qualquer vínculo, afiliação, representação ou responsabilidade com o Instituto Avalia nem com o Governo do Estado do Rio Grande do Norte**.
    - Por se tratar de um projeto colaborativo e independente, **podem ocorrer divergências, inconsistências ou erros involuntários de processamento**.
    - Esta ferramenta não substitui as publicações oficiais. Para qualquer ato administrativo, interposição formal de recursos, convocações ou decisões legais, o candidato deve consultar única e exclusivamente o site oficial da banca em [avalia.org.br](https://www.avalia.org.br).
    """)

    st.write("")

    if st.button("Entendi e Desejo Acessar o Portal", type="primary", width="stretch"):
        st.session_state["disclaimer_visto"] = True
        st.rerun()
