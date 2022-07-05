import face_recognition
import secrets
import random
import json

ARQUIVO_CONFIGURACAO = "./configuracao.json"

FOTOS_MOTORISTAS = [
  "./faces/fabio1.jpg",
  "./faces/fabio2.jpg",
  "./faces/fabio3.jpg",
  "./faces/faustao1.jpg",
  "./faces/faustao2.jpg",
  "./faces/faustao3.jpg",
  "./faces/lazaro1.jpg",
  "./faces/lazaro2.jpg",
  "./faces/lazaro3.jpg",
  "./faces/rodrigo1.jpg",
  "./faces/rodrigo2.jpg",
  "./faces/rodrigo3.jpg"
]

PROBABILIDADE_DE_SER_CADASTRADO = 60
PROBABILIDADE_DE_TER_CREDITO = 70 
PROBABILIDADE_COBRANCA = 50
PROBABILIDADE_DE_LIBERACAO = 30

# CAPACIDADE_MAXIMA_ESTACIONAMENTO = 10

TEMPO_ENTRE_MOTORISTAS = 300
TEMPO_RECONHECIMENTO_CADASTRO = 60
TEMPO_HA_CREDITO = 60
TEMPO_VERIFICACAO_DE_CREDITOS = 60
TEMPO_DEBITAR_VALOR = 30
TEMPO_LIBERACAO = 50


def preparar():
  global configuracao

  configuracao = None
  with open(ARQUIVO_CONFIGURACAO, "r") as arquivo_configuracao:
    configuracao = json.load(arquivo_configuracao)

    if configuracao:
      print("---------------------------------------------------------------")
      print("------------------------FAST-PEDÁDIO---------------------------")
      print("---------------------------------------------------------------")
      print("Arquivos de configuração sendo carregados")
      print("versão:", configuracao["versao"])
      print("---------------------------------------------------------------")

  return (configuracao != None), configuracao


def simular_motorista(foto):
  motorista = {
    "foto": foto,
    "cadastrado": None
  }

  return motorista


def indentificar_motorista(motorista, configuracao):
  print("iniciando o reconhecimento de motoristas...")
  foto_motorista = face_recognition.load_image_file(motorista["foto"])
  encoding_foto_motorista = face_recognition.face_encodings(foto_motorista)[0]

  reconhecido = False
  for motoristas in configuracao["motoristas"]:
    fotos_banco = motoristas["fotos"]
    total_reconhecimentos = 0

    for foto in fotos_banco:
      foto_banco = face_recognition.load_image_file(foto)
      encoding_foto_banco = face_recognition.face_encodings(foto_banco)[0]

      foto_reconhecida = face_recognition.compare_faces([encoding_foto_motorista], encoding_foto_banco)[0]
      if foto_reconhecida: 
        total_reconhecimentos += 1

    if total_reconhecimentos/len(fotos_banco) > 0.7:
      reconhecido = True

      motorista["motoristas"] = {}
      motorista["motoristas"]["nome"] = motoristas["nome"]
      motorista["motoristas"]["status"] = motoristas["status"]
      motorista["motoristas"]["cobranca"] = motoristas["cobranca"]

  return reconhecido, motorista


def imprimir_motorista(motorista_indentificado):
  print("****************************************************************")
  print("nome:", motorista_indentificado["motoristas"]["nome"])
  print("status:", motorista_indentificado["motoristas"]["status"])
  print("cobrança:", motorista_indentificado["motoristas"]["cobranca"])
  print("****************************************************************")


def reconhecer_motorista(motoristas_reconhecidos):
  motorista = simular_motorista()
  reconhecido, motorista_indentificado = indentificar_motorista(motorista)

  if reconhecido:
    id_atendimento = secrets.token_hex(nbytes=16).upper()
    motoristas_reconhecidos[id_atendimento] = motorista_indentificado

    print("---------------------------------------------------------------")
    print("motorista reconhecido, imprimindo dados do motorista...")
    imprimir_motorista(motorista_indentificado)
  else:
    print("---------------------------------------------------------------")
    print("motorista não reconhecido")


def identificar_cadastro(motoristas_reconhecidos, motoristas_cadastrados, probabilidade_de_ser_cadastrado):
  total_motoristas_cadastrados = 0

  if len(motoristas_reconhecidos):
    for id_atendimento, motorista in list(motoristas_reconhecidos.items()):
      cadastro_reconhecido = (random.randint(1, 100) <= probabilidade_de_ser_cadastrado)

      if cadastro_reconhecido:
        motoristas_cadastrados[id_atendimento] = motorista
        motoristas_reconhecidos.pop(id_atendimento)
        print("---------------------------------------------------------------")
        print("motorista", motorista["motoristas"]["nome"], "já é cadastrado")
        print("---------------------------------------------------------------")

        total_motoristas_cadastrados += 1

  return total_motoristas_cadastrados


def verificar_creditos(motoristas_cadastrados, mototoristas_com_creditos, probabilidade_de_ter_credito):
  total_verificacao_de_creditos = 0
  
  if len(motoristas_cadastrados):
    for id_atendimento, motorista in list(motoristas_cadastrados.items()):
      tem_credito = (random.randint(1, 100) <= probabilidade_de_ter_credito)

      if tem_credito:
        mototoristas_com_creditos[id_atendimento] = motorista
        motoristas_cadastrados.pop(id_atendimento)
        print("---------------------------------------------------------------")
        print("motorista", motorista["motoristas"]["nome"], "tem creditos")
        print("---------------------------------------------------------------")

        total_verificacao_de_creditos += 1

  return total_verificacao_de_creditos


def debitar_valor(mototoristas_com_creditos, mototoristas_para_liberar, probabilidade_cobranca):
  total_cobrancas = 0

  if len(mototoristas_com_creditos):
    for id_atendimento, motorista in list(mototoristas_com_creditos.items()):
      cobrar_motorista = (random.randint(1, 100) <= probabilidade_cobranca)

      if cobrar_motorista:
        mototoristas_para_liberar[id_atendimento] = motorista
        mototoristas_com_creditos.pop(id_atendimento)
        print("---------------------------------------------------------------")
        print(motorista["motoristas"]["nome"], "esta sendo cobrando no valor de", motorista["motoristas"]["cobranca"])
        print("---------------------------------------------------------------")
        
        total_cobrancas += 1

  return total_cobrancas


def liberar_motorista(mototoristas_para_liberar, probabilidade_de_liberacao):
  total_liberacoes = 0

  if len(mototoristas_para_liberar):
    for id_atendimento, motorista in list(mototoristas_para_liberar.items()):
      libera_motorista = (random.randint(1, 100) <= probabilidade_de_liberacao)

      if libera_motorista:
        print("---------------------------------------------------------------")
        print(motorista["motoristas"]["nome"] , "esta sendo liberado")
        print("---------------------------------------------------------------")
        mototoristas_para_liberar.pop(id_atendimento)

        total_liberacoes += 1

  return total_liberacoes
