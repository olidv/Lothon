"""
   Package lothon.domain.produto
   Module  quina.py

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

class Quina(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da produto Quina.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_loteria', '_nome_loteria', '_tem_bolas', '_intervalo_bolas', '_qtd_bolas', \
                '_qtd_bolas_sorteio', '_dias_sorteio', '_faixas', '_concursos'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, dados: tuple[str, ...]):
        super().__init__(dados)

    # --- METODOS ------------------------------------------------------------

    def parse_concurso(self, td: ResultSet) -> Concurso:
        bolas_sorteadas: list[Bola] = [Bola(td[2].text, 1), Bola(td[3].text, 2),
                                       Bola(td[4].text, 3), Bola(td[5].text, 4),
                                       Bola(td[6].text, 5)]

        premios: dict[int, Premio] = {5: Premio(5, td[8].text, td[10].text),
                                      4: Premio(4, td[11].text, td[12].text),
                                      3: Premio(3, td[13].text, td[14].text),
                                      2: Premio(2, td[15].text, td[16].text)}

        return Concurso(td[0].text, td[1].text, sortedas=bolas_sorteadas, premiacao=premios)

# ----------------------------------------------------------------------------
