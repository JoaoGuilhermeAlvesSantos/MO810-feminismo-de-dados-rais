import pandas as pd

# -----------------------------
# 1. Carregar arquivos (sempre como string)
# -----------------------------
dict_ocp = pd.read_csv("dict_sinonimos.csv", dtype={"cbo_2002": str})
regs_count = pd.read_csv("regs_count.csv", dtype={"cbo_2002": str})

dict_ocp["cbo_2002"] = dict_ocp["cbo_2002"].str.zfill(6)
regs_count["cbo_2002"] = regs_count["cbo_2002"].str.zfill(6)

# -----------------------------
# 2. Preparar dicionário único
# -----------------------------
dict_ocp = dict_ocp.sort_values(["cbo_2002", "descricao_atividade"])
dict_unique = dict_ocp.groupby("cbo_2002", as_index=False).first()

# -----------------------------
# 3. Merge inicial
# -----------------------------
merged = regs_count.merge(
    dict_unique[["cbo_2002", "descricao_atividade"]],
    on="cbo_2002",
    how="left"
)

# -----------------------------
# 4. Fallback para CBOs sem descrição
# -----------------------------
merged["prefix4"] = merged["cbo_2002"].str[:4]
dict_unique["prefix4"] = dict_unique["cbo_2002"].str[:4]

missing_mask = merged["descricao_atividade"].isna() | (merged["descricao_atividade"] == "")

def buscar_mais_proximo(cbo, prefix, tabela):
    candidatos = tabela[tabela["prefix4"] == prefix].copy()
    if candidatos.empty:
        return None
    candidatos["dist"] = (candidatos["cbo_2002"].astype(int) - int(cbo)).abs()
    linha = candidatos.sort_values("dist").iloc[0]
    return linha["descricao_atividade"]

merged.loc[missing_mask, "descricao_atividade"] = merged[missing_mask].apply(
    lambda row: buscar_mais_proximo(row["cbo_2002"], row["prefix4"], dict_unique),
    axis=1
)

# -----------------------------
# 5. (NOVO) Fazer merge final com dict_ocp e somar os duplicados
# -----------------------------
merged_final = merged.merge(
    dict_unique[["cbo_2002", "descricao_atividade"]],
    on="cbo_2002",
    how="left",
    suffixes=("", "_dict")
)

# Caso o fallback tenha preenchido descrição, manter a correta:
merged_final["descricao_atividade"] = merged_final["descricao_atividade"].fillna(
    merged_final["descricao_atividade_dict"]
)
merged_final = merged_final.drop(columns=["descricao_atividade_dict"])

# -----------------------------
# 6. Agrupar por CBO e somar registros
# -----------------------------
cols_numericas = merged_final.select_dtypes(include="number").columns.tolist()

merged_final = merged_final.groupby(["cbo_2002", "descricao_atividade"], as_index=False)[cols_numericas].sum()

# sortear por total_registros decrescente
merged_final = merged_final.sort_values(by="total_registros", ascending=False).reset_index(drop=True)
# -----------------------------
# 7. Salvar arquivo final
# -----------------------------
merged_final.to_csv("regs_counts_with_desc.csv", index=False)

print("Arquivo regs_counts_with_desc.csv criado com sucesso (com fallback e soma de duplicados)!")
