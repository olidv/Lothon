"""
   Package lothon.domain.basico
   Module  cor.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from enum import Enum

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# CLASSE ENUMERACAO
# ----------------------------------------------------------------------------

class Cor(Enum):
    """
    Implementacao de classe para .
    """

    # --- VALORES ENUMERADOS -------------------------------------------------
    BRANCA = 0
    VERMELHA = 1
    AMARELA = 2
    VERDE = 3
    MARROM = 4
    AZUL = 5
    ROSA = 6
    PRETA = 7
    CINZA = 8
    LARANJA = 9

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_int(value: int):
        if value is not None:
            return Cor(value % 10)
        else:
            raise ValueError(f"Valor invalido para criar instancia de Cor: {value}.")

    # ----------------------------------------------------------------------------
