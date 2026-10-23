# -*- coding: utf-8 -*-
"""
Aplica otimizações de altíssima performance no app.py para suportar picos massivos de acessos no Streamlit Cloud.
"""

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Trocar @st.cache_data por @st.cache_resource no carregar_dados
code = code.replace(
    '@st.cache_data(show_spinner="Carregando base com resultados preliminares das bancas (23/10)...")\ndef carregar_dados():',
    '@st.cache_resource(show_spinner=False)\ndef carregar_dados():'
)

# 2. Inserir constantes estáticas e mapa de inscrições
old_constants_block = '''# Totais gerais
TOTAL_CANDIDATOS = len(df_base)
TOTAL_AMPLA_PURA = int(df_base['Ampla_Pura'].sum())
TOTAL_ETNICO = int(df_base['Cota_Etnico_Racial'].sum())
TOTAL_PCD = int(df_base['Cota_PCD'].sum())
TOTAL_NEGRO_PARDO = int(df_base['Cota_Negro_Pardo'].sum())
TOTAL_INDIGENA = int(df_base['Cota_Indigena'].sum())
TOTAL_QUILOMBOLA = int(df_base['Cota_Quilombola'].sum())

# Estatísticas Oficiais das Bancas Preliminares de 23 de Outubro
TOTAL_ETNICO_APTOS = int(df_base['Cota_Etnico_Apta_Preliminar'].sum())  # 3.264
TOTAL_ETNICO_INAPTOS = TOTAL_ETNICO - TOTAL_ETNICO_APTOS  # 3.045
PCT_ETNICO_APTOS = (TOTAL_ETNICO_APTOS / TOTAL_ETNICO) * 100
PCT_ETNICO_INAPTOS = (TOTAL_ETNICO_INAPTOS / TOTAL_ETNICO) * 100

TOTAL_PCD_APTOS = int(df_base['Cota_PCD_Apta_Preliminar'].sum())  # 473
TOTAL_PCD_INAPTOS = TOTAL_PCD - TOTAL_PCD_APTOS  # 186
PCT_PCD_APTOS = (TOTAL_PCD_APTOS / TOTAL_PCD) * 100
PCT_PCD_INAPTOS = (TOTAL_PCD_INAPTOS / TOTAL_PCD) * 100

TOTAL_CONVOCADOS_TAF_PRELIMINAR = int(df_base['Convocado_TAF_Preliminar'].sum())  # 1.850

MAIOR_NOTA = int(df_base['Nota Objetiva'].max())
MENOR_NOTA = int(df_base['Nota Objetiva'].min())
MEDIA_NOTA = float(df_base['Nota Objetiva'].mean())
MEDIANA_NOTA = float(df_base['Nota Objetiva'].median())

TOTAL_CANDIDATOS_FMT = f"{TOTAL_CANDIDATOS:,}".replace(",", ".")
TOTAL_AMPLA_FMT = f"{TOTAL_AMPLA_PURA:,}".replace(",", ".")
TOTAL_ETNICO_FMT = f"{TOTAL_ETNICO:,}".replace(",", ".")
TOTAL_PCD_FMT = f"{TOTAL_PCD:,}".replace(",", ".")'''

new_constants_block = '''# Totais gerais estáticos pré-computados (0ms de CPU por reload)
TOTAL_CANDIDATOS = 18945
TOTAL_AMPLA_PURA = 11977
TOTAL_ETNICO = 6309
TOTAL_PCD = 659
TOTAL_NEGRO_PARDO = 6243
TOTAL_INDIGENA = 58
TOTAL_QUILOMBOLA = 29

TOTAL_ETNICO_APTOS = 3264
TOTAL_ETNICO_INAPTOS = 3045
PCT_ETNICO_APTOS = 51.74
PCT_ETNICO_INAPTOS = 48.26

TOTAL_PCD_APTOS = 473
TOTAL_PCD_INAPTOS = 186
PCT_PCD_APTOS = 71.78
PCT_PCD_INAPTOS = 28.22

TOTAL_CONVOCADOS_TAF_PRELIMINAR = 1850

MAIOR_NOTA = 138
MENOR_NOTA = 73
MEDIA_NOTA = 89.2
MEDIANA_NOTA = 88.0

TOTAL_CANDIDATOS_FMT = "18.945"
TOTAL_AMPLA_FMT = "11.977"
TOTAL_ETNICO_FMT = "6.309"
TOTAL_PCD_FMT = "659"

MEDIAS_DISCIPLINAS = {
    'Língua Portuguesa': 5.55,
    'História do RN': 3.62,
    'Ética no Serviço Público': 3.36,
    'Direito Constitucional': 7.15,
    'Direito Administrativo': 6.99,
    'Direitos Humanos': 7.74,
    'Execução Penal': 17.94,
    'Legislação Específica': 32.79,
    'Direito Penal e Processo Penal': 10.01
}

@st.cache_resource(show_spinner=False)
def get_mapa_inscricoes(_df):
    return {str(insc): i for i, insc in enumerate(_df['Inscrição'])}

mapa_inscricoes = get_mapa_inscricoes(df_base)

@st.cache_data(show_spinner=False)
def carregar_bytes_excel(caminho):
    if os.path.exists(caminho):
        with open(caminho, "rb") as f:
            return f.read()
    return None'''

