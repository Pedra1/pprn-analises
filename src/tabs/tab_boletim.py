"""
Aba 1: Consulta Individual do Candidato (Meu Boletim Oficial).
Melhorias implementadas:
- 2.3: Filtro inteligente para nomes comuns com paginação/lotes (evita truncamento aos 50 primeiros)
- Detecção de correspondência exata de nome completo
- Visualização completa de notas, posições ganhas nas cotas e confronto direto
"""

import math
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from src.config import (
    DISCIPLINAS,
    PONTOS_MAXIMOS,
    NOTA_MAXIMA_PROVA,
    TOTAL_CANDIDATOS,
    TOTAL_CANDIDATOS_FMT,
    TOTAL_AMPLA_FMT,
    TOTAL_ETNICO_APTOS,
    TOTAL_PCD_APTOS,
    MEDIAS_DISCIPLINAS
)
from src.data_loader import normalizar_texto


def limpar_termo_busca():
    st.session_state["termo_busca_input"] = ""


def render_tab_boletim(df_base, mapa_inscricoes):
    """Renderiza a aba de boletim individual com busca refinada e análise de desempenho."""
    st.subheader("🔍 Localize seu Desempenho e seu Resultado na Banca")
    st.write("Digite seu **Nome Completo** (ou parte dele) ou seu número de **Inscrição** para conferir seu boletim individual completo:")

    col_search, col_action = st.columns([3, 1])
    with col_search:
        termo_busca = st.text_input(
            "Buscar por Nome ou Inscrição",
            placeholder="Digite seu nome completo ou número de inscrição...",
            label_visibility="collapsed",
            key="termo_busca_input"
        )
    with col_action:
        if termo_busca.strip():
            st.button("✖️ Limpar Busca", width="stretch", on_click=limpar_termo_busca)
        else:
            st.caption("💡 Busca flexível (ignora maiúsculas e acentos)")

    candidato_selecionado = None

    if termo_busca.strip():
        termo_norm = normalizar_texto(termo_busca)
        # 1. Otimização O(1): verificação instantânea por número exato de inscrição
        if termo_norm in mapa_inscricoes:
            candidato_selecionado = df_base.iloc[mapa_inscricoes[termo_norm]]
        else:
            if termo_norm.isdigit():
                mascara = df_base['Inscrição_Str'].str.startswith(termo_norm)
            else:
                mascara = df_base['Nome_Busca'].str.contains(termo_norm, regex=False, na=False)
            resultados_busca = df_base[mascara]

            total_encontrados = len(resultados_busca)

            if total_encontrados == 0:
                st.warning("⚠️ Nenhum candidato encontrado com o termo informado. Verifique a grafia do nome ou tente buscar diretamente pelo número da inscrição.")
            elif total_encontrados == 1:
                candidato_selecionado = resultados_busca.iloc[0]
            else:
                # 2.3: MELHORIA NO FILTRO DE NOMES MUITO COMUNS
                # Verifica se há correspondência exata para evitar menus desnecessários
                match_exato = resultados_busca[resultados_busca['Nome_Busca'] == termo_norm]
                if len(match_exato) == 1:
                    candidato_selecionado = match_exato.iloc[0]
                    st.success(f"🎯 Candidato **{candidato_selecionado['Nome']}** localizado com correspondência exata!")
                else:
                    TAMANHO_PAGINA = 50
                    total_paginas = math.ceil(total_encontrados / TAMANHO_PAGINA)

                    if total_encontrados > TAMANHO_PAGINA:
                        st.info(
                            f"🔎 Encontrados **{total_encontrados}** candidatos contendo **\"{termo_busca}\"**. "
                            f"Para maior rapidez, digite o nome completo ou o número da inscrição."
                        )
                        col_pg, col_sel = st.columns([1, 2])
                        with col_pg:
                            opcoes_pag = [
                                f"Lote {p+1}: {p*TAMANHO_PAGINA + 1} a {min((p+1)*TAMANHO_PAGINA, total_encontrados)}"
                                for p in range(total_paginas)
                            ]
                            pag_idx = st.selectbox("Navegar entre os resultados:", range(total_paginas), format_func=lambda i: opcoes_pag[i])
                        
                        inicio = pag_idx * TAMANHO_PAGINA
                        fim = min(inicio + TAMANHO_PAGINA, total_encontrados)
                        resultados_pagina = resultados_busca.iloc[inicio:fim]
                    else:
                        st.info(f"🔎 Encontrados **{total_encontrados}** candidatos com esse termo. Selecione o seu abaixo:")
                        col_sel = st.container()
                        resultados_pagina = resultados_busca

                    with col_sel:
                        opcoes = [
                            f"{row['Posição_Geral']}º Geral - {row['Nome']} (Inscrição: {row['Inscrição']} | {row['Modalidade_Concorrencia']} | Nota: {row['Nota Objetiva']} pts)"
                            for _, row in resultados_pagina.iterrows()
                        ]
                        escolha = st.selectbox("Selecione o candidato correspondente:", opcoes)
                        idx_geral = int(escolha.split("º")[0]) - 1
                        candidato_selecionado = df_base.iloc[idx_geral]
    else:
        # Estado Inicial: Nenhuma busca realizada ainda
        st.markdown("""
        <div class="card border shadow-sm p-4 text-center my-3 rounded-3" style="background: #ffffff;">
            <div class="my-2">
                <i class="bi bi-person-badge text-primary" style="font-size: 3rem;"></i>
            </div>
            <h4 class="fw-bold text-dark mb-2">Consulte seu Boletim Individual com os Resultados Oficiais (23/10)</h4>
            <p class="text-secondary mx-auto mb-0" style="max-width: 620px; font-size: 0.95rem; line-height: 1.6;">
                Digite seu <strong>Nome Completo</strong> ou número de <strong>Inscrição</strong> no campo de busca acima para visualizar seu boletim oficial com nota objetiva, parecer da banca de cotas e projeção de convocação.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Exibição do Perfil do Candidato
    if candidato_selecionado is not None:
        pos_geral = int(candidato_selecionado['Posição_Geral'])
        nome = candidato_selecionado['Nome']
        inscricao = candidato_selecionado['Inscrição']
        nota_total = int(candidato_selecionado['Nota Objetiva'])
        aproveitamento_total = (nota_total / NOTA_MAXIMA_PROVA) * 100
        percentil = ((TOTAL_CANDIDATOS - pos_geral + 1) / TOTAL_CANDIDATOS) * 100
        top_pct = 100 - percentil
        top_pct_fmt = f"{top_pct:.2f}%"

        is_pcd = bool(candidato_selecionado['Cota_PCD'])
        is_etnico = bool(candidato_selecionado['Cota_Etnico_Racial'])
        is_ampla_pura = bool(candidato_selecionado['Ampla_Pura'])

        res_hetero = str(candidato_selecionado.get('Resultado_Hetero', 'Não se Aplica'))
        res_pcd = str(candidato_selecionado.get('Resultado_PCD', 'Não se Aplica'))

        # Tags de cotas
        tags_html = ""
        if is_ampla_pura:
            tags_html += '<span class="tag-cota tag-ampla">🏛️ Não Cotista (Ampla Concorrência)</span>'
        if candidato_selecionado['Cota_Negro_Pardo']:
            tags_html += '<span class="tag-cota tag-negro">🧑🏿 Cota Preto / Pardo</span>'
        if candidato_selecionado['Cota_Indigena']:
            tags_html += '<span class="tag-cota tag-indigena">🏹 Cota Indígena</span>'
        if candidato_selecionado['Cota_Quilombola']:
            tags_html += '<span class="tag-cota tag-quilombola">🏺 Cota Quilombola</span>'
        if is_pcd:
            tags_html += '<span class="tag-cota tag-pcd">♿ Cota PCD</span>'

        pos_class = "pos-top" if pos_geral <= 140 else "pos-standard"
        medalha = "🥇 " if pos_geral == 1 else ("🥈 " if pos_geral == 2 else ("🥉 " if pos_geral == 3 else "🎖️ "))

        # Montagem dos Cards de Resultado das Bancas de 23 de Outubro
        bloco_bancas_html = ""

        if is_etnico:
            if res_hetero == 'DEFERIDO':
                nova_pos_etn = int(candidato_selecionado['Nova_Pos_Lista_Etnico'])
                pos_orig_etn = int(candidato_selecionado['Pos_Lista_Etnico'])
                ganho_etn = int(candidato_selecionado['Ganho_Pos_Etnico'])
                bloco_bancas_html += f"""<div class="card-resultado-deferido">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
    <div style="font-size: 0.82rem; font-weight: 800; color: #15803D; text-transform: uppercase; letter-spacing: 0.04em;">
        ✅ RESULTADO PRELIMINAR DA HETEROIDENTIFICAÇÃO / ANÁLISE DOCUMENTAL (23/10/2026)
    </div>
    <span class="badge-pill">DEFERIDO</span>
</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 6px 0;">
    Sua condição na Cota Étnico-Racial foi CONFIRMADA pela comissão examinadora!
</div>
<div style="font-size: 0.9rem; color: #1E293B; line-height: 1.5; font-weight: 500;">
    Com a homologação preliminar e os 3.045 indeferimentos de concorrentes, sua classificação na cota avançou expressivamente:<br>
    • <strong>Posição Preliminar Pós-Banca:</strong> <span style="color: #6D28D9; font-weight: 800; font-size: 1.05rem;">{nova_pos_etn}º Lugar na Cota</span> (Posição original: {pos_orig_etn}º)<br>
    • <strong>Avanço na Fila:</strong> <span style="color: #15803D; font-weight: 800;">+{ganho_etn} posições conquistadas!</span>
</div>
</div>"""
            else:
                bloco_bancas_html += f"""<div class="card-resultado-indeferido">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
    <div style="font-size: 0.82rem; font-weight: 800; color: #B45309; text-transform: uppercase; letter-spacing: 0.04em;">
        ⚠️ RESULTADO PRELIMINAR DA HETEROIDENTIFICAÇÃO / ANÁLISE DOCUMENTAL (23/10/2026)
    </div>
    <span class="badge-pill-amber">INDEFERIDO NA COTA</span>
</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 6px 0;">
    Solicitação de Cota Étnico-Racial Indeferida Preliminarmente
</div>
<div style="font-size: 0.9rem; color: #1E293B; line-height: 1.55; font-weight: 500;">
    ⚖️ <strong>Regra do Edital (Art. 4º do Edital de Convocação):</strong> O indeferimento preliminar da autodeclaração <strong>NÃO ELIMINA você do concurso</strong>! Você continua concorrendo normalmente pelas vagas da <strong>Ampla Concorrência</strong>.<br>
    Sua classificação geral na Ampla: <strong>{pos_geral}º Lugar Geral ({nota_total} pontos)</strong>.
</div>
<div class="recurso-alert-box">
    📝 <strong>DIREITO A RECURSO ADMINISTRATIVO:</strong><br>
    • <strong>Prazo oficial:</strong> Da 0h00 de <strong>26/10/2026</strong> até às 23h59 de <strong>27/10/2026</strong> (horário de Brasília).<br>
    • <strong>Onde protocolar:</strong> No site oficial da banca: <a href="https://www.avalia.org.br" target="_blank" style="color: #1D4ED8; font-weight: 700; text-decoration: underline;">avalia.org.br</a>.<br>
    • <strong>Motivo da recusa:</strong> Acesse o link <em>"Boletim de Análise de Reserva de Vagas"</em> em avalia.org.br para consultar a justificativa e fundamentar seu recurso.
</div>
</div>"""

        if is_pcd:
            if res_pcd == 'DEFERIDO':
                nova_pos_pcd = int(candidato_selecionado['Nova_Pos_Lista_PCD'])
                pos_orig_pcd = int(candidato_selecionado['Pos_Lista_PCD'])
                ganho_pcd = int(candidato_selecionado['Ganho_Pos_PCD'])
                bloco_bancas_html += f"""<div class="card-resultado-deferido">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
    <div style="font-size: 0.82rem; font-weight: 800; color: #15803D; text-transform: uppercase; letter-spacing: 0.04em;">
        ✅ RESULTADO PRELIMINAR DA PERÍCIA MÉDICA PCD (23/10/2026)
    </div>
    <span class="badge-pill">LAUDO HOMOLOGADO</span>
</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 6px 0;">
    Laudo Médico e Condição de Pessoa com Deficiência (PCD) DEFERIDOS!
</div>
<div style="font-size: 0.9rem; color: #1E293B; line-height: 1.5; font-weight: 500;">
    A perícia médica multidisciplinar homologou sua documentação com sucesso:<br>
    • <strong>Posição Preliminar Pós-Perícia:</strong> <span style="color: #15803D; font-weight: 800; font-size: 1.05rem;">{nova_pos_pcd}º Lugar PCD</span> (Posição original: {pos_orig_pcd}º)<br>
    • <strong>Avanço na Fila PCD:</strong> <span style="color: #15803D; font-weight: 800;">+{ganho_pcd} posições conquistadas!</span>
</div>
</div>"""
            else:
                bloco_bancas_html += f"""<div class="card-resultado-indeferido">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
    <div style="font-size: 0.82rem; font-weight: 800; color: #B45309; text-transform: uppercase; letter-spacing: 0.04em;">
        ⚠️ RESULTADO PRELIMINAR DA PERÍCIA MÉDICA PCD (23/10/2026)
    </div>
    <span class="badge-pill-amber">LAUDO INDEFERIDO NA PERÍCIA</span>
</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin: 6px 0;">
    Solicitação de Cota PCD Indeferida Preliminarmente
</div>
<div style="font-size: 0.9rem; color: #1E293B; line-height: 1.55; font-weight: 500;">
    ⚖️ <strong>Regra do Edital (Art. 3º do Edital de Perícia Médica PCD):</strong> O não acolhimento do laudo na perícia médica <strong>NÃO ELIMINA você do concurso</strong>! Você continua concorrendo pelas vagas da <strong>Ampla Concorrência</strong>.<br>
    Sua classificação geral na Ampla: <strong>{pos_geral}º Lugar Geral ({nota_total} pontos)</strong>.
</div>
<div class="recurso-alert-box">
    📝 <strong>DIREITO A RECURSO CONTRA A PERÍCIA MÉDICA:</strong><br>
    • <strong>Período recursal:</strong> Da 0h00 de <strong>26/10/2026</strong> até às 23h59 de <strong>27/10/2026</strong> (horário de Brasília).<br>
    • <strong>Como consultar o laudo/motivo:</strong> Acesse o <em>"Boletim de Análise de Reserva de Vagas"</em> em <a href="https://www.avalia.org.br" target="_blank" style="color: #1D4ED8; font-weight: 700; text-decoration: underline;">avalia.org.br</a>.
</div>
</div>"""

        if is_ampla_pura:
            bloco_bancas_html += """<div class="card-resultado-ampla">
<div style="font-size: 0.82rem; font-weight: 800; color: #0369A1; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.04em;">
    🏛️ CANDIDATO NÃO COTISTA (AMPLA CONCORRÊNCIA PURA)
</div>
<div style="font-size: 1.05rem; font-weight: 800; color: #0F172A;">
    ⚪ As bancas de cotas e resultados de 23 de outubro não se aplicam a você
</div>
<div style="font-size: 0.88rem; color: #334155; margin-top: 6px; line-height: 1.5; font-weight: 500;">
    Como candidato exclusivo de Ampla Concorrência, sua pontuação concorre diretamente no cômputo universal de vagas e sua próxima etapa avaliativa do cronograma é a convocação para o TAF (conforme linha de corte).
</div>
</div>"""

        # Previsão Oficial do TAF pós-bancas
        status_taf_prel = str(candidato_selecionado.get('Previsao_TAF_Preliminar', ''))
        is_convocado_taf = bool(candidato_selecionado.get('Convocado_TAF_Preliminar', False))
        taf_class = "card-previsao-ok" if is_convocado_taf else "card-previsao"
        taf_badge_color = "#15803D" if is_convocado_taf else "#475569"
        taf_badge_text = "🟢 SITUAÇÃO TAF: DENTRO DO LIMITE DE CONVOCAÇÃO!" if is_convocado_taf else "⚪ SITUAÇÃO TAF: FORA DO CORTE PRELIMINAR"

        taf_html = f"""<div class="{taf_class}">
<div style="font-size: 0.82rem; font-weight: 800; color: {taf_badge_color}; text-transform: uppercase; margin-bottom: 6px;">
    🎯 {taf_badge_text}
</div>
<div style="font-size: 1.05rem; font-weight: 800; color: #0F172A; margin-bottom: 4px;">
    {status_taf_prel}
</div>
<div style="font-size: 0.88rem; color: #475569; font-weight: 600;">
    🏆 Situação de Vagas: <strong>{candidato_selecionado['Previsao_Vagas_Preliminar']}</strong>
</div>
</div>"""

        card_html = f"""<div class="candidate-card">
<div class="d-flex justify-content-between align-items-start flex-wrap gap-3">
<div>
<span class="badge-pill"><i class="bi bi-patch-check-fill text-success me-1"></i> BOLETIM ATUALIZADO • 23 DE OUTUBRO DE 2026</span>
<h2 class="hero-title mt-1 mb-2" style="font-size: 1.85rem;">{nome}</h2>
<p class="text-secondary mb-2" style="font-size: 0.95rem; font-weight: 500;">
<i class="bi bi-person-vcard text-primary me-1"></i> Inscrição: <strong class="text-dark">{inscricao}</strong> &nbsp;•&nbsp; <i class="bi bi-shield-lock text-primary me-1"></i> Cargo: <strong class="text-dark">401 - Policial Penal RN</strong>
</p>
<div class="mt-2">{tags_html}</div>
</div>
<div class="candidate-header-badge">
<div class="pos-badge {pos_class}">
{medalha}{pos_geral}º LUGAR GERAL
</div>
<div class="fw-bold text-primary mt-1" style="font-size: 0.85rem;">
<i class="bi bi-graph-up-arrow me-1"></i> Top {top_pct_fmt} de todos os {TOTAL_CANDIDATOS_FMT} candidatos
</div>
</div>
</div>
{bloco_bancas_html}
{taf_html}
</div>"""

        st.markdown(card_html, unsafe_allow_html=True)

        # 4 Indicadores Principais de Classificação
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-list-ol text-primary me-1"></i> Classificação Geral Oficial</div>
<div class="stat-value">{pos_geral}º</div>
<div class="stat-sub text-primary fw-bold">↑ De {TOTAL_CANDIDATOS_FMT} candidatos</div>
</div>""", unsafe_allow_html=True)
        with c2:
            if is_pcd and res_pcd == 'DEFERIDO' and is_etnico and res_hetero == 'DEFERIDO':
                if nota_total < 113:
                    lbl_cota = "<i class='bi bi-universal-access text-success me-1'></i> Posição Preliminar PCD (Convocado)"
                    val_cota = f"{int(candidato_selecionado['Nova_Pos_Lista_PCD'])}º"
                    sub_cota = f"♿ {int(candidato_selecionado['Nova_Pos_Lista_PCD'])}º PCD • 🧑🏿 {int(candidato_selecionado['Nova_Pos_Lista_Etnico'])}º na Cota Étnica"
                else:
                    lbl_cota = "<i class='bi bi-person-fill-check me-1' style='color: #6f42c1;'></i> Posição Preliminar nas Cotas"
                    val_cota = f"{int(candidato_selecionado['Nova_Pos_Lista_Etnico'])}º"
                    sub_cota = f"🧑🏿 {int(candidato_selecionado['Nova_Pos_Lista_Etnico'])}º Étnico • ♿ {int(candidato_selecionado['Nova_Pos_Lista_PCD'])}º PCD"
            elif is_pcd and res_pcd == 'DEFERIDO' and pd.notnull(candidato_selecionado['Nova_Pos_Lista_PCD']):
                lbl_cota = "<i class='bi bi-universal-access text-success me-1'></i> Posição Preliminar PCD"
                val_cota = f"{int(candidato_selecionado['Nova_Pos_Lista_PCD'])}º"
                sub_cota = f"↑ De {TOTAL_PCD_APTOS} PCDs deferidos"
            elif is_etnico and res_hetero == 'DEFERIDO' and pd.notnull(candidato_selecionado['Nova_Pos_Lista_Etnico']):
                lbl_cota = "<i class='bi bi-person-fill-check me-1' style='color: #6f42c1;'></i> Posição Preliminar na Cota"
                val_cota = f"{int(candidato_selecionado['Nova_Pos_Lista_Etnico'])}º"
                sub_cota = f"↑ De {TOTAL_ETNICO_APTOS:,} cotistas deferidos"
            elif is_etnico or is_pcd:
                lbl_cota = "<i class='bi bi-exclamation-circle-fill text-warning me-1'></i> Cota Indeferida (Concorre Ampla)"
                val_cota = f"{pos_geral}º"
                sub_cota = "Disputa universal na Ampla"
            else:
                lbl_cota = "<i class='bi bi-award-fill text-primary me-1'></i> Posição Não Cotista"
                val_cota = f"{int(candidato_selecionado['Pos_Lista_Ampla_Pura'])}º"
                sub_cota = f"↑ De {TOTAL_AMPLA_FMT} da Ampla Pura"
            st.markdown(f"""<div class="stat-card">
<div class="stat-label">{lbl_cota}</div>
<div class="stat-value">{val_cota}</div>
<div class="stat-sub text-primary fw-bold">{sub_cota}</div>
</div>""".replace(",", "."), unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-clipboard2-check text-success me-1"></i> Nota Objetiva</div>
<div class="stat-value">{nota_total} pts</div>
<div class="stat-sub text-success fw-bold">↑ {aproveitamento_total:.1f}% de aproveitamento (Máx {NOTA_MAXIMA_PROVA})</div>
</div>""", unsafe_allow_html=True)
        with c4:
            vaga_prel = str(candidato_selecionado['Previsao_Vagas_Preliminar'])
            if "Vaga Imediata" in vaga_prel:
                val_vagas = "Vagas Imediatas 🏆"
                color_vagas = "#198754"
            else:
                val_vagas = "Cadastro Reserva 📋"
                color_vagas = "#212529"
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-trophy text-warning me-1"></i> Situação de Vagas Preliminar</div>
<div class="stat-value" style="color: {color_vagas}; font-size: 1.35rem;">{val_vagas}</div>
<div class="stat-sub text-secondary fw-bold">{vaga_prel}</div>
</div>""", unsafe_allow_html=True)

        st.write("")

        # Projeção Preditiva pós-recursos e TAF (pré-computada)
        with st.expander("🔮 Sua Projeção Preditiva pós-Recursos e TAF (Simulador)", expanded=True):
            st.caption("Cenário de projeção considerando **5% de recursos deferidos** em 26-27/10 e **20% de reprovação no TAF** (médias históricas de carreiras policiais):")

            col_sim1, col_sim2, col_sim3 = st.columns(3)
            with col_sim1:
                pos_etn_sim = candidato_selecionado.get('Pos_Etnico_Sim_Padrao')
                pos_pcd_sim = candidato_selecionado.get('Pos_PCD_Sim_Padrao')
                if is_pcd and res_pcd == 'DEFERIDO' and is_etnico and res_hetero == 'DEFERIDO':
                    if nota_total < 113:
                        lbl_sim = "<i class='bi bi-universal-access text-success me-1'></i> Posição Estimada PCD (Convocado)"
                        val_sim = f"{int(pos_pcd_sim)}º" if pd.notnull(pos_pcd_sim) else "-"
                        sub_sim = f"PCD: {val_sim} • Étnico: {int(pos_etn_sim)}º" if pd.notnull(pos_etn_sim) else ""
                        color_sim = "#198754"
                    else:
                        lbl_sim = "<i class='bi bi-person-fill-check me-1' style='color: #6f42c1;'></i> Posição Estimada na Cota Étnica"
                        val_sim = f"{int(pos_etn_sim)}º" if pd.notnull(pos_etn_sim) else "-"
                        sub_sim = f"Étnico: {val_sim} • PCD: {int(pos_pcd_sim)}º" if pd.notnull(pos_pcd_sim) else ""
                        color_sim = "#6f42c1"
                    st.markdown(f"""<div class="stat-card">
<div class="stat-label">{lbl_sim}</div>
<div class="stat-value" style="color: {color_sim};">{val_sim}</div>
<div class="stat-sub text-success fw-bold">{sub_sim}</div>
</div>""", unsafe_allow_html=True)
                elif is_pcd and res_pcd == 'DEFERIDO' and pd.notnull(pos_pcd_sim):
                    st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-universal-access text-success me-1"></i> Posição Estimada PCD</div>
