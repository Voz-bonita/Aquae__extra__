import pandas as pd
import copy
import json
import os


def get_mm(mm):
    mm = str(mm)
    mm = mm.replace(",", ".")
    if not mm or "-" in mm:
        mm = 0.0
    return float(mm)


estados = [
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
]
dados = {uf: {} for uf in estados}
estacao_typos = {"BEBDOURO": "BEBEDOURO"}

DIR = "./Coleta_de_pluviometria/CSVs"
files = os.listdir(DIR)
for file in files:
    path = f"{DIR}/{file}"

    info = file.split("_")
    uf = info[2]
    estacao = info[4]

    if estacao in estacao_typos:
        estacao = estacao_typos[estacao]

    tabela = pd.read_csv(path, sep=";", skiprows=8, encoding="latin1")
    tabela = tabela.iloc[:, [0, 2]]

    tabela.set_axis(["Data", "Precipitacao"], axis="columns", inplace=True)
    tabela["Precipitacao"] = tabela["Precipitacao"].apply(get_mm)

    ano = tabela["Data"][0][:4]
    print(uf, estacao, ano)

    mensal = {}
    for mes in range(1, 13):
        mes = str(mes).zfill(2)
        tabela_mes = tabela[
            list(
                map(
                    lambda x: x.startswith(f"{ano}-{mes}")
                    or x.startswith(f"{ano}/{mes}"),
                    tabela.Data,
                )
            )
        ]
        total = tabela_mes["Precipitacao"].sum()
        mensal[mes] = round(total, 2)

    if estacao not in dados[uf]:
        dados[uf][estacao] = {}
    dados[uf][estacao][ano] = mensal


dados_clean = copy.deepcopy(dados)
for estado in dados:
    for estacao in dados[estado]:
        meses = [[] for _ in range(12)]
        for ano in dados[estado][estacao]:
            for i in range(12):
                pluv_i = dados[estado][estacao][ano][str(i + 1).zfill(2)]
                if pluv_i != 0:
                    meses[i].append(pluv_i)

        # pelo menos 3 observacoes em cada mes
        min3 = list(map(lambda x: len(x) >= 3, meses))
        if False in min3:
            dados_clean[estado].pop(estacao)


with open("./Coleta_de_pluviometria/Pluviometria_Brasil.json", "w") as file:
    json.dump(dados_clean, file)
