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
    bolas: tuple[int, ...]
    premios: dict[int, Premio]

    sort_index: int = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.id_concurso)

    # --- METODOS ------------------------------------------------------------

    def bolas_ordenadas(self) -> tuple[int, ...]:
        return tuple(sorted(self.bolas))

    def check_premiacao(self, numeros: tuple[int, ...]) -> Premio | None:
        acertos: int = 0
        for numero in numeros:
            if any(bola for bola in self.bolas if bola == numero):
                acertos += 1

        if acertos in self.premios:
            return self.premios[acertos]
        else:
            return None

# ----------------------------------------------------------------------------
