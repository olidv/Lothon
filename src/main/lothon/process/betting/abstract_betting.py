"""
   Package lothon.process.betting
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
import math
import random

# Libs/Frameworks modules
# Own/Project modules
from lothon.infra import console, parser_resultados
from lothon.stats import combinatoria as cb
from lothon import domain
from lothon.domain import Loteria, Concurso
from lothon.process.abstract_process import AbstractProcess


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
        self.jogos: list[tuple[int, ...]] = []

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- METODOS ------------------------------------------------------------

    @abstractmethod
    def execute(self, bolao: dict[int: int], concursos: list[Concurso] = None) -> list[tuple]:
        pass

    # --- METODOS HELPERS ----------------------------------------------------

    def executar_jlothon(self) -> bool:
        # executa rotina Java para processamento e selecao dos jogos computados:
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
        nm_lot: str = self.loteria.nome_loteria
        jogos_csv: list[tuple[int, ...]] = parser_resultados.read_jogos_loteria(nm_lot)
        return jogos_csv

    def get_topos_dezenas_jogos(self, qtd_topos: int):
        # extrai os topos do ranking com as dezenas com maior ausencia em todos os concursos:
        topos_ausencias_sorteios: list[int] = cb.calc_topos_ausencia(self.concursos,
                                                                     self.loteria.qtd_bolas,
                                                                     qtd_topos)

        # extrai os topos do ranking com as dezenas com maior frequencia em todos os concursos:
        topos_frequencias_sorteios: list[int] = cb.calc_topos_frequencia(self.concursos,
                                                                         self.loteria.qtd_bolas,
                                                                         qtd_topos)

        # contabiliza as frequencias das dezenas em todos os jogos considerados:
        frequencias_bolas: list[int] = cb.new_list_int(self.loteria.qtd_bolas)
        for jogo in self.jogos:
            # registra a frequencia para cada dezena dos jogos:
            for dezena in jogo:
                frequencias_bolas[dezena] += 1

        # identifica a frequencia das dezenas em ordem reversa do numero de ocorrencias nos jogos:
        frequencias_dezenas: dict = cb.to_dict(frequencias_bolas, reverse_value=True)
        topos_frequencias_jogos: list[int] = cb.take_keys(frequencias_dezenas)  # aqui pega todas

        # cria array complementar de dezenas a partir das 3 estatisticas distintas:
        topos_dezenas_jogos: list[int] = cb.merge_listas_dezenas(topos_ausencias_sorteios,
                                                                 topos_frequencias_sorteios,
                                                                 topos_frequencias_jogos)
        return topos_dezenas_jogos

    def get_max_recorrencias(self,  bolao: dict[int: int], faixas: dict[int: int]) -> int:
        max_recorrencias: int = 0

        # antes de sortear os jogos, identifica a faixa de recorrencias para o bolao a ser criado:
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

    def check_concursos_passados(self, jogo: tuple[int, ...]) -> bool:
        # percorre todos os concursos e verifica se o jogo nao repetiu algum sorteio:
        for concurso in self.concursos:
            if jogo == concurso.bolas:
                return False

        # se chegou ate o final, entao o jogo nao repetiu nenhum sorteio/concurso...
        return True

    def sortear_jogo(self, max_recorrencias: int,
                     jogos_sorteados: list[tuple[int, ...]]) -> tuple[int, ...]:
        # os limites para sorteio de numero aleatorio sao o minimo e maximo idx do array self.jogos:
        min_idx_jogos: int = 0
        max_idx_jogos: int = len(self.jogos) - 1

        # vai sortear um jogo, mas eh preciso verificar as recorrencias com os jogos ja sorteados:
        jogo_sorteado: tuple[int, ...]
        while True:
            # obtem um jogo qualquer, cujo indice eh obtido aleatoriamente:
            idx: int = random.randint(min_idx_jogos, max_idx_jogos)

            # se o jogo sorteado repetir muitas dezenas de algum jogo ja sorteado, sorteia outro:
            jogo_sorteado = self.jogos[idx]
            # o jogo não pode possuir recorrencias com os outros jogos ou concursos ja sorteados:
            if cb.check_max_recorrencias(jogo_sorteado, jogos_sorteados, max_recorrencias)\
                    and self.check_concursos_passados(jogo_sorteado):
                break  # este jogo pode ser aproveitado

        return jogo_sorteado

# ----------------------------------------------------------------------------
