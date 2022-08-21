"""
   Package lothon.process.analyze
   Module  analise_unitario.py

"""

__all__ = [
    'AnaliseUnitario'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria, Concurso
from lothon.process.analyze.abstract_analyze import AbstractAnalyze
from lothon.process.compute.compute_unitario import ComputeUnitario


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseUnitario(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Sorteios Unitarios")

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
        concursos: list[Concurso] = loteria.concursos
        qtd_concursos: int = len(concursos)

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeUnitario()
        cp.setup({
            'qtd_bolas': loteria.qtd_bolas,
            'qtd_bolas_sorteio': loteria.qtd_bolas_sorteio,
            'qtd_jogos': loteria.qtd_jogos
        })
        cp.execute(loteria.concursos)

        # efetua analise de todas as dezenas dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de frequencia de TODAS as "
                     f"dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # printa as frequencias e atrasos das dezenas em todos os sorteios ja realizados:
        output: str = f"\n\t  MES:   #SORTEIOS   ULTIMO      #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA   MEDIA   H.MEDIA   G.MEDIA      MEDIANA   " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in cp.frequencias_meses[1:]:
            output += f"\t  {formatd(serie.id,3)}:       " \
                      f"{formatd(serie.len_sorteios,5)}    " \
                      f"{formatd(serie.ultimo_sorteio,5)}           " \
                      f"{formatd(serie.len_atrasos,3)}      " \
                      f"{formatd(serie.ultimo_atraso,3)}     " \
                      f"{formatd(serie.min_atraso,3)}    " \
                      f"{formatd(serie.max_atraso,3)}     " \
                      f"{formatd(serie.mode_atraso,3)}   " \
                      f"{formatf(serie.mean_atraso,'5.1')}     " \
                      f"{formatf(serie.hmean_atraso,'5.1')}     " \
                      f"{formatf(serie.gmean_atraso,'5.1')}        " \
                      f"{formatf(serie.median_atraso,'5.1')}       " \
                      f"{formatf(serie.varia_atraso,'5.1')}           " \
                      f"{formatf(serie.stdev_atraso,'5.1')}\n"
        logger.debug(f"{nmlot}: Frequencia Resultante de Meses Sorteados: {output}")

        # efetua comparacao do ranking de frequencias versus ausencias:
        output: str = f"\n\t RANKING:    TOPOS FREQUENCIAS     TOPOS AUSENCIAS\n"
        for idx in range(0, 12):
            # formata os valores para cada posicao do ranking:
            output += f"\t      {formatd(idx+1,2)}                 " \
                      f"{formatd(cp.topos_frequentes[idx],5)}               " \
                      f"{formatd(cp.topos_ausentes[idx],5)}\n"
        logger.debug(f"{nmlot}: Comparativo dos rankings de frequencias versus ausencias: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
