"""
   Package lothon.domain.sorteio
   Module  concurso.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain.sorteio.bola import Bola
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
    bolas2: list[Bola]
    premios2: dict[int, Premio]

    # --- METODOS ------------------------------------------------------------

    def bolas_ordenadas(self) -> list[Bola]:
        todas_bolas: list[Bola] = [*self.bolas, *self.bolas2]
        return sorted(todas_bolas, key=lambda b: b.ordem)

    def check_premiacao2(self, numeros: list[int] | tuple[int, ...]) -> Premio | None:
        acertos2: int = 0
        for numero in numeros:
            if any(item for item in self.bolas2 if item.id_bola == numero):
                acertos2 += 1

        if acertos2 in self.premios2:
            return self.premios2[acertos2]
        else:
            return None

# ----------------------------------------------------------------------------
