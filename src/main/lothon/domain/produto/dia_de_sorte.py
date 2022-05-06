"""
   Package lothon.domain.produto
   Module  dia_de_sorte.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from datetime import date, datetime
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
class DiaDeSorte(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da produto Dia de Sorte.
    """

    # --- PROPRIEDADES -------------------------------------------------------

    # --- INICIALIZACAO ------------------------------------------------------

    # --- METODOS ------------------------------------------------------------

    def parse_concurso(self, td: ResultSet) -> Concurso:
        id_concurso: int = int(td[0].text)
        data_sorteio: date = datetime.strptime(td[2].text, "%d/%m/%Y").date()

        bolas_sorteadas: list[Bola] = [Bola(int(td[3].text), 1), Bola(int(td[4].text), 2),
                                       Bola(int(td[5].text), 3), Bola(int(td[6].text), 4),
                                       Bola(int(td[7].text), 5), Bola(int(td[8].text), 6),
                                       Bola(int(td[9].text), 7)]

        premios: dict[int, Premio] = {7: Premio(7, int(td[11].text), parse_money(td[16].text)),
                                      6: Premio(6, int(td[12].text), parse_money(td[17].text)),
                                      5: Premio(5, int(td[13].text), parse_money(td[18].text)),
                                      4: Premio(4, int(td[14].text), parse_money(td[19].text))}

        return Concurso(id_concurso, data_sorteio, bolas_sorteadas=bolas_sorteadas, premios=premios)

    # ----------------------------------------------------------------------------
