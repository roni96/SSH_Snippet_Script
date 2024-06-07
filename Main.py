import tkinter as tk
from tkinter import ttk
import os
import re

def secure_shell():
    ipadd = box_target.get()
    port = box_port.get()
    user = box_user.get()
    pwd = box_pass.get()

    os.system(f"start plink -ssh -v {user}@{ipadd} -P {port} -pw {pwd} -m ./scripts/comandos.txt")

# Função para listar os arquivos em uma pasta e retornar uma lista com seus nomes
def listar_arquivos(pasta):
    arquivos = os.listdir(pasta)
    return arquivos

def run_script(valores):
    cmd = []
    i = 0
    for linha in script:
        if "$(" in linha.strip():
            texto = linha.strip()
            padrao = r'\$\((.*?)\)'
            if valores[i] != '':
                linha = re.sub(padrao,valores[i], texto)
            cmd.append(linha)
            i = i + 1
        else:
            cmd.append(linha)
    
    # Nome do arquivo de saída
    nome_arquivo = "./scripts/comandos.txt"

    # Abrir o arquivo para escrita
    with open(nome_arquivo, "w") as arquivo:
        # Escrever cada elemento da lista no arquivo
        for item in cmd:
            arquivo.write("%s\n" % item)

    # Limpar qualquer texto existente no Text
    texto_box.delete('1.0', tk.END)
    
    # Ler o conteúdo do arquivo e exibi-lo no Text
    with open(nome_arquivo, "r") as arquivo:
        conteudo = arquivo.read()
        texto_box.insert(tk.END, conteudo)


def get_script():

    valores = [entry.get() for entry in campos]
    run_script(valores)

def load_script(event):
    global campos
    global labels
    global script

    # print(campos)
    if campos != []:
        for entry in campos:
            entry.destroy()
        for entry in labels:
            entry.destroy()

    # Limpar qualquer texto existente no Text
    texto_box.delete('1.0', tk.END)


    script = []
    variaveis = []
    campos = []
    labels = []
    coments = []

    arq_cmd = dropdown.get()
    with open(f"./scripts/{arq_cmd}","r") as arquivo:
        for linha in arquivo:
            if linha.startswith("#"):
                coments.append(linha)
            if not linha.startswith("#"):
                script.append(linha.strip())
                if "$(" in linha.strip():
                    texto = linha.strip()
                    padrao = r'\$\((.*?)\)'
                    valor = re.findall(padrao, texto)
                    variaveis.append(valor)

    coments = [item.strip() for item in coments if item.strip()]
    coments = "\n".join(coments)
    box_coments.config(state="normal")
    box_coments.delete('1.0', tk.END)
    box_coments.insert(tk.END, coments)
    box_coments.config(state="disabled")


    ind = 10
    for i in variaveis:
        label_new = tk.Label(janela, width=10, text=i[0])
        label_new.grid(column=0, row=ind)
        box_new = tk.Entry(janela, width=30)
        box_new.grid(column=1, row=ind)
        campos.append(box_new)
        labels.append(label_new)
        # campos.append([box_new,label_new])
        ind = ind + 1

campos = []
labels = []

janela = tk.Tk()
janela.title("SSH Snippet Script")
janela.geometry("1305x500")

# Pasta contendo os arquivos
pasta_arquivos = "./scripts/"
# Listar os arquivos na pasta
arquivos = listar_arquivos(pasta_arquivos)

selecionado = tk.StringVar(janela)
selecionado.set(arquivos[0])  # Define a primeira opção como padrão

# Criar um dropdown na janela
dropdown = ttk.Combobox(janela, values=arquivos, width=102, state='readonly')
dropdown.grid(row=4, column=0, columnspan=5, pady=3)
# Selecionar a primeira opção por padrão
dropdown.bind("<<ComboboxSelected>>", load_script)

# Criar um botão na janela
btn_run = tk.Button(janela, width=90, text="Mount Script", command=get_script)
btn_run.grid(row=20, column=0, columnspan=5, padx=5, pady=2)

# Criar um widget Text para exibir o conteúdo do arquivo
texto_box = tk.Text(janela, wrap="word")
texto_box.grid(row=0, column=5, rowspan=600, columnspan=4, padx=5, pady=2)

box_coments = tk.Text(janela, height=10, width=79, wrap="word", state="disabled")
box_coments.grid(column=0, row=2, columnspan=5, padx=4)


label_target = tk.Label(janela, width=10, text="IP Addr: " )
label_target.grid(row=601, column=5)
box_target = tk.Entry(janela, width=30)
box_target.grid(row=601, column=6)

label_port = tk.Label(janela, width=10, text="Port: " )
label_port.grid(row=602, column=5)
box_port = tk.Entry(janela, width=30)
box_port.grid(row=602, column=6)

label_user = tk.Label(janela, width=10, text="Username: " )
label_user.grid(row=601, column=7)
box_user = tk.Entry(janela, width=30)
box_user.grid(row=601, column=8)

label_pass = tk.Label(janela, width=10, text="Password: " )
label_pass.grid(row=602, column=7)
box_pass = tk.Entry(janela, width=30)
box_pass.grid(row=602, column=8)

# Criar um botão na janela
btn_shell = tk.Button(janela, width=91, height=3, text="Run Script", command=secure_shell)
btn_shell.grid(row=603, column=5, columnspan=4, padx=5, pady=6)

janela.mainloop()

