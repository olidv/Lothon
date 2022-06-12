"""
   Package lothon.process.analyze
   Module  analise_distancia.py

"""

__all__ = [
    'AnaliseDistancia'
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
from lothon.process.compute.compute_distancia import ComputeDistancia


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseDistancia(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Distancia nos Concursos")

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = payload.nome_loteria
        qtd_jogos: int = payload.qtd_jogos
        concursos: list[Concurso] = payload.concursos
        qtd_concursos: int = len(concursos)
        qtd_items: int = payload.qtd_bolas

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeDistancia()
        cp.execute(payload)

        # efetua analise de todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise de distancia dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # printa a distancia de cada combinacao de jogo:
        output: str = f"\n\t  ? DISTANTE     PERC%     #TOTAL\n"
        for key, value in enumerate(cp.distancias_jogos):
            percent: float = cp.distancias_percentos[key]
            output += f"\t {formatd(key,2)} distante:  {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Distancias Resultantes: {output}")

        # efetua analise diferencial dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise TOTAL de distancia dos  "
                     f"{formatf(qtd_concursos)}  concursos da loteria.")

        # printa a distancia de cada sorteio dos concursos:
        output: str = f"\n\t  ? DISTANTE     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(cp.distancias_concursos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            dif: float = percent - cp.distancias_percentos[key]
            output += f"\t {formatd(key,2)} distante:  {formatf(percent,'6.2')}% ... " \
                      f"{formatf(dif,'6.2')}%     #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Distancias Resultantes: {output}")

        # efetua analise comparativa dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise COMPARATIVA de distancia dos  "
                     f"{qtd_concursos:,}  concursos da loteria.")

        # contabiliza a distancia de cada sorteio dos concursos para exibicao em lista sequencial:
        output: str = f"\n\t CONCURSO   DISTANCIA         JOGOS%    #TOTAL CONCURSOS\n"
        for concurso in concursos:
            vl_distancia = cb.calc_distancia(concurso.bolas)
            percent = cp.distancias_percentos[vl_distancia]
            total = cp.distancias_concursos[vl_distancia]
            output += f"\t    {formatd(concurso.id_concurso,5)}         {formatd(vl_distancia,3)}"\
                      f"  ...   {formatf(percent,'6.2')}%    #{formatd(total)}\n"

        # printa o resultado:
        logger.debug(f"{nmlot}: COMPARATIVA das Distancias Resultantes: {output}")

        # efetua analise evolutiva de todos os concursos de maneira progressiva:
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de distancia dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # calcula distancias dos extremos de cada evolucao de concurso:
        concursos_passados: list[Concurso] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        list6_distancias: list[int] = []
        for concurso_atual in payload.concursos:
            # zera os contadores de cada distancia:
            distancias_passadas: list[int] = cb.new_list_int(qtd_items)

            # calcula a distancia nos concursos passados ate o concurso anterior:
            for concurso_passado in concursos_passados:
                vl_distancia_passada = cb.calc_distancia(concurso_passado.bolas)
                distancias_passadas[vl_distancia_passada] += 1

            # calcula a distancia do concurso atual para comparar a evolucao:
            vl_distancia_atual = cb.calc_distancia(concurso_atual.bolas)
            list6_distancias.append(vl_distancia_atual)
            # soh mantem as ultimas 6 distancias:
            while len(list6_distancias) > 6:
                del list6_distancias[0]

            # printa o resultado:
            output: str = f"\n\t  ? DISTANTE     PERC%       %DIF%  " \
                          f"----->  CONCURSO Nr {concurso_atual.id_concurso} :  " \
                          f"Ultimas Distancias == { list(reversed(list6_distancias))}\n"
            for key, value in enumerate(distancias_passadas):
                percent: float = round((value / qtd_concursos_passados) * 10000) / 100
                dif: float = percent - cp.distancias_percentos[key]
                output += f"\t {formatd(key,2)} distante:  {formatf(percent,'6.2')}% ... " \
                          f"{formatf(dif,'6.2')}%\n"
            logger.debug(f"{nmlot}: Distancias Resultantes da EVOLUTIVA: {output}")

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
