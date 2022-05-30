"""
   Package lothon.domain.modalidade
   Module  time_do_coracao.py

"""

__all__ = [
    'TimeDoCoracao'
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
class TimeDoCoracao(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da modalidade Time do Coracao.
    """

    # --- PROPRIEDADES -------------------------------------------------------

    # --- INICIALIZACAO ------------------------------------------------------

    # --- METODOS ------------------------------------------------------------

    def get_tag_resultados(self) -> str:
        return 'timemania'

    def get_file_resultados(self) -> str:
        return 'TIMEMANIA'

    def parse_concurso(self, td: ResultSet) -> Concurso:
        id_concurso: int = int(td[0].text)
        data_sorteio: date = parse_dmy(td[1].text)

        time = strip_accents(td[9].text.strip().lower().replace(" /", "/")
                                                       .replace("/ ", "/")
                                                       .replace("  ", " "))
        if time not in app_config.MAP_TIMES.keys():
            raise ValueError(f"*** ATENCAO: TIME-DO-CORACAO NAO IDENTIFICADO "
                             f"NO CONCURSO {td[0].text}: {time} ***")

        bolas: tuple[int, ...] = (app_config.MAP_TIMES[time])

        premios: dict[int, Premio] = {1: Premio(1, int(td[17].text), parse_money(td[23].text))}

        return Concurso(id_concurso, data_sorteio, bolas=bolas, premios=premios)

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_tuple(value: tuple):
        if value is None or len(value) == 0:
            raise ValueError(f"Valor invalido para criar instancia de TimeDoCoracao: {value}.")

        _time_do_coracao = TimeDoCoracao(id_loteria=value[0],
                                         nome_loteria=value[1],
                                         tem_bolas=to_bool(value[2]),
                                         qtd_bolas=int(value[3]),
                                         qtd_bolas_sorteio=int(value[4]),
                                         dias_sorteio=tuple(map(int, value[5].split('|'))),
                                         faixas=Faixa.from_str(value[6], int(value[3])))
        return _time_do_coracao

# ----------------------------------------------------------------------------
