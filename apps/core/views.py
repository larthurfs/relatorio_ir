from django.shortcuts import render, redirect
from django.core.files import File
from django.http import HttpResponse
from django.contrib import messages
import io

from apps.core.excel import criar_planilha, criar_planilha_modelo
from apps.core.relatorioir import relatorioir
from django.http import HttpResponseRedirect


def home(request):
    return render(request, 'index.html')


def criarrelatorio(request):
    ano = request.POST.get("ano")
    #print(ano)
    if request.method == 'POST':
        dados = File(request.FILES['excel_file'])
        if not dados.name.endswith('xlsx'):
            messages.info(request, 'Formato de arquivo incompativel! Só é aceito arquivo .xlsx')
            return render(request, 'index.html')


        output = io.BytesIO()
        try:
            df = relatorioir(int(ano), dados)
            criar_planilha(df, dados, output, request)
        except:
            erro = 'Verifique os nomes das abas de sua planilha! Subscrição, Movimentação e cnpj'
            messages.error(request, erro)

            return render(request, 'index.html')

        output.seek(0)

        filename = 'relatorio_ir.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response

    return redirect('home')


def modelo_excel(request):
    if request.method == 'GET':
        output = io.BytesIO()

        criar_planilha_modelo(output)

        output.seek(0)

        filename = 'mode_relatorio.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

    return render(request, 'index.html')