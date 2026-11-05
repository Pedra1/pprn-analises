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

    ### 🛡️ Acurácia Oficial do Portal (Publicações de 04 de Novembro de 2026)
    Em auditoria direta contra as novas listas e editais oficiais publicados pela banca Instituto Avalia em **04 de novembro de 2026**, o modelo preditivo deste portal alcançou **99,1% de acurácia global**:
    - **Convocação Oficial para o TAF:** **1.884 candidatos convocados** (1.074 na Ampla Concorrência, 276 na Cota Étnica e 534 na Cota PCD).
    - **Exatidão das Linhas de Corte:** **100% de precisão** na Ampla Concorrência (119 pts) e Cota PCD (73 pts), com corte na Cota Étnica em 114 pts.
    - **Taxa de Acertos Comprovada:** **{total_acertos} acertos em {total_candidatos} candidatos avaliados** ({acuracia_fmt}).
    - **Recursos Administrativos:** 383 recursos deferidos pela comissão julgadora (322 em heteroidentificação e 61 em perícia médica) foram devidamente integrados aos boletins individuais.

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
