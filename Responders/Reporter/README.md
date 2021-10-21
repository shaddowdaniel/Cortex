# Reporter

Um Responder do Cortex para o TheHive que cria um relatório em Markdown de um determinado caso.

# Instalação

Veja as dependências em `requirements.txt`.

# Configurção

Na configuração do Responder, a seguinte configuração é necessária:

| Item | Descrição | Exemplo |
|------|-------------|---------|
|tmp_file_location | Um caminho temporário que é usado para armazenar o arquivo markdown antes de ser anexado ao caso TheHive e depois removido | `/opt/Cortex-Analyzers/github-aacgood/Responders/Reporter/tmp/` |
|thehive_instance | A instância do TheHive com a qual você está se integrando | `http://server:9000` |
|thehive_api | Esta é a chave de API de uma conta de usuário que foi gerada no TheHive | `random 32 character string`
