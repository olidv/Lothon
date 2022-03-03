"""
   Package lothon.domain.sorteio
   Module  concurso.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging
from datetime import date, datetime

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain.sorteio.bola import Bola

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

class Concurso:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = 'id_concurso', 'data_sorteio', 'bolas_sorteadas'

    @property
    def id_concurso(self) -> int:
        return self.id_concurso

    @id_concurso.setter
    def id_concurso(self, value):
        if isinstance(value, int):
            self.id_concurso = value
        else:
            self.id_concurso = int(value)

    @property
    def data_sorteio(self) -> date:
        return self.data_sorteio

    @data_sorteio.setter
    def data_sorteio(self, value):
        if isinstance(value, date):
            self.data_sorteio = value
        elif isinstance(value, str):  # 20/11/2001
            self.data_sorteio = datetime.strptime(value, "%d/%m/%Y").date()
        else:
            raise ValueError(f"Valor invalido para a propriedade 'data_sorteio' = {value}.")

    @property
    def bolas_sorteadas(self) -> list[Bola]:
        return self.bolas_sorteadas

    @bolas_sorteadas.setter
    def bolas_sorteadas(self, value):
        if isinstance(value, list):
            self.bolas_sorteadas = value
        else:
            raise ValueError(f"Valor invalido para a propriedade 'bolas_sorteadas' = {value}.")

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, numr, dia, sortedas):
        self.id_concurso = numr
        self.data_sorteio = dia
        self.bolas_sorteadas = sortedas

    # --- METODOS ------------------------------------------------------------

    def bolas_ordenadas(self) -> list[Bola]:
        return sorted(self.bolas_sorteadas, key=lambda b: b.ordem)

# ----------------------------------------------------------------------------
