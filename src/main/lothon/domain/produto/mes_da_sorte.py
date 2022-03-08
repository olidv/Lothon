"""
   Package lothon.domain.produto
   Module  mes_da_sorte.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
# Libs/Frameworks modules
from bs4.element import ResultSet

# Own/Project modules
from lothon.conf import app_config
from lothon.domain.produto.loteria import Loteria
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.sorteio.premio import Premio


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class MesDaSorte(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da produto Mes da Sorte.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_loteria', '_nome_loteria', '_tem_bolas', '_intervalo_bolas', '_qtd_bolas', \
                '_qtd_bolas_sorteio', '_dias_sorteio', '_faixas', '_concursos'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, dados: tuple[str, ...]):
        super().__init__(dados)

    # --- METODOS ------------------------------------------------------------

    def get_tag_resultados(self) -> str:
        return 'diadesorte'

    def get_file_resultados(self) -> str:
        return 'DIA-DE-SORTE'

    def parse_concurso(self, td: ResultSet) -> Concurso:
        mes = td[10].text.strip().lower()
        if mes in app_config.MAP_MESES.keys():
            numero = app_config.MAP_MESES[mes]
        else:
            raise ValueError(f"*** ATENCAO: MES-DA-SORTE NAO IDENTIFICADO "
                             f"NO CONCURSO {td[0].text}: {mes} ***")

        premios: dict[int, Premio] = {1: Premio(1, td[15].text, td[20].text)}

        return Concurso(td[0].text, td[2].text, sorteado=numero, premiacao=premios)

# ----------------------------------------------------------------------------
