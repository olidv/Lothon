"""
   Package lothon.domain.sorteio
   Module  premio.py

"""

__all__ = [
    'Premio'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass, field

# Libs/Frameworks modules
# Own/Project modules
# from lothon.util.eve import *


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(frozen=True, order=True, slots=True)
class Premio:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    acertos: int
    qtd_ganhadores: int
    premio: float

    sort_index: int = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.acertos)

# ----------------------------------------------------------------------------
