"""
   Package lothon.domain.produto
   Module  lotofacil.py

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


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class Lotofacil(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da produto Lotofacil.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_loteria', '_nome_loteria', '_tem_bola', '_faixa_bola', '_qtd_bolas_sorteio', \
                '_dias_sorteio', '_faixa_aposta', '_preco_aposta', '_concursos'

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
                                       Bola(td[16].text, 15)]

        return Concurso(td[0].text, td[1].text, bolas_sorteadas)

# ----------------------------------------------------------------------------
