import json


with open("Coleta_de_pluviometria/Pluviometria_Brasil.json", "r") as file:
    pluv_br = json.load(file)


with open("./Coleta_de_pluviometria/Cidade_fixture.json", "w") as cf:
    fixtures = []
    k = 0
    for uf in pluv_br:
        for cidade in pluv_br[uf]:
            fixture = {
                "model": "base_de_dados.cidade",
                "pk": k,
                "fields": {"nome": cidade, "uf": uf},
            }
            fixtures.append(fixture)
            k += 1
    json.dump(fixtures, cf)


with open("./Coleta_de_pluviometria/Pluviometria_fixture.json", "w") as pf:
    fixtures = []
    m = 0
    k = 0
    for uf in pluv_br:
        for cidade in pluv_br[uf]:
            for ano in pluv_br[uf][cidade]:
                for mes in pluv_br[uf][cidade][ano]:
                    fixture = {
                        "model": "base_de_dados.indicepluviometrico",
                        "pk": k,
                        "fields": {
                            "ano": ano,
                            "mes": mes,
                            "media_pluviometrica": pluv_br[uf][cidade][ano][mes],
                            "cidade": m,
                        },
                    }
                    fixtures.append(fixture)
                    k += 1
            m += 1
    json.dump(fixtures, pf)
