import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Dados fornecidos
data = {
    "raca_cor": [1, 2, 4, 6, 8, 9],
    "vinculos": [16418, 7307361, 704445, 65366, 2206104, 8660960],
    "masculino": [8782, 3966066, 405491, 36821, 1221966, 5300374],
    "feminino": [7636, 3341295, 298954, 28545, 984138, 3360586],
    "nao_identificado": [0, 0, 0, 0, 0, 5]
}

df = pd.DataFrame(data)

# Agrupar por raça
df_grouped = df.groupby("raca_cor").sum().reset_index()

# Mapeamento dos códigos de raça
map_raca = {
    1: "Indígena",
    2: "Branca",
    4: "Preta",
    6: "Amarela",
    8: "Parda",
    9: "Não Informado"
}

df_grouped["raca_desc"] = df_grouped["raca_cor"].map(map_raca)

# Ordenar do maior para o menor
df_grouped = df_grouped.sort_values(by="vinculos", ascending=False).reset_index(drop=True)

# Cálculo do total geral
total_geral = df_grouped["vinculos"].sum()

# Percentual
df_grouped["pct"] = (df_grouped["vinculos"] / total_geral * 100).round(1)

# Plotar gráfico empilhado
plt.figure(figsize=(8, 6))

plt.bar(df_grouped["raca_desc"], df_grouped["masculino"], 
        label="Masculino", color="#F28E2B")

plt.bar(df_grouped["raca_desc"], df_grouped["feminino"], 
        bottom=df_grouped["masculino"], 
        label="Feminino", color="#1F77B4")

# Adicionar percentuais
for idx, row in df_grouped.iterrows():
    total = row["masculino"] + row["feminino"]
    plt.text(
        idx,
        total + (total * 0.01),
        f'{row["pct"]}%',
        ha='center',
        va='bottom',
        fontsize=10   # <<< sem negrito
    )

# Títulos
plt.title("Vínculos por Raça/Cor e Sexo (Empilhado)")
plt.xlabel("Raça/Cor")
plt.ylabel("Quantidade de Vínculos")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
