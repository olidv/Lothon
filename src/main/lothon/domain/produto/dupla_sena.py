"""
   Package lothon.domain.produto
   Module  dupla_sena.py

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

class DuplaSena(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da produto Dupla Sena.
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

                                       Bola(td[20].text, 1), Bola(td[21].text, 2),
                                       Bola(td[22].text, 3), Bola(td[23].text, 4),
                                       Bola(td[24].text, 5), Bola(td[25].text, 6)]

        return Concurso(td[0].text, td[1].text, bolas_sorteadas)

# ----------------------------------------------------------------------------
