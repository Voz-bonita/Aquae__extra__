import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


CAESB = {
    "io": "https://www.caesb.df.gov.br/tarifas-e-precos.html",
    "match": "RESIDENCIAL PADRÃO",
    "skiprows": 1,
    "header": [0],
}

# df = pd.read_html(**CAESB)[0]
# print(df)

CASAN = {
    "io": "https://www.casan.com.br/menu-conteudo/index/url/residencial",
    "header": [0],
}

# print(pd.read_html(**CASAN)[0])

# CAEMA = {
#     "io": "http://gsan.caema.ma.gov.br:8080/gsan/exibirConsultarEstruturaTarifariaPortalCaemaAction.do",
#     "match": "Valor (R$)",
# }

# print(pd.read_html(**CAEMA))

CAGECE = {
    "io": "https://www.cagece.com.br/produtos-e-servicos/precos-e-prazos/estrutura-tarifaria/",
    "header": [0],
}
# print(pd.read_html(**CAGECE))

DESOSE = {"io": "https://www.deso-se.com.br/menu/quadro-tarifario"}

df = pd.read_html(**DESOSE)[0]

# df["Tarifas"] = df["Tarifas"].apply(lambda x: x[1].split("- ")[1], axis=1)
# df["Faixas de Consumo"] = df["Faixas de Consumo"].apply(lambda x: str(x[0]), axis=1)
residencial = df.loc[(df["Categorias"] == "Residencial").iloc[:, 0]]
faixas__str__ = residencial["Faixas de Consumo"].loc[0][0]
faixas = re.findall("\d+ a \d+", faixas__str__)
faixas.insert(0, f"0 a {int(faixas[0].split(' a ')[0]) - 1}")
faixas.append(f"{int(faixas[-1].split(' a ')[1]) + 1} a 9999999")
aliquota__min__ = str(df["Tarifas"].loc[0][0])
aliquota__min__ = f"{aliquota__min__[:-2]},{aliquota__min__[-2:]}"
aliquotas = df["Tarifas"].loc[0][1].split("- ")[1].replace(",", ".").split("  ")
aliquotas.insert(0, aliquota__min__)
print(faixas)
print(aliquotas)

# DF = "https://www.caesb.df.gov.br/tarifas-e-precos.html"
# SC = "https://www.casan.com.br/menu-conteudo/index/url/residencial"
# CE = (
#     "https://www.cagece.com.br/produtos-e-servicos/precos-e-prazos/estrutura-tarifaria/"
# )
# SE = "https://www.deso-se.com.br/menu/quadro-tarifario"


Campo_Grande_MS = "https://www.aguasguariroba.com.br/legislacao-e-tarifas/"
MA = "http://gsan.caema.ma.gov.br:8080/gsan/exibirConsultarEstruturaTarifariaPortalCaemaAction.do"

AL = "https://www.casal.al.gov.br/estrutura-tarifaria/"
