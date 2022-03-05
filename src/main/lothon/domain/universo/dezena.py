"""
   Package lothon.domain.universo
   Module  dezena.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class Dezena:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_dez', '_faixa'

    @property
    def id_dez(self) -> int:
        return self._id_dez

    @id_dez.setter
    def id_dez(self, value):
        if isinstance(value, int):
            self._id_dez = value
        else:
            self._id_dez = int(value)

        maxim = self._id_dez * 10
        minim = maxim - 9
        self._faixa = (minim, maxim)

    @property
    def faixa(self) -> tuple[int, ...]:
        return self._faixa

    @faixa.setter
    def faixa(self, value):
        if isinstance(value, tuple):
            self._faixa = value
        elif isinstance(value, str):
            self._faixa = tuple(map(int, value.split('-')))
        else:
            raise ValueError(f"Valor invalido para a propriedade 'faixa' = {value}.")

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idz):
        self.id_dez = idz

    def __repr__(self):
        return f"Dezena{{ {self.id_dez}, {self.faixa} }}"

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_int(value: int):
        if (value is not None) and (0 <= value <= 10):
            return ALL_DEZENAS[value]
        else:
            raise ValueError(f"Valor invalido para criar instancia de Dezena: {value}.")


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

ALL_DEZENAS: list[Dezena] = [Dezena(0),  Dezena(1),  Dezena(2),  Dezena(3),  Dezena(4),
                             Dezena(5),  Dezena(6),  Dezena(7),  Dezena(8),  Dezena(9),
                             Dezena(10)]

# ----------------------------------------------------------------------------
