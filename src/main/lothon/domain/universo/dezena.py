"""
   Package lothon.domain.universo
   Module  dezena.py

"""

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
class Dezena:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    id_dez: int
    intervalo: tuple[int, int] = field(init=False, repr=False)

    sort_index: int = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        minim = (self.id_dez - 1) * 10
        maxim = minim + 9
        object.__setattr__(self, 'intervalo', (minim, maxim))
        object.__setattr__(self, 'sort_index', self.id_dez)

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_int(value: int):
        if (value is not None) and (0 <= value <= 10):
            return ALL_DEZENAS[value]
        else:
            raise ValueError(f"Valor invalido para criar instancia de Dezena: {value}.")


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

ALL_DEZENAS: list[Dezena] = [Dezena(0),  Dezena(1),  Dezena(2),  Dezena(3),  Dezena(4),
                             Dezena(5),  Dezena(6),  Dezena(7),  Dezena(8),  Dezena(9),
                             Dezena(10)]

# ----------------------------------------------------------------------------
