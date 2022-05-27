"""
   Package lothon.process
   Module  analise_frequencia.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria, Concurso, ConcursoDuplo, Bola
from lothon.process.analyze.abstract_analyze import AbstractAnalyze


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseFrequencia(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_process', '_options'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Frequencia dos Concursos")

    # --- METODOS STATIC -----------------------------------------------------

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # o numero de sorteios realizados pode dobrar se for instancia de ConcursoDuplo:
        nmlot: str = payload.nome_loteria
        concursos: list[Concurso | ConcursoDuplo] = payload.concursos
        qtd_concursos: int = len(concursos)
        eh_duplo: bool = ([0] is ConcursoDuplo)
        # if eh_duplo:
        #     fator_sorteios: int = 2
        # else:
        #     fator_sorteios: int = 1
        # qtd_sorteios: int = qtd_concursos * fator_sorteios
        qtd_items: int = payload.qtd_bolas

        # efetua analise de todas as dezenas dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de frequencia de TODAS as "
                     f"dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de frequencias e atrasos:
        dezenas: list[Bola | None] = self.new_list_bolas(qtd_items)

        # contabiliza as frequencias e atrasos das dezenas em todos os sorteios ja realizados:
        for concurso in concursos:
            # registra o concurso para cada dezena sorteada:
            for bola in concurso.bolas:
                dezenas[bola].add_sorteio(concurso.id_concurso)

            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                # se for concurso duplo, precisa comparar as bolas do segundo sorteio:
                for bola in concurso.bolas2:
                    dezenas[bola].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso | ConcursoDuplo = concursos[-1]
        for bola in dezenas:
            # ignora o primeiro item, criado apenas para evitar acesso zero-index
            if bola is None or bola.id_bola == 0:
                continue

            # vai aproveitar e contabilizar as medidas estatisticas para a bola:
            bola.last_concurso(ultimo_concurso.id_concurso)

        # printa o resultado:
        output: str = f"\n\t BOLA:   #SORTEIOS   ULTIMO      #ATRASOS   ULTIMO   MAIOR   " \
                      f"MENOR   MODA   MEDIA   H.MEDIA   G.MEDIA      MEDIANA   " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for bola in dezenas:
            if bola is None or bola.id_bola == 0:
                continue

            output += f"\t  {formatd(bola.id_bola,3)}:       " \
                      f"{formatd(bola.len_sorteios,5)}    " \
                      f"{formatd(bola.ultimo_sorteio,5)}           " \
                      f"{formatd(bola.len_atrasos,3)}      " \
                      f"{formatd(bola.ultimo_atraso,3)}     " \
                      f"{formatd(bola.max_atraso,3)}     " \
                      f"{formatd(bola.min_atraso,3)}    " \
                      f"{formatd(bola.mode_atraso,3)}   " \
                      f"{formatf(bola.mean_atraso,'5.1')}     " \
                      f"{formatf(bola.hmean_atraso,'5.1')}     " \
                      f"{formatf(bola.gmean_atraso,'5.1')}        " \
                      f"{formatf(bola.median_atraso,'5.1')}       " \
                      f"{formatf(bola.varia_atraso,'5.1')}           " \
                      f"{formatf(bola.stdev_atraso,'5.1')} \n"

        logger.debug(f"{nmlot}: Frequencia de Dezenas Resultantes: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
