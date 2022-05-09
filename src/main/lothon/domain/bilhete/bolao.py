"""
   Package lothon.domain.bilhete
   Module  bolao.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass, field

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain.bilhete.cota import Cota
from lothon.domain.bilhete.volante import Volante
from lothon.domain.modalidade.loteria import Loteria


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(frozen=True, order=True, slots=True)
class Bolao:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    id_bolao: int
    loteria: Loteria
    volantes: list[Volante]
    cota: Cota
    valor_total: float
    lucro: float

    sort_index: int = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.id_bolao)

    # ----------------------------------------------------------------------------
