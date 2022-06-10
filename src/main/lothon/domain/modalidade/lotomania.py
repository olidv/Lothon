"""
   Package lothon.domain.modalidade
   Module  lotomania.py

"""

__all__ = [
    'Lotomania'
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
class Lotomania(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da modalidade Lotomania.
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
                                  int(td[16].text), int(td[17].text),
                                  int(td[18].text), int(td[19].text),
                                  int(td[20].text), int(td[21].text))
        # garante a ordenacao das bolas:
        bolas = tuple(sorted(bolas))

        premios: dict[int, Premio] = {20: Premio(20, int(td[23].text), parse_money(td[31].text)),
                                      19: Premio(19, int(td[26].text), parse_money(td[32].text)),
                                      18: Premio(18, int(td[27].text), parse_money(td[33].text)),
                                      17: Premio(17, int(td[28].text), parse_money(td[34].text)),
                                      16: Premio(16, int(td[29].text), parse_money(td[35].text)),
                                      15: Premio(15, int(td[30].text), parse_money(td[36].text))}

        return Concurso(id_concurso, data_sorteio, bolas=bolas, premios=premios)

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_tuple(value: tuple):
        if value is None or len(value) == 0:
            raise ValueError(f"Valor invalido para criar instancia de Lotomania: {value}.")

        _lotomania = Lotomania(id_loteria=value[0],
                               nome_loteria=value[1],
                               tem_bolas=to_bool(value[2]),
                               qtd_bolas=int(value[3]),
                               qtd_bolas_sorteio=int(value[4]),
                               dias_sorteio=tuple(map(int, value[5].split('|'))),
                               faixas=Faixa.from_str(value[6], int(value[3]), int(value[4])))
        return _lotomania

# ----------------------------------------------------------------------------
