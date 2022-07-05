from behave import when, then
from pedagio import *

@when("a probabilidade de ser cadastrado for {100} porcento")
def when_tiver_probabilidade_de_ter_cadastro(context, probabilidade_de_ser_cadastrado):
    context.total_motoristas_cadastrados = identificar_cadastro(context.motoristas_reconhecidos, context.motoristas_cadastrados, int(probabilidade_de_ser_cadastrado))

@then("{numero_de_motoristas_cadastrados} motorista ja e cadastrado")
def then_verificar_motoristas_com_cadastro(context, numero_de_motoristas_cadastrados):
    assert context.total_motoristas_cadastrados == int(numero_de_motoristas_cadastrados)

