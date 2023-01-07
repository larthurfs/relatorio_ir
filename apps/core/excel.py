import xlsxwriter as xls
import xlsxwriter.utility as xl_util
import pandas as pd

def criar_planilha(df, dados, output):
    print('aqui excel')
    """

    :param df: Recebe um df pandas para ser utilizado como dados
    :param dados: planilha excel
    :param output:
    :return: Relatório para utilização no imposto de renda
    """
    wb = xls.Workbook(output)

    pesquisa = wb.add_worksheet("pesquisa")
    relatorio = wb.add_worksheet("relatorio")  # Relatório
    aux = wb.add_worksheet("aux")
    plan_pesquisa(pesquisa, wb)
    plan_relatorio(relatorio, df, wb)
    plan_aux(aux, dados, wb)



    wb.close()


def plan_relatorio(relatorio, df, wb):
    relatorio.add_table(xl_util.xl_range_abs(0, 0, len(df), 5),
                        {'name': 'relatorio', 'style': None, 'columns':
                            [
                                {'header': 'Produto'},
                                {'header': 'Movimentação'},
                                {'header': 'Data'},
                                {'header': 'Valor da Operação'},
                                {'header': 'Nome'},
                                {'header': 'CNPJ'}
                            ]})

    relatorio.write_row(0, 0, ['Produto', 'Movimentação', 'Data', 'Valor da Operação', 'Nome', 'CNPJ'],
                        wb.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '11'}))

    row_num = 1

    for dado in range(len(df)):
        if row_num % 2 == 0:
            relatorio.write_row(row_num,0, [df['Produto'].iloc[dado], df['Movimentação'].iloc[dado], df['Data'].iloc[dado],
                df['Valor da Operação'].iloc[dado], df['nome'].iloc[dado], df['cnpj'].iloc[dado]],
                wb.add_format({'align': 'center', 'valign': 'vcenter'}))
        else:
            relatorio.write_row(row_num, 0, [df['Produto'].iloc[dado], df['Movimentação'].iloc[dado], df['Data'].iloc[dado],
                                 df['Valor da Operação'].iloc[dado], df['nome'].iloc[dado], df['cnpj'].iloc[dado]],
                                 wb.add_format({'bg_color': '#bfbfbf', 'align': 'center', 'valign': 'vcenter'}))

        row_num += 1

    relatorio.hide_gridlines(2)
    relatorio.set_column('A:A', 12.00)
    relatorio.set_column('B:B', 24.43)
    relatorio.set_column('C:C', 8.86)
    relatorio.set_column('D:D', 21.29)
    relatorio.set_column('E:E', 47.00)
    relatorio.set_column('F:F', 17.29)
    relatorio.set_row(0, 40.0)
    relatorio.set_tab_color('green')
    relatorio.hide()


