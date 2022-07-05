from behave import when, then
from pedagio import *

@when("a probabilidade de ter credito for {probabilidade_de_ter_credito} porcento")
def when_tiver_probabilidade_de_ter_credito(context, probabilidade_de_ter_credito):
    context.total_verificacao_de_creditos = verificar_creditos(context.motoristas_reconhecidos, context.motoristas_cadastrados, int(probabilidade_de_ter_credito))

@then("{numero_de_motoristas_com_creditos} motorista foi indentificado com creditos no sistema")
def then_motoristas_tem_credito(context, numero_de_motoristas_com_creditos):
    assert context.total_verificacao_de_creditos == int(numero_de_motoristas_com_creditos)

