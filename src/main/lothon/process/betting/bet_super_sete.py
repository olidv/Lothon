"""
   Package lothon.process.quickpick
   Module  bet_super_sete.py

"""

__all__ = [
    'BetSuperSete'
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
from lothon.process.betting.abstract_betting import AbstractBetting


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# limite de recorrencias especificas para esta loteria:
FAIXA_RECORRENCIAS: int = 6


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class BetSuperSete(AbstractBetting):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, loteria: Loteria):
        super().__init__("Criacao de Boloes para Super Sete", loteria)

    # --- METODOS ------------------------------------------------------------

    @classmethod
    def check_jogos_iguais(cls, jogo: tuple[int, ...], list_jogos: list[tuple[int, ...]]) -> bool:
        # percorre todos os concursos e verifica se o jogo nao repetiu algum sorteio:
        for jogo_da_lista in list_jogos:
            if jogo == jogo_da_lista:
                return False

        # se chegou ate o final, entao o jogo nao repetiu nenhum sorteio/concurso...
        return True

    def gerar_palpite(self, qtd_dezenas: int,
                      jogos_sorteados: list[tuple[int, ...]]) -> tuple[int, ...]:
        # vai sortear um jogo, mas eh preciso verificar as recorrencias com os jogos ja sorteados:
        jogo_sorteado: tuple[int, ...]
        while True:
            # gera um jogo qualquer, sem repetir muitas dezenas de algum jogo ja sorteado:
            jogo_sorteado = cb.sortear_palpite_digito(qtd_dezenas)

            # o jogo não pode possuir recorrencias com os outros jogos ou concursos ja sorteados:
            if self.check_jogos_iguais(jogo_sorteado, jogos_sorteados) \
                    and self.check_concursos_passados(jogo_sorteado):
                break  # este jogo pode ser aproveitado

        return jogo_sorteado

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

        # identifica informacoes da loteria:
        nmlot: str = self.loteria.nome_loteria

        # antes de gerar os palpites, calcula o maximo de recorrencias para cada jogo sorteado:
        # com o numero real de apostas, verifica qual a faixa de recorrencias ira utilizar:
        max_recorrencias: int = FAIXA_RECORRENCIAS
        logger.info(f"{nmlot}: Vai utilizar como maximo de recorrencias a faixa  "
                    f"{max_recorrencias}.")

        # inicia a criacao do bolao, sorteando jogos para as apostas:
        logger.debug(f"{nmlot}: Iniciando a criacao do bolao para a loteria...")
        jogos_sorteados: list[tuple[int, ...]] = []  # aqui estao as apostas geradas
        # utiliza os topos acumulados (merge) para complementar os jogos com mais dezenas:
        for qtd_dezenas, qtd_apostas in bolao.items():
            # se o numero de apostas estiver zerado, entao ignora esta faixa
            if qtd_apostas == 0:
                continue

            # efetua o sorteio do(s) jogo(s) com o numero de dezenas requerido:
            for _ in range(0, qtd_apostas):
                jogo_sorteado: tuple[int, ...] = self.gerar_palpite(qtd_dezenas, jogos_sorteados)
                # adiciona o jogo sorteado a lista de palpites:
                jogos_sorteados.append(jogo_sorteado)

        logger.debug(f"{nmlot}: Finalizada a criacao de boloes para a loteria.")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return jogos_sorteados

# ----------------------------------------------------------------------------
