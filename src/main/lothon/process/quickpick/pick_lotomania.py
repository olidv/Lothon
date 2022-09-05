"""
   Package lothon.process.quickpick
   Module  pick_lotomania.py

"""

__all__ = [
    'PickLotomania'
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
from lothon.process.quickpick.abstract_quickpick import AbstractQuickPick


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# faixas de limites de recorrencias especificas para esta loteria:
FAIXA_RECORRENCIAS: int = 29

# a loteria lotomania permite a aposta com 50 dezenas, embora sejam sorteadas apenas 20:
QTD_BOLAS_APOSTA = 50


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class PickLotomania(AbstractQuickPick):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, loteria: Loteria):
        super().__init__("Geracao de Palpites para Lotomania", loteria)

    # --- METODOS ------------------------------------------------------------

    @classmethod
    def substitui_100(cls, jogo: tuple[int, ...]) -> tuple[int, ...]:
        # se tupla possuir 100, substitui por 00:
        if 100 in jogo:
            return tuple(sorted([dez % 100 for dez in jogo]))
        else:
            return jogo

    def gerar_palpite(self, max_recorrencias: int,
                      jogos_sorteados: list[tuple[int, ...]]) -> tuple[int, ...]:
        # vai sortear um jogo, mas eh preciso verificar as recorrencias com os jogos ja sorteados:
        jogo_sorteado: tuple[int, ...]
        while True:
            # gera um jogo qualquer, sem repetir muitas dezenas de algum jogo ja sorteado:
            jogo_sorteado = cb.sortear_palpite(self.loteria.qtd_bolas, QTD_BOLAS_APOSTA)
            # a dezena 100 eh substituida pela dezena 00:
            jogo_sorteado = self.substitui_100(jogo_sorteado)

            # o jogo não pode possuir recorrencias com os outros jogos ou concursos ja sorteados:
            if cb.check_max_recorrencias(jogo_sorteado, jogos_sorteados, max_recorrencias):
                break  # este jogo pode ser aproveitado

        return jogo_sorteado

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, qtd_palpites: int, concursos: list[Concurso] = None) -> list[tuple]:
        # valida se possui concursos a serem analisados:
        if qtd_palpites is None or qtd_palpites == 0:
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

        # inicia a geracao dos palpites, sorteando jogos para as apostas:
        logger.debug(f"{nmlot}: Iniciando a geracao dos palpites para a loteria...")
        jogos_sorteados: list[tuple[int, ...]] = []  # aqui estao todos os palpites

        # efetua o sorteio do(s) jogo(s) com o numero de dezenas requerido:
        for _ in range(0, qtd_palpites):
            jogo_sorteado: tuple[int, ...] = self.gerar_palpite(max_recorrencias, jogos_sorteados)
            # adiciona o jogo sorteado a lista de palpites:
            jogos_sorteados.append(jogo_sorteado)

        # com os jogos gerados, converte as dezenas das tuplas em strings de 2 digitos:
        palpites: list[tuple[str, ...]] = [tuple(f"{i:02}" for i in t) for t in jogos_sorteados]
        logger.debug(f"{nmlot}: Finalizada a geracao dos palpites para a loteria: \n"
                     f"{palpites}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return palpites

# ----------------------------------------------------------------------------