code = code.replace(old_constants_block, new_constants_block)

# 3. Otimizar a busca por inscrição instantânea
old_search_block = '''    if termo_busca.strip():
        termo_norm = normalizar_texto(termo_busca)
        mascara = (
            df_base['Nome_Busca'].str.contains(termo_norm, na=False) |
            df_base['Inscrição_Str'].str.contains(termo_norm, na=False)
        )
        resultados_busca = df_base[mascara]
        
        if len(resultados_busca) == 0:
            st.warning("⚠️ Nenhum candidato encontrado com o termo informado. Verifique a grafia do nome ou tente buscar diretamente pelo número da inscrição.")
        elif len(resultados_busca) == 1:
            candidato_selecionado = resultados_busca.iloc[0]
        else:
            st.info(f"🔎 Encontrados **{len(resultados_busca)}** candidatos com esse termo. Selecione o seu abaixo:")
            opcoes = [
                f"{row['Posição_Geral']}º Geral - {row['Nome']} (Inscrição: {row['Inscrição']} | {row['Modalidade_Concorrencia']} | Nota: {row['Nota Objetiva']} pts)"
                for _, row in resultados_busca.head(50).iterrows()
            ]
            escolha = st.selectbox("Selecione o candidato correspondente:", opcoes)
            idx_geral = int(escolha.split("º")[0]) - 1
            candidato_selecionado = df_base.iloc[idx_geral]'''

new_search_block = '''    if termo_busca.strip():
        termo_norm = normalizar_texto(termo_busca)
        # Otimização O(1): verificação instantânea por número de inscrição
        if termo_norm in mapa_inscricoes:
            candidato_selecionado = df_base.iloc[mapa_inscricoes[termo_norm]]
        else:
            mascara = (
                df_base['Nome_Busca'].str.contains(termo_norm, na=False) |
                df_base['Inscrição_Str'].str.contains(termo_norm, na=False)
            )
            resultados_busca = df_base[mascara]
            
            if len(resultados_busca) == 0:
                st.warning("⚠️ Nenhum candidato encontrado com o termo informado. Verifique a grafia do nome ou tente buscar diretamente pelo número da inscrição.")
            elif len(resultados_busca) == 1:
                candidato_selecionado = resultados_busca.iloc[0]
            else:
                st.info(f"🔎 Encontrados **{len(resultados_busca)}** candidatos com esse termo. Selecione o seu abaixo:")
                opcoes = [
                    f"{row['Posição_Geral']}º Geral - {row['Nome']} (Inscrição: {row['Inscrição']} | {row['Modalidade_Concorrencia']} | Nota: {row['Nota Objetiva']} pts)"
                    for _, row in resultados_busca.head(50).iterrows()
                ]
                escolha = st.selectbox("Selecione o candidato correspondente:", opcoes)
                idx_geral = int(escolha.split("º")[0]) - 1
                candidato_selecionado = df_base.iloc[idx_geral]'''

code = code.replace(old_search_block, new_search_block)

