from classes import Inventario
import tkinter as tk
from tkinter import ttk



#mainframe
window = tk.Tk()
window.title('Monitor de Inventário Steam - by Brook')
window.geometry('600x400')

bd = 'steamInv.db'

inv = Inventario()
inv.banco(bd)

#grid

window.columnconfigure(0, weight = 1) # Coluna 0, 1 coluna de tamanho
window.columnconfigure(1, weight = 1) # Coluna 1, 1 coluna de tamanho
window.columnconfigure(2, weight = 2) # Coluna 2, 2 colunas de tamanho

window.rowconfigure(0, weight = 1)
window.rowconfigure(1, weight = 1)
window.rowconfigure(2, weight = 1)


# o nome tira do hash
nomeitem_str = tk.StringVar()
nomeitem_entry = ttk.Entry(window, textvariable = nomeitem_str)
nomeitem_entry_label = ttk.Label(text = 'Nome do Item (Opcional)')
nomeitem_entry.pack()
nomeitem_entry_label.pack()

# id (auto incrementavel)

#data (botão de data?)

#custo por item
custoporitem_int = tk.StringVar() # mudar para float
custoporitem_entry = ttk.Entry(window, textvariable = custoporitem_int)
custoporitem_entry_label = ttk.Label(text = 'Custo por Item')
custoporitem_entry.pack()
custoporitem_entry_label.pack()

#numero de itens
numerodeitens_int = tk.IntVar()
numerodeitens_entry = ttk.Entry(window, textvariable = numerodeitens_int)
numerodeitens_entry_label = ttk.Label(text = 'Numero De Itens')
numerodeitens_entry.pack()
numerodeitens_entry_label.pack()

#preço atual (pode deixar vazio pq a atualização é chamada pela url)
precoatual_int = tk.IntVar()
precoatual_entry = ttk.Entry(window, textvariable = precoatual_int)
precoatual_entry_label = ttk.Label(text = 'Preço atual do Item')
precoatual_entry.pack()
precoatual_entry_label.pack()

#link
link_str = tk.StringVar()
link_entry = ttk.Entry(window, textvariable = link_str)
link_entry_label = ttk.Label(text = 'Link do Item')
link_entry.pack()
link_entry_label.pack()

#botão ADICIONAR
botao_adicionar = ttk.Button(window, 
                             text = 'Adicionar Item à Tabela',
                             command = lambda: inv.get_dados(nomeitem_str.get(), 
                                                             custoporitem_int.get(), 
                                                             numerodeitens_int.get(), 
                                                             precoatual_int.get(), 
                                                             link_str.get()))
botao_adicionar.pack()

#run
window.mainloop()