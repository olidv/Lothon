"""
   Package lothon.process
   Module analise_dispersao.py

"""

__all__ = [
    'AnaliseDispersao'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
import logging
import statistics as stts

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria, Concurso, SerieSorteio
from lothon.process.analyze.abstract_analyze import AbstractAnalyze


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseDispersao(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('frequencias_dezenas', 'atrasos_dezenas')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Dispersao das Dezenas")

        # estrutura para a coleta de dados a partir do processamento de analise:
        self.frequencias_dezenas: Optional[list[int]] = None
        self.atrasos_dezenas: Optional[list[int]] = None

    # --- METODOS ------------------------------------------------------------

    def list_frequencias(self, bolas: tuple[int, ...]) -> list[int]:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return []

        # obtem as frequencias das bolas:
        frequencias: list[int] = []
        for dezena in bolas:
            frequencias.append(self.frequencias_dezenas[dezena])

        return frequencias

    def list_atrasos(self, bolas: tuple[int, ...]) -> list[int]:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return []

        # obtem os atrasos das bolas:
        atrasos: list[int] = []
        for dezena in bolas:
            atrasos.append(self.atrasos_dezenas[dezena])

        return atrasos

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def list_espacos(cls, bolas: tuple[int, ...]) -> list[int]:
        # valida os parametros:
        if bolas is None or len(bolas) <= 1:  # eh preciso ao menos 2 itens para calcular espacos
            return []

        # obtem os espacamentos entre as bolas:
        espacos: list[int] = []
        aux: int = bolas[0]  # nao precisa iterar no primeiro, p/ agilizar o calculo da diferenca
        for dezena in sorted(bolas[1:]):  # tem q estar ordenada
            dif: int = dezena - aux
            espacos.append(dif)
            aux = dezena

        return espacos

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.frequencias_dezenas = None
        self.atrasos_dezenas = None

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = payload.nome_loteria
        concursos: list[Concurso] = payload.concursos
        qtd_concursos: int = len(concursos)
        qtd_items: int = payload.qtd_bolas

        # efetua analise de todas as dezenas dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de frequencias e atrasos de TODAS as "
                     f"dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de frequencias e atrasos - usa -1 para nao conflitar com teste == 0:
        self.frequencias_dezenas = self.new_list_int(qtd_items, -1)
        self.atrasos_dezenas = self.new_list_int(qtd_items, -1)  #

        # contabiliza as frequencias e atrasos das dezenas em todos os sorteios ja realizados:
        for concurso in reversed(concursos):
            # cada ocorrencia de dezena incrementa sua respectiva frequencia:
            for dezena in concurso.bolas:
                self.frequencias_dezenas[dezena] += 1
                # contabiliza tambem os atrasos, aproveitando a ordem reversa dos concursos:
                if self.atrasos_dezenas[dezena] == -1:
                    self.atrasos_dezenas[dezena] = qtd_concursos - concurso.id_concurso

        # printa o resultado:
        output: str = f"\n\t BOLA:   #SORTEIOS   #ATRASOS\n"
        for idx, frequencia in enumerate(self.frequencias_dezenas[1:]):
            dezena: int = idx + 1
            atrasos: int = self.atrasos_dezenas[dezena]
            output += f"\t   {formatd(dezena,2)}:       " \
                      f"{formatd(frequencia,5)}      " \
                      f"{formatd(atrasos,5)}\n"
        logger.debug(f"{nmlot}: Frequencias e Atrasos de Dezenas Resultantes: {output}")

        # efetua analise de variancia e desvio-padrao das dezenas:
        logger.debug(f"{nmlot}: Executando analise de variancia e desvio-padrao das dezenas "
                     f"sorteadas em TODOS os  {formatd(qtd_concursos)}  concursos da loteria.")

        # inicializa o print de resultado dos contadores de frequencias:
        output: str = f"\n\t CONCURSO  VARIANCIAS:   FREQUENCIAS    ATRASOS    ESPACOS\n"

        # contabiliza as variancias das dezenas em todos os sorteios ja realizados:
        for concurso in concursos:
            list_frequencias: list[int] = self.list_frequencias(concurso.bolas)
            list_atrasos: list[int] = self.list_atrasos(concurso.bolas)
            list_espacos: list[int] = self.list_espacos(concurso.bolas)

            # calcula as medidas estatisticas de dispersao:
            varia_frequencia: float = stts.pstdev(list_frequencias)
            varia_atrasos: float = stts.pstdev(list_atrasos)
            varia_espacos: float = stts.pstdev(list_espacos)

            # formata os valores para o concurso atual:
            output += f"\t    {formatd(concurso.id_concurso,5)}  ...........     " \
                      f"{formatf(varia_frequencia,'9.2')}  " \
                      f"{formatf(varia_atrasos,'9.2')}  " \
                      f"{formatf(varia_espacos,'9.2')}\n"
        # apos percorrer todos os concursos, printa as frequencias medias:
        logger.debug(f"{nmlot}: Variancias das Dezenas Sorteadas: {output}")
        if True is not None:
            return 0

        # efetua analise de atrasos medios das dezenas em todos os concursos:
        logger.debug(f"{nmlot}: Executando analise media de atrasos das dezenas sorteadas "
                     f"em TODOS os  {formatd(qtd_concursos)}  concursos da loteria.")

        # inicializa o print de resultado dos contadores de frequencias:
        output1: str = f"\n\tCONCURSO  ULTIMOS ATRASOS:   MENOR   MAIOR   MODA   MEDIA   MEDIANA\n"
        output2: str = f"\n\tCONCURSO   MEDIAS ATRASOS:   MENOR   MAIOR   MODA   MEDIA   MEDIANA\n"

        # contabiliza os atrasos das dezenas em todos os sorteios ja realizados:
        concursos_anteriores: list[Concurso] = [concursos[0]]
        for concurso in concursos[1:]:
            bolas_concurso: tuple[int, ...] = concurso.bolas
            # registra o atraso de cada dezena sorteada no concurso corrente:
            atrasos: list[SerieSorteio] = self.new_list_series(len(bolas_concurso)-1)
            for concurso_anterior in concursos_anteriores:
                id_dezena: int = -1
                for dezena in bolas_concurso:
                    id_dezena += 1  # na primeira iteracao, vai incrementar para zero
                    if dezena in concurso_anterior.bolas:
                        atrasos[id_dezena].add_sorteio(concurso_anterior.id_concurso)

            # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
            ultimo_concurso: Concurso = concursos_anteriores[-1]
            for serie in atrasos:
                # vai aproveitar e contabilizar as medidas estatisticas para o atraso:
                serie.last_sorteio(ultimo_concurso.id_concurso)

            # formata os valores para o concurso atual:
            ultimos_atrasos: list[int] = sorted([o.ultimo_atraso for o in atrasos])
            output1 += f"\t   {formatd(concurso.id_concurso,5)}  ................   " \
                       f"{formatd(min(ultimos_atrasos),5)}   " \
                       f"{formatd(max(ultimos_atrasos),5)}  " \
                       f"{formatd(round(stts.mode(ultimos_atrasos)),5)}   " \
                       f"{formatd(round(stts.fmean(ultimos_atrasos)),5)}     " \
                       f"{formatd(round(stts.median(ultimos_atrasos)),5)}\n"
            medias_atrasos: list[int] = sorted([round(o.mean_atraso) for o in atrasos])
            output2 += f"\t   {formatd(concurso.id_concurso,5)}  ................   " \
                       f"{formatd(min(medias_atrasos),5)}   " \
                       f"{formatd(max(medias_atrasos),5)}  " \
                       f"{formatd(round(stts.mode(medias_atrasos)),5)}   " \
                       f"{formatd(round(stts.fmean(medias_atrasos)),5)}     " \
                       f"{formatd(round(stts.median(medias_atrasos)),5)}\n"

            # adiciona o concurso atual para a proxima iteracao (ai ele sera um concurso anterior):
            concursos_anteriores.append(concurso)
        # apos percorrer todos os concursos, printa os atrasos medias:
        logger.debug(f"{nmlot}: Atrasos Medios das Dezenas Sorteadas: {output1}\n\n{output2}")

        # efetua analise evolutiva de todos os concursos de maneira progressiva:
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de frequencias dos ultimos  100  "
                     f"concursos da loteria.")

        # formata o cabecalho da impressao do resultado:
        output: str = f"\n\t CONCURSO"
        for val in range(1, payload.qtd_bolas_sorteio + 1):
            output += f"     {val:0>2}"
        output += f"     VARIANCIA     DESVIO-PADRAO\n"

        # acumula os concursos passados para cada concurso atual:
        qtd_concursos_anteriores: int = qtd_concursos - 100
        concursos_anteriores: list[Concurso] = concursos[:qtd_concursos_anteriores]
        for concurso_atual in concursos[qtd_concursos_anteriores:]:
            # zera os contadores de cada concurso:
            dezenas_sorteios: list[int] = self.new_list_int(payload.qtd_bolas)

            # quantas vezes cada uma das bolas sorteadas do concurso atual repetiu nos anteriores:
            for concurso_anterior in concursos_anteriores:
                self.count_repeticoes(concurso_anterior.bolas, dezenas_sorteios)

            # transforma a lista em dicionario para sortear pela frequencia nos sorteios:
            dezenas_frequencias: dict[int: int] = {}
            for key, val in enumerate(dezenas_sorteios):
                dezenas_frequencias[key] = val

            # ordena o dicionario para identificar o ranking de cada dezena:
            dezenas_frequencias = {k: v for k, v in sorted(dezenas_frequencias.items(),
                                                           key=lambda item: item[1], reverse=True)}
            dezenas_ranking: list[int] = self.new_list_int(payload.qtd_bolas)
            idx: int = 0
            for k, v in dezenas_frequencias.items():
                idx += 1  # comeca do ranking #1
                dezenas_ranking[k] = idx

            # prepara para calcular variancia e desvio padrao dos rankings:
            ranking_bolas: list[int] = []

            # printa o resultado do concurso atual:
            output += f"\t   {formatd(concurso_atual.id_concurso,6)}"
            for bola in concurso_atual.bolas:
                ranking: int = dezenas_ranking[bola]
                ranking_bolas.append(ranking)
                output += f"  {formatd(ranking,5)}"

            # calcula a variancia e desvio padrao dos rankings antes do fim da linha:
            varia_rank: float = stts.pvariance(ranking_bolas)
            stdev_rank: float = stts.pstdev(ranking_bolas)
            output += f"     {formatf(varia_rank,'9.3')}         {formatf(stdev_rank,'9.3')} \n"

            # inclui o concurso atual como anterior para a proxima iteracao:
            concursos_anteriores.append(concurso_atual)
        logger.debug(f"{nmlot}: Ranking de Frequencias da EVOLUTIVA: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        self.set_options(parms)

    def evaluate(self, pick) -> float:
        return 1.1  # valor temporario

# ----------------------------------------------------------------------------
