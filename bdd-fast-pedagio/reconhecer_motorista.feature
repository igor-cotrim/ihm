Feature: Reconhecer motorista pela foto

Scenario: Um motorista chega ao pedagio e deve ser reconhecido por uma camera
    Given o ambiente seja preparado com sucesso
    When a foto ./faces/faustao1.jpg de um motorista for capturada
    Then um motorista deve ser reconhecido
    When a foto ./faces/lazaro1.jpg de um motorista for capturada
    Then um motorista deve ser reconhecido

Scenario: Uma pessoa que nao e motorista chega ao pedagio e nao deve ser reconhecida
    Given o ambiente seja preparado com sucesso
    When a foto ./faces/rodrigo1.jpg de um motorista for capturada
    Then nenhum motorista deve ser reconhecido
