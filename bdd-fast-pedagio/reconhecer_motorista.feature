Feature: reconhecer um paciente pela foto

Scenario: Um motorista chega no pedagio e deve ser reconhecido por uma camera
Given o ambiente de reconhecimento foi preparado com sucesso
When a foto /home/igor-cotrim/Development/ifba/ihm/bdd-fast-pedagio/faces/faustao-2.jpg de um motorista for capturada
Then um motorista deve ser reconhecido