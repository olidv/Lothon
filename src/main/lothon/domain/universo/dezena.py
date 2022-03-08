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
    __slots__ = '_id_dez', '_intervalo'

    @property
    def id_dez(self) -> int:
        return self._id_dez

    @id_dez.setter
    def id_dez(self, value):
        if isinstance(value, int):
            self._id_dez = value
        elif isinstance(value, str):
            self._id_dez = int(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'id_dez' = {value}.")

        minim = self._id_dez * 10
        maxim = minim + 9
        self._intervalo = (minim, maxim)

    @property
    def intervalo(self) -> tuple[int, ...]:
        return self._intervalo

    @intervalo.setter
    def intervalo(self, value):
        if isinstance(value, tuple):
            self._intervalo = value
        elif isinstance(value, str):
            self._intervalo = tuple(map(int, value.split('-')))
        else:
            raise ValueError(f"Valor invalido para a propriedade 'intervalo' = {value}.")

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idz):
        self.id_dez = idz

    def __repr__(self):
        return f"Dezena{{ {self.id_dez}, {self.intervalo} }}"

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
