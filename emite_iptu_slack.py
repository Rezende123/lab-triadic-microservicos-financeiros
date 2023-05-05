from dotenv import load_dotenv
load_dotenv()

import glob
import os
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from message_service_slack import upload_arquivo_slack

driver = webdriver.Chrome()
# ABRE SITE DO IPTU
driver.get('https://servicosweb.sefaz.salvador.ba.gov.br/sistema/dam/IPTU_TL/servicos_DamIptuTL.asp?Tipo=D')

# # FECHA POPUP
# botao_fechar = driver.find_element(by=By.XPATH,value='/html/body/div[3]/div[2]/div/div/div[2]/button')
# botao_fechar.click()

# PREENCHE A INSCRICAO
valor_inscricao_imovel = os.environ.get("INSCRICAO_IMOVEL")
campo_inscricao = driver.find_element(by=By.XPATH,value='/html/body/div[2]/div[3]/form/div[1]/input')
campo_inscricao.send_keys(valor_inscricao_imovel)
print('INSCRIÇÃO PREENCHIDA')

# PREENCHE O EXERCICIO
exercicio = datetime.date.today().year
campo_inscricao = driver.find_element(by=By.XPATH,value='/html/body/div[2]/div[3]/form/div[2]/select')
campo_inscricao.send_keys(exercicio)
print('EXERCÍCIO PREENCHIDO')
time.sleep(10)

# BOTAO CONSULTAR
botao_consultar = driver.find_element(by=By.ID, value='btnConsulta')
botao_consultar.click()
time.sleep(5)

print('DAM CONSULTADO')

# BOTAO EMITIR
botao_emitir = driver.find_element(by=By.ID, value='bt_dam')
botao_emitir.click()
time.sleep(5)

print('DAM EMITIDO')

# BUSCA O ÚLTIMO ARQUIVO BAIXADO
caminho_download = os.environ.get("PATH_DOWNLOAD")
list_of_files = glob.glob(caminho_download) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print('BOLETO ENCONTRADO: ' + latest_file)

# FAZ UPLOAD E ENVIA O ARQUIVO VIA SLACK
upload_arquivo_slack("boleto-iptu", latest_file, "Boleto do último iptu pendente")