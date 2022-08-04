"""
   Package lothon.infra
   Module  parser_resultados.py

"""

__all__ = [
    'get_dir_contents',
    'read_dezenas_csv',
    'read_jogos_csv',
    'parse_concursos_loteria',
    'exist_jogos_loteria',
    'read_jogos_loteria',
    'read_pares_loteria',
    'export_sorteios_loteria',
    'export_boloes_loteria'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from datetime import date
import os
import glob
import csv
import logging

# Libs/Frameworks modules
from bs4 import BeautifulSoup

# Own/Project modules
from lothon.conf import app_config
from lothon.domain.modalidade.loteria import Loteria
from lothon.domain.basico.jogo import Jogo
from lothon.util.eve import *


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# relaciona todos os arquivos em um diretorio:
def get_dir_contents(path_dir: str, mask_files: str) -> (list[str], int):
    try:
        # utiliza mascara generica para abranger todos os arquivos no diretorio:
        source_path_files = os.path.join(path_dir, mask_files)

        dir_contents = glob.glob(source_path_files)
        len_dir_contents = len(dir_contents)
        if len_dir_contents > 0:
            logger.debug("Encontrado(s) %d arquivo(s) em '%s'.", len_dir_contents, path_dir)
        else:
            logger.debug("Nenhum arquivo encontrado em '%s'.", path_dir)

        return dir_contents, len_dir_contents

    # qualquer erro significa que ainda nao pode acessar a rede interna...
    except OSError as err:
        logger.error("Nao foi possivel ler o diretorio '%s'. ERRO: %s", path_dir, repr(err))
    except Exception as ex:
        logger.error("Nao foi possivel ler o diretorio '%s'. ERRO: %s", path_dir, repr(ex))

    # se nao conseguiu ler o diretorio, retorna 'vazio'...
    return [], 0


def read_dezenas_csv(file_path: str) -> list[tuple[int, ...]] | None:
    lista_dezenas: list[tuple[int, ...]] = []

    # abre arquivo para leitura e carrega todas as dezenas em cada linha (tupla):
    try:
        with open(file_path, 'r') as file_csv:
            csv_reader = csv.reader(file_csv)
            # cada linha do arquivo eh carregada em uma lista de tuplas:
            for row in csv_reader:
                # converte a linha para tupla de numeros, com menor consumo de recursos:
                tupla_dezenas: tuple[int, ...] = ()
                for dezena in row:
                    # somente pega os numeros, ignorando texto como mes a sorte ou time do coracao
                    if dezena.isdigit():
                        tupla_dezenas += (int(dezena),)
                lista_dezenas.append(tupla_dezenas)

        return lista_dezenas

    # captura as excecoes relativas a manipulacao de arquivos:
    except FileNotFoundError as ex:
        logger.error(f"Arquivo CSV '{file_path}' nao encontrado.\n{ex}")
        return None


def read_jogos_csv(file_path: str) -> list[Jogo] | None:
    lista_jogos: list[Jogo] = []

    # abre arquivo para leitura e carrega todas as dezenas em cada linha (tupla):
    try:
        with open(file_path, 'r') as file_csv:
            csv_reader = csv.reader(file_csv)
            # cada linha do arquivo eh carregada em uma lista de tuplas:
            ordinal: int = 0
            for row in csv_reader:
                # converte a linha para tupla de numeros, com menor consumo de recursos:
                tupla_dezenas: tuple[int, ...] = ()
                for dezena in row:
                    tupla_dezenas += (int(dezena),)
                ordinal += 1
                lista_jogos.append(Jogo(ordinal, 1.0, tupla_dezenas))

        return lista_jogos

    # captura as excecoes relativas a manipulacao de arquivos:
    except FileNotFoundError as ex:
        logger.error(f"Arquivo CSV '{file_path}' nao encontrado.\n{ex}")
        return None


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

    # carrega completamente o conteudo HTML do arquivo:
    content_htm = ler_arquivo_htm(loteria_htm_path)

    return content_htm


def exist_jogos_loteria(nome_loteria: str) -> bool:
    # identifica o arquivo com os jogos computados da loteria:
    loteria_jogos_file: str = app_config.DS_jogos_csv_name.format(nome_loteria)
    loteria_jogos_path: str = os.path.join(app_config.DS_cache_path, loteria_jogos_file)

    # verifica se o arquivo existe, usando o path completo:
    return os.path.exists(loteria_jogos_path)


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


def read_pares_loteria(id_loteria: str) -> list[tuple[int, ...]] | None:
    # identifica o arquivo com os conjuntos de pares da loteria:
    loteria_pares_file: str = app_config.DS_pares_csv_name.format(id_loteria)
    loteria_pares_path: str = os.path.join(app_config.DS_cache_path, loteria_pares_file)

    # abre arquivo para leitura e carrega todas as dezenas dos conjuntos de pares:
    sorteios: list[tuple[int, ...]] = read_dezenas_csv(loteria_pares_path)
    return sorteios


def read_jogos_loteria(nome_loteria: str) -> list[Jogo] | None:
    # identifica o arquivo com os jogos computados da loteria:
    loteria_jogos_file: str = app_config.DS_jogos_csv_name.format(nome_loteria)
    loteria_jogos_path: str = os.path.join(app_config.DS_cache_path, loteria_jogos_file)

    # abre arquivo para leitura e carrega todas as dezenas dos jogos computados:
    jogos_computados: list[Jogo] = read_jogos_csv(loteria_jogos_path)

    # converte para o objeto Jogo:

    return jogos_computados


# ----------------------------------------------------------------------------
# EXPORTACAO DE DADOS EM ARQUIVOS CSV
# ----------------------------------------------------------------------------

def export_sorteios_loteria(loteria: Loteria) -> int:
    # valida se possui concursos a serem exportados:
    if loteria is None or loteria.concursos is None or len(loteria.concursos) == 0:
        return -1

    # cria arquivo fisico para conter apenas as dezenas sorteadas:
    loteria_sorteios_file: str = app_config.DS_sorteios_csv_name.format(loteria.nome_loteria)
    loteria_sorteios_path: str = os.path.join(app_config.DS_cache_path, loteria_sorteios_file)

    # abre arquivo para escrita e salva todas as dezenas sorteadas:
    qt_rows: int = 0
    with open(loteria_sorteios_path, 'w', newline='', encoding='utf-8') as file_csv:
        # o conteudo do arquivo sera formatado como CSV padrao:
        csv_writer = csv.writer(file_csv)

        # percorre lista de concursos e exporta as bolas:
        for concurso in loteria.concursos:
            # salva as dezenas separadas por virgula:
            csv_writer.writerow(concurso.bolas)
            qt_rows += 1

    # informa quantas linhas de sorteios foram gravadas:
    return qt_rows


def export_boloes_loteria(nome_loteria: str, id_bolao: str, jogos: list[tuple]) -> int:
    # valida se possui jogos a serem exportados:
    if jogos is None or len(jogos) == 0:
        return -1

    # cria arquivo fisico para conter apenas as dezenas dos jogos:
    loteria_boloes_file: str = app_config.BA_bolao_csv_name.format(id_bolao, nome_loteria)
    # aplica a mascara na data fornecida, configurada no INI:
    hoje = date.today()
    loteria_boloes_file = hoje.strftime(loteria_boloes_file)
    loteria_boloes_path: str = os.path.join(app_config.DS_bolao_path, loteria_boloes_file)

    # abre arquivo para escrita e salva todos os jogos:
    qt_rows: int = 0
    with open(loteria_boloes_path, 'w', newline='', encoding='utf-8') as file_csv:
        # o conteudo do arquivo sera formatado como CSV padrao:
        csv_writer = csv.writer(file_csv)

        # percorre lista de jogos e exporta as dezenas:
        for jogo in jogos:
            # salva as dezenas separadas por virgula:
            csv_writer.writerow(jogo)
            qt_rows += 1

    # informa quantas linhas de jogos foram gravadas:
    return qt_rows

# ----------------------------------------------------------------------------
