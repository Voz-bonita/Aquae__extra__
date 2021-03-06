import requests
from datetime import date, timedelta
import json

hoje = date.today()
primeiro = hoje.replace(day=1)
mes_passado = primeiro - timedelta(days=1)
ano = mes_passado.year
mes = str(mes_passado.month).zfill(2)


url = "https://sidra.ibge.gov.br/Ajax/JSon/Valores/1/1737"
payload = {
    "params": f"t/1737/f/c/h/n/n1/all/V/2266/P/{ano}{mes}/d/v2266 13",
    "versao": "-1",
    "desidentifica": "false",
}

response = requests.post(url, data=payload, verify="ibge.pem")
print(response.status_code)
print(response.content)

response__list__ = json.loads(response.content.decode())
ni = float(response__list__[0]["V"])
print(ni)