<div class="stat-value text-success">{int(pos_pcd_sim)}º</div>
<div class="stat-sub text-success fw-bold">Classificação pós-perícia definitiva</div>
</div>""", unsafe_allow_html=True)
                elif is_etnico and res_hetero == 'DEFERIDO' and pd.notnull(pos_etn_sim):
                    st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-person-fill-check me-1' style='color: #6f42c1;'></i> Posição Estimada na Cota Étnica</div>
<div class="stat-value" style="color: #6f42c1;">{int(pos_etn_sim)}º</div>
<div class="stat-sub text-success fw-bold">Classificação pós-recursos estimada</div>
</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-award-fill text-primary me-1"></i> Situação na Ampla Concorrência</div>
<div class="stat-value text-primary">{pos_geral}º</div>
<div class="stat-sub text-secondary fw-bold">Disputa geral na Ampla Universal</div>
</div>""", unsafe_allow_html=True)

            with col_sim2:
                is_convocado_taf_sim = bool(candidato_selecionado.get('Convocado_TAF_Sim_Padrao', False))
                status_taf_text = "🟢 Convocado para o TAF!" if is_convocado_taf_sim else "⚪ Fora do corte do TAF"
                color_taf_text = "#198754" if is_convocado_taf_sim else "#6c757d"
                sub_taf_text = "Dentro da linha de corte estimada" if is_convocado_taf_sim else "Abaixo da pontuação de corte"
                st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-flag-fill me-1" style="color: {color_taf_text};"></i> Convocação para o TAF</div>
