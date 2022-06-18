"""
   Package lothon.domain.basico
   Module  jogo.py

"""

__all__ = [
    'Jogo'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(slots=True)
class Jogo:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    ordinal: int
    fator: float
    dezenas: tuple[int, ...]

    # --- METODOS ------------------------------------------------------------

    def to_string(self) -> str:
        # valida os parametros:
        if self.dezenas is None or len(self.dezenas) == 0:
            return ''

        tostr: str = ''
        for num in self.dezenas:
            tostr += f"{num:0>2}"

        return tostr

# ----------------------------------------------------------------------------
