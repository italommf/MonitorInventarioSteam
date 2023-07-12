from tkinter import *
import os
import sqlite3
import datetime
import json
import urllib.request

from classes import Inventario

def btn_clicked():
    print("Button Clicked")

def atualizar_interface():
    texto_multilinhas.delete(0, END)
    cursor.execute("SELECT item_nome FROM inventory ORDER BY id_item ASC")
    dados = cursor.fetchall()
    for linha in dados:
        item_nome = linha[0]
        texto_multilinhas.insert(END, item_nome)

    cursor.execute("SELECT SUM(numero_de_itens) FROM inventory")
    resultado = cursor.fetchone()[0]
    resultado = 0 if resultado is None else resultado
    canvas.itemconfig(texto_numero, text=resultado)

    cursor.execute("SELECT SUM(custo_total) FROM inventory")
    r_custo_total = cursor.fetchone()[0]
    r_custo_total = 0 if r_custo_total is None else round(r_custo_total, 2)
    canvas.itemconfig(custo_total_r, text=f'{r_custo_total} R$')

    cursor.execute("SELECT SUM(valor_total) FROM inventory")
    r_valor_total_b = cursor.fetchone()[0]
    r_valor_total_b = 0 if r_valor_total_b is None else round(r_valor_total_b, 2)
    canvas.itemconfig(valor_brut, text=f'{r_valor_total_b} R$')

    cursor.execute("SELECT SUM(valor_total) FROM inventory")
    result = cursor.fetchone()
    coluna_valor_total = result[0] if result and result[0] else 0
    cursor.execute("SELECT SUM(custo_total) FROM inventory")
    result = cursor.fetchone()
    coluna_custo_total = result[0] if result and result[0] else 0

    if coluna_custo_total != 0:
        multiplicador = (coluna_valor_total * 0.85) / coluna_custo_total
        multiplicador = round(multiplicador, 2)
    else:
        multiplicador = 0

    canvas.itemconfig(mult, text=f'{multiplicador}x')


    cursor.execute("SELECT SUM(valor_total) * 0.85 AS valor_descontado FROM inventory")
    r_valor_total_l = cursor.fetchone()[0]
    r_valor_total_l = 0 if r_valor_total_l is None else round(r_valor_total_l, 2)
    canvas.itemconfig(valor_total_liquido, text=f'{r_valor_total_l} R$')

    lucro = round(r_valor_total_l - r_custo_total, 2)
    canvas.itemconfig(lucro_total, text=f'{lucro} R$')

def insere_atualiza():
    inv.get_dados(nome.get(), custo.get(), int(quantidade.get()), preco_atual.get(), market_link.get())
    atualizar_interface()

def btn_atualizar_inventario():
    inv.update_price()
    atualizar_interface()

def get_icon_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(current_dir, "gui", "icone.ico")
    return icon_path

bd = 'steamInv.db'
inv = Inventario()
inv.banco(bd)
conn = sqlite3.connect(bd)
cursor = conn.cursor()

window = Tk()
window.geometry("600x700")
window.configure(bg="#FFFFFF")
window.iconbitmap(get_icon_path())
window.title('Monitor de Inventário - Brook')
window.resizable(False, False)

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=700,
    width=600,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

background_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "background.png"))
background = canvas.create_image(300.0, 350.0, image=background_img)

img_botao_ver_inventario = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "button_inv.png"))
botao_ver_inventario = Button(
    image=img_botao_ver_inventario,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)
botao_ver_inventario.place(x=367, y=578, width=173, height=44)

img_botao_atualizar = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "button_atualizar_val.png"))
botao_atualizar = Button(
    image=img_botao_atualizar,
    borderwidth=0,
    highlightthickness=0,
    command=btn_atualizar_inventario,
    relief="flat"
)
botao_atualizar.place(x=61, y=609, width=173, height=44)

img_botao_adicionar = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "button_adicionar.png"))
botao_adicionar = Button(
    image=img_botao_adicionar,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insere_atualiza(),
    relief="flat"
)
botao_adicionar.place(x=362, y=261, width=173, height=44)

img_entrada_nome = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox0.png"))
canvas.create_image(533.0, 132.5, image=img_entrada_nome)
nome = StringVar()
entrada_nome = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0,
    textvariable=nome
)
entrada_nome.place(x=480.0, y=124, width=106.0, height=15)

img_entrada_custo = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox1.png"))
canvas.create_image(533.0, 151.5, image=img_entrada_custo)
custo = StringVar()
entrada_custo = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0,
    textvariable=custo
)
entrada_custo.place(x=480.0, y=143, width=106.0, height=15)

