"""
   Package lothon.domain.bilhete
   Module  volante.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass, field

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain .basico.numeral import Numeral


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
    numeros: list[Numeral]
    qtd_numeros: int
    valor_aposta: float

    sort_index: int = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.id_volante)

# ----------------------------------------------------------------------------
