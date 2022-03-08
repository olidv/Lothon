"""
   Package lothon.domain.produto
   Module  lotomania.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
# Libs/Frameworks modules
from bs4.element import ResultSet

# Own/Project modules
from lothon.domain.produto.loteria import Loteria
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.sorteio.bola import Bola
from lothon.domain.sorteio.premio import Premio


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class Lotomania(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da produto Lotomania.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_loteria', '_nome_loteria', '_tem_bolas', 'intervalo_bolas', '_qtd_bolas', \
                '_qtd_bolas_sorteio', '_dias_sorteio', '_faixas', '_concursos'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, dados: tuple[str, ...]):
        super().__init__(dados)

    # --- METODOS ------------------------------------------------------------

    def parse_concurso(self, td: ResultSet) -> Concurso:
        bolas_sorteadas: list[Bola] = [Bola(td[2].text, 1), Bola(td[3].text, 2),
                                       Bola(td[4].text, 3), Bola(td[5].text, 4),
                                       Bola(td[6].text, 5), Bola(td[7].text, 6),
                                       Bola(td[8].text, 7), Bola(td[9].text, 8),
                                       Bola(td[10].text, 9), Bola(td[11].text, 10),
                                       Bola(td[12].text, 11), Bola(td[13].text, 12),
                                       Bola(td[14].text, 13), Bola(td[15].text, 14),
                                       Bola(td[16].text, 15), Bola(td[17].text, 16),
                                       Bola(td[18].text, 17), Bola(td[19].text, 18),
                                       Bola(td[20].text, 19), Bola(td[21].text, 20)]

        premios: dict[int, Premio] = {20: Premio(20, td[23].text, td[31].text),
                                      19: Premio(19, td[26].text, td[32].text),
                                      18: Premio(18, td[27].text, td[33].text),
                                      17: Premio(17, td[28].text, td[34].text),
                                      16: Premio(16, td[29].text, td[35].text),
                                      15: Premio(15, td[30].text, td[36].text)}

        return Concurso(td[0].text, td[1].text, sortedas=bolas_sorteadas, premiacao=premios)

# ----------------------------------------------------------------------------
