from behave import when, then
from pedagio import *

@when("a probabilidade de ser liberado for {probabilidade_de_liberacao} porcento")
def when_tiver_probabilidade_de_ser_liberado(context, probabilidade_de_liberacao):
    context.total_liberacoes = liberar_motorista(context.motoristas_reconhecidos, int(probabilidade_de_liberacao))

@then("{numero_de_motoristas_liberados} motorista foi liberado")
def then_verificar_motoristas_com_cadastro(context, numero_de_motoristas_liberados):
    assert context.total_liberacoes == int(numero_de_motoristas_liberados)

