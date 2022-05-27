"""
   Package lothon.domain.modalidade
   Module  mega_sena.py

"""

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
class MegaSena(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da modalidade Mega-Sena.
    """

    # --- PROPRIEDADES -------------------------------------------------------

    # --- INICIALIZACAO ------------------------------------------------------

    # --- METODOS ------------------------------------------------------------

    def parse_concurso(self, td: ResultSet) -> Concurso:
        id_concurso: int = int(td[0].text)
        data_sorteio: date = parse_dmy(td[1].text)

        bolas: tuple[int, ...] = (int(td[2].text), int(td[3].text),
                                  int(td[4].text), int(td[5].text),
                                  int(td[6].text), int(td[7].text))

        premios: dict[int, Premio] = {6: Premio(6, int(td[8].text), parse_money(td[11].text)),
                                      5: Premio(5, int(td[9].text), parse_money(td[12].text)),
                                      4: Premio(4, int(td[10].text), parse_money(td[13].text))}

        return Concurso(id_concurso, data_sorteio, bolas=bolas, premios=premios)

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_tuple(value: tuple):
        if value is None or len(value) == 0:
            raise ValueError(f"Valor invalido para criar instancia de MegaSena: {value}.")

        _mega_sena = MegaSena(id_loteria=value[0],
                              nome_loteria=value[1],
                              tem_bolas=to_bool(value[2]),
                              qtd_bolas=int(value[3]),
                              qtd_bolas_sorteio=int(value[4]),
                              dias_sorteio=tuple(map(int, value[5].split('|'))),
                              faixas=Faixa.from_str(value[6], int(value[3])))
        return _mega_sena

# ----------------------------------------------------------------------------
