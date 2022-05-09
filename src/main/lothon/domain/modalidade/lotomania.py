"""
   Package lothon.domain.modalidade
   Module  lotomania.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass

# Libs/Frameworks modules
from bs4.element import ResultSet

# Own/Project modules
from lothon.domain.modalidade.loteria import Loteria
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.sorteio.bola import Bola
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

        bolas_sorteadas: list[Bola] = [Bola(int(td[2].text), 1), Bola(int(td[3].text), 2),
                                       Bola(int(td[4].text), 3), Bola(int(td[5].text), 4),
                                       Bola(int(td[6].text), 5), Bola(int(td[7].text), 6),
                                       Bola(int(td[8].text), 7), Bola(int(td[9].text), 8),
                                       Bola(int(td[10].text), 9), Bola(int(td[11].text), 10),
                                       Bola(int(td[12].text), 11), Bola(int(td[13].text), 12),
                                       Bola(int(td[14].text), 13), Bola(int(td[15].text), 14),
                                       Bola(int(td[16].text), 15), Bola(int(td[17].text), 16),
                                       Bola(int(td[18].text), 17), Bola(int(td[19].text), 18),
                                       Bola(int(td[20].text), 19), Bola(int(td[21].text), 20)]

        premios: dict[int, Premio] = {20: Premio(20, int(td[23].text), parse_money(td[31].text)),
                                      19: Premio(19, int(td[26].text), parse_money(td[32].text)),
                                      18: Premio(18, int(td[27].text), parse_money(td[33].text)),
                                      17: Premio(17, int(td[28].text), parse_money(td[34].text)),
                                      16: Premio(16, int(td[29].text), parse_money(td[35].text)),
                                      15: Premio(15, int(td[30].text), parse_money(td[36].text))}

        return Concurso(id_concurso, data_sorteio, bolas_sorteadas=bolas_sorteadas, premios=premios)

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
