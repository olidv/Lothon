"""
   Package lothon.domain.universo
   Module  numeral.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass, field

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain.universo.dezena import Dezena
from lothon.domain.universo.cor import Cor


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(frozen=True, order=True, slots=True)
class Numeral:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    numero: int
    dezena: Dezena = field(init=False, repr=False)
    cor: Cor = field(init=False, repr=False)

    sort_index: int = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'dezena', Dezena.from_int(self.numero // 10))
        object.__setattr__(self, 'cor', Cor.from_int(self.numero))
        object.__setattr__(self, 'sort_index', self.numero)

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_int(value: int):
        if (value is not None) and (0 <= value <= 100):
            return ALL_NUMERALS[value]
        else:
            raise ValueError(f"Valor invalido para criar instancia de Numeral: {value}.")


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

ALL_NUMERALS: list[Numeral] = [Numeral(0),  Numeral(1),  Numeral(2),  Numeral(3),  Numeral(4),
                               Numeral(5),  Numeral(6),  Numeral(7),  Numeral(8),  Numeral(9),
                               Numeral(10), Numeral(11), Numeral(12), Numeral(13), Numeral(14),
                               Numeral(15), Numeral(16), Numeral(17), Numeral(18), Numeral(19),
                               Numeral(20), Numeral(21), Numeral(22), Numeral(23), Numeral(24),
                               Numeral(25), Numeral(26), Numeral(27), Numeral(28), Numeral(29),
                               Numeral(30), Numeral(31), Numeral(32), Numeral(33), Numeral(34),
                               Numeral(35), Numeral(36), Numeral(37), Numeral(38), Numeral(39),
                               Numeral(40), Numeral(41), Numeral(42), Numeral(43), Numeral(44),
                               Numeral(45), Numeral(46), Numeral(47), Numeral(48), Numeral(49),
                               Numeral(50), Numeral(51), Numeral(52), Numeral(53), Numeral(54),
                               Numeral(55), Numeral(56), Numeral(57), Numeral(58), Numeral(59),
                               Numeral(60), Numeral(61), Numeral(62), Numeral(63), Numeral(64),
                               Numeral(65), Numeral(66), Numeral(67), Numeral(68), Numeral(69),
                               Numeral(70), Numeral(71), Numeral(72), Numeral(73), Numeral(74),
                               Numeral(75), Numeral(76), Numeral(77), Numeral(78), Numeral(79),
                               Numeral(80), Numeral(81), Numeral(82), Numeral(83), Numeral(84),
                               Numeral(85), Numeral(86), Numeral(87), Numeral(88), Numeral(89),
                               Numeral(90), Numeral(91), Numeral(92), Numeral(93), Numeral(94),
                               Numeral(95), Numeral(96), Numeral(97), Numeral(98), Numeral(99),
                               Numeral(100)]

# ----------------------------------------------------------------------------
