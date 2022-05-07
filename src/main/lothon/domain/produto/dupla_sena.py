"""
   Package lothon.domain.produto
   Module  dupla_sena.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass

# Libs/Frameworks modules
from bs4.element import ResultSet

# Own/Project modules
from lothon.domain.produto.loteria import Loteria
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.sorteio.bola import Bola
from lothon.domain.sorteio.premio import Premio
from lothon.domain.bilhete.faixa import Faixa
from lothon.util.eve import *


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(order=True, slots=True)
class DuplaSena(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da produto Dupla Sena.
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

                                       Bola(int(td[20].text), 1), Bola(int(td[21].text), 2),
                                       Bola(int(td[22].text), 3), Bola(int(td[23].text), 4),
                                       Bola(int(td[24].text), 5), Bola(int(td[25].text), 6)]

        premios: dict[int, Premio] = {16: Premio(6, int(td[9].text), parse_money(td[11].text)),
                                      15: Premio(5, int(td[14].text), parse_money(td[15].text)),
                                      14: Premio(4, int(td[16].text), parse_money(td[17].text)),
                                      13: Premio(3, int(td[18].text), parse_money(td[19].text)),

                                      26: Premio(6, int(td[26].text), parse_money(td[27].text)),
                                      25: Premio(5, int(td[28].text), parse_money(td[29].text)),
                                      24: Premio(4, int(td[30].text), parse_money(td[31].text)),
                                      23: Premio(3, int(td[32].text), parse_money(td[33].text))}

        return Concurso(id_concurso, data_sorteio, bolas_sorteadas=bolas_sorteadas, premios=premios)

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_tuple(value: tuple):
        if value is not None:
            _dupla_sena = DuplaSena(id_loteria=value[0],
                                    nome_loteria=value[1],
                                    tem_bolas=to_bool(value[2]),
                                    intervalo_bolas=tuple(map(int, value[3].split('-'))),
                                    qtd_bolas_sorteio=int(value[4]),
                                    dias_sorteio=tuple(map(int, value[5].split('|'))),
                                    faixas=Faixa.from_str(value[6]))
            return _dupla_sena

        else:
            raise ValueError(f"Valor invalido para criar instancia de DuplaSena: {value}.")

# ----------------------------------------------------------------------------
