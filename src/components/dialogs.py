"""
Modais e Diálogos de Avisos e Orientações Oficiais.
"""

import streamlit as st


@st.dialog("📢 Atualização Importante: Listas Preliminares das Bancas (23/10)", width="large")
def modal_aviso_legal():
    st.markdown("""
    <div>
    <div class="alert alert-warning border-start border-4 border-warning shadow-sm rounded-3 p-3 mb-3">
        <div class="d-flex align-items-center gap-2 mb-1" style="font-size: 0.82rem; font-weight: 800; color: #664d03; text-transform: uppercase; letter-spacing: 0.04em;">
            <i class="bi bi-lightning-charge-fill text-warning fs-6"></i> PUBLICAÇÃO OFICIAL DAS BANCAS DE COTAS • 23 DE OUTUBRO DE 2026
        </div>
        <div style="font-size: 0.94rem; color: #212529; line-height: 1.55;">
            Hoje, <strong>23 de outubro de 2026</strong>, a banca examinadora (Instituto Avalia) publicou o <strong>Resultado Preliminar da Heteroidentificação Étnico-Racial</strong> (Pretos, Pardos, Indígenas e Quilombolas) e o <strong>Resultado Preliminar da Perícia Médica PCD</strong>.<br>
            O portal foi integralmente atualizado com todas as informações oficiais!
        </div>
    </div>

    <div class="modal-grid-2col">
        <div class="card border shadow-sm p-3 mb-2 rounded-3">
            <div class="d-flex align-items-center gap-2 mb-1" style="font-size: 0.85rem; font-weight: 700; color: #0d6efd; text-transform: uppercase;">
                <i class="bi bi-shield-check text-primary fs-5"></i> Indeferido(a) na Cota? Não se Desespere!
            </div>
            <div style="font-size: 0.88rem; color: #6c757d; line-height: 1.5;">
                Conforme o <strong>Art. 4º</strong> (Hetero) e <strong>Art. 3º</strong> (PCD) dos Editais de Convocação, o indeferimento da cota <strong>NÃO elimina o candidato do concurso</strong>. O candidato passa a concorrer normalmente pela Ampla Concorrência!
            </div>
        </div>
        <div class="card border shadow-sm p-3 mb-2 rounded-3">
            <div class="d-flex align-items-center gap-2 mb-1" style="font-size: 0.85rem; font-weight: 700; color: #198754; text-transform: uppercase;">
                <i class="bi bi-file-earmark-text text-success fs-5"></i> Prazo para Interposição de Recursos
            </div>
            <div style="font-size: 0.88rem; color: #6c757d; line-height: 1.5;">
                Caberá recurso contra o resultado preliminar da <strong>0h00 do dia 26/10/2026 até às 23h59 do dia 27/10/2026</strong> no endereço eletrônico <a href="https://www.avalia.org.br" target="_blank" class="fw-bold text-primary">avalia.org.br</a>. O motivo pode ser consultado no link <em>"Boletim de Análise de Reserva de Vagas"</em>.
            </div>
        </div>
    </div>

    <div class="alert alert-info border-start border-4 border-info shadow-sm rounded-3 p-3 mb-3 d-flex align-items-start gap-2" style="font-size: 0.88rem; color: #055160; line-height: 1.5;">
        <i class="bi bi-info-circle-fill text-info fs-5 flex-shrink-0 mt-1"></i>
        <div>
            <strong>Iniciativa Independente:</strong> Este portal é colaborativo e sem vínculo oficial com o Instituto Avalia ou SEAD/RN. Atos administrativos oficiais competem exclusivamente à banca examinadora em <a href="https://www.avalia.org.br" target="_blank" class="fw-bold text-primary">avalia.org.br</a>.
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✅ Entendi e Desejo Acessar o Portal Atualizado", type="primary", width="stretch"):
        st.session_state["disclaimer_visto"] = True
        st.rerun()
