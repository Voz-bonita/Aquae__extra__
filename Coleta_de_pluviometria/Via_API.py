import urllib.request
from datetime import date
from calendar import monthrange
import json


def get_mm(row):
    mm = row["CHUVA"]
    if not mm:
        mm = 0.0
    return float(mm)


ano_atual = date.today().year
ano_inicial = ano_atual - 5

DF = ["A045", "A001", "A042", "A046", "A047"]
anual = {}
for ano in range(ano_inicial, ano_atual):
    print("-" * 200)
    print(f"Ano: {ano}")
    mensal = {}
    for mes in range(1, 13):
        print(f"Mes: {mes}")
        ultimo_dia = monthrange(ano, mes)[1]
        mes = str(mes).zfill(2)
        url = f"https://apitempo.inmet.gov.br/estacao/{ano}-{mes}-01/{ano}-{mes}-{ultimo_dia}/{DF[0]}"
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            mm = list(map(get_mm, data))
            total = round(sum(mm), 2)

        mensal[mes] = total
        print(f"Pluviometria: {total}mm")
    anual[ano] = mensal


estacao = data[0]["DC_NOME"]
with open(f"{estacao}.json", "w") as file:
    json.dump(anual, file)
