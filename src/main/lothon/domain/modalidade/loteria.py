"""
   Package lothon.domain.modalidade
   Module  loteria.py

"""

__all__ = [
    'Loteria'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import logging
import math

# Libs/Frameworks modules
from bs4.element import ResultSet

# Own/Project modules
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.bilhete.faixa import Faixa


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE ABSTRATA
# ----------------------------------------------------------------------------

@dataclass(order=True)
class Loteria(ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de classes
    que representam as loterias da Caixa.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    id_loteria: str
    nome_loteria: str
    tem_bolas: bool
    qtd_bolas: int
    qtd_bolas_sorteio: int
    qtd_jogos: int = field(init=False)
    dias_sorteio: tuple[int, ...]
    faixas: dict[int, Faixa]
    concursos: Optional[list[Concurso]] = None

    sort_index: str = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'qtd_jogos', math.comb(self.qtd_bolas, self.qtd_bolas_sorteio))
        object.__setattr__(self, 'sort_index', self.id_loteria)

    # --- METODOS ------------------------------------------------------------

    def get_tag_resultados(self) -> str:
        return self.id_loteria

    def get_file_resultados(self) -> str:
        return self.nome_loteria

    def set_resultados(self, table_body: ResultSet) -> int:
        # dentro do TBODY tem uma unica TR contendo os dados relacionados em elementos TD:
        list_concursos: list[Concurso] = []
        for tbody in table_body:
            tr = tbody.find("tr", recursive=False)
            # logger.debug(f"tr = {type(tr)} {len(tr)}")
            td = tr.find_all("td", recursive=False)
            # logger.debug(f"td = {type(td)} {len(td)}")
            # logger.debug(f"td[0] = {type(td[0])} {len(td[0])} {td[0].text}")

            concurso = self.parse_concurso(td)
            # logger.debug(f"concurso = {concurso}")
            list_concursos.append(concurso)

        self.concursos = list_concursos
        return len(list_concursos)

    @abstractmethod
    def parse_concurso(self, td: ResultSet) -> Concurso:
        pass

    # ----------------------------------------------------------------------------
