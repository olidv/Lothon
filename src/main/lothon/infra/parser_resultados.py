"""
   Package lothon.infra
   Module  parser_resultados.py

"""

__all__ = [
    'parse_concursos_loteria',
    'read_pares_loteria',
    'export_sorteios_loteria'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging
import os
import csv

# Libs/Frameworks modules
from bs4 import BeautifulSoup

# Own/Project modules
from lothon.conf import app_config
from lothon.domain.modalidade.loteria import Loteria
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.sorteio.concurso_duplo import ConcursoDuplo
from lothon.util.eve import *


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
                     f"{formatb(file_size)} bytes lidos.")

    return content_htm


# efetua a verificacao e leitura do arquivo de resultados de determinada loteria:
def carregar_resultados(nome_loteria: str):
    logger.debug(f"Vai ler o arquivo HTM da loteria '{nome_loteria}'.")

    # identifica o nome e path do arquivo HTM a ser lido:
    loteria_htm_file = app_config.LC_loteria_htm_name.format(nome_loteria)
    loteria_htm_path = os.path.join(app_config.DS_caixa_path, loteria_htm_file)
    logger.debug(f"Path do Arquivo HTM da loteria '{nome_loteria}': {loteria_htm_path}")

    # precisa certificar que o arquivo existe antes da leitura:
    if not os.path.exists(loteria_htm_path):
        logger.error(f"O arquivo '{loteria_htm_file}' nao foi encontrado na pasta "
                     f"'{app_config.DS_caixa_path}' para leitura.")
        return

    # carrega todo o conteudo HTML do arquivo:
    content_htm = ler_arquivo_htm(loteria_htm_path)

    return content_htm


# ----------------------------------------------------------------------------
# LEITURA DE DADOS E PARSING DOS RESULTADOS
# ----------------------------------------------------------------------------

def parse_concursos_loteria(loteria: Loteria) -> int:
    nome_loteria = loteria.get_file_resultados()
    tag_loteria = loteria.get_tag_resultados()
    logger.info(f"Iniciando a carga dos concursos da loteria '{nome_loteria}'.")

    # efetua leitura dos resultados da loteria, verificando se o arquivo existe na pasta 'data'.
    content_htm = carregar_resultados(nome_loteria)
    # logger.debug(f"content_htm = {content_htm}")
    if content_htm is None or len(content_htm) == 0:
        logger.error(f"Nao foi possivel carregar os resultados da loteria '{nome_loteria}'.")
        return -1
    else:
        logger.info(f"Foram lidos {formatb(len(content_htm))} caracteres do arquivo de "
                    f"resultados da loteria '{nome_loteria}'.")

    # carrega no BeautifulSoup o HTML contendo uma <TABLE> de resultados:
    logger.debug(f"Vai efetuar o parsing do conteudo HTML de resultados da "
                 f"loteria '{nome_loteria}'.")
    soup = BeautifulSoup(content_htm, 'html.parser')
    # logger.debug(f"soup.prettify() = {soup.prettify()}")

    # pesquisa o elemento <TABLE> contendo a relacao de resultados / concursos da loteria:
    table_class = app_config.LC_table_class_find.format(tag_loteria)
    # formato do HTML atual:  <table class="tabela-resultado supersete">
    table = soup.find("table", {"class": table_class})
    # logger.debug(f"len(table) = {len(table)}")
    if table is None or len(table) == 0:
        logger.fatal(f"*** ATENCAO: O formato do arquivo HTM da loteria "
                     f"'{nome_loteria}' foi modificado! ***")
        return -1
    else:
        logger.info(f"Parsing do arquivo HTM da loteria '{nome_loteria}' efetuado com sucesso.")

    # cada linha de resultado/concurso esta envolta em um TBODY:
    table_body = table.find_all("tbody", recursive=False)
    # logger.debug(f"len(table_body) = {len(table_body)}")
    if table_body is None or len(table_body) == 0:
        logger.fatal(f"*** ATENCAO: O formato do arquivo HTM da loteria "
                     f"'{nome_loteria}' foi modificado! ***")
        return -1
    else:
        logger.info(f"Encontradas {len(table_body)} linhas de resultados no arquivo HTM da "
                    f"loteria '{nome_loteria}'.")

    # dentro do TBODY tem uma unica TR contendo os dados relacionados em elementos TD:
    return loteria.set_resultados(table_body)


def read_pares_loteria(id_loteria: str) -> list[tuple[int, ...]]:
    sorteios: list[tuple[int, ...]] = []

    # identifica o arquivo com os conjuntos de pares da loteria:
    loteria_pares_file: str = app_config.DS_pares_csv_name.format(id_loteria)
    loteria_pares_path: str = os.path.join(app_config.DS_input_path, loteria_pares_file)

    # abre arquivo para leitura e carrega todas as dezenas dos conjuntos de pares:
    with open(loteria_pares_path, 'r') as file_csv:
        csv_reader = csv.reader(file_csv)
        # cada linha do arquivo eh carregada em um list[]
        for row in csv_reader:
            # converte a linha para tupla de numeros, com menor consumo de recursos:
            sorteio: tuple[int, ...] = ()
            for dezena in row:
                sorteio += (int(dezena),)
            sorteios.append(sorteio)

    return sorteios


# ----------------------------------------------------------------------------
# EXPORTACAO DE DADOS EM ARQUIVOS CSV
# ----------------------------------------------------------------------------

def export_sorteios_loteria(loteria: Loteria) -> int:
    # valida se possui concursos a serem exportados:
    if loteria is None or loteria.concursos is None or len(loteria.concursos) == 0:
        return -1

    # o numero de sorteios realizados pode dobrar se for instancia de ConcursoDuplo:
    concursos: list[Concurso | ConcursoDuplo] = loteria.concursos
    eh_duplo: bool = isinstance(concursos[0], ConcursoDuplo)
    qt_rows: int = 0

    # cria arquivo fisico para conter apenas as dezenas sorteadas:
    loteria_sorteios_file: str = app_config.DS_sorteios_csv_name.format(loteria.id_loteria)
    loteria_sorteios_path: str = os.path.join(app_config.DS_output_path, loteria_sorteios_file)

    # abre arquivo para escrita e salva todas as dezenas sorteadas:
    with open(loteria_sorteios_path, 'w', newline='', encoding='utf-8') as file_csv:
        csv_writer = csv.writer(file_csv)
        # percorre lista de concursos e exporta as bolas:
        for concurso in concursos:
            # se for concurso duplo, concatena ambos sorteios em lista unica:
            bolas: tuple[int, ...] = concurso.bolas
            if eh_duplo:
                bolas += concurso.bolas2
            # salva as dezenas separadas por virgula:
            csv_writer.writerow(bolas)
            qt_rows += 1

    # informa quantas linhas de sorteios foram gravadas:
    return qt_rows

# ----------------------------------------------------------------------------
