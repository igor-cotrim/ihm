Feature: Verificando se o sistema consegue verificar se o motorista tem creditos

Scenario: Um motorista reconhecido pode ter creditos no sistema
    Given o ambiente seja preparado com sucesso
    When a foto ./faces/faustao1.jpg de um motorista for capturada
    Then um motorista deve ser reconhecido
    When a probabilidade de ter credito for 100 porcento
    Then 1 motorista foi indentificado com creditos no sistema
    When a foto ./faces/lazaro1.jpg de um motorista for capturada
    Then um motorista deve ser reconhecido
    When a probabilidade de ter credito for 0 porcento
    Then 0 motorista foi indentificado com creditos no sistema