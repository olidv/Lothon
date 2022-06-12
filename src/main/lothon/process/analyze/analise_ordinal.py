"""
   Package lothon.process.analyze
   Module  analise_ordinal.py

"""

__all__ = [
    'AnaliseOrdinal'
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
from lothon.process.compute.compute_ordinal import ComputeOrdinal


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseOrdinal(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise Ordinal dos Sorteios")

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
        # qtd_items: int = qtd_concursos

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeOrdinal()
        cp.execute(payload)

        # efetua analise de todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise ordinal dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # printa para cada concurso, o respectivo ordinal das combinacoes de jogos da loteria:
        output: str = f"\n\t ORDEM     PERC%     #CONCURSOS\n"
        for key, value in enumerate(cp.parciais_concursos):
            percent: float = round((value / qtd_concursos) * 1000) / 10
            output += f"\t    {key:0>2}    {formatf(percent,'5.1')}% ... {value:,}\n"
        logger.debug(f"{nmlot}: Concursos para cada Ordem de 100mil jogos: {output}")

        # calcula o diferencial em percentual entre o concurso e os demais abaixo e acima:
        vl_ordinal_anterior: int = cp.ordinais_concursos[1]  # ordinal do primeiro concurso
        # formata o cabecalho da impressao do resultado:
        output: str = f"\n\t CONCURSO         #ORDINAL      ANTERIOR   ABAIXO%       " \
                      f"PROXIMO   ACIMA%\n"
        for concurso in concursos:
            idx: int = concurso.id_concurso
            # verifica o ordinal do concurso atual e diferenca com ordinal do anterior:
            vl_ordinal_atual: int = cp.ordinais_concursos[idx]  # esta sincronizado com concursos
            dif_ordinal_anterior: int = abs(vl_ordinal_atual - vl_ordinal_anterior)
            dif_percent_abaixo: int = round((dif_ordinal_anterior / qtd_jogos) * 100)
            # calcula a diferenca com o ordinal do proximo concurso:
            idx_next: int = idx + 1
            dif_ordinal_proximo: int = abs(cp.ordinais_concursos[idx_next] -
                                           vl_ordinal_atual) if idx_next <= qtd_concursos else 0
            dif_percent_acima: int = round((dif_ordinal_proximo / qtd_jogos) * 100)

            # printa os valores do concurso atual:
            output += f"\t    {formatd(concurso.id_concurso,5)}  ...  " \
                      f"{formatd(vl_ordinal_atual,10)}    " \
                      f"{formatd(dif_ordinal_anterior,10)}      " \
                      f"{formatd(dif_percent_abaixo,3)}%    " \
                      f"{formatd(dif_ordinal_proximo,10)}     " \
                      f"{formatd(dif_percent_acima,3)}%\n"

            # atualiza o anterior (atual) para a proxima iteracao:
            vl_ordinal_anterior = vl_ordinal_atual
        logger.debug(f"{nmlot}: Relacao de Ordinais dos Concursos: {output}")

        # printa o resultado das faixas de percentuais:
        output: str = f"\n\t ABAIXO%     PERC%     #CONCURSOS\n"
        for key, value in enumerate(cp.ordinais_percentos):
            percent: float = round((value / qtd_concursos) * 1000) / 10
            output += f"\t     {key*10:0>2}%    {formatf(percent,'5.1')}% ... {value:,}\n"
        logger.debug(f"{nmlot}: Concursos para cada faixa de ordinais: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
