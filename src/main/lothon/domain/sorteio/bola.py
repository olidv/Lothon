"""
   Package lothon.domain.sorteio
   Module  bola.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
# Libs/Frameworks modules
# Own/Project modules
from lothon.domain.universo.numeral import Numeral


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class Bola:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_bola', '_numeral', '_ordem'

    @property
    def id_bola(self) -> int:
        return self._id_bola

    @id_bola.setter
    def id_bola(self, value):
        if isinstance(value, int):
            self._id_bola = value
        else:
            self._id_bola = int(value)

    @property
    def numeral(self) -> Numeral:
        return self._numeral

    @numeral.setter
    def numeral(self, value):
        if isinstance(value, Numeral):
            self._numeral = value
        elif isinstance(value, int):
            self._numeral = Numeral.from_int(value)
        elif isinstance(value, str):
            self._numeral = Numeral.from_int(int(value))
        else:
            raise ValueError(f"Valor invalido para a propriedade 'numeral' = {value}.")

    @property
    def ordem(self) -> int:
        return self._ordem

    @ordem.setter
    def ordem(self, value):
        if isinstance(value, int):
            self._ordem = value
        else:
            self._ordem = int(value)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idb, ordm):
        self.id_bola = idb
        self.numeral = idb
        self.ordem = ordm

    def __repr__(self):
        return f"Bola{{ {self.id_bola}, {self.ordem} }}"

# ----------------------------------------------------------------------------
