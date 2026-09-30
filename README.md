# 🛡️ Portal de Resultados • Policial Penal RN (PPRN)

Aplicação web interativa desenvolvida em **Python** e **Streamlit** para visualização, consulta e análise estatística aprofundada dos resultados preliminares da prova objetiva do concurso de **Policial Penal do Rio Grande do Norte (PPRN)**.

---

## 🌟 Funcionalidades Principais

1. **🔍 Consulta Individual (Boletim do Candidato)**:
   - Busca instantânea por **Nome** (com busca parcial, insensível a acentos e maiúsculas) ou por **Inscrição**.
   - Cartão com posição exata no concurso (ex: *1º Lugar*, *Top 0.5%*).
   - Métricas comparativas (distância da média geral e do primeiro colocado).
   - **Gráfico Radar (Spider Chart)** comparando notas do candidato com a média dos 18.944 candidatos.
   - **Gráfico de Aproveitamento (%)** em cada uma das 9 disciplinas.
   - Tabela detalhada de pontos e vizinhança de classificação (+/- 5 concorrentes ao redor).

2. **🏆 Classificação Geral Oficial**:
   - Tabela completa e interativa com os 18.944 candidatos.
   - Filtros por pontuação mínima e máxima (Slider).
   - Filtro de grupos rápidos (Top 50, Top 100, Top 500, etc.).
   - Ordenação personalizada por qualquer coluna.
   - **Exportação dos dados filtrados para CSV** (compatível com Excel com acentuação).

3. **📊 Raio-X & Inteligência Estatística**:
   - Histograma de distribuição de notas com linhas de corte e percentis (P90, P99, Média, Mediana).
   - Análise de dificuldade das disciplinas (% médio de acertos por matéria).
   - Tabela de marcas de corte histórico (Top 10, 50, 100, 500, 1.000, 5.000).

4. **🎯 Simulador de Vagas e Linha de Corte**:
   - Simulação instantânea de nota de corte para qualquer número de vagas (ex: 200, 500, 1.000 vagas).
   - Identificação de candidatos empatados na nota de corte.
   - Lista filtrada dos convocados.

5. **⚔️ Comparador Direto de Candidatos**:
   - Confronto direto entre quaisquer 2 candidatos.
   - Gráfico de barras agrupadas matéria a matéria.
   - Tabela de vantagens por disciplina.

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
