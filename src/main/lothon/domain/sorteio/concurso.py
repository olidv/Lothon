"""
   Package lothon.domain.sorteio
   Module  concurso.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from datetime import date
from dataclasses import dataclass, field
from typing import Optional

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain.basico.numeral import Numeral
from lothon.domain.sorteio.bola import Bola
from lothon.domain.sorteio.premio import Premio


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(frozen=True, order=True, slots=True)
class Concurso:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    id_concurso: int
    data_sorteio: date
    bolas_sorteadas: Optional[list[Bola]] = None
    numeral_sorteado: Optional[Numeral] = None
    premios: Optional[dict[int, Premio]] = None

    sort_index: int = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.id_concurso)

    # --- METODOS ------------------------------------------------------------

    def bolas_ordenadas(self) -> list[Bola]:
        return sorted(self.bolas_sorteadas, key=lambda b: b.ordem)

# ----------------------------------------------------------------------------
