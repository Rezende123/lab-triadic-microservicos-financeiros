from dotenv import load_dotenv
load_dotenv()

import glob
import os
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from services.message_service_slack import upload_arquivo_slack

driver = webdriver.Chrome()
# ABRE SITE DA FACULDADE
driver.get('https://aluno.unifacs.br/SOL/aluno/index.php/index/seguranca/dev/instituicao/127')

# LINK EX-ALUNO
link_exaluno = driver.find_element(by=By.ID, value='btnExAluno')
link_exaluno.click()
time.sleep(5)

# PREENCHE RA
valor_ra_universidade_pos = os.environ.get("RA_UNIVERSIDADE_POS")
campo_ra = driver.find_element(by=By.XPATH,value='/html/body/div[2]/div[1]/form/div[4]/div/input[1]')
campo_ra.send_keys(valor_ra_universidade_pos)
print('RA PREENCHIDO')

# PREENCHE SENHA
valor_senha_universidade_pos = os.environ.get("SENHA_UNIVERSIDADE_POS")
campo_senha = driver.find_element(by=By.XPATH,value='/html/body/div[2]/div[1]/form/div[4]/div/input[2]')
campo_senha.send_keys(valor_senha_universidade_pos)
print('SENHA PREENCHIDA')

# BOTÃO LOGAR
botao_logar = driver.find_element(by=By.ID, value='logar')
botao_logar.click()
print('USUÁRIO LOGADO')
time.sleep(5)

# BOTÃO MENU
botao_menu = driver.find_element(by=By.XPATH,value='/html/body/span/div[2]/div/div[1]/div[1]/i')
botao_menu.click()
time.sleep(5)

# BOTÃO MENU SERVICOS
botao_menu_servicos = driver.find_element(by=By.XPATH,value='/html/body/span/div[1]/div/div[2]/ul/li[2]')
botao_menu_servicos.click()
time.sleep(5)

# BOTÃO MENU EXTRATO FINANCEIRO
botao_menu_extrato_financeiro = driver.find_element(by=By.XPATH,value='/html/body/span/div[1]/div/div[2]/ul/ul[2]/a[3]')
botao_menu_extrato_financeiro.click()
time.sleep(5)

# # ABRE EXTRATO FINANCEIRO
# driver.get('https://cloudapp.animaeducacao.com.br/financeiroaluno/extratofinanceiro')
# print('NAVEGAÇÃO PARA O EXTRATO FINANCEIRO')
# time.sleep(50)

# BOTÃO BOLETO
botao_aba_boleto = driver.find_element(by=By.ID, value='aba_boleto')
botao_aba_boleto.click()
print('NAVEGAÇÃO PARA ABA BOLETO')
time.sleep(5)

# BOTÃO GERAR CÓDIGO DE BARRAS
botao_codigo_barra = driver.find_element(by=By.ID, value='gerar_codigo_barra')
botao_codigo_barra.click()
print('CÓDIGO DE BARRA GERADO')
time.sleep(10)

# BOTÃO IMPRIMIR BOLETO
botao_imprimir_boleto = driver.find_element(by=By.ID, value='imprimir_boleto')
botao_imprimir_boleto.click()
print('BOLETO IMPRESSO')
time.sleep(20)

# BUSCA O ÚLTIMO ARQUIVO BAIXADO
caminho_download = os.environ.get("PATH_DOWNLOAD")
list_of_files = glob.glob(caminho_download) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print('BOLETO ENCONTRADO: ' + latest_file)

# FAZ UPLOAD E ENVIA O ARQUIVO VIA SLACK
upload_arquivo_slack("boleto-pos-graduacao", latest_file, "Boleto da pós-graduação")
