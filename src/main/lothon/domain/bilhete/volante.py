"""
   Package lothon.domain.bilhete
   Module  volante.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
# Libs/Frameworks modules
# Own/Project modules
from lothon.domain .universo.numeral import Numeral


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class Volante:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_volante', '_numeros', '_qtd_numeros', '_valor_aposta'

    @property
    def id_volante(self) -> str:
        return self._id_volante

    @id_volante.setter
    def id_volante(self, value):
        if isinstance(value, str):
            self._id_volante = value
        else:
            self._id_volante = str(value)

    @property
    def numeros(self) -> list[Numeral]:
        return self._numeros

    @numeros.setter
    def numeros(self, value):
        if isinstance(value, list):
            self._numeros = value
            self._qtd_numeros = len(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'numeros' = {value}.")

    @property
    def qtd_numeros(self) -> int:
        return self._qtd_numeros

    @qtd_numeros.setter
    def qtd_numeros(self, value):
        if isinstance(value, int):
            self._qtd_numeros = value
        elif isinstance(value, str):
            self._qtd_numeros = int(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'qtd_numeros' = {value}.")

    @property
    def valor_aposta(self) -> float:
        return self._valor_aposta

    @valor_aposta.setter
    def valor_aposta(self, value):
        if isinstance(value, float):
            self._valor_aposta = value
        elif isinstance(value, str):
            self._valor_aposta = float(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'valor_aposta' = {value}.")

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idv, nums, val):
        self.id_volante = idv
        self.numeros = nums
        self.valor_aposta = val

    def __repr__(self):
        nums: str = ''
        for n in self.numeros:
            if len(nums) > 0:
                nums += ','
            nums += str(n.numero)

        return f"Volante{{ id_volante={self.id_volante}, qtd_numeros={self.qtd_numeros}, " \
               f"valor_aposta=R${self.valor_aposta}, numeros=[{nums}] }}"

# ----------------------------------------------------------------------------
