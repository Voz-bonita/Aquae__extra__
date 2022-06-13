from tabula import read_pdf
from datetime import datetime


ano = datetime.today().year - 3
snis = f"http://www.snis.gov.br/downloads/diagnosticos/ae/{ano}/Diagnostico-SNIS-AE-{ano}-Capitulo-12.pdf"
df = read_pdf(
    input_path=snis,
    pages=4,
    area=[290, 80, 800, 600],
)[0]
