from pathlib import Path
import streamlit as st
import glob
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from pathlib import Path
from time import sleep

if 'pagina_central' not in st.session_state:
    st.session_state.pagina_central = 'home'

def whats_bot(conteudo_template, conteudo_contatos):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    def abrir_janela_whatsapp():
        driver.get("https://web.whatsapp.com/")
        wait = WebDriverWait(driver, timeout=60)
        barra_lateral = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]')))
        driver.implicitly_wait(2)

    def abrir_janel_de_conversa(nome_contato):
        barra_pesquisa = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]')
        barra_pesquisa.send_keys(Keys.CONTROL + 'a')
        barra_pesquisa.send_keys(Keys.DELETE)

        barra_pesquisa = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]')
        barra_pesquisa.send_keys(nome_contato)

        wait = WebDriverWait(driver, timeout=2)
        span_buscando = f'//span[@title="{nome_contato}"]'
        conversa_lateral = wait.until(EC.presence_of_element_located((By.XPATH, span_buscando)))
        conversa_lateral.click()

    def sai_das_conversas():
        barra_pesquisa = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]')
        barra_pesquisa.send_keys(Keys.CONTROL + 'a')
        barra_pesquisa.send_keys(Keys.DELETE)
        barra_pesquisa.send_keys(Keys.ESCAPE)

    def envia_mensagem(mensagem):
        barra_de_mensagem = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[2]/div[1]')
        barra_de_mensagem.send_keys(mensagem)
        barra_de_mensagem.send_keys(Keys.RETURN)

    def deslogar():
        mais_opcoes = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span/div[5]/div').click()
        sleep(1)
        deslogar = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span/div[5]/span/div/ul/li[6]/div').click()
        sleep(1)
        deslogar_dois = driver.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[3]/div/button[2]').click()

    if __name__ == '__main__':

        abrir_janela_whatsapp()
        for contato in conteudo_contatos:
            abrir_janel_de_conversa(contato)
            sleep(2)
            envia_mensagem(conteudo_template.format(contato))
            sleep(2)
            sai_das_conversas()
            sleep(2)
            
    sleep(5)
    deslogar()    
    sleep(3)

PASTA_ATUAL = Path(__file__).parent
PASTA_TEMPLATES = PASTA_ATUAL / 'templates'
PASTA_CONTATOS = PASTA_ATUAL / 'contatos'

def mudar_pagina(nome_pagina):
    st.session_state.pagina_central = nome_pagina

##### HOME #####
def home():
    st.markdown("# Central de Mensagens")
    st.divider()
    st.text(
        """
Através desse aplicativo, faremos o envio de mensagens em massa
para nossos grupos, automatizando boa parte do atendimento a ser realizado.

Nessa Aba você pode prosseguir para o envio em massa para nossos grupos de What'sApp,
selecionando um template específico para envio. Na aba Gerenciar Templates você consegue
remover, incluir e editar templates que poderão ser utilizados posteriormente. Na aba
Gerenciar Contatos você pode incluir e retirar nomes de grupos que deverão ser contatados no envio.
        
        """)
    st.button("Realizar Envio em Massa",
               use_container_width= True,
               on_click= mudar_pagina,
               args= ('realizar_envio', ))

##### TEMPLATES #####
def pag_templates():
    st.markdown("# Templates")
    st.divider()

    for arquivo in PASTA_TEMPLATES.glob('*.txt'):
        nome_arquivo = arquivo.stem.replace('_',  '').upper()
        col1, col2= st.columns([0.6, 0.4])

        col1.button(nome_arquivo, key = f'{nome_arquivo}', use_container_width= True,
                               on_click = mudar_pagina,
                               args = ("visualizar_template"))
        col2.button('Remover', key = f'remover_{nome_arquivo}', use_container_width= True,
                               on_click = remove_template,
                               args = (nome_arquivo))

    st.divider()
    st.button('Adicionar Template', on_click = mudar_pagina, args = ('adicionar_novo_template', ))

def pag_adicionar_novo_template():
    st.title("Adição de Templates")
    nome_template = st.text_input("Nome do Template: ")
    conteudo_template = st.text_area("Escreva o Texto do Template: ", height= 400)
    st.button("Salvar", on_click = salvar_template, args = (nome_template, conteudo_template))

def salvar_template(nome, texto):
    PASTA_TEMPLATES.mkdir(exist_ok= True)
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(PASTA_TEMPLATES / nome_arquivo, 'w') as f:
        f.write(texto)
    mudar_pagina('templates')

