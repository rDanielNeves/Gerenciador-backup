import os
import json
from tkinter import Tk, Label, Button, ttk
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import shutil
import datetime

pasta_selecionada = ""
pasta_destino = ""


def escolher_pasta():
    global pasta_selecionada
    pasta = askdirectory()

    if pasta:
        pasta_selecionada = pasta
        label_pasta.config(text=f"Pasta de origem: {pasta_selecionada}")
        label_status.config(text="Pronto para selecionar destino.")


def escolher_destino():
    global pasta_destino
    pasta = askdirectory()

    if pasta:
        pasta_destino = pasta
        label_destino.config(text=f"Destino do backup: {pasta_destino}")
        label_status.config(text="Pronto para fazer backup.")


def criar_backup(pasta_origem, pasta_destino, barra_progresso):
    lista_arquivos = os.listdir(pasta_origem)
    total_itens = len(lista_arquivos)

    nome_pasta_backup = "backup"
    nome_completo_pasta_backup = os.path.join(pasta_destino, nome_pasta_backup)
    if not os.path.exists(nome_completo_pasta_backup):
        os.mkdir(nome_completo_pasta_backup)

    data_atual = datetime.datetime.today().strftime("%Y-%m-%d %Hh%Mm%Ss")

    arquivos_copiados = 0
    pastas_copiadas = 0
    erros = []

    barra_progresso["maximum"] = total_itens
    barra_progresso["value"] = 0

    for indice, arquivo in enumerate(lista_arquivos, start=1):
        nome_completo_arquivo = os.path.join(pasta_origem, arquivo)

        if arquivo == "backup":
            barra_progresso["value"] = indice
            janela.update()
            continue

        nome_completo_data = os.path.join(nome_completo_pasta_backup, data_atual)
        os.makedirs(nome_completo_data, exist_ok=True)

        nome_final_arquivo = os.path.join(nome_completo_data, arquivo)

        try:
            if os.path.isfile(nome_completo_arquivo):
                shutil.copy2(nome_completo_arquivo, nome_final_arquivo)
                arquivos_copiados += 1
            elif os.path.isdir(nome_completo_arquivo):
                shutil.copytree(nome_completo_arquivo, nome_final_arquivo)
                pastas_copiadas += 1

        except OSError as erro:
            print(f"Erro ao copiar {arquivo}: {erro}")
            erros.append(arquivo)

        barra_progresso["value"] = indice
        label_status.config(text=f"Copiando... {indice}/{total_itens}")
        janela.update()

    return arquivos_copiados, pastas_copiadas, erros


def salvar_historico(pasta_origem, arquivos_copiados, pastas_copiadas, quantidade_erros):
    caminho_historico = "historico.json"

    novo_registro = {
        "data": datetime.datetime.today().strftime("%Y-%m-%d"),
        "horario": datetime.datetime.today().strftime("%Hh%Mm%Ss"),
        "pasta_origem": pasta_origem,
        "arquivos_copiados": arquivos_copiados,
        "pastas_copiadas": pastas_copiadas,
        "erros": quantidade_erros
    }

    if os.path.exists(caminho_historico):
        with open(caminho_historico, "r") as arquivo:
            historico = json.load(arquivo)
    else:
        historico = []

    historico.append(novo_registro)

    with open(caminho_historico, "w") as arquivo:
        json.dump(historico, arquivo, indent=4)


def realizar_backup():
    if not pasta_selecionada:
        messagebox.showwarning("Atenção", "Selecione uma pasta de origem antes de fazer o backup.")
        return

    if not pasta_destino:
        messagebox.showwarning("Atenção", "Selecione uma pasta de destino antes de fazer o backup.")
        return

    label_status.config(text="Backup em andamento...")
    janela.update()

    arquivos_copiados, pastas_copiadas, erros = criar_backup(pasta_selecionada, pasta_destino, barra_progresso)

    salvar_historico(pasta_selecionada, arquivos_copiados, pastas_copiadas, len(erros))

    if not erros:
        mensagem_final = f"Backup realizado com sucesso!\n\nArquivos copiados: {arquivos_copiados}\nPastas copiadas: {pastas_copiadas}"
    else:
        lista_de_erros = ", ".join(erros)
        mensagem_final = (
            f"Backup concluído com {len(erros)} erro(s).\n\n"
            f"Arquivos copiados: {arquivos_copiados}\n"
            f"Pastas copiadas: {pastas_copiadas}\n\n"
            f"Itens com problema: {lista_de_erros}"
        )

    label_status.config(text="Backup concluído.")
    barra_progresso["value"] = 0
    messagebox.showinfo("Backup", mensagem_final)


janela = Tk()
janela.title("Gerenciador de Backup")
janela.geometry("420x320")

label_titulo = Label(janela, text="Gerenciador de Backup", font=("Arial", 14, "bold"))
label_titulo.pack(pady=10)

botao_selecionar = Button(janela, text="Selecionar pasta de origem", command=escolher_pasta)
botao_selecionar.pack(pady=5)

label_pasta = Label(janela, text="Nenhuma pasta de origem selecionada")
label_pasta.pack(pady=5)

botao_destino = Button(janela, text="Selecionar destino do backup", command=escolher_destino)
botao_destino.pack(pady=5)

label_destino = Label(janela, text="Nenhum destino selecionado")
label_destino.pack(pady=5)

botao_backup = Button(janela, text="Fazer Backup", command=realizar_backup)
botao_backup.pack(pady=5)

barra_progresso = ttk.Progressbar(janela, orient="horizontal", length=300, mode="determinate")
barra_progresso.pack(pady=10)

label_status = Label(janela, text="")
label_status.pack(pady=5)

janela.mainloop()