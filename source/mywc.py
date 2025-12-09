import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Carregar
df = pd.read_csv("regs_counts_with_desc.csv")

# Remover descrições vazias
df["descricao_atividade"] = df["descricao_atividade"].astype(str).str.strip()

# Construção do dicionário de frequências
if "total_registros" in df.columns:
    freqs = df.groupby("descricao_atividade", as_index=False)["total_registros"].sum()
    freqs = dict(zip(freqs["descricao_atividade"], freqs["total_registros"]))
else:
    freqs = df["descricao_atividade"].value_counts().to_dict()

# Gerar WordCloud de alta qualidade para apresentação
wc = WordCloud(
    width=3000,         # muito maior que o padrão
    height=2000,        # garante nitidez no slide
    background_color="white",
    collocations=False,
    prefer_horizontal=0.9,
    max_words=500,      # ajustável
).generate_from_frequencies(freqs)

# Plotar
plt.figure(figsize=(14, 9), dpi=300)  # proporção perfeita para slides 16:9
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")

# Salvar com resolução altíssima
plt.savefig(
    "wordcloud_profissoes_hd.png",
    dpi=600,             # DPI altíssimo → perfeito para projeção
    bbox_inches="tight",
    pad_inches=0
)

plt.show()
