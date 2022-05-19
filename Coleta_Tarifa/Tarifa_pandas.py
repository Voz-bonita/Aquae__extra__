import pandas as pd


CAESB = {
    "io": "https://www.caesb.df.gov.br/tarifas-e-precos.html",
    "match": "RESIDENCIAL PADRÃO",
    "skiprows": 1,
}

df = pd.read_html(**CAESB)
print(df[0])
