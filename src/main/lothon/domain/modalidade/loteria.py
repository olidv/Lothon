"""
   Package lothon.domain.modalidade
   Module  loteria.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Any
import logging

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
    dias_sorteio: tuple[int, ...]
    faixas: dict[int, Faixa]

    concursos: Optional[list[Concurso]] = None
    boloes: dict[int: int] = None  # propriedade temporaria para auxiliar processamentos.
    statis: dict[str: Any] = None  # registra as estatisticas apos analise dos sorteios.

    sort_index: str = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.id_loteria)
        # tambem inicializa estrutura para registro das estatisticas coletaas apos analises:
        object.__setattr__(self, 'statis', {})

    # --- METODOS ------------------------------------------------------------

    def get_tag_resultados(self) -> str:
        return self.id_loteria

    def get_file_resultados(self) -> str:
        return self.nome_loteria

    def set_resultados(self, table_body: ResultSet):
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

    @abstractmethod
    def parse_concurso(self, td: ResultSet) -> Concurso:
        pass

    # ----------------------------------------------------------------------------
