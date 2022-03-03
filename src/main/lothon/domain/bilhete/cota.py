"""
   Package lothon.domain.bilhete
   Module  cota.py

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

class Cota:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    # __slots__ = 'id_cota', 'qtd_cotas', 'preco_unitario', 'preco_total'

    @property
    def id_cota(self) -> str:
        return self._id_cota

    @id_cota.setter
    def id_cota(self, value):
        if isinstance(value, str):
            self._id_cota = value
        else:
            self._id_cota = str(value)

    @property
    def qtd_cotas(self) -> int:
        return self._qtd_cotas

    @qtd_cotas.setter
    def qtd_cotas(self, value):
        if isinstance(value, int):
            self._qtd_cotas = value
        else:
            self._qtd_cotas = int(value)

    @property
    def preco_unitario(self) -> float:
        return self._preco_unitario

    @preco_unitario.setter
    def preco_unitario(self, value):
        if isinstance(value, float):
            self._preco_unitario = value
        else:
            self._preco_unitario = float(value)

    @property
    def preco_total(self) -> float:
        return self._preco_total

    @preco_total.setter
    def preco_total(self, value):
        if isinstance(value, float):
            self._preco_total = value
        else:
            self._preco_total = float(value)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idc, qtd, punt, ptot):
        self.id_cota = idc
        self.qtd_cotas = qtd
        self.preco_unitario = punt
        self.preco_total = ptot

# ----------------------------------------------------------------------------
