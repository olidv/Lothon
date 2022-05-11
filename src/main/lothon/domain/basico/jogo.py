"""
   Package lothon.domain.basico
   Module  jogo.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass, field

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(slots=True)  # order=True, slots=True)
class Jogo:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    id_jogo: int
    numeros: tuple[int, ...]
    # qtd_numeros: int = field(init=False)
    # escala: int = 0
    fator: int = 0
    # metrica: int = 0

    # sort_index: int = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    # def __post_init__(self):
        # self.qtd_numeros = len(self.numeros)
        # self.sort_index = self.id_jogo

# ----------------------------------------------------------------------------
