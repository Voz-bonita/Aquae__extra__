import json
import os


def get_codigo(csv_INMET):
    info = csv_INMET.split("_")
    return info[3]


DIR = "Coleta_de_pluviometria"
with open(f"{DIR}/Pluviometria_Mediana.json", "r") as file:
    medianas = json.load(file)

csvs = os.listdir(f"{DIR}/CSVs")

cidades = list(medianas.keys())
codigos_unicos = set()
for cidade in cidades:
    arquivos = list(filter(lambda csv: cidade in csv, csvs))
    codigos = list(map(get_codigo, arquivos))
    for c in codigos:
        codigos_unicos.add(c)

with open(f"{DIR}/Cidades_Track.csv", "w") as file:
    file.write(",".join(codigos_unicos))
