"""
   Package lothon.domain.modalidade
   Module  lotofacil.py

"""

__all__ = [
    'Lotofacil'
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
from lothon.domain.modalidade.loteria import Loteria
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.sorteio.premio import Premio
from lothon.domain.bilhete.faixa import Faixa
from lothon.util.eve import *


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(order=True, slots=True)
class Lotofacil(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da modalidade Lotofacil.
    """

    # --- PROPRIEDADES -------------------------------------------------------

    # --- INICIALIZACAO ------------------------------------------------------

    # --- METODOS ------------------------------------------------------------

    def parse_concurso(self, td: ResultSet) -> Concurso:
        id_concurso: int = int(td[0].text)
        data_sorteio: date = parse_dmy(td[1].text)

        bolas: tuple[int, ...] = (int(td[2].text), int(td[3].text),
                                  int(td[4].text), int(td[5].text),
                                  int(td[6].text), int(td[7].text),
                                  int(td[8].text), int(td[9].text),
                                  int(td[10].text), int(td[11].text),
                                  int(td[12].text), int(td[13].text),
                                  int(td[14].text), int(td[15].text),
                                  int(td[16].text))
        # garante a ordenacao das bolas:
        bolas = tuple(sorted(bolas))

        premios: dict[int, Premio] = {15: Premio(15, int(td[18].text), parse_money(td[24].text)),
                                      14: Premio(14, int(td[20].text), parse_money(td[25].text)),
                                      13: Premio(13, int(td[21].text), parse_money(td[26].text)),
                                      12: Premio(12, int(td[22].text), parse_money(td[27].text)),
                                      11: Premio(11, int(td[23].text), parse_money(td[28].text))}

        return Concurso(id_concurso, data_sorteio, bolas=bolas, premios=premios)

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_tuple(value: tuple):
        if value is None or len(value) == 0:
            raise ValueError(f"Valor invalido para criar instancia de Lotofacil: {value}.")

        _lotofacil = Lotofacil(id_loteria=value[0],
                               nome_loteria=value[1],
                               tem_bolas=to_bool(value[2]),
                               qtd_bolas=int(value[3]),
                               qtd_bolas_sorteio=int(value[4]),
                               dias_sorteio=tuple(map(int, value[5].split('|'))),
                               faixas=Faixa.from_str(value[6], int(value[3])))
        return _lotofacil

# ----------------------------------------------------------------------------
