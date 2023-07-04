from classes import BuscaSteam, Inventario
from colorama import Style, Fore

caixa_fraturada = 'https://steamcommunity.com/market/listings/730/Fracture%20Case'
apeks = 'https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Apeks%20%28Holo%29%20%7C%20Paris%202023'
pain = 'https://steamcommunity.com/market/listings/730/Sticker%20%7C%20paiN%20Gaming%20%28Holo%29%20%7C%20Paris%202023'
navi = 'https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Natus%20Vincere%20%28Holo%29%20%7C%20Paris%202023'
fluxo = 'https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Fluxo%20%28Holo%29%20%7C%20Paris%202023'
heroic = 'https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Heroic%20%28Holo%29%20%7C%20Paris%202023'
nip = 'https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Ninjas%20in%20Pyjamas%20%28Holo%29%20%7C%20Paris%202023'
gamer_legion = 'https://steamcommunity.com/market/listings/730/Sticker%20%7C%20GamerLegion%20%28Holo%29%20%7C%20Paris%202023'
furia = 'https://steamcommunity.com/market/listings/730/Sticker%20%7C%20FURIA%20(Holo)%20%7C%20Paris%202023'
nine = 'https://steamcommunity.com/market/listings/730/Sticker%20%7C%209INE%20(Holo)%20%7C%20Paris%202023'
fnatic = 'https://steamcommunity.com/market/listings/730/Sticker%20%7C%20Fnatic%20(Holo)%20%7C%20Paris%202023'
capsula_lendas = 'https://steamcommunity.com/market/listings/730/Paris%202023%20Legends%20Sticker%20Capsule'
capsula_desafiantes = 'https://steamcommunity.com/market/listings/730/Paris%202023%20Challengers%20Sticker%20Capsule'
capsula_regionais = 'https://steamcommunity.com/market/listings/730/Paris%202023%20Contenders%20Sticker%20Capsule'

links = [
    caixa_fraturada,        # 2,80 cada - 280 reais - 5 unidades
    #apeks, 
    #pain, 
    #navi, 
    #fluxo,
    #heroic, 
    #nip, 
    #gamer_legion,
    furia,                  # 45,00 cada - 225 reais - 5 unidades
    nine,                   # 20,00 cada - 100 reais - 5 unidades
    fnatic,                 # 20,00 cada - 200 reais - 10 unidades
    capsula_lendas,         # 1,29 cada - 51,60 reais - 40 unidades
    capsula_desafiantes,    # 1,29 cada - 51,60 reais - 40 unidades
    capsula_regionais,      # 1,29 cada - 51,60 reais - 40 unidades
    ]

itens = {
    'Caixa Fraturada': 100,     
    #'Apeks': 5,                 
    #'Pain': 5,
    #'natus': 5,
    #'fluxo':5,
    #'heroic': 5,
    #'ninjas in': 5,
    #'gamerlegion': 5,
    'furia': 5,
    '9ine': 5,
    'fnatic': 10,
    'Lendas do Paris 2023': 40,
    'Desafiantes do Paris 2023': 40,
    'das Desafiantes Regionais do Paris 2023': 40

}

db_name = "dados.db"
busca = BuscaSteam(links, db_name)

try:
    busca.abrir_navegador()
    print(f'\n{Fore.GREEN}Navegador aberto!{Style.RESET_ALL}')
except Exception:
    print(f"{Fore.RED}Não foi possível abrir o navegador{Style.RESET_ALL}")

try:
    print(f'{Fore.GREEN}Inciando raspagem de dados...{Style.RESET_ALL}\n')
    busca.fazer_scrapping()
except Exception:
    print(f"{Fore.RED}Não foi possível fazer o scrapping de dados{Style.RESET_ALL}")

valor_item = Inventario(itens, db_name)
valor = valor_item.calcula_valor_por_item()

valor_total = 0

print('')
for chave, valor_item in valor.items():
    print(f'Item: {Fore.LIGHTBLUE_EX} {chave} {Style.RESET_ALL}- Valor total: {Fore.LIGHTGREEN_EX} R$ {valor_item} {Style.RESET_ALL}')
    valor_total += valor_item

valor_inicial = 959.8 
valor_atual = round(valor_total, 2)

print(f'\nValor inicial: {Fore.GREEN} R$ {valor_inicial} {Style.RESET_ALL}')
print(f'O valor atual dos investimentos é: {Fore.GREEN} R$ {valor_atual} {Style.RESET_ALL}')

if valor_inicial > valor_atual:
    deficit = valor_inicial - valor_atual
    deficit = round(deficit, 2)
    print(f'\nDeficit de {Fore.RED} R${deficit} {Style.RESET_ALL}\n')

else:
    lucro = valor_atual - valor_inicial
    lucro = round(lucro, 2)
    print(f'\nLucro de {Fore.GREEN} R${lucro} {Style.RESET_ALL}\n')