def plan_pesquisa(pesquisa, wb):
    wb.define_name('valor_procurado', '=Relatório!$P$5')

    pesquisa.merge_range(1, 1, 1, 9, "RELATÓRIO IR - ATIVOS",
                          wb.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '22', 'bg_color': '#bfbfbf'}))

    pesquisa.write(3, 1, "Ativo:",
                    wb.add_format(
                        {'bold': True, 'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 2,
                         'top': 2, 'bottom': 1, 'right': 1, 'bottom_color': 'white', 'right_color': 'white',
                         'top_color': 'gray', 'left_color': 'gray'}))


    pesquisa.merge_range(3, 2, 3, 3, "",
                          wb.add_format(
                              {'bold': True, 'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 1,
                               'top': 2, 'bottom': 1, 'right': 1, 'bottom_color': 'white', 'right_color': 'white',
                               'top_color': 'gray', 'left_color': 'white'}))

    pesquisa.data_validation('C4', {'validate': 'list', 'source': '=OFFSET(aux!A2,0,0,COUNTA(Aux!A:A),1)'})

    pesquisa.write(3, 4, '=IFERROR(IF(VLOOKUP(pesquisa!$C$4,aux!$A:$B,2,0)="A","Dividendo:","Rendimento:"),"Dividendo:")', wb.add_format(
        {'bold': True, 'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 1,
         'top': 2, 'bottom': 1, 'right': 1, 'bottom_color': 'white', 'right_color': 'white',
         'top_color': 'gray', 'left_color': 'white'}))

    pesquisa.merge_range(3, 5, 3, 6, '=IFERROR(IF(VLOOKUP(pesquisa!$C$4,aux!$A:$B,2,0)="A", sumifs(relatorio!D:D,relatorio!A:A,pesquisa!$C$4,relatorio!B:B,pesquisa!$L$1),sumifs(relatorio!D:D,relatorio!A:A,pesquisa!$C$4,relatorio!B:B,pesquisa!$K$1)),"")',
                    wb.add_format(
                        {'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 1,
                         'top': 2, 'bottom': 1, 'right': 1, 'bottom_color': 'white', 'right_color': 'white',
                         'top_color': 'gray', 'left_color': 'white', 'align': 'center', 'valign': 'vcenter'}))

    pesquisa.write(3, 7, "Juros:",
                    wb.add_format(
                        {'bold': True, 'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 1,
                         'top': 2, 'bottom': 1, 'right': 1, 'bottom_color': 'white', 'right_color': 'white',
                         'top_color': 'gray', 'left_color': 'white'}))

    pesquisa.merge_range(3, 8, 3, 9,'=IFERROR(IF(VLOOKUP(pesquisa!$C$4,aux!$A:$B,2,0)="A", sumifs(relatorio!D:D,relatorio!A:A,pesquisa!$C$4,relatorio!B:B,pesquisa!$M$1),"-"),"")',
                          wb.add_format(
                              {'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 1,
                               'top': 2, 'bottom': 1, 'right': 2, 'bottom_color': 'white', 'right_color': 'gray',
                               'top_color': 'gray', 'left_color': 'white', 'align': 'center', 'valign': 'vcenter'}))

    pesquisa.write(4, 1, "Nome:",
                   wb.add_format(
                       {'bold': True, 'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 2,
                        'top': 1, 'bottom': 2, 'right': 1, 'bottom_color': 'gray', 'right_color': 'white',
                        'top_color': 'white', 'left_color': 'gray'}))


    pesquisa.merge_range(4, 2, 4, 6, "=IFERROR(VLOOKUP(pesquisa!$C$4,relatorio!$A:$F,5,0),"")",
                          wb.add_format(
                              {'bold': True, 'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 1,
                               'top': 1, 'bottom': 2, 'right': 1, 'bottom_color': 'gray', 'right_color': 'white',
                               'top_color': 'white', 'left_color': 'white'}))

    pesquisa.write(4, 7, "CNPJ:",
                    wb.add_format(
                        {'bold': True, 'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 1,
                         'top': 1, 'bottom': 2, 'right': 1, 'bottom_color': 'gray', 'right_color': 'white',
                         'top_color': 'white', 'left_color': 'white'}))

    pesquisa.merge_range(4, 8, 4, 9,'=IFERROR(VLOOKUP(pesquisa!$C$4,relatorio!$A:$F,6,0),"")',
                    wb.add_format(
                        {'font_color': 'white', 'bg_color': '#0066cc', 'font_size': '11', 'left': 1,
                         'top': 1, 'bottom': 2, 'right': 2, 'bottom_color': 'gray', 'right_color': 'gray',
                         'top_color': 'white', 'left_color': 'white', 'align': 'center', 'valign': 'vcenter'}))

    pesquisa.write(0, 10, "Rendimento",
                   wb.add_format(
                       {'bold': True, 'font_color': 'white'}))
    pesquisa.write(0, 11, "Dividendo",
                   wb.add_format(
                       {'bold': True, 'font_color': 'white'}))
    pesquisa.write(0, 12, "Juros Sobre Capital Próprio",
                   wb.add_format(
                       {'bold': True, 'font_color': 'white'}))

    pesquisa.write(7, 1, 'Orientação', wb.add_format({'bold': True}))


    pesquisa.merge_range(8, 1, 13, 9, "", wb.add_format(
        {'bold': False, 'font_color': 'black', 'border': 1, 'align': 'center',
         'valign': 'vcenter'}))



    #nome = f'relatorio.xlsm'
    pesquisa.hide_gridlines(2)
    pesquisa.set_column('A:A', 1.00)
    pesquisa.set_column('B:B', 6.30)
    pesquisa.set_column('C:C', 8.43)
    pesquisa.set_column('D:D', 8.43)
    pesquisa.set_column('E:E', 11.86)
    pesquisa.set_column('F:F', 8.43)
    pesquisa.set_column('G:G', 8.43)
    pesquisa.set_column('H:H', 5.50)
    pesquisa.set_column('I:I', 8.43)
    pesquisa.set_column('J:J', 8.43)

    pesquisa.set_row(2, 8.25)

    #relatorio.hide()

def plan_aux(aux, dados, wb):
    df = pd.read_excel(dados, 'cnpj')
    aux.add_table(xl_util.xl_range_abs(0, 0, len(df), 1),
                        {'name': 'ativos', 'style': None, 'columns':
                            [
                                {'header': 'Ativo'},
                                {'header': 'Tipo'},

                            ]})

    aux.write_row(0, 0, ['Ativo', 'Tipo'],
                        wb.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '11'}))

    row_num = 1

    for dado in range(len(df)):
        aux.write_row(row_num, 0, [df['Ativo'].iloc[dado], df['Tipo'].iloc[dado]],
                      wb.add_format({'align': 'center', 'valign': 'vcenter'}))


        row_num += 1

    aux.hide_gridlines(2)
    aux.set_column('A:A', 20.00)
    aux.set_column('B:B', 20.00)
    aux.set_tab_color('orange')
    aux.hide()


def criar_planilha_modelo(output):
    """
    Retorna o modelo de excel para input de dados a serem tratadosa e
    """
    wb = xls.Workbook(output)

    movimentacao = wb.add_worksheet("Movimentação")
    cnpj = wb.add_worksheet("cnpj")  # Relatório
    subscricao = wb.add_worksheet("Subscrição")

    plan_cnpj(cnpj, wb)
    plan_subscricao(subscricao, wb)

    wb.close()


def plan_cnpj(cnpj, wb):
    cnpj.add_table(xl_util.xl_range_abs(0, 0, 1, 3),
                  {'name': 'cnpj', 'style': None, 'columns':
                      [
                          {'header': 'Ativo'},
                          {'header': 'nome'},
                          {'header': 'cnpj'},
                          {'header': 'Tipo'},

                      ]})

    cnpj.write_row(0, 0, ['Ativo', 'nome', 'cnpj', 'Tipo'],
                  wb.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '11'}))

    cnpj.set_column('A:A', 10.00)
    cnpj.set_column('B:B', 47.00)
    cnpj.set_column('C:C', 17.29)
    cnpj.set_column('D:D', 9.00)


def plan_subscricao(subscricao, wb):
    subscricao.add_table(xl_util.xl_range_abs(0, 0, 1, 1),
                   {'name': 'subscricao', 'style': None, 'columns':
                       [
                           {'header': 'Ativo'},
                           {'header': 'Cod'},

                       ]})

    subscricao.write_row(0, 0, ['Ativo', 'Cod'],
                   wb.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '11'}))

    subscricao.set_column('A:A', 10.00)
    subscricao.set_column('B:B', 10.00)
