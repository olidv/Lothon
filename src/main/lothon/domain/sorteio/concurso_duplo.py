"""
   Package lothon.domain.sorteio
   Module  concurso.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass
from typing import Optional

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain.sorteio.premio import Premio
from lothon.domain.sorteio.concurso import Concurso


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(frozen=True, order=True, slots=True)
class ConcursoDuplo(Concurso):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    bolas2: tuple[int, ...]
    premios2: dict[int, Premio]

    # --- METODOS ------------------------------------------------------------

    def bolas2_ordenadas(self) -> tuple[int, ...]:
        return tuple(sorted(self.bolas2))

    def check_premiacao2(self, numeros: tuple[int, ...]) -> Optional[Premio]:
        acertos2: int = 0
        for numero in numeros:
            if any(bola for bola in self.bolas2 if bola == numero):
                acertos2 += 1

        if acertos2 in self.premios2:
            return self.premios2[acertos2]
        else:
            return None

# ----------------------------------------------------------------------------
