"""
   Package lothon.domain.sorteio
   Module  faixa.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import math
from dataclasses import dataclass, field

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(frozen=True, order=True, slots=True)
class Faixa:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    id_faixa: int
    preco: float
    qtd_apostas: int

    sort_index: float = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', float(self.id_faixa))

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_str(vals: str) -> list:
        if vals is None:
            raise ValueError(f"Valor invalido para criar instancia de Faixa: {vals}.")

        # 7-15:2.00   |   10-10:3.00   |   1-1:2.00
        termos = vals.split(':')
        if len(termos) == 0:
            raise ValueError(f"Valor invalido para criar instancia de Faixa: {vals}.")

        interval = termos[0].split('-')
        if len(interval) == 0:
            raise ValueError(f"Valor invalido para criar instancia de Faixa: {vals}.")

        qtd_min = int(interval[0])
        qtd_max = int(interval[1])
        preco_min = float(termos[1])

        faixas: list[Faixa] = [Faixa(qtd_min, preco_min, 1)]
        if qtd_max > qtd_min:
            for qtd in range(qtd_min + 1, qtd_max + 1):
                jogos = math.comb(qtd, qtd_min)
                preco = jogos * preco_min

                fx = Faixa(qtd, preco, jogos)
                faixas.append(fx)

        return faixas

# ----------------------------------------------------------------------------
