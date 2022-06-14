"""
   Package lothon.process.analyze
   Module  analise_somatorio.py

"""

__all__ = [
    'AnaliseSomatorio'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
from lothon.domain import Loteria, Concurso
from lothon.process.analyze.abstract_analyze import AbstractAnalyze
from lothon.process.compute.compute_somatorio import ComputeSomatorio


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseSomatorio(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Somatorio das Dezenas")

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
        qtd_jogos: int = loteria.qtd_jogos
        concursos: list[Concurso] = loteria.concursos
        qtd_concursos: int = len(concursos)
        # qtd_items: int = sum(range(loteria.qtd_bolas - loteria.qtd_bolas_sorteio + 1,
        #                            loteria.qtd_bolas + 1)) + 1  # soma 1 para nao usar zero-index.

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeSomatorio()
        cp.execute(loteria)

        # efetua analise de todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise de somatorio dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # printa o somatorio de cada combinacao de jogo:
        output: str = f"\n\t   ? SOMADO      PERC%     #TOTAL\n"
        for key, value in enumerate(cp.somatorios_jogos):
            percent: float = cp.somatorios_percentos[key]
            output += f"\t {formatd(key,3)} somado:  {formatf(percent,'7.3')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Somatorios Resultantes: {output}")

        # efetua analise diferencial dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise TOTAL de somatorio dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # printa o somatorio de cada sorteio dos concursos:
        output: str = f"\n\t   ? SOMADO      PERC%        %DIF%     #TOTAL\n"
        for key, value in enumerate(cp.somatorios_concursos):
            percent: float = round((value / qtd_concursos) * 100000) / 1000
            dif: float = percent - cp.somatorios_percentos[key]
            output += f"\t {formatd(key,3)} somado:  {formatf(percent,'7.3')}% ... " \
                      f"{formatf(dif,'7.3')}%     #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Somatorios Resultantes: {output}")

        # printa quais os somatorios que repetiram no ultimo sorteio dos concursos:
        output: str = f"\n\t   ? SOMADO     PERC%       #REPETIDOS\n"
        for key, value in enumerate(cp.ultimos_somatorios_repetidos):
            percent: float = cp.ultimos_somatorios_percentos[key]
            output += f"\t {formatd(key,3)} somado:  {formatf(percent,'6.2')}%  ...  " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Concursos que repetiram o ultimo somatorio: {output}")

        # efetua analise comparativa dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise COMPARATIVA de somatorio dos  "
                     f"{qtd_concursos:,}  concursos da loteria.")

        # contabiliza a somatorio de cada sorteio dos concursos para exibicao em lista sequencial:
        output: str = f"\n\t CONCURSO   SOMA         JOGOS%    #TOTAL CONCURSOS\n"
        for concurso in concursos:
            soma_dezenas = cb.soma_dezenas(concurso.bolas)
            percent = cp.somatorios_percentos[soma_dezenas]
            total = cp.somatorios_concursos[soma_dezenas]
            output += f"\t    {formatd(concurso.id_concurso,5)}    {formatd(soma_dezenas,3)}  " \
                      f"...  {formatf(percent,'7.3')}%    #{formatd(total)}\n"

        # printa o resultado:
        logger.debug(f"{nmlot}: COMPARATIVA dos Somatorios Resultantes: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
