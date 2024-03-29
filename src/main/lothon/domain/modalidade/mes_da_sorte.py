"""
   Package lothon.domain.modalidade
   Module  mes_da_sorte.py

"""

__all__ = [
    'MesDaSorte'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from datetime import date
from dataclasses import dataclass

# Libs/Frameworks modules
from bs4.element import ResultSet

# Own/Project modules
from lothon.conf import app_config
from lothon.domain.modalidade.loteria import Loteria
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.sorteio.premio import Premio
from lothon.domain.bilhete.faixa import Faixa
from lothon.util.eve import *


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(order=True, slots=True)
class MesDaSorte(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da modalidade Mes da Sorte.
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
        if mes not in app_config.MAP_MESES.keys():
            raise ValueError(f"*** ATENCAO: MES-DA-SORTE NAO IDENTIFICADO "
                             f"NO CONCURSO {td[0].text}: {mes} ***")

        bolas: tuple[int, ...] = (app_config.MAP_MESES[mes],)

        premios: dict[int, Premio] = {1: Premio(1, int(td[15].text), parse_money(td[20].text))}

        return Concurso(id_concurso, data_sorteio, bolas=bolas, premios=premios)

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_tuple(value: tuple):
        if value is None or len(value) == 0:
            raise ValueError(f"Valor invalido para criar instancia de MesDaSorte: {value}.")

        _mes_da_sorte = MesDaSorte(id_loteria=value[0],
                                   nome_loteria=value[1],
                                   tag_loteria='e',
                                   tem_bolas=to_bool(value[2]),
                                   qtd_bolas=int(value[3]),
                                   qtd_bolas_sorteio=int(value[4]),
                                   dias_sorteio=tuple(map(int, value[5].split('|'))),
                                   faixas=Faixa.from_str(value[6], int(value[3])))
        return _mes_da_sorte

# ----------------------------------------------------------------------------
