from tabula import read_pdf
from datetime import datetime


Estado_Sigla = {
    "Acre": "AC",
    "Alagoas": "AL",
    "Amapá": "AP",
    "Amazonas": "AM",
    "Bahia": "BA",
    "Ceará": "CE",
    "Espírito Santo": "ES",
    "Goiás": "GO",
    "Maranhão": "MA",
    "Mato Grosso": "MT",
    "Mato Grosso do Sul": "MS",
    "Minas Gerais": "MG",
    "Pará": "PA",
    "Paraíba": "PB",
    "Paraná": "PR",
    "Pernambuco": "PE",
    "Piauí": "PI",
    "Rio de Janeiro": "RJ",
    "Rio Grande do Norte": "RN",
    "Rio Grande do Sul": "RS",
    "Rondônia": "RO",
    "Roraima": "RR",
    "Santa Catarina": "SC",
    "São Paulo": "SP",
    "Sergipe": "SE",
    "Tocantins": "TO",
    "Distrito Federal": "DF",
}

ano = datetime.today().year - 3
snis = f"http://www.snis.gov.br/downloads/diagnosticos/ae/{ano}/Diagnostico-SNIS-AE-{ano}-Capitulo-12.pdf"
df = read_pdf(
    input_path=snis,
    pages=4,
    area=[290, 80, 800, 600],
)[0]

df = df.iloc[:, 0:2]
df.set_axis(["UF", "Tarifa"], axis=1, inplace=True)
df["Tarifa"] = df["Tarifa"].apply(lambda tarifa: float(tarifa.replace(",", ".")))
df.query(
    "UF not in ['Brasil', 'Sul', 'Sudeste', 'Centro-Oeste', 'Norte', 'Nordeste']",
    inplace=True,
)
df["UF"] = df["UF"].apply(lambda uf: Estado_Sigla[uf])

print(df)
