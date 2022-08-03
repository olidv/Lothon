"""
   Package lothon.process
   Module  abstract_betting.py

"""

__all__ = [
    'AbstractBetting'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from abc import ABC, abstractmethod
from typing import Any
import math
import random

# Libs/Frameworks modules
# Own/Project modules
from lothon.infra import console, parser_resultados
from lothon.stats import combinatoria as cb
from lothon import domain
from lothon.domain import Loteria, Concurso, Jogo
from lothon.process.abstract_process import AbstractProcess
from lothon.process.compute.compute_ausencia import ComputeAusencia
from lothon.process.compute.compute_frequencia import ComputeFrequencia


# ----------------------------------------------------------------------------
# CLASSE ABSTRATA
# ----------------------------------------------------------------------------

class AbstractBetting(AbstractProcess, ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de
    processos de computacao e calculo de jogos.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('loteria', 'concursos', 'jogos')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idp: str, loteria: Loteria):
        super().__init__(idp)

        # auxiliares para avaliacao de jogos combinados e concursos da loteria:
        self.loteria: Loteria = loteria
        self.concursos: list[Concurso] = loteria.concursos
        self.jogos: list[Jogo] = []

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- METODOS ------------------------------------------------------------

    @abstractmethod
    def execute(self, bolao: dict[int: int],
                concursos: list[Concurso] = None) -> list[tuple]:
        pass

    # --- METODOS HELPERS ----------------------------------------------------

    def executar_jlothon(self) -> bool:
        # executa rotina Java para processamento e geracao dos jogos computados:
        run_ok: bool = console.execute_jlothon(self.loteria.tag_loteria)
        return run_ok

    def existe_jogos_computados(self):
        return parser_resultados.exist_jogos_loteria(self.loteria.nome_loteria)

    def exportar_sorteios(self):
        # o local de gravacao dos arquivos ja foi padronizado na configuracao INI
        qtd_export: int = domain.export_sorteios(self.loteria)
        return qtd_export

    def importar_jogos(self):
        # importa os jogos computados em jLothon para prosseguir com o processamento:
        jogos_csv: list[Jogo] = parser_resultados.read_jogos_loteria(self.loteria.nome_loteria)
        return jogos_csv

    def get_topos_dezenas(self):
        # contabiliza as frequencias das dezenas em todos os jogos considerados:
        frequencias_bolas: list[int] = cb.new_list_int(self.loteria.qtd_bolas)
        for jogo in self.jogos:
            # registra a frequencia para cada dezena dos jogos:
            for dezena in jogo.dezenas:
                frequencias_bolas[dezena] += 1

        # identifica a frequencia das dezenas em ordem reversa do numero de ocorrencias nos jogos:
        frequencias_dezenas: dict = cb.to_dict(frequencias_bolas, reverse_value=True)
        top_dezenas_jogos: list[int] = cb.take_keys(frequencias_dezenas)  # aqui pega todas

        # define os parametros para configurar o processamento de computacao de sorteios:
        parms: dict[str: Any] = {  # aplica limites e/ou faixas de corte...
            'qtd_bolas': self.loteria.qtd_bolas,
            'qtd_bolas_sorteio': self.loteria.qtd_bolas_sorteio,
            'qtd_jogos': self.loteria.qtd_jogos
        }
        # executa o processamento das dezenas mais ausentes:
        cp_ausencia: ComputeAusencia = ComputeAusencia()
        cp_ausencia.setup(parms)
        cp_ausencia.execute(self.concursos)
        # executa o processamento das dezenas mais frequentes:
        cp_frequencia: ComputeFrequencia = ComputeFrequencia()
        cp_frequencia.setup(parms)
        cp_frequencia.execute(self.concursos)

        # cria array complementar de dezenas a partir das 3 estatisticas distintas:
        topos_dezenas: list[int] = cb.mergeListasDezenas(cp_ausencia.topos_dezenas,
                                                         cp_frequencia.topos_dezenas,
                                                         top_dezenas_jogos)
        return topos_dezenas

    def get_max_recorrencias(self,  bolao: dict[int: int], faixas: dict[int: int]) -> int:
        max_recorrencias: int = 0

        # antes de gerar os jogos, calcula o maximo de recorrencias para o bolao a ser gerado:
        qtd_jogos_bolao: int = 0
        for qtd_dezenas, qtd_apostas in bolao.items():
            qtd_jogos_bolao += math.comb(qtd_dezenas, self.loteria.qtd_bolas_sorteio) * qtd_apostas

        # considera a quantidade real de apostas como 80% do limite para a faixa de recorrencias
        qtd_jogos_limite: int = math.ceil(qtd_jogos_bolao / 0.8)

        # com o numero real de apostas, verifica qual a faixa de recorrencias ira utilizar:
        for faixa, qtd_apostas in faixas.items():
            max_recorrencias = faixa  # se nao achar, vai ficar com a ultima faixa ao fim do loop
            if qtd_apostas > qtd_jogos_limite:
                break  # ja pegou a faixa em max_recorrencias, apenas sai do loop

        return max_recorrencias

    def sortear_jogo(self, max_recorrencias: int,
                     jogos_sorteados: list[tuple[int, ...]]) -> tuple[int, ...]:
        # os limites para geracao de numero aleatorio sao o minimo e maximo idx do array self.jogos:
        min_idx_jogos: int = 0
        max_idx_jogos: int = len(self.jogos) - 1

        # vai sortear um jogo, mas eh preciso verificar as recorrencias com os jogos ja sorteados:
        jogo_sorteado: Jogo
        while True:
            # obtem um jogo qualquer, cujo indice eh gerado aleatoriamente:
            idx: int = random.randint(min_idx_jogos, max_idx_jogos)
            print("random.randint : idx = ", idx)

            # se o jogo sorteado repetir muitas dezenas de algum jogo sorteado, sorteia outro:
            jogo_sorteado = self.jogos[idx]
            # verifica se o jogo possui max-recorrencias com os outros jogos ja sorteados:
            if cb.check_max_recorrencias(jogo_sorteado.dezenas, jogos_sorteados, max_recorrencias):
                break  # este jogo pode ser aproveitado

        return jogo_sorteado.dezenas

# ----------------------------------------------------------------------------
