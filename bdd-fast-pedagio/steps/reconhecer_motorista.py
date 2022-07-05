from behave import given, when, then
from pedagio import *

@given("o ambiente seja preparado com sucesso")
def given_ambiente_reconhecimento_preparado(context):
  preparado, context.configuracao = preparar()

  context.motoristas_reconhecidos = {}
  context.motoristas_cadastrados = {}
  context.mototoristas_com_creditos = {}
  context.mototoristas_para_liberar = {}

  assert preparado is True

@when("a foto {foto} de um motorista for capturada")
def when_foto_capturada(context, foto):
  motorista = simular_motorista(foto)
  context.reconhecido, context.motorista = indentificar_motorista(motorista, context.configuracao)

  assert True

@then("um motorista deve ser reconhecido")
def then_motorista_reconhecido(context):
  id_atendimento = secrets.token_hex(nbytes=16).upper()
  context.motoristas_reconhecidos[id_atendimento] = context.motorista

  assert context.reconhecido is True

@then("nenhum motorista deve ser reconhecido")
def then_motorista_nao_reconhecido(context):
  assert context.reconhecido is False