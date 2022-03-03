"""
   Package lothon.domain.universo
   Module  jogo.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain.universo.numeral import Numeral


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

class Jogo:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = 'id_jogo', 'numeros', 'escala', 'fator', 'metrica'

    @property
    def id_jogo(self) -> int:
        return self.id_jogo

    @id_jogo.setter
    def id_jogo(self, value):
        if isinstance(value, int):
            self.id_jogo = value
        else:
            self.id_jogo = int(value)

    @property
    def numeros(self) -> list[Numeral]:
        return self.numeros

    @numeros.setter
    def numeros(self, value):
        if isinstance(value, list):
            self.numeros = value
        else:
            raise ValueError(f"Valor invalido para a propriedade 'numeros' = {value}.")

    @property
    def escala(self) -> int:
        return self.escala

    @escala.setter
    def escala(self, value):
        if isinstance(value, int):
            self.escala = value
        else:
            self.escala = int(value)

    @property
    def fator(self) -> int:
        return self.fator

    @fator.setter
    def fator(self, value):
        if isinstance(value, int):
            self.fator = value
        else:
            self.fator = int(value)

    @property
    def metrica(self) -> int:
        return self.metrica

    @metrica.setter
    def metrica(self, value):
        if isinstance(value, int):
            self.metrica = value
        else:
            self.metrica = int(value)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idj, nums, escl, fatr, rank):
        self.id_jogo = idj
        self.numeros = nums
        self.escala = escl
        self.fator = fatr
        self.metrica = rank

# ----------------------------------------------------------------------------
