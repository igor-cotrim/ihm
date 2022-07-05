from behave import when, then
from pedagio import *

@when("a probabilidade de ser liberado for {100} porcento")
def when_tiver_probabilidade_de_ser_liberado(context, probabilidade_de_liberacao):
    context.total_liberacoes = liberar_motorista(context.mototoristas_para_liberar, int(probabilidade_de_liberacao))

@then("{numero_de_motoristas_liberados} motorista foi liberado")
def then_verificar_motoristas_com_cadastro(context, numero_de_motoristas_liberados):
    assert context.total_liberacoes == int(numero_de_motoristas_liberados)

