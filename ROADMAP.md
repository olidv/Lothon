
--- PENDENTE --------------------------------------------------------

Implementar rotinas de geração de palpites e bolões para todas as loterias "computadas" em Java.
    Gerar 100 palpites de jogos para todas as loterias em arquivo TXT formatado.
    Adicionar rotina para efetuar upload dos arquivos para o Google Drive.
    Implementar geração de imagem JPG com palpites para compatilhar nas redes sociais.

Adotar "async def" nos métodos de jobs.

??? Mudar o codename de cada job para 3 letras ao gerar arquivo de controle (\temp) ???

Buscar informações sobre os clubes de loterias/investidores nos USA
    Verificar se é empresa, como é feito, legalidade, se pode usar no Brasil.

Verificar se tem algum serviço ou API gratuito para geração de voz para gerar áudio com resultado das loterias e enviar nas redes sociais / chats.
    Resultado, dezenas, premiação, etc.
    Utilizar audio como exemplo na pasta \Audios.
    https://podcasts.google.com/feed/aHR0cHM6Ly9hbmNob3IuZm0vcy8zY2I1NTBmNC9wb2RjYXN0L3Jzcw/episode/ODk0YjliOGEtOWVhZS00OWI5LTliMWUtZmIwYjNlNjQ2MmRl?sa=X&ved=0CAUQkfYCahgKEwiI48LVnZ71AhUAAAAAHQAAAAAQgAE

Apos a aplicação atingir maturidade, desligar o logging dos frameworks.
    loggers:
      schedule:
        level: ERROR
      selenium:
        level: ERROR
      urllib3:
        level: ERROR


--- OK --------------------------------------------------------------

---------------------------------------------------------------------
