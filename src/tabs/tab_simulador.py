"""
Aba 2: Simulador de Colocações e Cenários do Concurso (Validade de 4 Anos e Impacto das Bancas/TAF).
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from src.data_loader import normalizar_texto
from src.simulation import executar_simulacao_pos_bancas


def render_tab_simulador(df_base, mapa_inscricoes):
    """Renderiza a aba de simuladores com projeção de CR em 4 anos e Monte Carlo de TAF/Recursos."""
    st.markdown("""<div class="sim-banner">
    <span class="sim-badge"><i class="bi bi-sliders me-1"></i> SIMULADORES ESTRATÉGICOS • PPRN</span>
    <h2 class="hero-title mt-1 mb-2" style="font-size: 1.75rem;"><i class="bi bi-diagram-3-fill text-primary me-2"></i>Simulador de Convocação & Cenários do Concurso</h2>
    <p class="text-secondary mb-0" style="font-size: 0.95rem; line-height: 1.55;">
    Projete suas chances reais com base no número total de nomeações ao longo dos 4 anos de validade ou simule o impacto dos recursos e atrito do TAF.
    </p>
    </div>""", unsafe_allow_html=True)

    sim_subtab1, sim_subtab2 = st.tabs([
        "🎯 Quantas Pessoas a Banca vai Chamar? (Validade de 4 Anos)",
        "🏃‍♂️ Impacto dos Recursos & Reprovação no TAF"
    ])

    with sim_subtab1:
        st.markdown("#### 🎯 Projeção de Nomeações ao Longo da Validade (2+2 anos)")
        st.caption("O edital prevê inicialmente **200 vagas imediatas**, mas historicamente concursos de segurança pública convocam turmas adicionais do Cadastro de Reserva.")

        col_sim_c1, col_sim_c2 = st.columns([1, 1])
        with col_sim_c1:
            total_convocados = st.slider(
                "Quantas pessoas você estima que o Estado/Banca vai chamar ao total nos 4 anos?",
                min_value=200, max_value=1200, value=400, step=25,
                help="Total acumulado de nomeações de Policiais Penais no período de validade do certame."
            )
        with col_sim_c2:
            taxa_atrito = st.slider(
                "Taxa Estimada de Desistências / Reprovações nas Fases (TAF, Psico, Médico, CFP e outros certames):",
                min_value=0, max_value=40, value=15, step=5, format="%d%%",
                help="Percentual de candidatos que não chegam à posse devido a desistências ou inaptidões. Use 0% para um cálculo conservador direto da lista."
            )

        fator_atrito = 1.0 - (taxa_atrito / 100.0)

        vagas_ac = int(round(total_convocados * 0.70))
        vagas_etn = int(round(total_convocados * 0.20))
        vagas_pcd = int(round(total_convocados * 0.10))

        alcance_ac = int(round(vagas_ac / fator_atrito)) if fator_atrito > 0 else vagas_ac
        alcance_etn = int(round(vagas_etn / fator_atrito)) if fator_atrito > 0 else vagas_etn
        alcance_pcd = int(round(vagas_pcd / fator_atrito)) if fator_atrito > 0 else vagas_pcd

        ca1, ca2, ca3, ca4 = st.columns(4)
        with ca1:
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-people-fill text-primary me-1"></i> Total de Chamados</div>
<div class="stat-value">{total_convocados}</div>
<div class="stat-sub">Vagas distribuídas nos 4 anos</div>
</div>""", unsafe_allow_html=True)
        with ca2:
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-award-fill text-primary me-1"></i> Ampla Concorrência (70%)</div>
<div class="stat-value text-primary">{vagas_ac} vagas</div>
<div class="stat-sub text-success fw-bold">Alcança até o {alcance_ac}º Geral</div>
</div>""", unsafe_allow_html=True)
        with ca3:
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-person-fill-check me-1" style="color: #6f42c1;"></i> Cota Étnica (20%)</div>
<div class="stat-value" style="color: #6f42c1;">{vagas_etn} vagas</div>
<div class="stat-sub text-success fw-bold">Alcança até o {alcance_etn}º da Cota</div>
</div>""", unsafe_allow_html=True)
        with ca4:
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-universal-access text-success me-1"></i> Cota PCD (10%)</div>
<div class="stat-value text-success">{vagas_pcd} vagas</div>
<div class="stat-sub text-success fw-bold">Alcança até o {alcance_pcd}º PCD</div>
</div>""", unsafe_allow_html=True)

        st.write("")

        st.markdown("#### 🔎 E você, está dentro desse cenário?")
        st.write(f"Digite seu **Nome** ou **Inscrição** para checar se você seria convocado(a) com **{total_convocados} chamados**:")

        termo_sim_pessoal = st.text_input("Consultar candidato na simulação:", placeholder="Digite o nome ou número de inscrição...", key="input_sim_pessoal")

        cand_sim_pessoal = None
        if termo_sim_pessoal.strip():
            norm_p = normalizar_texto(termo_sim_pessoal)
            if norm_p in mapa_inscricoes:
                cand_sim_pessoal = df_base.iloc[mapa_inscricoes[norm_p]]
            elif norm_p.isdigit():
                m_res = df_base[df_base['Inscrição_Str'].str.startswith(norm_p)]
                if len(m_res) > 0:
                    cand_sim_pessoal = m_res.iloc[0]
            else:
                m_res = df_base[df_base['Nome_Busca'].str.contains(norm_p, regex=False, na=False)]
                if len(m_res) > 0:
                    cand_sim_pessoal = m_res.iloc[0]

        if cand_sim_pessoal is not None:
            p_pos_geral = int(cand_sim_pessoal['Posição_Geral'])
            p_res_etn = str(cand_sim_pessoal.get('Resultado_Hetero', ''))
            p_res_pcd = str(cand_sim_pessoal.get('Resultado_PCD', ''))

            if cand_sim_pessoal['Cota_Etnico_Racial'] and p_res_etn == 'DEFERIDO' and pd.notnull(cand_sim_pessoal['Nova_Pos_Lista_Etnico']):
                p_modalidade = "Cota Étnico-Racial"
                p_pos = int(cand_sim_pessoal['Nova_Pos_Lista_Etnico'])
                p_alcance = alcance_etn
                p_vagas_pct = 0.20
                tipo_fila = "na Cota Étnica"
            elif cand_sim_pessoal['Cota_PCD'] and p_res_pcd == 'DEFERIDO' and pd.notnull(cand_sim_pessoal['Nova_Pos_Lista_PCD']):
                p_modalidade = "Cota PCD"
                p_pos = int(cand_sim_pessoal['Nova_Pos_Lista_PCD'])
                p_alcance = alcance_pcd
                p_vagas_pct = 0.10
                tipo_fila = "na Cota PCD"
            else:
                p_modalidade = "Ampla Concorrência"
                p_pos = p_pos_geral
                p_alcance = alcance_ac
                p_vagas_pct = 0.70
                tipo_fila = "na Ampla (Geral)"

            esta_dentro = p_pos <= p_alcance
            total_necessario = int(round((p_pos * fator_atrito) / p_vagas_pct))

            if esta_dentro:
                st.markdown(f"""
                <div class="card bg-success-subtle border-start border-4 border-success p-3 rounded-3 shadow-sm my-2">
                    <div class="fw-bold text-success fs-5">
                        <i class="bi bi-check-circle-fill me-1"></i> PARABÉNS! VOCÊ SERIA CONVOCADO(A) NESTE CENÁRIO!
                    </div>
                    <div class="text-dark mt-1" style="font-size: 0.92rem; line-height: 1.55;">
                        Candidato: <strong>{cand_sim_pessoal['Nome']}</strong> • Modalidade: <strong>{p_modalidade}</strong><br>
                        Sua posição: <strong>{p_pos}º {tipo_fila}</strong> | Alcance máximo estimado: <strong>até o {p_alcance}º colocado</strong>.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                diff_pos = p_pos - p_alcance
                st.markdown(f"""
                <div class="card bg-warning-subtle border-start border-4 border-warning p-3 rounded-3 shadow-sm my-2">
                    <div class="fw-bold text-warning-emphasis fs-5">
                        <i class="bi bi-clock-history me-1"></i> Fora por {diff_pos} posições neste cenário de {total_convocados} chamados
                    </div>
                    <div class="text-dark mt-1" style="font-size: 0.92rem; line-height: 1.55;">
                        Candidato: <strong>{cand_sim_pessoal['Nome']}</strong> • Sua posição: <strong>{p_pos}º {tipo_fila}</strong> (Alcance atual: até o {p_alcance}º).<br>
                        Se o Estado chamar turmas extras até <strong>{total_necessario} convocados</strong> ao longo dos 4 anos de validade, você será nomeado(a)!
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("##### 📊 Tabela de Cenários de Convocação nos 4 Anos:")
        cenarios = [200, 300, 400, 500, 600, 800, 1000]
        cenarios_dados = []
        for c in cenarios:
            v_ac = int(round(c * 0.70))
            v_et = int(round(c * 0.20))
            v_pc = int(round(c * 0.10))
            alc_ac = int(round(v_ac / fator_atrito)) if fator_atrito > 0 else v_ac
            alc_et = int(round(v_et / fator_atrito)) if fator_atrito > 0 else v_et
            alc_pc = int(round(v_pc / fator_atrito)) if fator_atrito > 0 else v_pc
            cenarios_dados.append({
                "Total Chamados": f"{c} candidatos",
                "Ampla Concorrência (70%)": f"{v_ac} vagas (até {alc_ac}º Geral)",
                "Cota Étnica (20%)": f"{v_et} vagas (até {alc_et}º Cota)",
                "Cota PCD (10%)": f"{v_pc} vagas (até {alc_pc}º PCD)",
                "Contexto Típico": "Vagas originais do Edital" if c == 200 else ("2 turmas (dobra)" if c == 400 else ("3 turmas" if c == 600 else "Aproveitamento amplo CR"))
            })
        st.dataframe(pd.DataFrame(cenarios_dados), width="stretch", hide_index=True)

    with sim_subtab2:
        st.markdown("#### ⚙️ Parâmetros de Simulação de Recursos & TAF")
        st.caption("Projete o impacto dos **3.045 indeferimentos da Heteroidentificação** e **186 PCDs** nas vagas imediatas:")

        col_ctrl1, col_ctrl2 = st.columns(2)
        with col_ctrl1:
            taxa_rev_etn = st.slider(
                "Taxa Estimada de Reversão de Recursos na Heteroidentificação Étnica:",
                min_value=0, max_value=25, value=5, step=1, format="%d%%",
                help="Porcentagem dos candidatos indeferidos que revertem na fase recursal."
            )
            taxa_rev_pcd = st.slider(
                "Taxa Estimada de Reversão de Recursos na Perícia Médica PCD:",
                min_value=0, max_value=25, value=5, step=1, format="%d%%",
                help="Porcentagem dos PCDs indeferidos que revertem no recurso."
            )

        with col_ctrl2:
            taxa_taf = st.slider(
                "Taxa Estimada de Reprovação / Abstenção no TAF:",
                min_value=0, max_value=45, value=20, step=1, format="%d%%",
                help="Atrito médio nos testes físicos (barra, corrida, abdominal)."
            )
            st.markdown(f"""
            <div class="card bg-light border p-3 rounded-3 mt-1" style="font-size: 0.85rem; line-height: 1.45;">
            <div class="fw-bold text-dark mb-1"><i class="bi bi-pin-angle-fill text-primary me-1"></i> Resumo dos Parâmetros:</div>
            • Recursos Aceitos Cota Étnica: <strong>{taxa_rev_etn}%</strong> (~{int(3045 * taxa_rev_etn / 100)})<br>
            • Recursos Aceitos Perícia PCD: <strong>{taxa_rev_pcd}%</strong> (~{int(186 * taxa_rev_pcd / 100)})<br>
            • Reprovação no TAF: <strong>{taxa_taf}%</strong> de atrito
            </div>
            """, unsafe_allow_html=True)

        df_simulada, res_sim, novos_ampla, novos_etnico, novos_pcd = executar_simulacao_pos_bancas(
            df_base,
            modo="real_bancas",
            taxa_reversao_etnico_pct=taxa_rev_etn,
            taxa_reversao_pcd_pct=taxa_rev_pcd,
            taxa_taf_pct=taxa_taf
        )

        st.write("---")
        st.markdown("#### 📊 Impacto nas Vagas Imediatas e Linhas de Corte")

        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-people-fill text-primary me-1"></i> Alcance Ampla (140 vagas)</div>
<div class="stat-value text-primary">Até o {res_sim['ultimo_ampla_orig']}º</div>
<div class="stat-sub text-success fw-bold">+{res_sim['ganho_ampla']} posições ganhas pós-TAF</div>
</div>""", unsafe_allow_html=True)

        with sc2:
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-person-fill-check me-1" style="color: #6f42c1;"></i> Alcance Cota Étnica (40 vagas)</div>
<div class="stat-value" style="color: #6f42c1;">Até o {res_sim['ultimo_etnico_orig']}º</div>
<div class="stat-sub text-success fw-bold">+{res_sim['ganho_etnico']} cotistas beneficiados</div>
</div>""", unsafe_allow_html=True)

        with sc3:
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-universal-access text-success me-1"></i> Alcance PCD (20 vagas)</div>
<div class="stat-value text-success">Até o {res_sim['ultimo_pcd_orig']}º</div>
<div class="stat-sub text-success fw-bold">+{res_sim['ganho_pcd']} PCDs beneficiados</div>
</div>""", unsafe_allow_html=True)

        with sc4:
            st.markdown(f"""<div class="stat-card">
<div class="stat-label"><i class="bi bi-arrow-down-circle-fill text-primary me-1"></i> Linha de Corte TAF (Cota)</div>
<div class="stat-value">{res_sim['corte_etnico_taf']} pts</div>
<div class="stat-sub text-primary fw-bold">Caiu de 115 para {res_sim['corte_etnico_taf']} pts</div>
</div>""", unsafe_allow_html=True)

        st.write("")

        fig_comp = go.Figure()
        modalidades_k = ['Ampla Concorrência', 'Cota Étnico-Racial', 'Cota PCD']
        valores_orig = [140, 40, 20]
        valores_sim = [res_sim['ultimo_ampla_orig'], res_sim['ultimo_etnico_orig'], res_sim['ultimo_pcd_orig']]

        fig_comp.add_trace(go.Bar(
            name='Oficial (Sem atrito de banca/TAF)',
            x=modalidades_k,
            y=valores_orig,
            marker_color='#6c757d',
            text=[f"{v}º" for v in valores_orig],
            textposition='auto',
            textfont=dict(weight=700, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif')
        ))
        fig_comp.add_trace(go.Bar(
            name=f'Simulação pós-Bancas e TAF ({taxa_taf}%)',
            x=modalidades_k,
            y=valores_sim,
            marker_color=['#0d6efd', '#6f42c1', '#198754'],
            text=[f"{v}º (+{v-orig})" for v, orig in zip(valores_sim, valores_orig)],
            textposition='auto',
            textfont=dict(weight=700, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif')
        ))
        fig_comp.update_layout(
            title=dict(text="Alcance Máximo de Convocação para as Vagas Imediatas (Oficial vs Simulado)", font=dict(color='#212529', size=14, family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif')),
            barmode='group',
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(title="Última Colocação Alcançada", gridcolor='#dee2e6'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif')),
            margin=dict(l=10, r=20, t=50, b=30),
            height=340
        )
        st.plotly_chart(fig_comp, width="stretch")

        # Detalhamento
        st.markdown("#### 📋 Detalhamento dos Candidatos no Cenário Simulado")
        tab_sub1, tab_sub2, tab_sub3, tab_sub4 = st.tabs([
            f"🏆 Entram nas Vagas da Geral ({len(novos_ampla)})",
            f"🧑🏿 Entram nas Vagas da Cota ({len(novos_etnico)})",
            f"♿ Entram nas Vagas PCD ({len(novos_pcd)})",
            "🔍 Consultar Candidato na Simulação"
        ])

        with tab_sub1:
            st.write(f"Candidatos que estavam no **Cadastro de Reserva da Geral** (> 140º) e agora alcançam uma das **140 Vagas Imediatas**:")
            if len(novos_ampla) > 0:
                cols_show_ampla = ['Posição_Geral', 'Nome', 'Inscrição', 'Modalidade_Concorrencia', 'Nota Objetiva', 'Execução Penal', 'Legislação Específica']
                st.dataframe(novos_ampla[cols_show_ampla], width="stretch", hide_index=True)
            else:
                st.info("Nenhum candidato além do 140º com a configuração atual.")

        with tab_sub2:
            st.write(f"Cotistas étnicos que estavam no **Cadastro de Reserva da Cota** (> 40º) e agora alcançam uma das **40 Vagas Imediatas Reservadas**:")
            if len(novos_etnico) > 0:
                cols_show_etnico = ['Pos_Lista_Etnico', 'Posição_Geral', 'Nome', 'Inscrição', 'Nota Objetiva', 'Execução Penal', 'Legislação Específica']
                st.dataframe(novos_etnico[cols_show_etnico], width="stretch", hide_index=True)
            else:
                st.info("Nenhum cotista além do 40º com a configuração atual.")

        with tab_sub3:
            st.write(f"Candidatos PCD que estavam além da 20ª colocação e agora alcançam uma das **20 Vagas Imediatas PCD**:")
            if len(novos_pcd) > 0:
                cols_show_pcd = ['Pos_Lista_PCD', 'Posição_Geral', 'Nome', 'Inscrição', 'Nota Objetiva']
                st.dataframe(novos_pcd[cols_show_pcd], width="stretch", hide_index=True)
            else:
                st.info("Nenhum candidato PCD além do 20º com a configuração atual.")

        with tab_sub4:
            st.write("Verifique a projeção de qualquer concorrente:")
            col_bs1, col_bs2 = st.columns([2, 1])
            with col_bs1:
                nome_busca_sim = st.text_input("Buscar por Nome ou Inscrição na Lista Simulada:", placeholder="Digite o nome ou número de inscrição...", key="input_busca_sim")

            if nome_busca_sim.strip():
                norm_bs = normalizar_texto(nome_busca_sim)
                if norm_bs.isdigit():
                    filtro_sim = df_simulada[df_simulada['Inscrição_Str'].str.startswith(norm_bs)]
                else:
                    filtro_sim = df_simulada[df_simulada['Nome_Busca'].str.contains(norm_bs, regex=False, na=False)]
                if len(filtro_sim) == 0:
                    st.warning("Nenhum candidato encontrado com esse termo.")
                else:
                    c_cand_sim = filtro_sim.iloc[0]
                    st.markdown(f"""
                    <div class="candidate-card" style="margin-top: 10px;">
                    <h3 style="margin: 0 0 6px 0; color: #0F172A;">{c_cand_sim['Nome']}</h3>
                    <div style="font-size: 0.9rem; color: #475569; margin-bottom: 12px;">Inscrição: <strong>{c_cand_sim['Inscrição']}</strong> | Modalidade: <strong>{c_cand_sim['Modalidade_Concorrencia']}</strong> | Nota: <strong>{c_cand_sim['Nota Objetiva']} pts</strong></div>
                    <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                        <span class="sim-gain-pill">Posição Geral: {c_cand_sim['Posição_Geral']}º</span>
                        <span class="sim-gain-pill">Status TAF Simulado: {c_cand_sim['Status_TAF_Sim']}</span>
                        <span class="sim-gain-pill">Vagas: {c_cand_sim['Vaga_Imediata_Sim']}</span>
                    </div>
                    </div>
                    """, unsafe_allow_html=True)
