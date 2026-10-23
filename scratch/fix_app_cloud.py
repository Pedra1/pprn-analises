# -*- coding: utf-8 -*-
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Substituir use_container_width=True por width="stretch"
content_fixed = content.replace("use_container_width=True", 'width="stretch"')

# 2. Corrigir o bloco do modal / dialog para não auto-executar e causar loop no healthz
old_modal_trigger = '''if "disclaimer_visto" not in st.session_state:
    st.session_state["disclaimer_visto"] = False

if not st.session_state["disclaimer_visto"]:
    st.session_state["disclaimer_visto"] = True
    modal_aviso_legal()'''

new_modal_trigger = '''# O modal pode ser aberto manualmente pelo usuário sem travar o health check do Streamlit Cloud'''

if old_modal_trigger in content_fixed:
    content_fixed = content_fixed.replace(old_modal_trigger, new_modal_trigger)
    print("Auto-trigger do modal removido com sucesso!")
else:
    print("Aviso: old_modal_trigger não encontrado exatamente, verificando regex...")
    # Tenta com regex
    content_fixed = re.sub(
        r'if "disclaimer_visto" not in st\.session_state:.*?modal_aviso_legal\(\)',
        '# Modal acionado sob demanda\n',
        content_fixed,
        flags=re.DOTALL
    )

# 3. Adicionar botão e banner do aviso no Header Hero para que o usuário ainda possa abrir o modal quando quiser
old_hero_badge = '''<span class="badge-pill-amber">⚡ ATUALIZAÇÃO 23 DE OUTUBRO DE 2026 • RESULTADO PRELIMINAR DAS BANCAS</span>
<span style="font-size: 0.82rem; font-weight: 800; color: #0284C7; letter-spacing: 0.05em; text-transform: uppercase;">GOVERNO DO ESTADO DO RIO GRANDE DO NORTE • SEAD / SEAP</span>
</div>
<h1 class="hero-title">Portal de Resultados • Concurso Policial Penal RN</h1>
<p class="hero-subtitle">
Boletim do candidato com resultado oficial preliminar da <strong>Heteroidentificação Étnico-Racial</strong> e da <strong>Perícia Médica PCD</strong>, orientações recursais (26 e 27/10) e avanço na reclassificação das cotas.
</p>
</div>""", unsafe_allow_html=True)'''

new_hero_badge = '''<span class="badge-pill-amber">⚡ ATUALIZAÇÃO 23 DE OUTUBRO DE 2026 • RESULTADO PRELIMINAR DAS BANCAS</span>
<span style="font-size: 0.82rem; font-weight: 800; color: #0284C7; letter-spacing: 0.05em; text-transform: uppercase;">GOVERNO DO ESTADO DO RIO GRANDE DO NORTE • SEAD / SEAP</span>
</div>
<h1 class="hero-title">Portal de Resultados • Concurso Policial Penal RN</h1>
<p class="hero-subtitle">
Boletim do candidato com resultado oficial preliminar da <strong>Heteroidentificação Étnico-Racial</strong> e da <strong>Perícia Médica PCD</strong>, orientações recursais (26 e 27/10) e avanço na reclassificação das cotas.
</p>
<div style="background: #FFFDF5; border: 1.5px solid #FCD34D; border-left: 5px solid #D97706; border-radius: 8px; padding: 10px 14px; margin-top: 14px; font-size: 0.88rem; color: #1E293B; line-height: 1.5;">
    ⚖️ <strong>Informação Importante aos Convocados:</strong> Candidatos indeferidos na cota <strong>não estão eliminados</strong> do concurso (Art. 4º Hetero / Art. 3º PCD) e continuam na <strong>Ampla Concorrência</strong>. Prazo para recursos: <strong>26 e 27 de outubro</strong> no site <a href="https://www.avalia.org.br" target="_blank" style="color: #0284C7; font-weight: 700;">avalia.org.br</a>.
</div>
</div>""", unsafe_allow_html=True)'''

content_fixed = content_fixed.replace(old_hero_badge, new_hero_badge)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content_fixed)

print("app.py atualizado com sucesso!")
