"""
   Package lothon.process.analyze
   Module  analise_premiacao.py

"""

__all__ = [
    'AnalisePremiacao'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria, Concurso, SerieSorteio
from lothon.process.analyze.abstract_analyze import AbstractAnalyze
from lothon.process.compute.compute_premiacao import ComputePremiacao


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnalisePremiacao(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Frequencia das Premiacoes Maximas")

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, loterias: dict[str: Loteria]) -> int:
        # valida se possui concursos a serem analisados:
        if loterias is None or len(loterias) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # ao processasr, vai recolher os valores de frequencia em DICT para depois ordenar:
        frequencias_premiacoes: dict[str: SerieSorteio] = {}
        medias_premiacoes: dict[str: float] = {}

        # vai efetuar a computacao das frequencias dos sorteios para todas as loterias:
        for idlot, loteria in loterias.items():
            # identifica informacoes da loteria:
            nmlot: str = loteria.nome_loteria
            concursos: list[Concurso] = loteria.concursos
            qtd_concursos: int = len(concursos)

            # inicializa componente para computacao dos sorteios da loteria:
            cp = ComputePremiacao()
            cp.setup({
                'qtd_bolas_sorteio': loteria.qtd_bolas_sorteio
            })
            # efetua analise de todas as dezenas dos sorteios da loteria:
            logger.debug(f"{nmlot}: Executando analise da frequencia de TODAS as "
                         f"premiacoes nos  {formatd(qtd_concursos)}  concursos da loteria...")
            cp.execute(loteria.concursos)

            # salva a frequencia das premiacoes para depois imprimir:
            frequencias_premiacoes[idlot] = cp.frequencia_premiacoes
            medias_premiacoes[idlot] = qtd_concursos / cp.frequencia_premiacoes.len_sorteios

        # ordena o DICT de frequencias pela media de premiacoes (ascendente):
        medias_premiacoes = {k: v for k, v in sorted(medias_premiacoes.items(),
                                                     key=lambda item: item[1])}

        # vai printar as frequencias e atrasos das premiacoes maximas em todos os sorteios:
        output: str = f"\n\t LOTERIA          #CONCURSOS      #PREMIADOS   ULTIMO   MEDIA      "\
                      f"#ATRASOS   ULTIMO   MAIOR   MEDIA\n"
        for idlot, media_premiacoes in medias_premiacoes.items():
            # identifica informacoes da loteria:
            nmlot: str = loterias[idlot].nome_loteria
            concursos: list[Concurso] = loterias[idlot].concursos
            qtd_concursos: int = len(concursos)
            serie = frequencias_premiacoes[idlot]

            # formata para impressao os resultados da loteria corrente:
            output += f"\n\t {nmlot:17}     " \
                      f"{formatd(qtd_concursos,5)}           " \
                      f"{formatd(serie.len_sorteios,5)}    " \
                      f"{formatd(serie.ultimo_sorteio,5)}   " \
                      f"{formatf(media_premiacoes,'5.1')}         " \
                      f"{formatd(serie.len_atrasos,5)}      " \
                      f"{formatd(serie.ultimo_atraso,3)}     " \
                      f"{formatd(serie.max_atraso,3)}   " \
                      f"{formatf(serie.mean_atraso,'5.1')}\n"

        # printa o quadro comparativo contendo o resultado geral da computacao:
        logger.debug(f"LOTERIAS: Frequencia das Premiacoes Maximas: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"LOTERIAS: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
