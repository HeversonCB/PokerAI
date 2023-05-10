import random
import os
import pandas as pd
from treys import Card, Evaluator
from tqdm import tqdm

def salvar_simulacao(jogador1, jogador2, mesa, vencedor):
    if vencedor:
        resultado = vencedor['nome']
    else:
        resultado = "Tie"
    
    data = {'Jogador 1': [jogador1['mao']],
            'Jogador 2': [jogador2['mao']],
            'Mesa': [mesa],
            'Vencedor': [resultado]}
    
    df = pd.DataFrame(data)
    df.to_csv('simulacoes.csv', mode='a', index=False, header=not os.path.isfile('simulacoes.csv'))


def gerar_baralho():
    naipes = ['c', 'h', 's', 'd']
    valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    return [valor + naipe for naipe in naipes for valor in valores]

def distribuir_cartas(baralho):
    baralho = list(baralho)  # Converter o baralho para lista
    mao = random.sample(baralho, 2)
    baralho = [carta for carta in baralho if carta not in mao]
    return mao, baralho

def gerar_flop(baralho):
    baralho = list(baralho)  # Converter o baralho para lista
    mesa = random.sample(baralho, 5)
    baralho = [carta for carta in baralho if carta not in mesa]
    return mesa, baralho

def gerar_jogador(baralho, nome):
    jogador = {}
    jogador['nome'] = nome
    jogador['mao'], baralho = distribuir_cartas(baralho)
    jogador['forca_mao'] = 0
    jogador['decisao'] = ' '
    jogador['fichas'] = 5000
    return jogador, baralho

def determinar_forca_mao_jogador(jogador, mesa, evaluator):
    mao = [Card.new(carta) for carta in jogador['mao']]
    cartas_mesa = [Card.new(carta) for carta in mesa]
    forca = evaluator.evaluate(cartas_mesa, mao)
    return forca

def determinar_vencedor(jogador1, jogador2):
    if jogador1['forca_mao'] < jogador2['forca_mao']:
        return jogador1
    elif jogador2['forca_mao'] < jogador1['forca_mao']:
        return jogador2
    
def pergunta1(jogador1, jogador2, pote):
    decisao = input(jogador1['nome'] + ":\n 1 - Apostar\n 2 - Desistir?\n> ")
    if decisao == '1':
        jogador1['decisao'] = 'apostar'
        aposta1 = int(input("Valor: "))
        jogador1['fichas'] -= aposta1
        pote += aposta1
        jogador1, jogador2, pote = pergunta2(jogador1, jogador2, pote, aposta1)
    else:
        jogador1['decisao'] = 'desistir'
        jogador2['fichas'] += pote
        pote = 0
    return jogador1, jogador2, pote

def pergunta2(jogador1, jogador2, pote, aposta):
    decisao = input(jogador2['nome'] + ":\n 1 - Pagar\n 2 - Apostar\n 3 - Desistir?\n> ")
    if decisao == '1':
        jogador2['decisao'] = 'pagar'
        jogador2['fichas'] -= aposta
        pote += aposta
    elif decisao == '2':
        jogador2['decisao'] = 'apostar'
        aposta1 = int(input("Valor: "))
        jogador2['fichas'] -= aposta1
        pote += aposta1
        jogador1, jogador2, pote = pergunta2(jogador2, jogador1, pote, aposta1-aposta)
    else:
        jogador2['decisao'] = 'desistir'
        jogador1['fichas'] += pote
        pote = 0
    return jogador1, jogador2, pote

def jogar_poker(baralho, evaluator):
    jogador1, baralho = gerar_jogador(baralho, 'Jogador 1')
    jogador2, baralho = gerar_jogador(baralho, 'Jogador 2')
    pote = 0

    print("=== JOGADOR 1 ===")
    print("Cartas do Jogador 1:", jogador1['mao'])
    print("=== JOGADOR 2 ===")
    print("Cartas do Jogador 2:", jogador2['mao'])

    jogador1, jogador2, pote = pergunta1(jogador1, jogador2, pote)
    mesa, baralho = gerar_flop(baralho)




    # for turno in range(5):
    #     if turno == 0:

    #         if jogador1['decisao'] == 'apostar' and jogador2['decisao'] == 'apostar':
    #             mesa, baralho = gerar_flop(baralho)

    print("=== MESA ===")
    print("Cartas da Mesa:", mesa)

    print("=== BARALHO ===")
    print("Cartas Restantes no Baralho:", baralho)
    jogador1['forca_mao'] = determinar_forca_mao_jogador(jogador1, mesa, evaluator)
    jogador2['forca_mao'] = determinar_forca_mao_jogador(jogador2, mesa, evaluator)
    vencedor = determinar_vencedor(jogador1, jogador2)

    # salvar_simulacao(jogador1, jogador2, mesa, vencedor)

    return jogador1, jogador2, pote, vencedor

def simular_jogos(num_simulacoes):
    baralho = set(gerar_baralho())
    evaluator = Evaluator()

    resultados = []

    for _ in tqdm(range(num_simulacoes), desc='Simulações'):
        jogador1, jogador2, pote, vencedor = jogar_poker(baralho, evaluator)
        if vencedor:
            vencedor['fichas'] += pote
            print(jogador1['nome'])
            print(jogador1['fichas'])
            print(jogador1['decisao'])
            print("\n")
            print(jogador2['nome'])
            print(jogador2['fichas'])
            print(jogador2['decisao'])
            print(pote)
            print("=== RESULTADO ===")
            print("Vencedor:", vencedor['nome'])
            resultados.append(vencedor)

    return resultados

resultados = simular_jogos(1)

