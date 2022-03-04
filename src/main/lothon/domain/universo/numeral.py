"""
   Package lothon.domain.universo
   Module  numeral.py

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

class Numeral:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_numero',

    @property
    def numero(self) -> int:
        return self._numero

    @numero.setter
    def numero(self, value):
        if isinstance(value, int):
            self._numero = value
        else:
            self._numero = int(value)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, numr):
        self.numero = numr

    def __repr__(self):
        return str(self.numero)

# ----------------------------------------------------------------------------
