"""
   Package lothon.domain.bilhete
   Module  bolao.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain.bilhete.cota import Cota
from lothon.domain.bilhete.volante import Volante
from lothon.domain.produto.loteria import Loteria


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

class Bolao:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    # __slots__ = 'id_bolao', 'loteria', 'volantes', 'cota', 'valor_total', 'lucro'

    @property
    def id_bolao(self) -> str:
        return self._id_bolao

    @id_bolao.setter
    def id_bolao(self, value):
        if isinstance(value, str):
            self._id_bolao = value
        else:
            self._id_bolao = str(value)

    @property
    def loteria(self) -> Loteria:
        return self._loteria

    @loteria.setter
    def loteria(self, value):
        if isinstance(value, Loteria):
            self._loteria = value
        else:
            raise ValueError(f"Valor invalido para a propriedade 'loteria' = {value}.")

    @property
    def volantes(self) -> list[Volante]:
        return self._volantes

    @volantes.setter
    def volantes(self, value):
        if isinstance(value, list):
            self._volantes = value
        else:
            raise ValueError(f"Valor invalido para a propriedade 'volantes' = {value}.")

    @property
    def cota(self) -> Cota:
        return self._cota

    @cota.setter
    def cota(self, value):
        if isinstance(value, Cota):
            self._cota = value
        else:
            raise ValueError(f"Valor invalido para a propriedade 'cota' = {value}.")

    @property
    def valor_total(self) -> float:
        return self._valor_total

    @valor_total.setter
    def valor_total(self, value):
        if isinstance(value, float):
            self._valor_total = value
        else:
            self._valor_total = float(value)

    @property
    def lucro(self) -> float:
        return self._lucro

    @lucro.setter
    def lucro(self, value):
        if isinstance(value, float):
            self._lucro = value
        else:
            self._lucro = float(value)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idb, lot, vols, cta, vtot, lcro):
        self.id_bolao = idb
        self.loteria = lot
        self.volantes = vols
        self.cota = cta
        self.valor_total = vtot
        self.lucro = lcro

# ----------------------------------------------------------------------------
