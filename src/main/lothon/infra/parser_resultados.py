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

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# le arquivo de resultados e retorna conteudo HTML:
def ler_arquivo_htm(path_arquivo: str) -> str:
    logger.debug(f"Vai abrir para leitura o arquivo texto '{path_arquivo}'.")
    with open(path_arquivo, "rt", encoding='utf-8') as htm:
        content_htm = htm.read()

    if len(content_htm) == 0:
        logger.warning(f"Este arquivo HTM de resultados esta vazio: '{path_arquivo}'")
    else:
        file_size = os.path.getsize(path_arquivo)
        logger.debug(f"Leitura do arquivo '{path_arquivo}' realizada com sucesso: "
                     f"{human_format(file_size)} bytes lidos.")

    return content_htm


# efetua a verificacao e leitura do arquivo de resultados de determinada loteria:
def carregar_resultados(nome_loteria: str):
    logger.debug(f"Vai ler o arquivo HTM da loteria '{nome_loteria}'.")

    # identifica o nome e path do arquivo HTM a ser lido:
    loteria_htm_file = app_config.LC_loteria_htm_name.format(nome_loteria)
    loteria_htm_path = os.path.join(app_config.RT_dat_path, loteria_htm_file)
    logger.debug(f"Path do Arquivo HTM da loteria '{nome_loteria}': {loteria_htm_path}")

    # precisa certificar que o arquivo existe antes da leitura:
    if not os.path.exists(loteria_htm_path):
        logger.error(f"O arquivo '{loteria_htm_file}' nao foi encontrado na pasta "
                     f"'{app_config.RT_dat_path}' para leitura.")
        return

    # carrega todo o conteudo HTML do arquivo:
    content_htm = ler_arquivo_htm(loteria_htm_path)

    return content_htm


# ----------------------------------------------------------------------------
# LEITURA E PARSING DOS RESULTADOS
# ----------------------------------------------------------------------------

def parse_concursos_loteria(loteria: Loteria):
    nome_loteria = loteria.get_file_resultados()
    tag_loteria = loteria.get_tag_resultados()
    logger.info(f"Iniciando a carga dos concursos da loteria '{nome_loteria}'.")

    # efetua leitura dos resultados da loteria, verificando se o arquivo existe na pasta 'data'.
    content_htm = carregar_resultados(nome_loteria)
    # print(content_htm)
    if content_htm is None or len(content_htm) == 0:
        logger.error(f"Nao foi possivel carregar os resultados da loteria '{nome_loteria}'.")
        return
    else:
        logger.info(f"Foram lidos {human_format(len(content_htm))} caracteres do arquivo de "
                    f"resultados da loteria '{nome_loteria}'.")

    # carrega no BeautifulSoup o HTML contendo uma <TABLE> de resultados:
    logger.debug(f"Vai efetuar o parsing do conteudo HTML de resultados da "
                 f"loteria '{nome_loteria}'.")
    soup = BeautifulSoup(content_htm, 'html.parser')
    # print(soup.prettify())

    # pesquisa o elemento <TABLE> contendo a relacao de resultados / concursos da loteria:
    table_class = app_config.LC_table_class_find.format(tag_loteria)
    # formato do HTML atual:  <table class="tabela-resultado supersete">
    table = soup.find("table", {"class": table_class})
    # print(len(table))
    if table is None or len(table) == 0:
        logger.fatal(f"*** ATENCAO: O formato do arquivo HTM da loteria "
                     f"'{nome_loteria}' foi modificado! ***")
        return
    else:
        logger.info(f"Parsing do arquivo HTM da loteria '{nome_loteria}' efetuado com sucesso.")

    # cada linha de resultado/concurso esta envolta em um TBODY:
    table_body = table.find_all("tbody", recursive=False)
    # print(len(table_body))
    if table_body is None or len(table_body) == 0:
        logger.fatal(f"*** ATENCAO: O formato do arquivo HTM da loteria "
                     f"'{nome_loteria}' foi modificado! ***")
        return
    else:
        logger.info(f"Encontradas {len(table_body)} linhas de resultados no arquivo HTM da "
                    f"loteria '{nome_loteria}'.")

    # dentro do TBODY tem uma unica TR contendo os dados relacionados em elementos TD:
    loteria.set_resultados(table_body)

# ----------------------------------------------------------------------------
