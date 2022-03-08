"""
   Package lothon.domain.produto
   Module  time_do_coracao.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
# Libs/Frameworks modules
from bs4.element import ResultSet

# Own/Project modules
from lothon.util.eve import *
from lothon.conf import app_config
from lothon.domain.produto.loteria import Loteria
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.sorteio.premio import Premio


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class TimeDoCoracao(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da produto Time do Coracao.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_loteria', '_nome_loteria', '_tem_bolas', '_intervalo_bolas', '_qtd_bolas', \
                '_qtd_bolas_sorteio', '_dias_sorteio', '_faixas', '_concursos'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, dados: tuple[str, ...]):
        super().__init__(dados)

    # --- METODOS ------------------------------------------------------------

    def get_tag_resultados(self) -> str:
        return 'timemania'

    def get_file_resultados(self) -> str:
        return 'TIMEMANIA'

    def parse_concurso(self, td: ResultSet) -> Concurso:
        time = strip_accents(td[9].text.strip().lower().replace(" /", "/")
                                                       .replace("/ ", "/")
                                                       .replace("  ", " "))
        if time in app_config.MAP_TIMES.keys():
            numero = app_config.MAP_TIMES[time]
        else:
            raise ValueError(f"*** ATENCAO: TIME-DO-CORACAO NAO IDENTIFICADO "
                             f"NO CONCURSO {td[0].text}: {time} ***")

        premios: dict[int, Premio] = {1: Premio(1, td[17].text, td[23].text)}

        return Concurso(td[0].text, td[1].text, sorteado=numero, premiacao=premios)

# ----------------------------------------------------------------------------
