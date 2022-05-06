"""
   Package lothon.domain.produto
   Module  lotofacil.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass

# Libs/Frameworks modules
from bs4.element import ResultSet

# Own/Project modules
from lothon.domain.produto.loteria import Loteria
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.sorteio.bola import Bola
from lothon.domain.sorteio.premio import Premio
from lothon.util.eve import *


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(order=True, slots=True)
class Lotofacil(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da produto Lotofacil.
    """

    # --- PROPRIEDADES -------------------------------------------------------

    # --- INICIALIZACAO ------------------------------------------------------

    # --- METODOS ------------------------------------------------------------

    def parse_concurso(self, td: ResultSet) -> Concurso:
        id_concurso: int = int(td[0].text)
        data_sorteio: date = parse_dmy(td[1].text)

        bolas_sorteadas: list[Bola] = [Bola(int(td[2].text), 1), Bola(int(td[3].text), 2),
                                       Bola(int(td[4].text), 3), Bola(int(td[5].text), 4),
                                       Bola(int(td[6].text), 5), Bola(int(td[7].text), 6),
                                       Bola(int(td[8].text), 7), Bola(int(td[9].text), 8),
                                       Bola(int(td[10].text), 9), Bola(int(td[11].text), 10),
                                       Bola(int(td[12].text), 11), Bola(int(td[13].text), 12),
                                       Bola(int(td[14].text), 13), Bola(int(td[15].text), 14),
                                       Bola(int(td[16].text), 15)]

        premios: dict[int, Premio] = {15: Premio(15, int(td[18].text), parse_money(td[24].text)),
                                      14: Premio(14, int(td[20].text), parse_money(td[25].text)),
                                      13: Premio(13, int(td[21].text), parse_money(td[26].text)),
                                      12: Premio(12, int(td[22].text), parse_money(td[27].text)),
                                      11: Premio(11, int(td[23].text), parse_money(td[28].text))}

        return Concurso(id_concurso, data_sorteio, bolas_sorteadas=bolas_sorteadas, premios=premios)

# ----------------------------------------------------------------------------
