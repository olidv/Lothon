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

    def __init__(self, idz, fxa):
        self.id_dez = idz
        self.faixa = fxa

    def __repr__(self):
        return f"Dezena{{ {self.id_dez}, {self.faixa} }}"

# ----------------------------------------------------------------------------
