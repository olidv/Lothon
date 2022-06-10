"""
   Package lothon.domain.modalidade
   Module  dupla_sena.py

"""

__all__ = [
    'DuplaSena'
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
from lothon.domain.sorteio.concurso_duplo import ConcursoDuplo
from lothon.domain.sorteio.premio import Premio
from lothon.domain.bilhete.faixa import Faixa
from lothon.util.eve import *


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(order=True, slots=True)
class DuplaSena(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da modalidade Dupla Sena.
    """

    # --- PROPRIEDADES -------------------------------------------------------

    # --- INICIALIZACAO ------------------------------------------------------

    # --- METODOS ------------------------------------------------------------

    def parse_concurso(self, td: ResultSet) -> ConcursoDuplo:
        id_concurso: int = int(td[0].text)
        data_sorteio: date = parse_dmy(td[1].text)

        bolas1: tuple[int, ...] = (int(td[2].text), int(td[3].text),
                                   int(td[4].text), int(td[5].text),
                                   int(td[6].text), int(td[7].text))

        bolas2: tuple[int, ...] = (int(td[20].text), int(td[21].text),
                                   int(td[22].text), int(td[23].text),
                                   int(td[24].text), int(td[25].text))
        # garante a ordenacao das bolas:
        bolas1 = tuple(sorted(bolas1))
        bolas2 = tuple(sorted(bolas2))

        premios1: dict[int, Premio] = {6: Premio(6, int(td[9].text), parse_money(td[11].text)),
                                       5: Premio(5, int(td[14].text), parse_money(td[15].text)),
                                       4: Premio(4, int(td[16].text), parse_money(td[17].text)),
                                       3: Premio(3, int(td[18].text), parse_money(td[19].text))}

        premios2: dict[int, Premio] = {6: Premio(6, int(td[26].text), parse_money(td[27].text)),
                                       5: Premio(5, int(td[28].text), parse_money(td[29].text)),
                                       4: Premio(4, int(td[30].text), parse_money(td[31].text)),
                                       3: Premio(3, int(td[32].text), parse_money(td[33].text))}

        return ConcursoDuplo(id_concurso, data_sorteio,
                             bolas=bolas1, premios=premios1,
                             bolas2=bolas2, premios2=premios2)

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_tuple(value: tuple):
        if value is None or len(value) == 0:
            raise ValueError(f"Valor invalido para criar instancia de DuplaSena: {value}.")

        _dupla_sena = DuplaSena(id_loteria=value[0],
                                nome_loteria=value[1],
                                tem_bolas=to_bool(value[2]),
                                qtd_bolas=int(value[3]),
                                qtd_bolas_sorteio=int(value[4]),
                                dias_sorteio=tuple(map(int, value[5].split('|'))),
                                faixas=Faixa.from_str(value[6], int(value[3])))
        return _dupla_sena

# ----------------------------------------------------------------------------
