import enum
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


def build_mocks(faixas, aliquotas):
    mock = []

    for faixa, aliquota in zip(faixas, aliquotas):
        mn, mx = faixa.split(" a ")
        mock.append({"min": mn, "max": mx, "tarifa": round(float(aliquota), 2)})

    return mock


def tarifa_DF():
    CAESB = {
        "io": "https://www.caesb.df.gov.br/tarifas-e-precos.html",
        "match": "RESIDENCIAL PADRÃO",
        "skiprows": 1,
        "header": [0],
        "thousands": ".",
        "decimal": ",",
    }

    df = pd.read_html(**CAESB)[0]
    df.drop(len(df) - 1, inplace=True)
    faixas = list(df["Faixa m³.1"])
    faixas[-1] = f"{faixas[-1][-2:]} a 9999999"
    aliquotas = list(df["Alíquota (R$)  Preço p/ m³"])
    return build_mocks(faixas=faixas, aliquotas=aliquotas)


def tarifa_SC():
    CASAN = {
        "io": "https://www.casan.com.br/menu-conteudo/index/url/residencial",
        "header": [0],
    }

    df = pd.read_html(**CASAN)[0]
    df = df[1:]
    faixas = list(df["Volumes (m³)"])
    faixas[0] = f"0 a {faixas[0].split(' a ')[1]}"
    aliquotas = list(
        df["Água (R$)"].apply(lambda x: x.replace("R$ ", "").replace(",", "."))
    )
    return build_mocks(faixas=faixas, aliquotas=aliquotas)


def tarifa_MA():
    CAEMA = {
        "io": "http://gsan.caema.ma.gov.br:8080/gsan/exibirConsultarEstruturaTarifariaPortalCaemaAction.do",
        "thousands": ".",
        "decimal": ",",
    }

    # indice 1 já representa o residencial normal
    df = pd.read_html(**CAEMA)[1]
    df["Faixa de Consumo (m³/Eco/mês)"] = df["Faixa de Consumo (m³/Eco/mês)"].apply(
        lambda x: x.replace("até ", "")
        .replace("excedente de ", "")
        .replace("m³", "")
        .replace("-", "a")
    )
    faixas = list(df["Faixa de Consumo (m³/Eco/mês)"])
    faixas[0] = f"0 a {int(faixas[0]) - 1}"
    faixas[-1] = f"{int(faixas[-1]) + 1} a 999999"
    aliquotas = list(df["Valor (R$)"])

    return build_mocks(faixas=faixas, aliquotas=aliquotas)


def tarifa_CE():
    CAGECE = {
        "io": "https://www.cagece.com.br/produtos-e-servicos/precos-e-prazos/estrutura-tarifaria/",
        "header": [0],
    }

    df = pd.read_html(**CAGECE)[0]
    df["Categoria"] = df["Categoria"].apply(lambda x: x.split("Demanda")[0])
    residencial = df[df["Categoria"] == "Residencial Normal"]
    faixas = list(residencial["Faixa de Consumo (m³)"])[0]
    faixas = re.findall("\d+ a \d+", faixas)
    faixas.append(f"{int(faixas[-1][-2:]) + 1} a 999999")
    aliquotas = list(residencial["Tarifa Água(R$/m³)"])[0]
    aliquotas = aliquotas.replace(",", ".").split()

    return build_mocks(faixas=faixas, aliquotas=aliquotas)


def tarifa_SE():
    DESOSE = {"io": "https://www.deso-se.com.br/menu/quadro-tarifario"}

    df = pd.read_html(**DESOSE)[0]

    residencial = df.loc[(df["Categorias"] == "Residencial").iloc[:, 0]]
    faixas__str__ = residencial["Faixas de Consumo"].loc[0][0]
    faixas = re.findall("\d+ a \d+", faixas__str__)
    faixas.insert(0, f"0 a {int(faixas[0].split(' a ')[0]) - 1}")
    faixas.append(f"{int(faixas[-1].split(' a ')[1]) + 1} a 9999999")
    aliquota__min__ = str(df["Tarifas"].loc[0][0])
    aliquota__min__ = float(f"{aliquota__min__[:-2]}.{aliquota__min__[-2:]}") / float(
        faixas[0].split(" a ")[1]
    )
    aliquotas = df["Tarifas"].loc[0][1].split("- ")[1].replace(",", ".").split("  ")
    aliquotas.insert(0, aliquota__min__)
    return build_mocks(faixas=faixas, aliquotas=aliquotas)


def tarifa_AL():
    url = "https://www.casal.al.gov.br/estrutura-tarifaria/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    data = soup.find_all("td")

    faixas = list(
        map(
            lambda x: x.text.replace("Até ", "")
            .replace("m³", "")
            .replace("–", "a")
            .replace("\xa0 ", ""),
            data[5].find_all("p"),
        )
    )
    aliquotas = list(map(lambda x: x.text.replace(",", "."), data[6].find_all("p")))

    faixas.pop(1)
    faixas = faixas[:8]
    faixas[0] = f"0 a {faixas[0]}"
    faixas.append(f"{int(faixas[-1].split('a')[1]) + 1} a 999999")

    aliquotas.pop(1)
    aliquotas = aliquotas[:9]

    return build_mocks(faixas=faixas, aliquotas=aliquotas)


Campo_Grande_MS = "https://www.aguasguariroba.com.br/legislacao-e-tarifas/"
