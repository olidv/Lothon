"""
   Package lothon.domain.universo
   Module  numeral.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules


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

class Numeral:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = 'numero'

    @property
    def numero(self) -> int:
        return self.numero

    @numero.setter
    def numero(self, value):
        if isinstance(value, int):
            self.numero = value
        else:
            self.numero = int(value)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, numr):
        self.numero = numr

# ----------------------------------------------------------------------------
