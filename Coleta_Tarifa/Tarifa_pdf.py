from tabula import read_pdf

dfs = read_pdf(
    "https://www.cesama.com.br/ckfinder/files/RESOLU%C3%87%C3%83O%20DE%20FISCALIZA%C3%87%C3%83O%20E%20REGULA%C3%87%C3%83O%20%E2%80%93%20ARISB-MG%20N%C2%BA%20187.pdf",
    pages=3,
)

df = dfs[0]
df.drop([*range(5), *range(11, 19)], axis=0, inplace=True)
df.set_axis(["Faixa", "Residencial 1", "Residencial 2"], axis=1, inplace=True)
df["Residencial 1"] = df["Residencial 1"].apply(lambda x: x.split()[1])

print(df)
