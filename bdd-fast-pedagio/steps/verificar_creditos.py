from behave import when, then
from pedagio import *

@when("a probabilidade de ter credito for {100} porcento")
def when_tiver_probabilidade_de_ter_credito(context, probabilidade_de_ter_credito):
    context.total_verificacao_de_creditos = verificar_creditos(context.motoristas_cadastrados, context.mototoristas_com_creditos, int(probabilidade_de_ter_credito))

@then("{numero_de_motoristas_tem_creditos} motorista tem credito")
def then_verificar_motoristas_tem_credito(context, numero_de_motoristas_com_creditos):
    assert context.total_verificacao_de_creditos == int(numero_de_motoristas_com_creditos)