<div class="stat-value" style="color: {color_taf_text}; font-size: 1.25rem;">{status_taf_text}</div>
<div class="stat-sub text-secondary fw-bold">{sub_taf_text}</div>
</div>""", unsafe_allow_html=True)

            with col_sim3:
                vaga_sim = str(candidato_selecionado.get('Vaga_Imediata_Sim_Padrao', '📋 Cadastro de Reserva'))
                is_vaga_imediata = "Vaga Imediata" in vaga_sim
                if is_vaga_imediata:
                    val_vaga_text = "Vaga Imediata 🏆"
                    sub_vaga_text = "↑ Entra nas 200 vagas imediatas pós-TAF!"
                    color_vaga_text = "#198754"
                else:
                    val_vaga_text = "Cadastro Reserva 📋"
                    sub_vaga_text = "Dentro do Cadastro de Reserva"
                    color_vaga_text = "#212529"
                st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-award me-1" style="color: {color_vaga_text};"></i> Projeção Pós-TAF</div>
<div class="stat-value" style="color: {color_vaga_text}; font-size: 1.25rem;">{val_vaga_text}</div>
<div class="stat-sub text-secondary fw-bold">{sub_vaga_text}</div>
</div>""", unsafe_allow_html=True)

                st.info("💡 **Deseja personalizar taxas de recurso e atrito do TAF?** Acesse a aba **'🔮 Simuladores'** no menu superior!")

        st.write("")

        # Detalhamento de Disciplinas
        st.markdown("#### 📋 Detalhamento do seu Aproveitamento por Disciplina")
        dados_detalhamento = []
        for d in DISCIPLINAS:
            nota_cand = int(candidato_selecionado[d])
            max_p = PONTOS_MAXIMOS[d]
            aprov = (nota_cand / max_p) * 100
            media_disc = MEDIAS_DISCIPLINAS.get(d, 10.0)
            diff_media = nota_cand - media_disc
            dados_detalhamento.append({
                "Disciplina": d,
                "Sua Nota": f"{nota_cand} / {max_p} pts",
                "Aproveitamento": f"{aprov:.1f}%",
                "Média Geral da Prova": f"{media_disc:.2f} pts",
                "Comparativo com a Média": f"{diff_media:+.2f} pts" + (" 🟢 Acima" if diff_media > 0 else " 🔴 Abaixo")
            })
        st.dataframe(pd.DataFrame(dados_detalhamento), width="stretch", hide_index=True)

        # Gráfico de barras horizontal
        pct_candidato = [(candidato_selecionado[d] / PONTOS_MAXIMOS[d]) * 100 for d in DISCIPLINAS]
        nomes_curtos = [
            d.replace("História do RN e Aspectos Geoeconômicos do RN", "História RN")
             .replace("Ética no Serviço Público", "Ética")
             .replace("Direito Penal e Processo Penal", "Penal / Processo")
             .replace("Legislação Específica", "Leg. Específica")
            for d in DISCIPLINAS
        ]
        cores = ['#198754' if p >= 80 else ('#ffc107' if p >= 60 else '#dc3545') for p in pct_candidato]

        fig_bar = go.Figure(go.Bar(
            x=pct_candidato,
            y=nomes_curtos,
            orientation='h',
            marker_color=cores,
            text=[f"{p:.1f}% ({candidato_selecionado[d]}/{PONTOS_MAXIMOS[d]} pts)" for p, d in zip(pct_candidato, DISCIPLINAS)],
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(color='white', size=11, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif', weight=700)
        ))
        fig_bar.update_layout(
            title=dict(text="Aproveitamento Percentual por Disciplina", font=dict(color='#212529', size=14, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif')),
            xaxis=dict(range=[0, 105], title="Aproveitamento (%)", gridcolor='#dee2e6', tickfont=dict(color='#6c757d')),
            yaxis=dict(autorange="reversed", tickfont=dict(color='#212529')),
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=20, t=40, b=30),
            height=340
        )
        st.plotly_chart(fig_bar, width="stretch")

        # Vizinhos de Classificação
        with st.expander("👥 Candidatos Próximos na Classificação Geral (+/- 5 concorrentes ao redor)"):
            st.caption("Veja os candidatos imediatamente antes e depois da sua posição e o status de cada um nas bancas preliminares:")
            start_idx = max(0, pos_geral - 6)
            end_idx = min(TOTAL_CANDIDATOS, pos_geral + 5)
            vizinhos = df_base.iloc[start_idx:end_idx][['Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Status_Cota_Preliminar', 'Nota Objetiva', 'Execução Penal', 'Legislação Específica', 'Previsao_TAF_Preliminar']]

            def destacar_linha(row):
                if row['Posição_Geral'] == pos_geral:
                    return ['background-color: #E0F2FE; font-weight: bold; color: #0369A1;'] * len(row)
                return [''] * len(row)

            st.dataframe(
                vizinhos.style.apply(destacar_linha, axis=1),
                width="stretch",
                hide_index=True
            )

        # Confronto Direto
        with st.expander("⚔️ Comparar Meu Resultado com Outro Candidato"):
            st.caption("Compare seu boletim de notas matéria por matéria com qualquer concorrente da lista:")
            col_comp_busca, col_comp_sel = st.columns([1, 1])
            with col_comp_busca:
                termo_outro = st.text_input("Buscar Concorrente (Nome ou Inscrição):", placeholder="Digite o nome do concorrente...", key="busca_outro")

            if termo_outro.strip():
                norm_outro = normalizar_texto(termo_outro)
                if norm_outro in mapa_inscricoes:
                    filtro_outro = df_base.iloc[[mapa_inscricoes[norm_outro]]]
                elif norm_outro.isdigit():
                    filtro_outro = df_base[df_base['Inscrição_Str'].str.startswith(norm_outro)]
                else:
                    filtro_outro = df_base[df_base['Nome_Busca'].str.contains(norm_outro, regex=False, na=False)]
                if len(filtro_outro) > 0:
                    opcoes_outro = [
                        f"{row['Posição_Geral']}º - {row['Nome']} (Nota: {row['Nota Objetiva']} pts | {row['Status_Cota_Preliminar']})"
                        for _, row in filtro_outro.head(25).iterrows()
                    ]
                    with col_comp_sel:
                        escolha_outro = st.selectbox("Selecione o concorrente:", opcoes_outro, key="sel_outro")
                    pos_outro = int(escolha_outro.split("º")[0]) - 1
                    outro_dados = df_base.iloc[pos_outro]

                    diff_total = nota_total - int(outro_dados['Nota Objetiva'])
                    if diff_total > 0:
                        st.success(f"🏆 Você está à frente por **+{diff_total} pontos** ({nota_total} vs {outro_dados['Nota Objetiva']} pts).")
                    elif diff_total < 0:
                        st.warning(f"O concorrente está à frente por **+{abs(diff_total)} pontos** ({outro_dados['Nota Objetiva']} vs {nota_total} pts).")
                    else:
                        st.info(f"🤝 **Empate em {nota_total} pontos!** Desempate do edital: {nome} ({pos_geral}º) vs {outro_dados['Nome']} ({outro_dados['Posição_Geral']}º).")

                    confronto_rows = []
                    for d in DISCIPLINAS:
                        n1 = int(candidato_selecionado[d])
                        n2 = int(outro_dados[d])
                        if n1 > n2:
                            vantagem = f"🟢 +{n1 - n2} pts (Você)"
                        elif n2 > n1:
                            vantagem = f"🔵 +{n2 - n1} pts ({outro_dados['Nome'].split()[0]})"
                        else:
                            vantagem = "⚪ Empate"
                        confronto_rows.append({
                            "Disciplina": d,
                            "Sua Nota": f"{n1} pts",
                            f"{outro_dados['Nome']}": f"{n2} pts",
                            "Vantagem": vantagem
                        })
                    st.dataframe(pd.DataFrame(confronto_rows), width="stretch", hide_index=True)
                else:
                    st.warning("Nenhum candidato encontrado com esse nome.")
            else:
                st.caption("Digite o nome ou número de inscrição no campo acima para iniciar o confronto.")

        with st.expander("❓ Critérios Oficiais de Desempate do Edital (Item 21.2.1)"):
            st.markdown("""
            Conforme o **Item 21.2.1 do Edital**, em caso de igualdade de pontos na nota final da prova objetiva, o desempate oficial seguiu rigorosamente a ordem:
            1. **Idade igual ou superior a 60 anos** (Estatuto da Pessoa Idosa);
            2. **Maior pontuação na disciplina de Execução Penal** (peso de 30 pts);
            3. **Maior pontuação em Legislação Específica** (peso de 40 pts);
            4. **Maior pontuação em Direito Penal e Processo Penal** (peso de 20 pts);
            5. **Maior pontuação em Língua Portuguesa** (peso de 15 pts);
            6. **Maior pontuação em História do RN**;
            7. **Maior idade cronológica geral**.
            """)
