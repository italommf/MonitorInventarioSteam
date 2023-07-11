from tkinter import *
from classes import Inventario
import os
import sqlite3
import time


def btn_clicked():
    print("Button Clicked")

window = Tk()
window.geometry("600x700")
window.configure(bg="#FFFFFF")

def atualizar_interface():
    # Atualizar a caixa de texto com os dados do banco de dados
    texto_multilinhas.delete(0, END)  # Limpar a caixa de texto
    cursor.execute("SELECT item_nome FROM inventory ORDER BY id_item ASC")
    dados = cursor.fetchall()
    for linha in dados:
        item_nome = linha[0]
        texto_multilinhas.insert(END, item_nome)

    # Atualizar as informações numéricas
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

    cursor.execute("SELECT SUM(valor_total / custo_total) * 0.85 AS valor_descontado FROM inventory")
    multiplicador = cursor.fetchone()[0]
    multiplicador = 0 if multiplicador is None else round(multiplicador, 2)
    canvas.itemconfig(mult, text=f'{multiplicador}x')

    cursor.execute("SELECT SUM(valor_total) * 0.85 AS valor_descontado FROM inventory")
    r_valor_total_l = cursor.fetchone()[0]
    r_valor_total_l = 0 if r_valor_total_l is None else round(r_valor_total_l, 2)
    canvas.itemconfig(valor_total_liquido, text=f'{r_valor_total_l} R$')

    lucro = round(r_valor_total_l - r_custo_total, 2)
    canvas.itemconfig(lucro_total, text=f'{lucro} R$')


bd = 'steamInv.db'

inv = Inventario()
inv.banco(bd)
conn = sqlite3.connect(bd)
cursor = conn.cursor()

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


button_ver_inv = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "button_inv.png"))
b2 = Button(
    image=button_ver_inv,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)

b2.place(x=367, y=578, width=173, height=44)

def btn_atualizar_inventario():
    inv.atualizar_precos()
    atualizar_interface()

button_atualizar = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "button_atualizar_val.png"))
b3 = Button(
    image=button_atualizar,
    borderwidth=0,
    highlightthickness=0,
    command=btn_atualizar_inventario,
    relief="flat"
)

b3.place(x=61, y=609, width=173, height=44)

entry0_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox0.png"))
entry0_bg = canvas.create_image(533.0, 132.5, image=entry0_img)
nome = StringVar()
entry0 = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0,
    textvariable=nome
)

entry0.place(x=480.0, y=124, width=106.0, height=15)


entry1_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox1.png"))
entry1_bg = canvas.create_image(533.0, 151.5, image=entry1_img)
custo = StringVar()
entry1 = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0,
    textvariable=custo
)

entry1.place(x=480.0, y=143, width=106.0, height=15)

entry2_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox2.png"))
entry2_bg = canvas.create_image(533.0, 170.5, image=entry2_img)
quantidade = IntVar()
entry2 = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0,
    textvariable=quantidade
)

entry2.place(x=480.0, y=162, width=106.0, height=15)

entry3_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox3.png"))
entry3_bg = canvas.create_image(533.0, 189.5, image=entry3_img)
preco_atual = IntVar()
entry3 = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0,
    textvariable=preco_atual
)

entry3.place(x=480.0, y=181, width=106.0, height=15)

entry4_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox4.png"))
entry4_bg = canvas.create_image(487.5, 222.5, image=entry4_img)
market_link = StringVar()
entry4 = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0,
    textvariable=market_link, 
)

entry4.place(x=389.0, y=214, width=197.0, height=15)

button_adicionar = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "button_adicionar.png"))

def insere_atualiza():
    inv.get_dados(nome.get(), custo.get(), quantidade.get(), preco_atual.get(), market_link.get())
    atualizar_interface()

b1 = Button(
    image=button_adicionar,
    borderwidth=0,
    highlightthickness=0,
    command = lambda: insere_atualiza(),
    relief="flat")
                
b1.place(x=362, y=261, width=173, height=44)

tam_fonte = 10

# numero total de itens
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


# Valor BRUTO total do inventário
cursor.execute("SELECT SUM(valor_total) FROM inventory")
result = cursor.fetchone()
if result[0] is None:
    r_valor_total_b = 0
else:
    r_valor_total_b = round(result[0], 2)
valor_brut = canvas.create_text(505, 450.5, text=f'{r_valor_total_b} R$', fill="#ffffff", font=("Alata-Regular", int(tam_fonte)))

# Multiplicador do valor
cursor.execute("SELECT SUM(valor_total / custo_total) * 0.85 AS valor_descontado FROM inventory")
result = cursor.fetchone()
if result[0] is None:
    multiplicador = 0
else:
    multiplicador = round(result[0], 2)
mult = canvas.create_text(505, 508.5, text=f'{multiplicador}x', fill="#ffffff", font=("Alata-Regular", int(tam_fonte)))

# Valor líquido total do inventário
cursor.execute("SELECT SUM(valor_total) * 0.85 AS valor_descontado FROM inventory")
result = cursor.fetchone()
if result[0] is None:
    r_valor_total_l = 0
else:
    r_valor_total_l = round(result[0], 2)
valor_total_liquido = canvas.create_text(505, 468.5, text=f'{r_valor_total_l} R$', fill="#ffffff", font=("Alata-Regular", int(tam_fonte)))

# Lucro
if result[0] is None or r_valor_total_b is None:
    lucro = 0
else:
    lucro = round(r_valor_total_l - r_valor_total_b, 2)
lucro_total = canvas.create_text(505, 491.5, text=f'{lucro} R$', fill="#ffffff", font=("Alata-Regular", int(tam_fonte)))

# Criação da caixa de texto
texto_multilinhas = Listbox(
    window,
    bg="#16202d",
    fg="#FFFFFF",
    bd=0,
    highlightthickness=0,
)
texto_multilinhas.place(x=18.0, y=95, width=265.0, height=426)

# Recuperar os dados do banco de dados
cursor.execute("SELECT item_nome, numero_de_itens, custo_por_item, data FROM inventory ORDER BY id_item ASC")
dados = cursor.fetchall()

# Inserção dos dados na caixa de texto
for linha in dados:
    item_nome = linha[0]
    numero_de_itens = linha[1]
    custo_por_item = linha[2]
    data = linha[3]

    # Formatar a linha de dados
    linha_formatada = f"{item_nome}"

    # Inserir a linha formatada na caixa de texto
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

def get_icon_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(current_dir, "gui", "icone.ico")
    return icon_path

window.iconbitmap(get_icon_path())
window.title('Monitor de Inventário - Brook')
window.resizable(False, False)
window.mainloop()
