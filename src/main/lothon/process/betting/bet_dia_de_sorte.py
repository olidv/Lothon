"""
   Package lothon.process.compute
   Module  bet_dia_de_sorte.py

"""

__all__ = [
    'BetDiaDeSorte'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import itertools as itt
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
from lothon.domain import Loteria, Concurso
from lothon.process.betting.abstract_betting import AbstractBetting

# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# faixas de limites de recorrencias especificas para esta loteria:
FAIXAS_RECORRENCIAS: dict[int: int] = {0: 3, 1: 6, 2: 39, 3: 271, 4: 2.939}

# medidas otimas de equilibrio de paridades para boloes:
PARIDADES_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
SEQUENCIAS_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
AUSENCIAS_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
FREQUENCIAS_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
REPETENCIAS_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class BetDiaDeSorte(AbstractBetting):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('loteria_mes', 'concursos_mes', 'meses')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, loteria1: Loteria, loteria2: Loteria):
        super().__init__("Geracao de Jogos para 'Dia de Sorte'", loteria1)

        # mantem as informacoes da loteria secundaria mes da sorte:
        self.loteria_mes: Loteria = loteria2
        self.concursos_mes: list[Concurso] = loteria2.concursos
        self.meses: list[int] = []

    # --- METODOS HELPERS ----------------------------------------------------

    def compute_meses_sorteados(self) -> list[int]:
        # extrai o ranking dos meses a partir dos topos de frequencias e ausencias nos concursos:
        meses_frequentes: list[int] = cb.calc_topos_frequencia(self.concursos_mes,
                                                               self.loteria_mes.qtd_bolas,
                                                               self.loteria_mes.qtd_bolas)
        meses_ausentes: list[int] = cb.calc_topos_ausencia(self.concursos_mes,
                                                           self.loteria_mes.qtd_bolas,
                                                           self.loteria_mes.qtd_bolas)

        meses_computados: list[int] = cb.merge_topos(meses_frequentes, meses_ausentes)
        return meses_computados

    def add_mes_da_sorte(self, apostas: list[tuple[int, ...]]) -> list[tuple]:
        apostas_com_mes: list[tuple] = []

        last_idx: int = len(self.meses) - 1  # idx_mes vai circular entre 0 ... 11
        idx_mes: int = last_idx
        for aposta in apostas:
            idx_mes = 0 if (idx_mes == last_idx) else (idx_mes + 1)
            mes_da_sorte: int = self.meses[idx_mes]
            aposta += (mes_da_sorte,)  # mes no formato numerico (1 ... 12)
            apostas_com_mes.append(aposta)

        return apostas_com_mes

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, bolao: dict[int: int], concursos: list[Concurso] = None) -> list[tuple]:
        # valida se possui concursos a serem analisados:
        if bolao is None or len(bolao) == 0:
            return []
        elif concursos is not None:
            if len(concursos) > 0:
                self.concursos = concursos
            else:
                return []
        _startWatch = startwatch()

        # verifica se os concursos ja foram computados e gerou arquivo com jogos computados:
        if self.existe_jogos_computados():
            logger.debug("Arquivo com jogos computados ja existe. Processo externo ignorado.")
        # se ainda nao existe o arquivo com os jogos computados, entao inicia o processo externo:
        else:
            logger.debug("Arquivo com jogos computados nao encontrado. Iniciando processo externo.")
            # Vai exportar os arquivos CSV com dezenas sorteadas das loterias...
            qtd_export: int = self.exportar_sorteios()
            logger.debug(f"Foram exportados  #{formatd(qtd_export)}  sorteios da loteria "
                         f"'{self.loteria.nome_loteria}' em arquivo CSV.")

            # executa rotina Java para processamento e geracao dos jogos computados:
            run_ok: bool = self.executar_jlothon()
            if run_ok:
                logger.debug(f"Programa jLothon foi executado com sucesso.")
            else:
                logger.error(f"Erro na execucao do programa jLothon. Geracao de boloes abortada.")
                return []

        # importa os jogos computados em jLothon para prosseguir com o processamento:
        self.jogos = self.importar_jogos()
        qtd_jogos: int = len(self.jogos)
        logger.debug(f"Foram importados  #{formatd(qtd_jogos)}  jogos computados da loteria "
                     f"{self.loteria.nome_loteria}' de arquivo CSV.")

        # contabiliza as frequencias das dezenas em todos os jogos considerados:
        logger.debug("Processando sorteios e jogos para computacao de frequencias e ausencias...")
        topos_dezenas: list[int] = self.get_topos_dezenas_jogos(10)

        # antes de gerar os jogos, calcula o maximo de recorrencias para o bolao a ser gerado:
        # com o numero real de apostas, verifica qual a faixa de recorrencias ira utilizar:
        max_recorrencias: int = self.get_max_recorrencias(bolao, FAIXAS_RECORRENCIAS)
        logger.info(f"Vai utilizar como maximo de recorrencias a faixa  {max_recorrencias}.")

        # com as dezenas sorteadas ja computadas e organizadas, agora processa os meses da sorte:
        logger.debug("Executando computacao dos sorteios do Mes da Sorte...")
        self.meses = self.compute_meses_sorteados()
        logger.debug(f"Ranking dos meses da sorte conforme frequencias e ausencias:\n"
                     f"\t{self.meses}")

        # inicia a geracao do bolao, sorteando jogos para as apostas:
        logger.debug(f"Iniciando a geracao do bolao para loteria DIA-DE-SORTE...")
        apostas_sorteadas: list[tuple[int, ...]] = []  # aqui estao as apostas
        jogos_bolao: list[tuple[int, ...]] = []  # aqui estao todas as combinacoes das apostas
        # utiliza os topos acumulados (merge) para complementar os jogos com mais dezenas:
        for qtd_dezenas, qtd_apostas in bolao.items():
            # se o numero de apostas estiver zerado, entao ignora esta faixa
            if qtd_apostas == 0:
                continue

            # efetua o sorteio do(s) jogo(s) com o numero de dezenas requerido:
            for _ in range(0, qtd_apostas):
                jogo_sorteado: tuple[int, ...] = self.sortear_jogo(max_recorrencias, jogos_bolao)
                # se for um numero maior de dezenas, eh preciso complementar o jogo:
                if qtd_dezenas > self.loteria.qtd_bolas_sorteio:
                    qtd_add: int = qtd_dezenas - self.loteria.qtd_bolas_sorteio
                    # obtem mais qtd-add dezenas a partir da lista topo-dezenas (do inicio):
                    for dezena in topos_dezenas:
                        # se ja pegou as dezenas necessarias, pula fora
                        if qtd_add == 0:
                            break
                        # eh preciso verificar se a dezena ja esta no jogo sorteado antes:
                        elif dezena not in jogo_sorteado:
                            qtd_add -= 1
                            jogo_sorteado += (dezena,)

                # se nao houver problema com as recorrencias, adiciona o jogo sorteado ao bolao:
                apostas_sorteadas.append(jogo_sorteado)
                # se for um numero maior de dezenas, tem q gerar os jogos de base antes de incluir:
                if len(jogo_sorteado) == self.loteria.qtd_bolas_sorteio:
                    jogos_bolao.append(jogo_sorteado)
                else:
                    for jogo in itt.combinations(jogo_sorteado, self.loteria.qtd_bolas_sorteio):
                        jogos_bolao.append(jogo)

        # com os jogos gerados, adiciona o mes da sorte:
        apostas_bolao: list[tuple] = self.add_mes_da_sorte(apostas_sorteadas)
        logger.debug(f"Finalizada a geracao do bolao para loteria DIA-DE-SORTE: \n{apostas_bolao}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return apostas_bolao

# ----------------------------------------------------------------------------
