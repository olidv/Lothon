"""
   Package lothon.infra
   Module  parser_resultados.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging
import os

# Libs/Frameworks modules
from bs4 import BeautifulSoup

# Own/Project modules
from lothon.util.eve import *
from lothon.conf import app_config
from lothon.domain import Loteria


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# le arquivo de resultados e retorna conteudo HTML:
def ler_arquivo_htm(path_arquivo: str) -> str:
    logger.debug("Vai abrir para leitura o arquivo texto '%s'.", path_arquivo)
    with open(path_arquivo, "rt", encoding='utf-8') as htm:
        content_htm = htm.read()

    if len(content_htm) == 0:
        logger.warning("Este arquivo HTM de resultados esta vazio: '%s'", path_arquivo)
    else:
        file_size = os.path.getsize(path_arquivo)
        logger.debug("Leitura do arquivo '%s' realizada com sucesso: %s bytes lidos.",
                     path_arquivo, human_format(file_size))

    return content_htm


# efetua a verificacao e leitura do arquivo de resultados de determinada loteria:
def carregar_resultados(nome_loteria: str):
    logger.debug("Vai ler o arquivo HTM da loteria '%s'.", nome_loteria)

    # identifica o nome e path do arquivo HTM a ser lido:
    loteria_htm_file = app_config.LC_loteria_htm_name.format(nome_loteria)
    loteria_htm_path = os.path.join(app_config.RT_dat_path, loteria_htm_file)
    logger.debug("Path do Arquivo HTM da loteria '%s': %s", nome_loteria, loteria_htm_path)

    # precisa certificar que o arquivo existe antes da leitura:
    if not os.path.exists(loteria_htm_path):
        logger.error("O arquivo '%s' nao foi encontrado na pasta '%s' para leitura.",
                     loteria_htm_file, app_config.RT_dat_path)
        return None

    # carrega todo o conteudo HTML do arquivo:
    content_htm = ler_arquivo_htm(loteria_htm_path)

    return content_htm


# ----------------------------------------------------------------------------
# LEITURA E PARSING DOS RESULTADOS
# ----------------------------------------------------------------------------

def parse_concursos_loteria(loteria: Loteria):
    nome_loteria = loteria.get_file_resultados()
    tag_loteria = loteria.get_tag_resultados()
    logger.info("Iniciando a carga dos concursos da loteria '%s'.", nome_loteria)

    # efetua leitura dos resultados da loteria, verificando se o arquivo existe na pasta 'data'.
    content_htm = carregar_resultados(nome_loteria)
    # print(content_htm)
    if content_htm is None or len(content_htm) == 0:
        logger.error("Nao foi possivel carregar os resultados da loteria '%s'.", nome_loteria)
        return
    else:
        logger.info("Foram lidos %s caracteres do arquivo de resultados da loteria '%s'.",
                    human_format(len(content_htm)), nome_loteria)

    # carrega no BeautifulSoup o HTML contendo uma <TABLE> de resultados:
    logger.debug("Vai efetuar o parsing do conteudo HTML de resultados da loteria '%s'.",
                 nome_loteria)
    soup = BeautifulSoup(content_htm, 'html.parser')
    # print(soup.prettify())

    # pesquisa o elemento <TABLE> contendo a relacao de resultados / concursos da loteria:
    table_class = app_config.LC_table_class_find.format(tag_loteria)
    # formato do HTML atual:  <table class="tabela-resultado supersete">
    table = soup.find("table", {"class": table_class})
    # print(len(table))
    if table is None or len(table) == 0:
        logger.fatal("*** ATENCAO: O formato do arquivo HTM da loteria '%s' foi modificado! ***",
                     nome_loteria)
        return
    else:
        logger.info("Parsing do arquivo HTM da loteria '%s' efetuado com sucesso.", nome_loteria)

    # cada linha de resultado/concurso esta envolta em um TBODY:
    table_body = table.find_all("tbody", recursive=False)
    # print(len(table_body))
    if table_body is None or len(table_body) == 0:
        logger.fatal("*** ATENCAO: O formato do arquivo HTM da loteria '%s' foi modificado! ***",
                     nome_loteria)
        return
    else:
        logger.info("Encontradas %d linhas de resultados no arquivo HTM da loteria '%s'.",
                    len(table_body), nome_loteria)

    # dentro do TBODY tem uma unica TR contendo os dados relacionados em elementos TD:
    loteria.set_resultados(table_body)

# ----------------------------------------------------------------------------