img_entrada_quantidade = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox2.png"))
canvas.create_image(533.0, 170.5, image=img_entrada_quantidade)
quantidade = IntVar()
entrada_quantidade = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0,
    textvariable=quantidade
)
entrada_quantidade.place(x=480.0, y=162, width=106.0, height=15)

img_entrada_preco_atual = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox3.png"))
canvas.create_image(533.0, 189.5, image=img_entrada_preco_atual)
preco_atual = IntVar()
entrada_preco_atual = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0,
    textvariable=preco_atual
)
entrada_preco_atual.place(x=480.0, y=181, width=106.0, height=15)

img_entrada_market_link = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox4.png"))
canvas.create_image(487.5, 222.5, image=img_entrada_market_link)
market_link = StringVar()
entrada_market_link = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0,
    textvariable=market_link,
)
entrada_market_link.place(x=389.0, y=214, width=197.0, height=15)

tam_fonte = 10

cursor.execute("SELECT SUM(numero_de_itens) FROM inventory")
resultado = cursor.fetchone()[0]
texto_numero = canvas.create_text(505, 415.5, text=resultado, fill="#ffffff", font=("Alata-Regular", int(tam_fonte)))

cursor.execute("SELECT SUM(custo_total) FROM inventory")
result = cursor.fetchone()

if result is None or result[0] is None:
    r_custo_total = 0
else:
    r_custo_total = round(result[0], 2)

custo_total_r = canvas.create_text(505, 433.5, text=f'{r_custo_total} R$', fill="#ffffff", font=("Alata-Regular", int(tam_fonte)))

cursor.execute("SELECT SUM(valor_total) FROM inventory")
result = cursor.fetchone()
if result[0] is None:
    r_valor_total_b = 0
else:
    r_valor_total_b = round(result[0], 2)
valor_brut = canvas.create_text(505, 450.5, text=f'{r_valor_total_b} R$', fill="#ffffff", font=("Alata-Regular", int(tam_fonte)))

cursor.execute("SELECT SUM(valor_total) FROM inventory")
result = cursor.fetchone()
if result[0] is None:
    r_valor_total_l = 0
else:
    r_valor_total_l = round(result[0], 2)
valor_total_liquido = canvas.create_text(505, 468.5, text=f'{r_valor_total_l * 0.85} R$', fill="#ffffff", font=("Alata-Regular", int(tam_fonte)))

cursor.execute("SELECT SUM(valor_total) FROM inventory")
result = cursor.fetchone()
coluna_valor_total = result[0] if result[0] else 0

cursor.execute("SELECT SUM(custo_total) FROM inventory")
result = cursor.fetchone()
coluna_custo_total = result[0] if result[0] else 0

if coluna_custo_total != 0:
    multiplicador = (coluna_valor_total * 0.85) / coluna_custo_total
    multiplicador = round(multiplicador, 2)
else:
    multiplicador = 0

#print(multiplicador, coluna_valor_total, coluna_custo_total)

mult = canvas.create_text(505, 508.5, text=f'{multiplicador}x', fill="#ffffff", font=("Alata-Regular", int(tam_fonte)))
#print(multiplicador, coluna_valor_total, coluna_custo_total)

if result[0] is None or r_valor_total_b is None:
    lucro = 0
else:
    lucro = round(r_valor_total_l - r_custo_total, 2)
lucro_total = canvas.create_text(505, 491.5, text=f'{lucro} R$', fill="#ffffff", font=("Alata-Regular", int(tam_fonte)))

texto_multilinhas = Listbox(
    window,
    bg="#16202d",
    fg="#FFFFFF",
    bd=0,
    highlightthickness=0,
)
texto_multilinhas.place(x=18.0, y=95, width=265.0, height=426)

cursor.execute("SELECT item_nome, numero_de_itens, custo_por_item, data FROM inventory ORDER BY id_item ASC")
dados = cursor.fetchall()

for linha in dados:
    item_nome = linha[0]
    numero_de_itens = linha[1]
    custo_por_item = linha[2]
    data = linha[3]
    linha_formatada = f"{item_nome}"
    texto_multilinhas.insert(END, linha_formatada)

def apagar_item_selecionado():    
    indice_selecionado = texto_multilinhas.curselection()

    if indice_selecionado:       
        item_selecionado = texto_multilinhas.get(indice_selecionado)
        cursor.execute("DELETE FROM inventory WHERE item_nome=?", (item_selecionado,))
        conn.commit()
        atualizar_interface()
        texto_multilinhas.delete(indice_selecionado)

botao_apagar = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "button_apagar.png"))
b0 = Button(
    image=botao_apagar,
    borderwidth=0,
    highlightthickness=0,
    command=apagar_item_selecionado,
    relief="flat"
)

b0.place(x=61, y=547, width=173, height=44)

atualizar_interface()  # Atualiza os valores da interface com os valores atuais do banco de dados

window.mainloop()
