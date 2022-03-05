"""
   Package lothon.domain.universo
   Module  jogo.py

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

class Jogo:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_jogo', '_numeros', '_escala', '_fator', '_metrica'

    @property
    def id_jogo(self) -> int:
        return self._id_jogo

    @id_jogo.setter
    def id_jogo(self, value):
        if isinstance(value, int):
            self._id_jogo = value
        elif isinstance(value, str):
            self._id_jogo = int(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'id_jogo' = {value}.")

    @property
    def numeros(self) -> list[Numeral]:
        return self._numeros

    @numeros.setter
    def numeros(self, value):
        if isinstance(value, list):
            self._numeros = value
        else:
            raise ValueError(f"Valor invalido para a propriedade 'numeros' = {value}.")

    @property
    def escala(self) -> int:
        return self._escala

    @escala.setter
    def escala(self, value):
        if isinstance(value, int):
            self._escala = value
        elif isinstance(value, str):
            self._escala = int(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'escala' = {value}.")

    @property
    def fator(self) -> int:
        return self._fator

    @fator.setter
    def fator(self, value):
        if isinstance(value, int):
            self._fator = value
        elif isinstance(value, str):
            self._fator = int(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'fator' = {value}.")

    @property
    def metrica(self) -> int:
        return self._metrica

    @metrica.setter
    def metrica(self, value):
        if isinstance(value, int):
            self._metrica = value
        elif isinstance(value, str):
            self._metrica = int(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'metrica' = {value}.")

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idj, nums, escl, fatr, rank):
        self.id_jogo = idj
        self.numeros = nums
        self.escala = escl
        self.fator = fatr
        self.metrica = rank

    def __repr__(self):
        nums: str = ''
        for n in self.numeros:
            if len(nums) > 0:
                nums += ','
            nums += str(n)

        return f"Jogo{{ {self.id_jogo}, [{nums}], escala={self.escala}, fator={self.fator}, " \
               f"metrica={self.metrica} }}"

# ----------------------------------------------------------------------------
