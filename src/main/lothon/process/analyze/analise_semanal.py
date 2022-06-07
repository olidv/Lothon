"""
   Package lothon.process
   Module  analise_semanal.py

"""

__all__ = [
    'AnaliseSemanal'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria
from lothon.process.analyze.abstract_analyze import AbstractAnalyze


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# dias da semana para facilitar a impressao dos resultados - acesso = [0] [1] ... [6]
DIAS: tuple[str, ...] = ('Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom')


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseSemanal(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('semanal_premiacoes', 'semanal_ganhadores')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise Semanal de Premiacoes")

        # estrutura para a coleta de dados a partir do processamento de analise:
        self.semanal_premiacoes: Optional[list[int]] = None
        self.semanal_ganhadores: Optional[list[int]] = None

    # --- METODOS STATIC -----------------------------------------------------

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.semanal_premiacoes = None
        self.semanal_ganhadores = None

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = payload.nome_loteria
        qtd_concursos: int = len(payload.concursos)
        qt_acertos_premio_maximo: int = min(payload.faixas)  # a menor faixa eh o premio principal
        qtd_items: int = 6  # dias da semana onde ocorrem sorteios - vai de 0=Seg, ..., 6=Dom

        # efetua analise de todas as premiacoes dos concursos da loteria:
        logger.debug(f"{nmlot}: Executando analise semanal de premiacoes de TODOS os  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de premiacoes:
        self.semanal_premiacoes = self.new_list_int(qtd_items)  # vai de 0=Seg, ..., 6=Dom
        self.semanal_ganhadores = self.new_list_int(qtd_items)

        # contabiliza as premiacoes e identifica o dia da semana para cada faixa de premiacao:
        for concurso in payload.concursos:
            # identifica o numero de ganhadores do premio maximo:
            qt_ganhadores: int = concurso.get_ganhadores_premio(qt_acertos_premio_maximo)
            if qt_ganhadores > 0:
                dia: int = concurso.data_sorteio.weekday()
                self.semanal_premiacoes[dia] += 1
                self.semanal_ganhadores[dia] += qt_ganhadores

        # printa o resultado:
        output: str = f"\n\t DIA   #PREMIACOES    PERC%       #GANHADORES   PARTILHA\n"
        total: float = sum(self.semanal_premiacoes)
        for idx, value in enumerate(self.semanal_premiacoes):
            percent: float = 0.0 if total == 0 else round((value / total) * 1000) / 10
            ganhadores: int = self.semanal_ganhadores[idx]
            partilha: float = 0.0 if value == 0 else ganhadores / value
            output += f"\t {DIAS[idx]}        {formatd(value,6)}   {formatf(percent,'5.1')}%" \
                      f"   ...      {formatd(ganhadores,6)}      {formatf(partilha,'5.1')}\n"
        logger.debug(f"{nmlot}: Premiacoes Semanais Resultantes: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        self.set_options(parms)

    def evaluate(self, payload) -> float:
        return 1.1  # valor temporario

# ----------------------------------------------------------------------------
