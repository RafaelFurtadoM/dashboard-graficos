# Dashboard de Gráficos - Atividade de Fixação 07

Dashboard feito com **Streamlit** juntando os 9 gráficos da [atividade 06](https://github.com/RafaelFurtadoM/graficos-dados).

- **Aluno:** Rafael Furtado Magalhães
- **Nº da chamada:** 48
- **Turma:** 3D1
- **Disciplina:** Python

## O que tem no dashboard

- Sidebar (dá pra recolher) com meu nome, número da chamada e turma
- Os 9 gráficos organizados de três em três:
  - **Vendas:** barras agrupadas, linhas e pizza
  - **Clientes e atendimento:** histograma de idades, heatmap e frequência de chamados
  - **Relações e comparações:** dispersão, regressão linear e boxplot
- Embaixo de cada gráfico uma análise curta do que os dados mostram

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

Os CSVs ficam na pasta `dados/` (são os mesmos da atividade 06).
