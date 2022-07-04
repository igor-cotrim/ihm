import face_recognition
import secrets
import random
import simpy
import json

FOTOS_MOTORISTAS = [
  "./faces/fabio-assuncao-1.jpg",
  "./faces/fabio-assuncao-2.jpg",
  "./faces/fabio-assuncao-3.jpg",
  "./faces/faustao-1.jpg",
  "./faces/faustao-2.jpg",
  "./faces/faustao-3.jpg",
  "./faces/lazaro-ramos-1.jpg",
  "./faces/lazaro-ramos-2.jpg",
  "./faces/lazaro-ramos-3.jpg",
  "./faces/rodrigo-faro-1.jpg",
  "./faces/rodrigo-faro-2.jpg",
  "./faces/rodrigo-faro-3.jpg"
]

ARQUIVO_CONFIGURACAO = "./configuracao.json"

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

  global motoristas_reconhecidos
  motoristas_reconhecidos = {}

  global motoristas_cadastrados
  motoristas_cadastrados = {}

  global mototoristas_com_creditos
  mototoristas_com_creditos = {}

  global mototoristas_para_liberar
  mototoristas_para_liberar = {}


def simular_motorista():
  motorista = {
    "foto": random.choice(FOTOS_MOTORISTAS),
    "cadastrado": None
  }

  return motorista


def indentificar_motorista(motorista):
  global configuracao
  global gerador_dados_falsos

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


def reconhecer_motorista(env):
  global motoristas_reconhecidos
  
  while True:
    print("---------------------------------------------------------------")
    print("ciclo/tempo", env.now)
    print("reconhecendo um motorista cadastrado...")
    print("---------------------------------------------------------------")

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

    yield env.timeout(TEMPO_ENTRE_MOTORISTAS)


def identificar_cadastro(env):
  global motoristas_reconhecidos
  global motoristas_cadastrados
  
  while True:
    if len(motoristas_reconhecidos):
      print("---------------------------------------------------------------")
      print("ciclo/tempo", env.now)
      print("verificando cadastro do motorista...")
      print("---------------------------------------------------------------")

      total_motoristas_cadastrados = 0

      for id_atendimento, motorista in list(motoristas_reconhecidos.items()):
        cadastro_reconhecido = (random.randint(1, 100) <= PROBABILIDADE_DE_SER_CADASTRADO)
        if cadastro_reconhecido:
          motoristas_cadastrados[id_atendimento] = motorista
          motoristas_reconhecidos.pop(id_atendimento)
          print("---------------------------------------------------------------")
          print("motorista", motorista["motoristas"]["nome"], "já é cadastrado")
          print("---------------------------------------------------------------")
          total_motoristas_cadastrados += 1

      timeout = 1
      if total_motoristas_cadastrados > 0:
        timeout = total_motoristas_cadastrados * TEMPO_RECONHECIMENTO_CADASTRO

      yield env.timeout(timeout)
    else:
      yield env.timeout(1)


def verificar_creditos(env):
  global motoristas_cadastrados
  global mototoristas_com_creditos
  
  while True:
    if len(motoristas_cadastrados):
      print("---------------------------------------------------------------")
      print("ciclo/tempo", env.now)
      print("verificando se motorista tem creditos")
      print("---------------------------------------------------------------")

      total_verificacao_de_creditos = 0

      for id_atendimento, motorista in list(motoristas_cadastrados.items()):
        tem_credito = (random.randint(1, 100) <= PROBABILIDADE_DE_TER_CREDITO)
        if tem_credito:
          mototoristas_com_creditos[id_atendimento] = motorista
          motoristas_cadastrados.pop(id_atendimento)
          print("---------------------------------------------------------------")
          print(motorista["motoristas"]["nome"], "tem creditos")
          print("---------------------------------------------------------------")
          total_verificacao_de_creditos += 1

      timeout = 1
      if total_verificacao_de_creditos > 0:
        timeout = total_verificacao_de_creditos * TEMPO_HA_CREDITO

      yield env.timeout(timeout)
    else:
      yield env.timeout(1)


def debitar_valor(env):
  global mototoristas_com_creditos
  global mototoristas_para_liberar

  while True:
    if len(mototoristas_com_creditos):
      print("---------------------------------------------------------------")
      print("ciclo/tempo", env.now)
      print("fazendo cobrança do valor")
      print("---------------------------------------------------------------")

      total_cobrancas = 0

      for id_atendimento, motorista in list(mototoristas_com_creditos.items()):
        cobrar_motorista = (random.randint(1, 100) <= PROBABILIDADE_COBRANCA)

        if cobrar_motorista:
          mototoristas_para_liberar[id_atendimento] = motorista
          mototoristas_com_creditos.pop(id_atendimento)
          print("---------------------------------------------------------------")
          print(motorista["motoristas"]["nome"], "esta sendo cobrando no valor de", motorista["motoristas"]["cobranca"])
          print("---------------------------------------------------------------")
          
          total_cobrancas += 1

      timeout = 1
      if total_cobrancas > 0:
        timeout = total_cobrancas * TEMPO_DEBITAR_VALOR

      yield env.timeout(timeout)
    else:
      yield env.timeout(1)


def liberar_motorista(env):
  global mototoristas_para_liberar

  while True:
    if len(mototoristas_para_liberar):
      print("---------------------------------------------------------------")
      print("liberacao do motorista no pedagio...", env.now)

      total_liberacoes = 0
      for id_atendimento, motorista in list(mototoristas_para_liberar.items()):
        libera_motorista = (random.randint(1, 100) <= PROBABILIDADE_DE_LIBERACAO)

        if libera_motorista:
          print("---------------------------------------------------------------")
          print(motorista["motoristas"]["nome"] , "esta sendo liberado")
          print("---------------------------------------------------------------")
          
          mototoristas_para_liberar.pop(id_atendimento)
          total_liberacoes += 1

      timeout = 1
      if total_liberacoes > 0:
        timeout = total_liberacoes * TEMPO_LIBERACAO

      yield env.timeout(timeout)
    else:
      yield env.timeout(1)


if __name__ == "__main__":
  preparar()

  env = simpy.Environment()
  env.process(reconhecer_motorista(env))
  env.process(identificar_cadastro(env))
  env.process(verificar_creditos(env))
  env.process(debitar_valor(env))
  env.process(liberar_motorista(env))
  env.run(until=10000)
