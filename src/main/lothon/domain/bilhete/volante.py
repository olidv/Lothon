"""
   Package lothon.domain.bilhete
   Module  volante.py

"""

__all__ = [
    'Volante'
]

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

@dataclass(frozen=True, order=True, slots=True)
class Volante:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    id_volante: int
    numeros: tuple[int, ...]
    qtd_numeros: int
    valor_aposta: float

    sort_index: int = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.id_volante)

# ----------------------------------------------------------------------------
