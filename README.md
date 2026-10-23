# 🛡️ Portal de Resultados • Policial Penal RN (PPRN)

Aplicação web interativa desenvolvida em **Python** e **Streamlit** para visualização, consulta e análise estatística aprofundada dos resultados preliminares da prova objetiva do concurso de **Policial Penal do Rio Grande do Norte (PPRN)**.

---

## 🌟 Funcionalidades Principais (Atualizado em 23 de Outubro de 2026)

1. **⚡ Consulta Individual de Resultados das Bancas (23/10/2026)**:
   - Consulta instantânea por **Nome** ou **Inscrição**.
   - **Status Oficial da Banca**: `DEFERIDO` ou `INDEFERIDO` na Heteroidentificação Étnico-Racial (Pretos, Pardos, Indígenas e Quilombolas) e na Perícia Médica PCD.
   - **Nova Posição Recalculada na Cota**: Posição oficial pós-banca e cálculo exato de quantas posições o candidato avançou na fila (+XX posições ganhas).
   - **Orientações Recursais Oficiais**: Prazos de recurso (26 e 27/10/2026), orientações legais sobre o Art. 4º (Hetero) e Art. 3º (PCD) garantindo a concorrência na Ampla Concorrência, e link para o *Boletim de Análise de Reserva de Vagas* no site da banca `avalia.org.br`.

2. **🔮 Simulador de Colocações pós-Bancas e TAF**:
   - Modelagem preditiva baseada nos dados reais de 23 de outubro (3.045 indeferimentos na hetero e 186 no PCD).
   - Simulação de taxa de reversão em recursos (26 e 27/10) e taxa de reprovação no TAF.
   - Projeção de alcance para as 140 vagas da Ampla, 40 da Cota Étnica e 20 da Cota PCD.

3. **📋 As Listas Oficiais & Resultados das Bancas (Downloads Excel)**:
   - Visualização e download de 6 relações oficiais:
     - Relação Preliminar da Heteroidentificação & Análise Documental (6.309 candidatos);
     - Relação Preliminar da Perícia Médica PCD (659 candidatos);
     - Nova Lista Reclassificada da Cota Étnico-Racial (3.264 cotistas deferidos);
     - Nova Lista Reclassificada da Cota PCD (473 PCDs deferidos);
     - Lista Geral Completa com Situação Atualizada das Bancas (18.945 candidatos);
     - Lista Exclusiva de Não Cotistas (Ampla Concorrência Pura).

4. **🎯 Entenda as Regras, Recursos & Linhas de Corte do TAF**:
   - Quadro oficial detalhado com a nova linha de corte do TAF (Ampla: 119 pts | Cota Étnica: desceu de 115 para 113 pts!).
   - Explicação jurídica sobre o não cancelamento da participação dos indeferidos (migração automática para a Ampla).

5. **📅 Cronograma Oficial do Concurso Atualizado**:
   - Timeline interativa com o marco de hoje (23/10 - Resultado Preliminar) e contagem regressiva para os recursos (26 e 27/10) e resultado definitivo com corte do TAF (04/11).

---

## 💻 Como Rodar Localmente no seu Computador

### Opção 1: Pelo arquivo executável (.bat)
Dê um duplo clique no arquivo:
```
iniciar_site.bat
```

### Opção 2: Pelo Terminal / PowerShell
```bash
# 1. Instalar as dependências (caso ainda não tenha instalado)
pip install -r requirements.txt

# 2. Executar o Streamlit
python -m streamlit run app.py
```
O aplicativo abrirá automaticamente no seu navegador em: `http://localhost:8501`.

---

## ☁️ Como Hospedar Gratuitamente no Streamlit Community Cloud

O Streamlit disponibiliza hospedagem gratuita para você compartilhar o link com qualquer pessoa pela internet.

### Passo 1: Subir o projeto para o GitHub
No terminal da pasta deste projeto, rode:
```bash
git init
git add .
git commit -m "Publicação do Portal PPRN"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```
*(Substitua com o link do seu repositório criado no GitHub)*

### Passo 2: Publicar no Streamlit Cloud
1. Acesse [share.streamlit.io](https://share.streamlit.io) e entre com sua conta do GitHub.
2. Clique em **"Create app"** (ou **"New app"**).
3. Selecione o repositório criado, branch `main` e arquivo principal `app.py`.
4. Clique em **"Deploy!"**.

Seu site estará no ar em poucos segundos em um endereço do tipo:
`https://pprn-analises.streamlit.app`
