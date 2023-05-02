import pandas as pd

def gerar_baralho():
    naipes = ['c', 'h', 's', 'd']
    valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    return [valor + naipe for naipe in naipes for valor in valores]

def gerar_pares(baralho):
    pares = []
    for i in range(len(baralho)):
        for j in range(i+1, len(baralho)):
            pares.append((baralho[i], baralho[j], 0))
    return pares

baralho = gerar_baralho()
pares = gerar_pares(baralho)

df = pd.DataFrame(pares, columns=['Carta 1', 'Carta 2', 'Valor'])
df.to_csv('maos.csv', index=False)