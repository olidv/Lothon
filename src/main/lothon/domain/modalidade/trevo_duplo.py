"""
   Package lothon.domain.modalidade
   Module  trevo_duplo.py

"""

__all__ = [
    'TrevoDuplo'
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
from lothon.domain.bilhete.faixa import Faixa
from lothon.util.eve import *


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(order=True, slots=True)
class TrevoDuplo(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da modalidade Trevo Duplo (Numerado).
    """

    # --- PROPRIEDADES -------------------------------------------------------

    # --- INICIALIZACAO ------------------------------------------------------

    # --- METODOS ------------------------------------------------------------

    def get_tag_resultados(self) -> str:
        return 'trevoduplo'

    def get_file_resultados(self) -> str:
        return 'TREVO_DUPLO'

    def parse_concurso(self, td: ResultSet = None) -> list[Concurso]:
        # estes valores foram extraidos diretamente da pagina da loteria +Milionaria:
        self.concursos = [
            Concurso(1, date(2022, 5, 28), self.get_bolas('42'), {}),
            Concurso(2, date(2022, 6, 4), self.get_bolas('62'), {}),
            Concurso(3, date(2022, 6, 11), self.get_bolas('14'), {}),
            Concurso(4, date(2022, 6, 18), self.get_bolas('12'), {}),
            Concurso(5, date(2022, 6, 25), self.get_bolas('25'), {}),
            Concurso(6, date(2022, 7, 2), self.get_bolas('51'), {}),
            Concurso(7, date(2022, 7, 9), self.get_bolas('51'), {}),
            Concurso(8, date(2022, 7, 16), self.get_bolas('13'), {}),
            Concurso(9, date(2022, 7, 23), self.get_bolas('34'), {}),
            Concurso(10, date(2022, 7, 30), self.get_bolas('52'), {}),
            Concurso(11, date(2022, 8, 6), self.get_bolas('42'), {}),
            Concurso(12, date(2022, 8, 13), self.get_bolas('15'), {}),
            Concurso(13, date(2022, 8, 20), self.get_bolas('21'), {}),
            Concurso(14, date(2022, 8, 27), self.get_bolas('31'), {}),
            Concurso(15, date(2022, 9, 3), self.get_bolas('64'), {})
        ]

        return self.concursos

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def get_bolas(str_trevos: str) -> tuple[int, ...]:
        num_trevo: int = int(str_trevos)
        trevo1: int = num_trevo % 10
        trevo2: int = num_trevo // 10

        _bolas: tuple[int, ...] = (trevo1, trevo2,) if trevo1 < trevo2 else (trevo2, trevo1,)
        return _bolas

    @staticmethod
    def from_tuple(value: tuple):
        if value is None or len(value) == 0:
            raise ValueError(f"Valor invalido para criar instancia de TrevoDuplo: {value}.")

        _trevo_duplo = TrevoDuplo(id_loteria=value[0],
                                  nome_loteria=value[1],
                                  tag_loteria='o',
                                  tem_bolas=to_bool(value[2]),
                                  qtd_bolas=int(value[3]),
                                  qtd_bolas_sorteio=int(value[4]),
                                  dias_sorteio=tuple(map(int, value[5].split('|'))),
                                  faixas=Faixa.from_str(value[6], int(value[3])))

        # como nao ha ainda arquivo HTML de resultados, adiciona os concursos programaticamente:
        _trevo_duplo.parse_concurso()

        return _trevo_duplo

# ----------------------------------------------------------------------------
