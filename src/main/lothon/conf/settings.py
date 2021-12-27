"""
   Package infinite.conf
   Module  settings.py

   Carga das configuracoes da aplicacao a partir de arquivo INI.
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import os.path
import logging
import logging.config
from configparser import ConfigParser, ExtendedInterpolation

# Libs/Frameworks modules
import yaml

# Own/Project modules
from infinite.conf import app_config
# from infinite.conf.appconfig import AppConfig


# ----------------------------------------------------------------------------
# CONSTANTES
# ----------------------------------------------------------------------------

# nome do arquivo de configuracao do logging:
APP_CONFIG_LOG = "logging.yaml"

# nome do arquivo de configuracao da aplicacao:
APP_CONFIG_INI = "app_config.ini"


# ----------------------------------------------------------------------------
# VARIAVEIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# instancia global para leitura das configuracoes da aplicacao:
# app_config: AppConfig = AppConfig()  # apenas para utilizar o code-assist (type hint)...


# ----------------------------------------------------------------------------
# CONFIGURACAO DO LOGGING (YAML)
# ----------------------------------------------------------------------------

# configura o logging da aplicacao conforme arquivo de configuracao:
def setup_logging(config_path: str = '.') -> bool:
    # somente efetua a configuracao do logging se o arquivo existir no path indicado:
    file_config_log = os.path.join(config_path, APP_CONFIG_LOG)
    if os.path.isfile(file_config_log):
        with open(file_config_log, 'rt') as f:
            config = yaml.safe_load(f.read())

        # configura o logging da aplicacao:
        logging.config.dictConfig(config)

        # redefine os levels do logging para melhor legibilidade do output:
        logging.addLevelName(logging.INFO, 'INFOR')
        logging.addLevelName(logging.WARNING, 'WARNG')
        logging.addLevelName(logging.CRITICAL, 'FATAL')

        logger.debug("O arquivo '%s' foi utilizado para configurar o logging.", file_config_log)
        return True

    else:  # arquivo INI nao existe:
        logger.critical("O arquivo de configuracao do logging '%s' nao foi localizado.",
                        file_config_log)
        return False


# ----------------------------------------------------------------------------
# CONFIGURACAO DA APLICACAO (INI)
# ----------------------------------------------------------------------------

# leitura do arquivo INI para registrar a configuracao usada na execucao corrente:
def read_ini(parser: ConfigParser) -> str:
    ini_text = ''
    for section in parser.sections():
        # a partir da segunda secao, adiciona uma linha para separacao entre secoes:
        if len(ini_text) > 0:
            ini_text += '\n'
        ini_text += '[' + section + ']\n'
        # identa os valores com 2 espacos, para maior legibilidade
        for name, value in parser.items(section):
            ini_text += '  ' + name + ' = ' + value.strip() + '\n'

    return ini_text


# Leitura das configuracoes da aplicacao dentro de arquivo INI
def setup_config(config_path: str = '.') -> bool:
    # global app_config

    # somente efetua a leitura do arquivo INI se existir no path corrente:
    file_config_ini = os.path.join(config_path, APP_CONFIG_INI)
    if os.path.isfile(file_config_ini):
        parser = ConfigParser(interpolation=ExtendedInterpolation())
        read_ok = parser.read(file_config_ini)

        # verifica se o arquivo esta valido e possui parametros:
        secoes = parser.sections()
        if len(read_ok) == 0 or len(secoes) == 0:
            logger.critical("O arquivo de configuracao '%s' esta vazio.", file_config_ini)
            return False

        # atualiza os principais parametros utilizados na aplicacao:
        # app_config = AppConfig(parser)
        app_config.load_properties(parser)

        # se tudo ok, pode prosseguir com a execucao:
        ini_contents = read_ini(parser)
        logger.debug("O arquivo de configuracao '%s' foi carregado com os valores:\n%s",
                     file_config_ini, ini_contents)
        return True

    else:  # arquivo INI nao existe:
        logger.critical("O arquivo de configuracao '%s' nao foi localizado.", file_config_ini)
        return False

# ----------------------------------------------------------------------------
