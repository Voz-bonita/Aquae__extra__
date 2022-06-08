from tabula import read_pdf


snis = "http://www.snis.gov.br/downloads/diagnosticos/ae/2019/Diagnostico-SNIS-AE-2019-Capitulo-12.pdf"
df = read_pdf(
    input_path=snis,
    pages=4,
    area=[290, 80, 800, 600],
)[0]
print(df.iloc[:, 0:2])
