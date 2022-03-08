"""
   Package lothon.domain.produto
   Module  mega_sena.py

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

class MegaSena(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da produto Mega-Sena.
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
                                       Bola(td[6].text, 5), Bola(td[7].text, 6)]

        premios: dict[int, Premio] = {6: Premio(6, td[8].text, td[11].text),
                                      5: Premio(5, td[9].text, td[12].text),
                                      4: Premio(4, td[10].text, td[13].text)}

        return Concurso(td[0].text, td[1].text, sortedas=bolas_sorteadas, premiacao=premios)

# ----------------------------------------------------------------------------