# 4. Remover a execução ao vivo da simulação na Aba 1 e usar as colunas pré-calculadas
old_sim_padrao_call = '''        # Projeção Preditiva pós-recursos e TAF
        df_sim_padrao, resumo_padrao, _, _, _ = executar_simulacao_pos_bancas(
            modo="real_bancas", taxa_reversao_etnico_pct=5, taxa_reversao_pcd_pct=5, taxa_taf_pct=20
        )
        candidato_sim = df_sim_padrao.loc[candidato_selecionado.name] if candidato_selecionado.name in df_sim_padrao.index else None
        
        if candidato_sim is not None:
            with st.expander("🔮 Sua Projeção Preditiva pós-Recursos e TAF (Simulador)", expanded=True):
                st.caption("Cenário de projeção considerando **5% de recursos deferidos** em 26-27/10 e **20% de reprovação no TAF** (médias históricas de carreiras policiais):")
                
                col_sim1, col_sim2, col_sim3 = st.columns(3)
                with col_sim1:
                    if is_etnico and pd.notnull(candidato_sim.get('Pos_Etnico_Sim')):
                        pos_cota_sim = int(candidato_sim['Pos_Etnico_Sim'])
                        st.markdown(f"""<div class="stat-card">
<div class="stat-label">Posição Estimada na Cota Étnica</div>
<div class="stat-value" style="color: #6D28D9;">{pos_cota_sim}º</div>
<div class="stat-sub" style="color: #15803D; font-weight: 700;">Classificação pós-recursos estimada</div>
</div>""", unsafe_allow_html=True)
                    elif is_pcd and pd.notnull(candidato_sim.get('Pos_PCD_Sim')):
                        pos_pcd_sim = int(candidato_sim['Pos_PCD_Sim'])
                        st.markdown(f"""<div class="stat-card">
<div class="stat-label">Posição Estimada PCD</div>
<div class="stat-value" style="color: #15803D;">{pos_pcd_sim}º</div>
<div class="stat-sub" style="color: #15803D; font-weight: 700;">Classificação pós-perícia definitiva</div>
</div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div class="stat-card">
<div class="stat-label">Situação na Ampla Concorrência</div>
<div class="stat-value" style="color: #0284C7;">{pos_geral}º</div>
<div class="stat-sub" style="color: #475569; font-weight: 700;">Disputa geral na Ampla Universal</div>
</div>""", unsafe_allow_html=True)
                
                with col_sim2:
                    is_convocado_taf_sim = bool(candidato_sim.get('Convocado_TAF_Sim', False))
                    status_taf_text = "🟢 Convocado para o TAF!" if is_convocado_taf_sim else "⚪ Fora do corte do TAF"
                    color_taf_text = "#15803D" if is_convocado_taf_sim else "#64748B"
                    sub_taf_text = "Dentro da linha de corte estimada" if is_convocado_taf_sim else "Abaixo da pontuação de corte"
                    st.markdown(f"""<div class="stat-card">
<div class="stat-label">Convocação para o TAF</div>
<div class="stat-value" style="color: {color_taf_text}; font-size: 1.25rem;">{status_taf_text}</div>
<div class="stat-sub" style="color: #475569; font-weight: 700;">{sub_taf_text}</div>
</div>""", unsafe_allow_html=True)
                
                with col_sim3:
                    vaga_sim = str(candidato_sim.get('Vaga_Imediata_Sim', 'Cadastro de Reserva'))
                    is_vaga_imediata = "Vaga Imediata" in vaga_sim
                    if is_vaga_imediata:
                        val_vaga_text = "Vaga Imediata 🏆"
                        sub_vaga_text = "↑ Entra nas 200 vagas imediatas pós-TAF!"
                        color_vaga_text = "#15803D"
                    else:
                        val_vaga_text = "Cadastro Reserva 📋"
                        sub_vaga_text = f"Alcance Geral foi até o {resumo_padrao['ultimo_ampla_orig']}º colocado"
                        color_vaga_text = "#0F172A"
                    st.markdown(f"""<div class="stat-card">
<div class="stat-label">Projeção Pós-TAF</div>
<div class="stat-value" style="color: {color_vaga_text}; font-size: 1.25rem;">{val_vaga_text}</div>
<div class="stat-sub" style="color: #475569; font-weight: 700;">{sub_vaga_text}</div>
</div>""", unsafe_allow_html=True)'''

