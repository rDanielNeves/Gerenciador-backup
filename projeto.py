import os
from tkinter.filedialog import askdirectory
import shutil
import datetime

nome_pasta_selecionada = askdirectory()
if not nome_pasta_selecionada:
    exit()

lista_arquivos = os.listdir(nome_pasta_selecionada)

nome_pasta_backup = "backup"
nome_completo_pasta_backup = os.path.join(nome_pasta_selecionada, nome_pasta_backup)
if not os.path.exists(nome_completo_pasta_backup):
    os.mkdir(nome_completo_pasta_backup)

data_atual = datetime.datetime.today().strftime("%Y-%m-%d %H%M%S")

for arquivo in lista_arquivos:
    nome_completo_arquivo = os.path.join(nome_pasta_selecionada, arquivo)

    nome_completo_data = os.path.join(nome_completo_pasta_backup, data_atual)

    if not os.path.exists(nome_completo_data):
        os.mkdir(nome_completo_data)

    nome_final_arquivo = os.path.join(nome_completo_data, arquivo)

    if os.path.isfile(nome_completo_arquivo):
        shutil.copy2(nome_completo_arquivo, nome_final_arquivo)
    elif os.path.isdir(nome_completo_arquivo):
        shutil.copytree(nome_completo_arquivo, nome_final_arquivo)