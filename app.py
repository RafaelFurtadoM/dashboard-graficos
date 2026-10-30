# Atividade de Fixação 07 - Dashboard com Streamlit
# Peguei os 9 gráficos que fiz na atividade 06 (graficos-dados) e juntei tudo num dashboard só.
# Os CSVs são os mesmos da atv 06, estão na pasta dados/
# pra rodar: streamlit run app.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Dashboard - Atv 07", page_icon="📊", layout="wide",
                   initial_sidebar_state="expanded")

# ---------------- meus dados ----------------
NOME = "Rafael Furtado Magalhães"
NUMERO_CHAMADA = 48
TURMA = "3D1"

PASTA_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados")
CORES = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3"]


@st.cache_data
def ler(nome_arquivo, **kwargs):
    return pd.read_csv(os.path.join(PASTA_DADOS, nome_arquivo), **kwargs)


def novo_grafico():
    # deixei todos do mesmo tamanho pra ficarem alinhados nas colunas
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.spines[["top", "right"]].set_visible(False)
    return fig, ax


def mostrar(fig, analise):
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.markdown(f"**Análise:** {analise}")


# ---------------- sidebar ----------------
# dá pra recolher na setinha do canto de cima
with st.sidebar:
    st.title("👤 Aluno")
    st.write(f"**Nome:** {NOME}")
    st.write(f"**Nº da chamada:** {NUMERO_CHAMADA}")
    st.write(f"**Turma:** {TURMA}")
    st.divider()
    st.caption("Disciplina: Python")
    st.caption("Prof. Rubens Lemos da Cruz Junior")
    st.caption("Atividade de Fixação 07")

# ---------------- leitura dos dados ----------------
df_barras = ler("dados_barras.csv")
df_box = ler("dados_boxplot.csv")
df_disp = ler("dados_dispersao.csv")
df_idade = ler("dados_distribuicao.csv")
df_freq = ler("dados_frequencia.csv")
df_linhas = ler("dados_linhas.csv", parse_dates=["data"]).sort_values("data")
df_pizza = ler("dados_pizza.csv").sort_values("faturamento", ascending=False)
df_reg = ler("dados_regressao.csv")
df_heat = ler("dados_heatmap.csv")

# ---------------- topo ----------------
st.title("📊 Dashboard - Gráficos da Atividade 06")
st.write("Juntei aqui os 9 gráficos que fiz na atividade 06, separados de três em três. "
         "Embaixo de cada um coloquei o que eu consegui tirar dos dados.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Faturamento total (canais)", f"R$ {df_pizza['faturamento'].sum():,.0f}".replace(",", "."))
c2.metric("Idade média dos clientes", f"{df_idade['idade'].mean():.1f} anos")
c3.metric("Chamados registrados", len(df_freq))
c4.metric("Salário mediano geral", f"R$ {df_box['salario'].median():,.0f}".replace(",", "."))

st.divider()

# ===================== LINHA 1 - VENDAS =====================
st.subheader("🛒 Vendas")
col1, col2, col3 = st.columns(3)