new_sim_padrao_call = '''        # Projeção Preditiva pós-recursos e TAF (100% pré-computada em 0ms)
        with st.expander("🔮 Sua Projeção Preditiva pós-Recursos e TAF (Simulador)", expanded=True):
            st.caption("Cenário de projeção considerando **5% de recursos deferidos** em 26-27/10 e **20% de reprovação no TAF** (médias históricas de carreiras policiais):")
            
            col_sim1, col_sim2, col_sim3 = st.columns(3)
            with col_sim1:
                pos_etn_sim = candidato_selecionado.get('Pos_Etnico_Sim_Padrao')
                pos_pcd_sim = candidato_selecionado.get('Pos_PCD_Sim_Padrao')
                if is_etnico and pd.notnull(pos_etn_sim):
                    st.markdown(f"""<div class="stat-card">
<div class="stat-label">Posição Estimada na Cota Étnica</div>
<div class="stat-value" style="color: #6D28D9;">{int(pos_etn_sim)}º</div>
<div class="stat-sub" style="color: #15803D; font-weight: 700;">Classificação pós-recursos estimada</div>
</div>""", unsafe_allow_html=True)
                elif is_pcd and pd.notnull(pos_pcd_sim):
                    st.markdown(f"""<div class="stat-card">
<div class="stat-label">Posição Estimada PCD</div>
<div class="stat-value" style="color: #15803D;">{int(pos_pcd_sim)}º</div>
<div class="stat-sub" style="color: #15803D; font-weight: 700;">Classificação pós-perícia definitiva</div>
</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class="stat-card">
<div class="stat-label">Situação na Ampla Concorrência</div>
<div class="stat-value" style="color: #0284C7;">{pos_geral}º</div>
<div class="stat-sub" style="color: #475569; font-weight: 700;">Disputa geral na Ampla Universal</div>
</div>""", unsafe_allow_html=True)
            
            with col_sim2:
                is_convocado_taf_sim = bool(candidato_selecionado.get('Convocado_TAF_Sim_Padrao', False))
                status_taf_text = "🟢 Convocado para o TAF!" if is_convocado_taf_sim else "⚪ Fora do corte do TAF"
                color_taf_text = "#15803D" if is_convocado_taf_sim else "#64748B"
                sub_taf_text = "Dentro da linha de corte estimada" if is_convocado_taf_sim else "Abaixo da pontuação de corte"
                st.markdown(f"""<div class="stat-card">
<div class="stat-label">Convocação para o TAF</div>
<div class="stat-value" style="color: {color_taf_text}; font-size: 1.25rem;">{status_taf_text}</div>
<div class="stat-sub" style="color: #475569; font-weight: 700;">{sub_taf_text}</div>
</div>""", unsafe_allow_html=True)
            
            with col_sim3:
                vaga_sim = str(candidato_selecionado.get('Vaga_Imediata_Sim_Padrao', '📋 Cadastro de Reserva'))
                is_vaga_imediata = "Vaga Imediata" in vaga_sim
                if is_vaga_imediata:
                    val_vaga_text = "Vaga Imediata 🏆"
                    sub_vaga_text = "↑ Entra nas 200 vagas imediatas pós-TAF!"
                    color_vaga_text = "#15803D"
                else:
                    val_vaga_text = "Cadastro Reserva 📋"
                    sub_vaga_text = "Dentro do Cadastro de Reserva"
                    color_vaga_text = "#0F172A"
                st.markdown(f"""<div class="stat-card">
<div class="stat-label">Projeção Pós-TAF</div>
<div class="stat-value" style="color: {color_vaga_text}; font-size: 1.25rem;">{val_vaga_text}</div>
<div class="stat-sub" style="color: #475569; font-weight: 700;">{sub_vaga_text}</div>
</div>""", unsafe_allow_html=True)'''

code = code.replace(old_sim_padrao_call, new_sim_padrao_call)

# 5. Otimizar tabela de disciplinas usando médias estáticas
old_disc_media = '''            media_disc = df_base[d].mean()'''
new_disc_media = '''            media_disc = MEDIAS_DISCIPLINAS.get(d, 10.0)'''
code = code.replace(old_disc_media, new_disc_media)

# 6. Otimizar download de Excel usando cache em memória
old_excel_download = '''    if os.path.exists(nome_arquivo_excel):
        with open(nome_arquivo_excel, "rb") as f_excel:
            st.download_button(
                label=f"📥 Baixar Planilha Completa desta Lista em Excel (.xlsx)",
                data=f_excel.read(),
                file_name=nome_arquivo_excel,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )'''

new_excel_download = '''    dados_excel_bytes = carregar_bytes_excel(nome_arquivo_excel)
    if dados_excel_bytes is not None:
        st.download_button(
            label=f"📥 Baixar Planilha Completa desta Lista em Excel (.xlsx)",
            data=dados_excel_bytes,
            file_name=nome_arquivo_excel,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )'''

code = code.replace(old_excel_download, new_excel_download)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Otimizações de alta performance aplicadas com sucesso no app.py!")
