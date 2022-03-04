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


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class TimeDoCoracao(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da produto Time do Coracao.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_loteria', '_nome_loteria', '_tem_bola', '_faixa_bola', '_qtd_bolas_sorteio', \
                '_dias_sorteio', '_faixa_aposta', '_preco_aposta', '_concursos'

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

        return Concurso(td[0].text, td[1].text, sorteado=numero)

# ----------------------------------------------------------------------------
