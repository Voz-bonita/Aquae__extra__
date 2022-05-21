import urllib.request
from datetime import date
from calendar import monthrange
import json


def get_mm(row):
    mm = row["CHUVA"]
    if not mm:
        mm = 0.0
    return float(mm)


with open("Coleta_de_pluviometria/Cidades_Track.csv", "r") as file:
    estacoes = file.read().split(",")


ano_atual = date.today().year
ano_inicial = ano_atual - 1


estacional = {}
for estacao in estacoes:
    anual = {}
    for ano in range(ano_inicial, ano_atual):
        print(f"Ano: {ano}")
        mensal = {}
        for mes in range(1, 13):
            print(f"Mes: {mes}")
            ultimo_dia = monthrange(ano, mes)[1]
            mes = str(mes).zfill(2)
            url = f"https://apitempo.inmet.gov.br/estacao/{ano}-{mes}-01/{ano}-{mes}-{ultimo_dia}/{estacoes[0]}"
            with urllib.request.urlopen(url) as url:
                data = json.loads(url.read().decode())
                mm = list(map(get_mm, data))
                total = round(sum(mm), 2)

            mensal[mes] = total
            print(f"Pluviometria: {total}mm")
        anual[ano] = mensal
    estacional[estacao] = anual
