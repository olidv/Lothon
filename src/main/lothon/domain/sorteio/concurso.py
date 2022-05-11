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

# Libs/Frameworks modules
# Own/Project modules
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
    bolas: list[Bola]
    premios: dict[int, Premio]

    sort_index: int = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.id_concurso)

    # --- METODOS ------------------------------------------------------------

    def bolas_ordenadas(self) -> list[Bola]:
        return sorted(self.bolas, key=lambda b: b.ordem)

    def check_premiacao(self, numeros: list[int] | tuple[int, ...]) -> Premio | None:
        acertos: int = 0
        for numero in numeros:
            if any(item for item in self.bolas if item.id_bola == numero):
                acertos += 1

        if acertos in self.premios:
            return self.premios[acertos]
        else:
            return None

# ----------------------------------------------------------------------------
