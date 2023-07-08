from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import sqlite3
from datetime import datetime
import requests
from colorama import Fore, Style

class SeleniumBrowser:
    def __init__(self):
        self.driver = None

    def open_browser(self):
        chrome_options = Options()
        chrome_options.headless = False
        self.driver = webdriver.Chrome(options=chrome_options)
        return self.driver

class Banco:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_connection = None

    def conectar(self):
        self.db_connection = sqlite3.connect(self.db_name)

    def fechar_conexao(self):
        if self.db_connection:
            self.db_connection.close()

    def criar_tabela(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dados (
                nome TEXT PRIMARY KEY,
                preco REAL,
                data_hora TEXT
            )
        ''')
        self.db_connection.commit()

    def inserir_dados(self, nome, preco, data_hora):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO dados (nome, preco, data_hora) VALUES (?, ?, ?)
        ''', (nome, preco, data_hora))
        self.db_connection.commit()

class BuscaSteam:
    def __init__(self, link, db_name):
        self.link = link
        self.navegador = None
        self.banco = Banco(db_name)

    def abrir_navegador(self):
        self.navegador = SeleniumBrowser().open_browser()

    def fechar_navegador(self):
        if self.navegador:
            self.navegador.quit()

    def fazer_scrapping(self):
        if not self.navegador:
            raise Exception("Navegador não foi aberto. Chame o método abrir_navegador() primeiro.")

        self.banco.conectar()
        self.banco.criar_tabela()

        for link in self.link:
            self.navegador.get(link)
            time.sleep(10)
            try:
                preco_element = self.navegador.find_element(By.XPATH, '//*[@id="market_commodity_forsale"]/span[2]')
                preco = preco_element.text
            except NoSuchElementException:
                raise Exception(f"Não foi possível encontrar o preço de ({link}).")
            
            try:
                nome_element = self.navegador.find_element(By.XPATH, '//*[@id="largeiteminfo_item_name"]')
                nome = nome_element.text
            except NoSuchElementException:
                raise Exception(f"Não foi possível encontrar o nome de ({link}).")

            data_hora = datetime.now().strftime('%d/%m/%y - %H:%M:%S')

            print(f'Dados de:  {Fore.BLUE} {nome} {Fore.WHITE} encontrados às {Fore.BLUE} {data_hora} {Style.RESET_ALL}, atualizando no banco...')
            self.banco.inserir_dados(nome, preco, data_hora)

        self.banco.fechar_conexao()
        self.fechar_navegador()
        print(f'{Fore.GREEN}Navegador fechado.{Style.RESET_ALL}')

class Inventario:
    def __init__(self, itens, db_name):
        self.itens = itens
        self.db_name = db_name

    def calcula_valor_por_item(self):

        requisicao = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL')
        cotacao_atual = requisicao.json()
        valor_cotacao = cotacao_atual['USD']['bid']
        valor_cotacao = float(valor_cotacao)
        valor_cotacao = round(valor_cotacao, 2)

        valores = {}
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        for nome_item, quantidade in self.itens.items():
            preco_str = self.obter_valor_por_item(cursor, nome_item)
            preco_float = self.parse_preco(preco_str)        
            quantidade = int(quantidade)
            valor = (preco_float * quantidade) * valor_cotacao
            valor = round(valor, 2)
            
            valores[nome_item] = valor

        conn.close()

        return valores

    def obter_valor_por_item(self, cursor, nome_item):
        cursor.execute("SELECT preco FROM dados WHERE nome LIKE ?", ('%' + nome_item + '%',))
        resultado = cursor.fetchone()

        if resultado:
            return resultado[0]
        else:
            return '$0.00'

    def parse_preco(self, preco):
        preco = preco.replace('$', '')
        preco = preco.replace(',', '')
        return float(preco)