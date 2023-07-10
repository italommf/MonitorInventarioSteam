import datetime
import json
import sqlite3
import time
import urllib.request

class Inventario:

    def __init__(self):
        self.item_id = None
        self.item_link = None
        self.data = None
        self.custo_por_item = None
        self.numero_de_itens = None
        self.preço_atual = None
        self.item_nome = None
        self.valor_total = None
        self.custo_total = None
        self.porcentagem_retorno_total = None
        self.retorno_total = None

        self.cursor = None
        self.conexao = None

    def banco(self, nome_banco_de_dados):

        self.conexao = sqlite3.connect(nome_banco_de_dados)
        self.cursor = self.conexao.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS inventory "
                            "(id_item INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "data STRING NOT NULL, "
                            "item_nome TEXT NOT NULL, "
                            "custo_por_item REAL NOT NULL, "
                            "numero_de_itens INTEGER NOT NULL, "
                            "preço_atual REAL NOT NULL, "
                            "custo_total REAL NOT NULL, "
                            "valor_total REAL NOT NULL, "
                            "porcentagem_retorno_total REAL NOT NULL, "
                            "retorno_total REAL, "
                            "item_link TEXT NOT NULL)")

        return self.cursor


    def get_dados(self, nome, custoporitem, quantidade, p_atual, link):

        self.nome = nome
        self.custoporitem = custoporitem
        self.custoporitem = self.custoporitem.replace(',','.')
        self.custoporitem = float(self.custoporitem)
        self.quantidade = quantidade
        self.p_atual = p_atual
        self.link = link

        #data (get da inferface?)
        data_atual = datetime.now().strftime('%d/%m/%Y')


        #item_nome (if vazio, tirar da url, else, usa o nome informado)
        if self.nome == '':
            hash_link = link[47:]
            self.nome = hash_link.replace("%20", " ").replace("%7C", "|").replace("%28", "(").replace("%29", ")").replace("%26", "&")
            print('nome vazio, teste de tipo abaixo:')
            print(type(self.nome))
        else:
            print('nome preenchido, teste de tipo abaixo:')
            print(type(self.nome))

        #preço_atual (usar o request)
        hash_link = link[47:]
        url_destino = 'https://steamcommunity.com/market/priceoverview/?appid=730&currency=7&market_hash_name=' + hash_link
        url_request = urllib.request.urlopen(url_destino)
        data = json.loads(url_request.read().decode())

        self.p_atual = str(data.get('lowest_price'))
        self.p_atual = float(self.p_atual.replace('R$', '').replace(',', '.'))

        #custo_total (numero_de_itens * custo_por_item)
        custo_total = self.quantidade * self.custoporitem

        #valor_total (numero_de_itens * preço_atual)
        valor_total = self.quantidade * self.p_atual

        #porcentagem_retorno_total - round(((preço_atual - custo_por_item) / custo_por_item) * 100, 2)
        porcentagem_retorno_total = round(((self.p_atual - self.custoporitem) / self.custoporitem) * 100, 2)

        #retorno_total (valor_total - custo_total)
        retorno_total = valor_total - custo_total

        print(f'nome:{self.nome}')
        print(f'custo por item: {self.custoporitem}')
        print(f'quantidade: {self.quantidade}')
        print(f'preço atual: {self.p_atual}')
        print(f'link: {self.link}')
        print(f'custo total: {custo_total}')
        print(f'valor total: {valor_total}')
        print(f'porentagem de retorno total: {porcentagem_retorno_total}')
        print(f'retorno total: {retorno_total}')

        query = 'INSERT INTO inventory (data, item_nome, custo_por_item, numero_de_itens, preço_atual, custo_total, valor_total, porcentagem_retorno_total, retorno_total, item_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        self.cursor.execute(query, (data_atual, self.nome, self.custoporitem, self.quantidade, self.p_atual, custo_total, valor_total, porcentagem_retorno_total, retorno_total, self.link))
        self.cursor.connection.commit()
    