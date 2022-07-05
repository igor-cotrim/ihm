from behave import when, then
from pedagio import *

@when("a probabilidade de ser debitado for {probabilidade_cobranca} porcento")
def when_tiver_probabilidade_de_ser_debitado(context, probabilidade_cobranca):
    context.total_cobrancas = debitar_valor(context.motoristas_reconhecidos, context.motoristas_cadastrados, int(probabilidade_cobranca))

@then("{numero_de_motoristas_debitados} motorista foi debitado")
def then_verificar_motoristas_foi_debitado(context, numero_de_motoristas_debitados):
    assert context.total_cobrancas == int(numero_de_motoristas_debitados)

