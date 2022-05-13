import functools
import statistics
import json


DIR = "Coleta_de_pluviometria"
with open(f"{DIR}/Pluviometria_Brasil.json", "r") as file:
    pluv_br = json.load(file)


with open(f"{DIR}/Pluviometria_Mediana.json", "w") as file:
    medianas = {}
    for estado in pluv_br:
        medianas[estado] = {}
        for estacao in pluv_br[estado]:

            meses = [[] for _ in range(12)]
            for ano in pluv_br[estado][estacao]:
                for i in range(12):
                    pluv_i = pluv_br[estado][estacao][ano][str(i + 1).zfill(2)]
                    if pluv_i != 0:
                        meses[i].append(pluv_i)

            # pelo menos 3 observacoes em cada mes
            min3 = list(map(lambda x: len(x) >= 3, meses))
            if functools.reduce(lambda x, y: x and y, min3):
                medianas[estado][estacao] = list(
                    map(lambda x: round(statistics.median(x), 2), meses)
                )

    json.dump(medianas, file)
