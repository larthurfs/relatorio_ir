import pandas as pd

def etl_movimentacao(ano, movimentacao, subscricao):
    """
    Recebe os dados pré processados da função relatorioir e faz toda a transformação

    :param ano: Valor com os quatros dígitos do ano como inteiro.
    :param movimentacao: DF pandas
    :param subscricao: DF pandas
    :return:retorna um DF pandas com os dados tratados
    """
    movimentacao['Produto'] = movimentacao['Produto'].str.split(' ', expand=True)[0]
    movimentacao = movimentacao[
        (movimentacao['Movimentação'] == 'Rendimento') |
        (movimentacao['Movimentação'] == 'Dividendo') |
        (movimentacao['Movimentação'] == 'Juros Sobre Capital Próprio')
        ]
    movimentacao = movimentacao.astype({'Data': 'datetime64', 'Valor da Operação': 'float'})
    movimentacao.drop('Quantidade', axis=1, inplace=True)
    movimentacao = movimentacao[movimentacao['Data'].dt.year == ano]
    movimentacao['Data'] = movimentacao['Data'].dt.year
    for k, v in zip(subscricao['Ativo'], subscricao['Cod']):
        movimentacao.loc[movimentacao['Produto'] == v, 'Produto'] = k

    return movimentacao


def relatorioir(ano, dados):
    """
    Pré processamento do arquivo excel e chama a função elt_movimentacao
    :param ano: Valor com os quatros dígitos do ano como inteiro.
    :param dados: Excel
    :return: retorna um df para ser utilizado na função criar_planilha
    """
    subscricao = pd.read_excel(dados, 'Subscrição')
    movimentacao = pd.read_excel(dados, 'Movimentação')
    cnpj_nome = pd.read_excel(dados, 'cnpj')

    movimentacao = etl_movimentacao(ano, movimentacao, subscricao)

    relatorio = movimentacao.groupby(['Produto', 'Movimentação', 'Data'], as_index=False).sum()
    relatorio = relatorio.merge(cnpj_nome, left_on='Produto', right_on='Ativo', how='left').drop('Ativo', axis=1)
    return relatorio