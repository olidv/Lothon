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
from lothon.domain.basico.numeral import Numeral


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(order=True, slots=True)
class Jogo:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    id_jogo: int
    numeros: list[Numeral]
    escala: int
    fator: int
    metrica: int

    sort_index: int = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        self.sort_index = self.id_jogo

# ----------------------------------------------------------------------------