def remove_template(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    (PASTA_TEMPLATES / nome_arquivo).unlink()

##### CONTATOS #####
def pag_contatos():
    st.title("Gerenciar Contatos")
    st.divider()

    st.button('Adicionar Contatos', use_container_width = True, on_click = mudar_pagina, args = ('novo_contato', ))
    st.button('Visualizar Listas', use_container_width = True, on_click = mudar_pagina, args = ('verificar_contatos', ))

def pag_novo_contato():
    st.title("Adição de Lista de Grupos")
    listas_contatos = [file.name for file in PASTA_CONTATOS.glob("*.txt")]
    lista_selecionada =  st.selectbox("Selecione a Lista de Contatos para adição.", listas_contatos)
    contatos_lista = st.text_area("Escreva os nomes dos grupos separados por vírgula: ", height= 400)
    st.button("Salvar", on_click = salvar_lista, args = (lista_selecionada, contatos_lista))

def salvar_lista(nome, texto):
    PASTA_CONTATOS.mkdir(exist_ok= True)
    with open(PASTA_CONTATOS / nome, 'a') as f:
        f.write("," + texto)
    mudar_pagina('contatos')

def verificar_contatos():
    st.title("Listas e Contatos")
    st.divider()

    listas_contatos = [file.name for file in PASTA_CONTATOS.glob("*.txt")]
    lista_selecionada =  st.selectbox("Selecione a Lista de Contatos para adição.", listas_contatos)
    with open(PASTA_CONTATOS / lista_selecionada, 'r') as f:
        contatos = list()
        for line in f:
            split_line = [item.strip() for item in line.split(',')]
            contatos.append(split_line)
        flat_list = [item for sublist in contatos for item in sublist]
        flat_list = list(filter(None, flat_list))
        st.write(flat_list)
        st.divider()

        st.text("# Remover Contatos")
        remover_contatos = st.multiselect("Contatos da Lista", flat_list)
        st.button("Remover", use_container_width= True, on_click = excluir_contatos, args = (lista_selecionada, remover_contatos, flat_list))

def excluir_contatos(lista, contatos, lista_original):
    updated_list = [item for item in lista_original if item not in contatos]
    with open(PASTA_CONTATOS / lista, 'w') as file:
        for item in updated_list:
            file.write(item + ',\n') 

##### ENVIO #####
def realizar_envio():
    st.title("Envio em Massa")
    st.divider()

    arquivos_template = [file.name for file in PASTA_TEMPLATES.glob("*.txt")]
    template_selecionado = st.selectbox("Selecione o Template para envio em massa.", arquivos_template)
    PASTA_TEMPLATES.mkdir(exist_ok= True)
    with open(PASTA_TEMPLATES / template_selecionado, 'r') as f:
        conteudo_template = f.read()
        st.text_area("Counteúdo do Template", conteudo_template, height= 200)

    arquivos_lista = [file.name for file in PASTA_CONTATOS.glob("*.txt")]
    lista_selecionada = st.selectbox("Selecione a lista de contatos para envio em massa.", arquivos_lista)
    PASTA_CONTATOS.mkdir(exist_ok= True)
    with open(PASTA_CONTATOS / lista_selecionada, 'r') as f:
        contatos = list()
        for line in f:
            split_line = [item.strip() for item in line.split(',')]
            contatos.append(split_line)
        conteudo_contatos = [item for sublist in contatos for item in sublist]
        conteudo_contatos = list(filter(None, conteudo_contatos))

    st.divider()
    st.button("Enviar", use_container_width = True, on_click = whats_bot, args = (conteudo_template, conteudo_contatos))

def main():
    st.sidebar.button("Central de Mensagens", use_container_width= True, on_click= mudar_pagina, args = ('home',))
    st.sidebar.button("Gerenciar Templates", use_container_width= True, on_click= mudar_pagina, args = ('templates',))
    st.sidebar.button("Gerenciar Contatos", use_container_width= True, on_click = mudar_pagina, args = ('contatos', ))

    if st.session_state.pagina_central == 'home':
        home()
    elif st.session_state.pagina_central == 'templates':
        pag_templates()
    elif st.session_state.pagina_central == 'adicionar_novo_template':
        pag_adicionar_novo_template()
    elif st.session_state.pagina_central == 'realizar_envio':
        realizar_envio()
    elif st.session_state.pagina_central == 'contatos':
        pag_contatos()
    elif st.session_state.pagina_central == 'novo_contato':
        pag_novo_contato()
    elif st.session_state.pagina_central == 'verificar_contatos':
        verificar_contatos()

main()