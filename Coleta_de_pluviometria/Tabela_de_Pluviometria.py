from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import date
from calendar import monthrange
import json
import re


def get_mm(row):
    row_as_text = row.get_attribute("innerHTML")[-15:]
    mm = (
        re.findall(">.*<", row_as_text)[0]
        .replace(">", "")
        .replace("<", "")
        .replace(",", ".")
    )

    if not mm:
        mm = 0.0

    return float(mm)


def setup(driver, estado, xpaths):
    driver.find_element_by_xpath(xpaths["produto"]).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["tabela_estacao"])))
    driver.find_element_by_xpath(xpaths["tabela_estacao"]).click()

    wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["uf"])))
    uf_selector = driver.find_element_by_xpath(xpaths["uf"])
    uf_selector.click()
    uf = driver.find_elements_by_xpath(xpaths["uf_opt"])
    uf.pop(0)
    uf[estado].click()


atual = date.today().year
ano_inicial = atual - 5
ano_final = atual - 1


xpaths = {
    "menu": '//*[@id="root"]/div[1]/div[1]',
    "produto": '//*[@id="root"]/div[2]/div[1]/div/div/input',
    "tabela_estacao": '//*[@id="root"]/div[2]/div[1]/div/div/div[2]/div[10]',
    "uf": '//*[@id="root"]/div[2]/div[1]/div[2]/div[2]/input',
    "uf_opt": '//*[@id="root"]/div[2]/div[1]/div[2]/div[2]/div[2]/div',
    "estacao": '//*[@id="root"]/div[2]/div[1]/div[2]/div[3]/input',
    "estacao_opt": '//*[@id="root"]/div[2]/div[1]/div[2]/div[3]/div[2]/div',
    "data_0": '//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input',
    "data_f": '//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input',
    "gerar": '//*[@id="root"]/div[2]/div[1]/div[2]/button',
    "table_rows": '//*[@id="root"]/div[2]/div[2]/div/div/table/tbody/tr',
    "table_row_0": '//*[@id="root"]/div[2]/div[2]/div/div/table/tbody/tr[1]/td[1]',
}

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get("https://tempo.inmet.gov.br/")
setup(driver, 6, xpaths)

data_0 = driver.find_element_by_xpath(xpaths["data_0"])
data_f = driver.find_element_by_xpath(xpaths["data_f"])
gerar = driver.find_element_by_xpath(xpaths["gerar"])

menu = driver.find_element_by_xpath(xpaths["menu"])
menu.click()


for i in range(4, 5):
    menu.click()

    wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["estacao"])))
    estacao_selector = driver.find_element_by_xpath(xpaths["estacao"])
    estacao_selector.click()
    estacoes = driver.find_elements_by_xpath(xpaths["estacao_opt"])
    estacoes[i].click()
    estacao = estacoes[i].find_element_by_xpath("span").get_attribute("innerHTML")[:-7]

    menu.click()
    anual = {}
    for ano in range(ano_inicial, ano_final + 1):
        mensal = {}
        for mes in range(1, 13):
            ultimo_dia = monthrange(ano, mes)[1]
            mes = str(mes).zfill(2)

            menu.click()
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["data_0"])))
            data_0.send_keys(f"01{mes}{ano}")
            data_f.send_keys(f"{ultimo_dia}{mes}{ano}")
            gerar.click()

            try:
                wait.until(
                    EC.text_to_be_present_in_element(
                        (By.XPATH, xpaths["table_row_0"]), f"01/{mes}/{ano}"
                    )
                )
            except TimeoutException:
                menu.click()
                gerar.click()

            rows = driver.find_elements_by_xpath(xpaths["table_rows"])

            mm = list(map(get_mm, rows))

            total = sum(mm)
            mensal[mes] = total

        anual[ano] = mensal

    with open(f"{estacao}.json", "w") as file:
        json.dump(anual, file)
