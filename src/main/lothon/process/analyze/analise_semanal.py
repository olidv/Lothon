"""
   Package lothon.process.analyze
   Module  analise_semanal.py

"""

__all__ = [
    'AnaliseSemanal'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria
from lothon.process.analyze.abstract_analyze import AbstractAnalyze
from lothon.process.compute.compute_semanal import ComputeSemanal


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
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise Semanal de Premiacoes")

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, loteria: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if loteria is None or loteria.concursos is None or len(loteria.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = loteria.nome_loteria
        qtd_concursos: int = len(loteria.concursos)
        # qt_acertos_premio_maximo: int = min(loteria.faixas)  # a menor faixa eh o premio principal
        # qtd_items: int = 6  # dias da semana onde ocorrem sorteios - vai de 0=Seg, ..., 6=Dom

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeSemanal()
        cp.execute(loteria)

        # efetua analise de todas as premiacoes dos concursos da loteria:
        logger.debug(f"{nmlot}: Executando analise semanal de premiacoes de TODOS os  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # printa as premiacoes e identifica o dia da semana para cada faixa de premiacao:
        output: str = f"\n\t DIA   #PREMIACOES    PERC%       #GANHADORES   PARTILHA\n"
        total: float = sum(cp.semanal_premiacoes)
        for idx, value in enumerate(cp.semanal_premiacoes):
            percent: float = 0.0 if total == 0 else round((value / total) * 1000) / 10
            ganhadores: int = cp.semanal_ganhadores[idx]
            partilha: float = 0.0 if value == 0 else ganhadores / value
            output += f"\t {DIAS[idx]}        {formatd(value,6)}   {formatf(percent,'5.1')}%" \
                      f"   ...      {formatd(ganhadores,6)}      {formatf(partilha,'5.1')}\n"
        logger.debug(f"{nmlot}: Premiacoes Semanais Resultantes: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
