Feature: Verificando se o sistema consegue verificar se o motorista tem cadastro

Scenario: Um motorista reconhecido pode ja ter cadastro no sistema
    Given o ambiente seja preparado com sucesso
    When a foto ./faces/faustao1.jpg de um motorista for capturada
    Then um motorista deve ser reconhecido
    When a probabilidade de ser cadastrado for 100 porcento
    Then 1 motorista ja e cadastrado
    When a foto ./faces/lazaro1.jpg de um motorista for capturada
    Then um motorista deve ser reconhecido
    When a probabilidade de ser cadastrado for 0 porcento
    Then 0 motorista ja e cadastrado