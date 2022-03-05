"""
   Package lothon.domain.sorteio
   Module  concurso.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from datetime import date, datetime

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain.universo.numeral import Numeral
from lothon.domain.sorteio.bola import Bola


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class Concurso:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_concurso', '_data_sorteio', '_bolas_sorteadas', '_numeral_sorteado'

    @property
    def id_concurso(self) -> int:
        return self._id_concurso

    @id_concurso.setter
    def id_concurso(self, value):
        if isinstance(value, int):
            self._id_concurso = value
        else:
            self._id_concurso = int(value)

    @property
    def data_sorteio(self) -> date:
        return self._data_sorteio

    @data_sorteio.setter
    def data_sorteio(self, value):
        if isinstance(value, date):
            self._data_sorteio = value
        elif isinstance(value, str):  # 20/11/2001
            self._data_sorteio = datetime.strptime(value, "%d/%m/%Y").date()
        else:
            raise ValueError(f"Valor invalido para a propriedade 'data_sorteio' = {value}.")

    @property
    def bolas_sorteadas(self) -> list[Bola]:
        return self._bolas_sorteadas

    @bolas_sorteadas.setter
    def bolas_sorteadas(self, value):
        if value is None or isinstance(value, list):
            self._bolas_sorteadas = value
        else:
            raise ValueError(f"Valor invalido para a propriedade 'bolas_sorteadas' = {value}.")

    @property
    def numeral_sorteado(self) -> Numeral:
        return self._numeral_sorteado

    @numeral_sorteado.setter
    def numeral_sorteado(self, value):
        if value is None or isinstance(value, Numeral):
            self._numeral_sorteado = value
        elif isinstance(value, int):
            self._numeral_sorteado = Numeral.from_int(value)
        else:
            self._numeral_sorteado = Numeral.from_int(int(value))

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, numr, dia, sortedas=None, sorteado=None):
        self.id_concurso = numr
        self.data_sorteio = dia
        self.bolas_sorteadas = sortedas
        self.numeral_sorteado = sorteado

    # --- METODOS ------------------------------------------------------------

    def bolas_ordenadas(self) -> list[Bola]:
        return sorted(self.bolas_sorteadas, key=lambda b: b.ordem)

    def __repr__(self):
        sorteado: str = ''
        if self.bolas_sorteadas is not None:
            for bola in self.bolas_sorteadas:
                if len(sorteado) > 0:
                    sorteado += ','
                sorteado += str(bola.id_bola)
        elif self.numeral_sorteado is not None:
            sorteado = str(self.numeral_sorteado)

        return f"Concurso{{ {self.id_concurso}, {self.data_sorteio}, [{sorteado}] }}"

# ----------------------------------------------------------------------------
