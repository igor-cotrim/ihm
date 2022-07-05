from behave import *
from pedagio import *

@given("o ambiente de reconhecimento foi preparado com sucesso")
def given_ambiente_reconhecimento_preparado(context):
  context.configuracao, context.motoristas_reconhecidos, context.motoristas_cadastrados, context.mototoristas_com_creditos, context.mototoristas_para_liberar = preparar()

  context.motoristas_reconhecidos = {}

  assert context.configuracao != None

@when("a foto {foto_motorista} de um motorista for capturada")
def when_foto_motorista_capturada(context, foto_motorista):
  motorista = simular_motorista(foto_motorista)
  context.reconhecido, context.motorista_indentificado = reconhecer_motorista(motorista, context.configuracao)

  assert True

@then("um motorista deve ser reconhecido")
def then_motorista_reconhecido(context):
  id_atendimento = secrets.token_hex(nbytes=16).upper()
  context.motoristas_reconhecidos[id_atendimento] = context.motorista_indentificado

  assert context.reconhecido is True