with col1:
    pivot = df_barras.pivot(index="categoria", columns="regiao", values="vendas_medias")
    pivot = pivot[[r for r in ["Norte", "Sul", "Leste", "Oeste"] if r in pivot.columns]]
    x = np.arange(len(pivot.index))
    largura = 0.8 / len(pivot.columns)

    fig, ax = novo_grafico()
    for i, regiao in enumerate(pivot.columns):
        desloc = (i - (len(pivot.columns) - 1) / 2) * largura
        ax.bar(x + desloc, pivot[regiao], largura, label=regiao, color=CORES[i])
    ax.set_title("Vendas médias por categoria e região", fontweight="bold")
    ax.set_ylabel("Vendas médias (R$)")
    ax.set_xticks(x)
    ax.set_xticklabels(pivot.index, rotation=20, fontsize=8)
    ax.legend(title="Região", fontsize=7, title_fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    mostrar(fig, "O Oeste é a região que mais vende na maioria das categorias, com destaque "
                 "para Livros e Brinquedos (passando de R$ 280). A exceção são os Eletrônicos, "
                 "que vendem melhor no Leste. O Norte é o mais fraco em Alimentos e Livros.")

with col2:
    fig, ax = novo_grafico()
    for i, (loja, grupo) in enumerate(df_linhas.groupby("loja")):
        ax.plot(grupo["data"], grupo["vendas"], label=loja, color=CORES[i],
                linewidth=1.5, marker="o", markersize=2)
    ax.set_title("Evolução das vendas diárias por loja", fontweight="bold")
    ax.set_ylabel("Vendas (R$)")
    ax.legend(title="Loja", fontsize=7, title_fontsize=8)
    ax.grid(linestyle="--", alpha=0.4)
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%d/%m"))
    fig.autofmt_xdate(rotation=45)
    mostrar(fig, "As duas lojas cresceram bastante de janeiro a março: a média diária saiu "
                 "de uns R$ 113 na primeira semana pra quase R$ 240 na última. Elas andam "
                 "praticamente juntas, mas no total do trimestre a Loja B vendeu um pouco mais.")

with col3:
    fig, ax = novo_grafico()
    explode = [0.05] + [0] * (len(df_pizza) - 1)  # destaca a maior fatia
    _, _, autotextos = ax.pie(df_pizza["faturamento"], labels=df_pizza["canal_venda"],
                              autopct="%1.1f%%", startangle=90, counterclock=False,
                              colors=CORES[:len(df_pizza)], explode=explode,
                              wedgeprops=dict(edgecolor="white", linewidth=2),
                              textprops=dict(fontsize=8))
    for t in autotextos:
        t.set_color("white")
        t.set_fontweight("bold")
    ax.set_title("Faturamento por canal de venda", fontweight="bold")
    ax.axis("equal")
    mostrar(fig, "O site sozinho traz 37,5% do faturamento, mais que a loja física (26,7%). "
                 "Somando site e aplicativo, o online passa da metade. O telefone quase "
                 "não pesa mais (6,7%).")

st.divider()

# ===================== LINHA 2 - CLIENTES =====================
st.subheader("👥 Clientes e atendimento")
col1, col2, col3 = st.columns(3)

with col1:
    idades = df_idade["idade"]
    fig, ax = novo_grafico()
    ax.hist(idades, bins=15, color=CORES[0], edgecolor="white", alpha=0.85)
    ax.axvline(idades.mean(), color=CORES[3], linestyle="--", linewidth=2,
               label=f"Média = {idades.mean():.1f} anos")
    ax.set_title("Distribuição de idades dos clientes", fontweight="bold")
    ax.set_xlabel("Idade (anos)")
    ax.set_ylabel("Nº de clientes")
    ax.legend(fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    mostrar(fig, "O público é bem jovem: quase metade dos clientes (94 de 200) tem entre 21 e "
                 "30 anos. Tem um segundo grupinho entre 40 e 50, e quase ninguém acima de 60. "
                 "A média deu 33,6 anos.")

with col2:
    ordem_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    horarios = sorted(df_heat["horario"].unique())
    matriz = (df_heat.pivot(index="dia_semana", columns="horario", values="movimento_clientes")
              .reindex(index=ordem_dias, columns=horarios).values)

    fig, ax = novo_grafico()
    im = ax.imshow(matriz, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(horarios)))
    ax.set_xticklabels(horarios, fontsize=8)
    ax.set_yticks(range(len(ordem_dias)))
    ax.set_yticklabels(ordem_dias, fontsize=8)
    limite = np.nanmax(matriz) * 0.6
    for i in range(len(ordem_dias)):
        for j in range(len(horarios)):
            v = matriz[i, j]
            ax.text(j, i, int(v), ha="center", va="center", fontsize=7,
                    color="white" if v > limite else "black")
    fig.colorbar(im, ax=ax)
    ax.set_title("Movimento por dia e horário", fontweight="bold")
    mostrar(fig, "Fim de semana é disparado o mais movimentado: domingo e sábado têm bem "
                 "mais movimento que qualquer dia útil. O pico é domingo ao meio-dia (199). Quinta é o "
                 "dia mais parado, só melhora às 20h.")

with col3:
    freq = df_freq["tipo_atendimento"].value_counts().sort_values()
    fig, ax = novo_grafico()
    barras = ax.barh(freq.index, freq.values, color=CORES[2], alpha=0.9)
    for barra, valor in zip(barras, freq.values):
        ax.text(valor + 1, barra.get_y() + barra.get_height() / 2, str(valor),
                va="center", fontsize=8)
    ax.set_title("Chamados por tipo de atendimento", fontweight="bold")
    ax.set_xlabel("Quantidade")
    ax.set_xlim(0, freq.max() * 1.12)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    mostrar(fig, "Dúvida é o motivo nº 1, com 116 dos 300 chamados (uns 39%). Isso mostra que "
                 "um FAQ melhor já ia aliviar bastante o atendimento. Reclamação vem em segundo "
                 "e elogio é o que menos aparece.")

st.divider()

# ===================== LINHA 3 - RELAÇÕES E COMPARAÇÕES =====================
st.subheader("📐 Relações e comparações")
col1, col2, col3 = st.columns(3)

with col1:
    cores_sexo = {"Masculino": CORES[0], "Feminino": CORES[3]}
    fig, ax = novo_grafico()
    for sexo, grupo in df_disp.groupby("sexo"):
        ax.scatter(grupo["altura_cm"], grupo["peso_kg"], label=sexo, s=25,
                   color=cores_sexo.get(sexo, "#888888"), alpha=0.7, edgecolor="white")
    ax.set_title("Altura x peso por sexo", fontweight="bold")
    ax.set_xlabel("Altura (cm)")
    ax.set_ylabel("Peso (kg)")
    ax.legend(title="Sexo", fontsize=7, title_fontsize=8)
    ax.grid(linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    mostrar(fig, "Quanto mais alta a pessoa, mais pesada ela tende a ser: a correlação deu "
                 "0,85, que é forte. Uma coisa que me surpreendeu é que homens e mulheres ficaram "
                 "misturados, com médias quase iguais (~170 cm e ~63 kg).")

with col2:
    x = df_reg["renda_mensal"].values
    y = df_reg["gasto_mensal"].values
    a, b = np.polyfit(x, y, 1)
    r2 = 1 - np.sum((y - (a * x + b)) ** 2) / np.sum((y - y.mean()) ** 2)
    x_linha = np.linspace(x.min(), x.max(), 100)

    fig, ax = novo_grafico()
    ax.scatter(x, y, color=CORES[0], alpha=0.6, edgecolor="white", s=25, label="Observações")
    ax.plot(x_linha, a * x_linha + b, color=CORES[3], linewidth=2.5,
            label=f"y = {a:.3f}x + {b:.1f}\nR² = {r2:.3f}")
    ax.set_title("Regressão: gasto x renda", fontweight="bold")
    ax.set_xlabel("Renda mensal (R$)")
    ax.set_ylabel("Gasto mensal (R$)")
    ax.legend(loc="upper left", fontsize=7)
    ax.grid(linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    mostrar(fig, "A reta encaixou muito bem nos pontos (R² de 0,98). Pela equação, a cada "
                 "R$ 100 a mais de renda a pessoa gasta uns R$ 57 a mais. Ou seja, renda "
                 "explica quase todo o gasto mensal nesses dados.")

with col3:
    ordem = df_box.groupby("departamento")["salario"].median().sort_values().index.tolist()
    dados = [df_box.loc[df_box["departamento"] == d, "salario"] for d in ordem]
    fig, ax = novo_grafico()
    bp = ax.boxplot(dados, tick_labels=ordem, patch_artist=True, showmeans=True,
                    medianprops=dict(color=CORES[3], linewidth=2),
                    meanprops=dict(marker="D", markerfacecolor="white",
                                   markeredgecolor="black", markersize=5),
                    flierprops=dict(marker="o", markerfacecolor="#888888",
                                    markersize=4, alpha=0.6))
    for patch, cor in zip(bp["boxes"], [CORES[0], CORES[2], CORES[1], CORES[4]]):
        patch.set_facecolor(cor)
        patch.set_alpha(0.7)
    ax.set_title("Salários por departamento", fontweight="bold")
    ax.set_ylabel("Salário (R$)")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    mostrar(fig, "TI e Vendas pagam bem mais que RH e Marketing (mediana perto de R$ 7 mil "
                 "contra uns R$ 4,2 mil). Os pontinhos lá em cima são outliers: tem salário "
                 "de R$ 21 mil em TI e Vendas, o que puxa a média pra cima.")

st.divider()
st.caption(f"Feito por {NOME} - {TURMA} • Atividade de Fixação 07 • dados da Atividade 06")
