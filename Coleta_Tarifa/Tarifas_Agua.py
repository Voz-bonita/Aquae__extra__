import requests
import re


def meio_int(meio: str):
    a, b = list(map(int, meio.split(" a ")))
    return [a, b]


def build_mocks(meio: list, aliquotas: list):
    maior = float("-inf")
    agrupado = []
    grupo = []

    for intervalo, preco in zip(meio, aliquotas):
        preco = float(preco.replace(",", "."))
        if intervalo[1] < maior:
            grupo.append(
                {"min": grupo[-1]["max"] + 1, "max": 99999999999, "tarifa": preco}
            )
            agrupado.append(grupo.copy())
            grupo.clear()

        maior = intervalo[1]
        grupo.append({"min": intervalo[0], "max": intervalo[1], "tarifa": preco})

    agrupado.append(grupo.copy())
    return agrupado


faixa_0 = "Ate \d+"
faixa_m = "(?<!\d)\d{1,2} a \d+"
# faixa_f = "Acima de \d{2}"

aliquotas_regex = "\d+,\d+"

url_CAESB = "https://www.caesb.df.gov.br/tarifas-e-precos.html"
response = requests.get(url_CAESB)
html = response.content.decode("utf8").replace("\n", "")

# ultimas = re.findall(faixa_f, html)
meio = re.findall(faixa_m, html)
meio = list(map(meio_int, meio))

aliquotas = re.findall(aliquotas_regex, html)

caesb = build_mocks(meio, aliquotas[1::2])
print(caesb)
