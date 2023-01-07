from django.urls import path

from apps.core.views import home, criarrelatorio, modelo_excel

urlpatterns = [
    path('', home, name='home'),
    path('criarrelatorio', criarrelatorio, name='criarrelatorio'),
    path('modelorelatorio', modelo_excel, name='modelorelatorio'),
]