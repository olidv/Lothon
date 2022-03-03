"""
   Package lothon.domain.bilhete
   Module  volante.py

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

class Volante:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = 'id_volante', 'numeros', 'qtd_numeros', 'valor_aposta'

    @property
    def id_volante(self) -> str:
        return self.id_volante

    @id_volante.setter
    def id_volante(self, value):
        if isinstance(value, str):
            self.id_volante = value
        else:
            self.id_volante = str(value)

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
    def qtd_numeros(self) -> int:
        return self.qtd_numeros

    @qtd_numeros.setter
    def qtd_numeros(self, value):
        if isinstance(value, int):
            self.qtd_numeros = value
        else:
            self.qtd_numeros = int(value)

    @property
    def valor_aposta(self) -> float:
        return self.valor_aposta

    @valor_aposta.setter
    def valor_aposta(self, value):
        if isinstance(value, float):
            self.valor_aposta = value
        else:
            self.valor_aposta = float(value)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idv, nums, qtd, val):
        self.id_volante = idv
        self.numeros = nums
        self.qtd_numeros = qtd
        self.valor_aposta = val

# ----------------------------------------------------------------------------
