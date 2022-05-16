import requests
import re


def meio_int(meio: str):
    a, b = list(map(int, meio.split(" a ")))
    return [a, b]


def meio_arr(meio: list):
    maior = float("-inf")
    agrupado = []
    grupo = []

    for intervalo in meio:
        if intervalo[1] < maior:
            grupo.append({"min": grupo[-1]["max"] + 1, "max": 99999999999})
            agrupado.append(grupo.copy())
            grupo.clear()

        maior = intervalo[1]
        grupo.append({"min": intervalo[0], "max": intervalo[1]})

    agrupado.append(grupo.copy())
    return agrupado


faixa_0 = "Ate \d+"
faixa_m = "(?<!\d)\d{1,2} a \d+"
# faixa_f = "Acima de \d{2}"

url_CAESB = "https://www.caesb.df.gov.br/tarifas-e-precos.html"
response = requests.get(url_CAESB)
html = response.content.decode("utf8").replace("\n", "")

# ultimas = re.findall(faixa_f, html)
meio = re.findall(faixa_m, html)
meio = list(map(meio_int, meio))
meio = meio_arr(meio)
