"""
   Package lothon.domain.produto
   Module  mes_da_sorte.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass

# Libs/Frameworks modules
from bs4.element import ResultSet

# Own/Project modules
from lothon.conf import app_config
from lothon.domain.produto.loteria import Loteria
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.sorteio.premio import Premio
from lothon.util.eve import *


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(order=True, slots=True)
class MesDaSorte(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da produto Mes da Sorte.
    """

    # --- PROPRIEDADES -------------------------------------------------------

    # --- INICIALIZACAO ------------------------------------------------------

    # --- METODOS ------------------------------------------------------------

    def get_tag_resultados(self) -> str:
        return 'diadesorte'

    def get_file_resultados(self) -> str:
        return 'DIA-DE-SORTE'

    def parse_concurso(self, td: ResultSet) -> Concurso:
        id_concurso: int = int(td[0].text)
        data_sorteio: date = parse_dmy(td[2].text)

        mes = td[10].text.strip().lower()
        if mes in app_config.MAP_MESES.keys():
            mes_sorteado = app_config.MAP_MESES[mes]
        else:
            raise ValueError(f"*** ATENCAO: MES-DA-SORTE NAO IDENTIFICADO "
                             f"NO CONCURSO {td[0].text}: {mes} ***")

        premios: dict[int, Premio] = {1: Premio(1, int(td[15].text), parse_money(td[20].text))}

        return Concurso(id_concurso, data_sorteio, numeral_sorteado=mes_sorteado, premios=premios)

# ----------------------------------------------------------------------------