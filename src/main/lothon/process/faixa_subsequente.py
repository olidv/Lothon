"""
   Package lothon.process
   Module  faixa_subsequente.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.process.processo import Processo


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class FaixaSubsequente(Processo):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_processo'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idp):
        super().__init__(idp)

    # --- METODOS ------------------------------------------------------------

    def init(self, universo) -> None:
        pass

    def execute(self) -> None:
        pass

# ----------------------------------------------------------------------------
