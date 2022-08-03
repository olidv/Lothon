"""
   Package lothon.infra
   Module  console.py

"""

__all__ = [
    'execute_jlothon'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import subprocess
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.conf import app_config


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# relaciona todos os arquivos em um diretorio:
def execute_jlothon(tag_loteria: str) -> bool:
    # indica a loteria para o jLothon como argumento do script batch:
    jlothon: str = app_config.RT_jlothon_batch.format(tag_loteria)
    workdir: str = app_config.RT_lib_path

    # executa o programa jLothon para processar os jogos da loteria indicada:
    exit_code: int = subprocess.call(jlothon, cwd=workdir)

    # informa True se foi executado com sucesso ou False caso contrario.
    return exit_code == 0

# ----------------------------------------------------------------------------
