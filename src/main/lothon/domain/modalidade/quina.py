"""
   Package lothon.domain.modalidade
   Module  quina.py

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
class Quina(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da modalidade Quina.
    """

    # --- PROPRIEDADES -------------------------------------------------------

    # --- INICIALIZACAO ------------------------------------------------------

    # --- METODOS ------------------------------------------------------------

    def parse_concurso(self, td: ResultSet) -> Concurso:
        id_concurso: int = int(td[0].text)
        data_sorteio: date = parse_dmy(td[1].text)

        bolas: tuple[int, ...] = (int(td[2].text), int(td[3].text),
                                  int(td[4].text), int(td[5].text),
                                  int(td[6].text))

        premios: dict[int, Premio] = {5: Premio(5, int(td[8].text), parse_money(td[10].text)),
                                      4: Premio(4, int(td[11].text), parse_money(td[12].text)),
                                      3: Premio(3, int(td[13].text), parse_money(td[14].text)),
                                      2: Premio(2, int(td[15].text), parse_money(td[16].text))}

        return Concurso(id_concurso, data_sorteio, bolas=bolas, premios=premios)

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_tuple(value: tuple):
        if value is None or len(value) == 0:
            raise ValueError(f"Valor invalido para criar instancia de Quina: {value}.")

        _quina = Quina(id_loteria=value[0],
                       nome_loteria=value[1],
                       tem_bolas=to_bool(value[2]),
                       qtd_bolas=int(value[3]),
                       qtd_bolas_sorteio=int(value[4]),
                       dias_sorteio=tuple(map(int, value[5].split('|'))),
                       faixas=Faixa.from_str(value[6], int(value[3])))
        return _quina

# ----------------------------------------------------------------------------
