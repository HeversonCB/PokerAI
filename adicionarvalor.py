import pandas as pd
from tqdm import tqdm

def atualizar_maos():
    df_simulacoes = pd.read_csv('teste.csv')
    df_maos = pd.read_csv('maos.csv')

    for _, row in tqdm(df_simulacoes.iterrows(), total=len(df_simulacoes)):
        vencedor = row['Vencedor']
        jogador1 = eval(row['Jogador 1'])
        jogador2 = eval(row['Jogador 2'])
        mesa = eval(row['Mesa'])

        mao_vencedor = jogador1 if vencedor == 'Jogador 1' else jogador2

        if vencedor == 'Tie':
            continue

        par_cartas = [mao_vencedor, mao_vencedor[::-1]]  # Par de cartas e seu inverso

        filtro = (df_maos['Carta 1'].isin(par_cartas[0])) & (df_maos['Carta 2'].isin(par_cartas[0]))
        filtro |= (df_maos['Carta 1'].isin(par_cartas[1])) & (df_maos['Carta 2'].isin(par_cartas[1]))

        if df_maos.loc[filtro].empty:
            continue

        df_maos.loc[filtro, 'Valor'] += 1

    df_maos.to_csv('maos.csv', index=False)

# Chamar a função para atualizar os valores das mãos
# atualizar_maos()

def reordenar_maos():
    df_maos = pd.read_csv('maos.csv')
    df_maos = df_maos.sort_values(by='Valor', ascending=False)
    df_maos.to_csv('maos.csv', index=False)

# Chamar a função para reordenar o arquivo maos.csv
reordenar_maos()
