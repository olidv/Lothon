"""
   Package lothon.stats
   Module  combinatoria.py

"""

__all__ = [
    'new_list_int',
    'new_list_float',
    'new_list_str',
    'new_list_series',
    'numerology',
    'is_par',
    'is_impar',
    'qtd_combinacoes',
    'get_coluna',
    'get_linha',
    'get_colunario',
    'get_decenario',
    'to_string',
    'count_dezenas_repetidas',
    'count_repeticoes',
    'count_ocorrencias',
    'count_sequencias',
    'count_dezenas',
    'soma_dezenas',
    'count_recorrencias',
    'max_recorrencias',
    'count_pares',
    'calc_numerology',
    'max_colunas',
    'max_linhas',
    'calc_espacada',
    'calc_distancia',
    'count_decenarios',
    'count_colunarios',
    'list_espacos',
    'rank',
    'partial_matches',
    'all_combinations',
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import itertools
import math
from collections.abc import Collection

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain import SerieSorteio, Concurso


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# INICIALIZACAO DE ESTRUTURAS
# ----------------------------------------------------------------------------

def new_list_int(qtd_items: int, valor: int = 0) -> list[int]:
    list_zerado: list[int] = [valor] * (qtd_items + 1)  # adiciona 1 para ignorar zero-index

    return list_zerado


def new_list_float(qtd_items: int, valor: float = 0.0) -> list[float]:
    list_zerado: list[float] = [valor] * (qtd_items + 1)  # adiciona 1 para ignorar zero-index

    return list_zerado


def new_list_str(qtd_items: int, valor: str = '') -> list[str]:
    list_vazia: list[str] = [valor] * (qtd_items + 1)  # adiciona 1 para ignorar zero-index

    return list_vazia


def new_list_series(qtd_items: int) -> list[SerieSorteio]:
    # valida os parametros:
    if qtd_items is None or qtd_items == 0:
        return []

    bolas: list[SerieSorteio] = []
    for i in range(0, qtd_items + 1):
        bolas.append(SerieSorteio(i))

    return bolas


# ----------------------------------------------------------------------------
# FUNCOES PARA CALCULOS ESPECIAIS
# ----------------------------------------------------------------------------

def numerology(numeros: tuple[int, ...]) -> int:
    # condicao de saida da recursividade:
    if numeros is None or len(numeros) == 0:
        return 0
    elif len(numeros) == 1 and numeros[0] < 10:
        return numeros[0]

    # calcula a soma os numeros:
    soma: int = sum(numeros)

    # extrai os digitos da soma:
    digitos: tuple[int, ...] = ()
    while soma > 0:
        digito: int = soma % 10
        digitos += (digito,)
        soma = soma // 10

    return numerology(digitos)


def sqrt_mean(numeros: Collection) -> float:
    # valida a relacao dos numeros:
    if numeros is None or len(numeros) == 0:
        return 0.0

    # calcula a soma das raizes dos numeros:
    soma: float = 0.0
    for num in numeros:
        soma += math.sqrt(num)

    return soma / len(numeros)


def root_mean(numeros: Collection) -> int:
    return round(sqrt_mean(numeros))


def is_par(val: int | float) -> bool:
    if val is None:
        return False
    elif isinstance(val, int):
        return (val % 2) == 0
    else:
        return (int(val) % 2) == 0


def is_impar(val: int | float) -> bool:
    if val is None:
        return False
    elif isinstance(val, int):
        return (val % 2) != 0
    else:
        return (int(val) % 2) != 0


# Number of combinations of 'n' elements for sets of size 's'
def qtd_combinacoes(n: int, s: int) -> int:
    if s <= n:
        return math.factorial(n) // (math.factorial(s) * math.factorial(n - s))
    else:
        return 0


def get_coluna(dezena: int) -> int:
    return dezena % 10


def get_linha(dezena: int) -> int:
    return (dezena - 1) // 10


def get_colunario(coluna: int) -> int:
    if coluna is None or coluna == 0:
        return 0

    return coluna % 10


def get_decenario(dezena: int) -> int:
    if dezena is None or dezena == 0:
        return 0

    return (dezena - 1) // 10


def to_string(valores: Collection) -> str:  # valores: list | tuple | Iterable | Collection
    # valida os parametros:
    if valores is None or len(valores) == 0:
        return ''

    tostr: str = ''
    for num in valores:
        tostr += f"{num:0>2}"

    return tostr


def to_dict(valores: Collection, order_key: bool = False, order_value: bool = False,
            reverse_key: bool = False, reverse_value: bool = False) -> dict:
    # identifica as frequencias das dezenas em ordem: FIXME: criar funcao helper em cb
    dicio: dict = {}
    for key, value in enumerate(valores):
        dicio[key] = value

    # ordena o dicionario conforme solicitado - parametros mutualmente exclusivos (usar apenas um):
    if order_key:
        dicio = {k: v for k, v in sorted(dicio.items(), key=lambda item: item[0])}
    elif order_value:
        dicio = {k: v for k, v in sorted(dicio.items(), key=lambda item: item[1])}
    elif reverse_key:
        dicio = {k: v for k, v in sorted(dicio.items(), key=lambda item: item[0], reverse=True)}
    elif reverse_value:
        dicio = {k: v for k, v in sorted(dicio.items(), key=lambda item: item[1], reverse=True)}

    return dicio


def sort_dict(dicio: dict, order_key: bool = False, order_value: bool = False,
              reverse_key: bool = False, reverse_value: bool = False) -> dict:
    # ordena o dicionario conforme solicitado - parametros mutualmente exclusivos (usar apenas um):
    if order_key:
        return {k: v for k, v in sorted(dicio.items(), key=lambda item: item[0])}
    elif order_value:
        return {k: v for k, v in sorted(dicio.items(), key=lambda item: item[1])}
    elif reverse_key:
        return {k: v for k, v in sorted(dicio.items(), key=lambda item: item[0], reverse=True)}
    elif reverse_value:
        return {k: v for k, v in sorted(dicio.items(), key=lambda item: item[1], reverse=True)}
    else:  # nada informado, nada faz...
        return dicio


def take_keys(dicio: dict, qtd_keys: int = None) -> list:
    list_keys: list
    if qtd_keys is None:
        list_keys = [k for k in dicio.keys()]
    else:
        list_keys = [k for k in list(dicio.keys())[0:qtd_keys]]

    return list_keys


def rtrim_list(valores: list) -> list:
    lista_trimmed: list = []

    # identifica a ultima posicao com valor valido:
    idx_ultima: int = len(valores) - 1
    while idx_ultima >= 0:
        # desconsidera o ultimo elemento, se estiver zerado ou vazio:
        if valores[idx_ultima] == 0:
            idx_ultima -= 1
        else:
            break

    # copia os elementos para a nova lista:
    if idx_ultima >= 0:
        lista_trimmed = valores[0:idx_ultima+1]

    return lista_trimmed


# ----------------------------------------------------------------------------
# PROCESSAMENTO DE DEZENAS E SORTEIOS
# ----------------------------------------------------------------------------

def count_dezenas_repetidas(bolas1: tuple[int, ...], bolas2: tuple[int, ...]) -> int:
    # aqui nao precisa validar os parametros:
    qtd_repete: int = 0
    for num1 in bolas1:
        if num1 in bolas2:
            qtd_repete += 1

    return qtd_repete


def count_repeticoes(bolas1: tuple[int, ...], bolas2: tuple[int, ...],
                     dezenas: list[SerieSorteio], id_concurso: int) -> int:
    # valida os parametros:
    if bolas1 is None or len(bolas1) == 0 or bolas2 is None or len(bolas2) == 0:
        return 0

    qtd_repete: int = 0
    for num1 in bolas1:
        if num1 in bolas2:
            qtd_repete += 1
            dezenas[num1].add_sorteio(id_concurso)

    return qtd_repete


def count_ocorrencias(bolas: tuple[int, ...], dezenas: list[int]):
    # nao precisa validar os parametros:
    for num in bolas:
        dezenas[num] += 1

    return


def count_sequencias(bolas: tuple[int, ...]) -> int:
    # valida os parametros:
    if bolas is None or len(bolas) == 0:
        return 0

    # eh preciso ordenar a tupla para verificar se ha sequencia:
    bolas: tuple[int, ...] = tuple(sorted(bolas))

    qtd_sequencias: int = 0
    seq_posterior: int = -1
    for num in bolas:
        if num == seq_posterior:
            qtd_sequencias += 1
        seq_posterior = num + 1

    return qtd_sequencias


def count_consecutivas(bolas: tuple[int, ...]) -> int:
    # valida os parametros:
    if bolas is None or len(bolas) == 0:
        return 0

    # eh preciso ordenar a tupla para verificar se ha dezenas consecutivas:
    bolas: tuple[int, ...] = tuple(sorted(bolas))

    qtd_consecutivas: int = 0
    qtd_sequencias: int = 0
    seq_posterior: int = -1
    for num in bolas:
        if num == seq_posterior:
            qtd_sequencias += 1
        else:
            if qtd_sequencias > qtd_consecutivas:
                qtd_consecutivas = qtd_sequencias
            qtd_sequencias = 0

        seq_posterior = num + 1

    # ao final, precisa testar novamente:
    if qtd_sequencias > qtd_consecutivas:
        qtd_consecutivas = qtd_sequencias

    return qtd_consecutivas


def count_dezenas(bolas: tuple[int, ...], dezenas: list[int]):
    # valida os parametros:
    if bolas is None or len(bolas) == 0 or dezenas is None or len(dezenas) == 0:
        return

    for num in bolas:
        dezenas[num] += 1

    return


def soma_dezenas(bolas: tuple[int, ...]) -> int:
    # valida os parametros:
    if bolas is None or len(bolas) == 0:
        return 0

    soma: int = sum(bolas)
    return soma


def count_recorrencias(bolas1: Collection, bolas2: Collection) -> int:
    # valida os parametros:
    if bolas1 is None or len(bolas1) == 0 or bolas2 is None or len(bolas2) == 0:
        return 0

    qtd_recorre: int = 0
    for num1 in bolas1:
        if num1 in bolas2:
            qtd_recorre += 1

    return qtd_recorre


def max_recorrencias(bolas: tuple[int, ...], concursos: list[Concurso],
                     id_concurso_ignore: int = 0) -> int:
    # valida os parametros:
    if bolas is None or len(bolas) == 0 or concursos is None or len(concursos) == 0:
        return 0

    # percorre todos os concursos e retorna o numero maximo de recorrencias de [bolas]:
    qt_max_recorrencias: int = 0
    for concurso in concursos:
        # nao deixa comparar com o mesmo concurso:
        if concurso.id_concurso == id_concurso_ignore:
            continue

        qt_recorrencias: int = count_recorrencias(bolas, concurso.bolas)
        if qt_recorrencias > qt_max_recorrencias:
            qt_max_recorrencias = qt_recorrencias

    return qt_max_recorrencias


def check_max_recorrencias(bolas: tuple[int, ...], jogos: list[tuple[int, ...]],
                           limite_recorrencias: int = 0) -> bool:
    # valida os parametros:
    if bolas is None or len(bolas) == 0 or jogos is None:
        return False

    # percorre todos os concursos e verifica se ultrapassou o limite de recorrencias de [jogo]:
    qtd_max_recorrencias: int = 0
    for jogo in jogos:
        qtd_recorrencias: int = count_recorrencias(bolas, jogo)
        if qtd_recorrencias > qtd_max_recorrencias:
            qtd_max_recorrencias = qtd_recorrencias
            # ja testa para verificar se pode parar de testar toda a lista de jogos:
            if qtd_max_recorrencias > limite_recorrencias:
                break

    return qtd_max_recorrencias <= limite_recorrencias


def calc_topos_frequencia(concursos: list[Concurso], qtd_bolas: int, qtd_topos: int) -> list[int]:
    # extrai as frequencias de todas as bolas ate o concurso atual:
    frequencias_concursos: list[int] = new_list_int(qtd_bolas)
    for concurso in concursos:
        # registra a frequencia geral de todas as bolas dos concursos anteriores:
        for dezena in concurso.bolas:
            frequencias_concursos[dezena] += 1

    # identifica as frequencias das dezenas em ordem reversa da frequencia nos sorteios:
    frequencias_dezenas: dict = to_dict(frequencias_concursos, reverse_value=True)

    # extrai o topo do ranking com as dezenas com maior frequencia e retorna:
    list_topos: list[int] = take_keys(frequencias_dezenas, qtd_topos)
    return list_topos


def calc_topos_ausencia(concursos: list[Concurso], qtd_bolas: int, qtd_topos: int) -> list[int]:
    # contabiliza o numero de concursos em que cada dezena ficou ausente ate ser sorteada:
    ausencias_concursos: list[int] = new_list_int(qtd_bolas, -1)
    qtd_concursos: int = 0
    for concurso in reversed(concursos):
        # registra o sorteio da dezena com o numero de concursos em que ficou ausente:
        for dezena in concurso.bolas:
            if ausencias_concursos[dezena] == -1:  # se a dezena ainda estiver ausente:
                ausencias_concursos[dezena] = qtd_concursos
        # vai continuar processando enquanto não tiver contado todas as dezenas
        if -1 in ausencias_concursos:
            qtd_concursos += 1
        else:  # nao tendo mais dezenas a processar, ja pode pular fora:
            break

    # identifica as ausencias das dezenas em ordem reversa do atraso ate o ultimo sorteio:
    ausencias_dezenas: dict = to_dict(ausencias_concursos, reverse_value=True)

    # extrai o topo do ranking com as dezenas com maior ausencia e retorna:
    list_topos: list[int] = take_keys(ausencias_dezenas, qtd_topos)
    return list_topos


def count_pares(bolas: tuple[int, ...]) -> int:
    # valida os parametros:
    if bolas is None or len(bolas) == 0:
        return 0

    qtd_pares: int = 0
    for bola in bolas:
        if (bola % 2) == 0:
            qtd_pares += 1

    return qtd_pares


def calc_numerology(bolas: tuple[int, ...]) -> int:
    # valida os parametros:
    if bolas is None or len(bolas) == 0:
        return 0

    return numerology(bolas)


def max_colunas(bolas: tuple[int, ...]) -> int:
    # prepara contador de dezenas por coluna
    colunas: list[int] = new_list_int(9)

    # verifica quantas dezenas em cada coluna:
    for num in bolas:
        colunas[get_coluna(num)] += 1

    # informa o maior numero de dezenas encontradas em determinada coluna:
    return max(colunas)


def max_linhas(bolas: tuple[int, ...]):
    # prepara contador de dezenas por linha
    linhas: list[int] = new_list_int(9)

    # verifica quantas dezenas em cada linha:
    for num in bolas:
        linhas[get_linha(num)] += 1

    # informa o maior numero de dezenas encontradas em determinada linha:
    return max(linhas)


def calc_espacada(bolas: tuple[int, ...]) -> int:
    # valida os parametros:
    if bolas is None or len(bolas) == 0:
        return 0

    # calcula o espacamento medio entre cada bola:
    qtd: int = 0
    soma: int = 0
    aux: int = 0
    for num in sorted(bolas):  # tem q estar ordenada
        if aux == 0:
            aux = num
        else:
            dif: int = num - aux
            soma += dif
            qtd += 1
            aux = num

    return soma // qtd


def calc_distancia(bolas: tuple[int, ...]) -> int:
    # valida os parametros:
    if bolas is None or len(bolas) == 0:
        return 0

    # calcula a distancia entre a menor e a maior bola:
    return abs(max(bolas) - min(bolas))


def count_decenarios(bolas: tuple[int, ...], decenario: list[int]) -> None:
    # valida os parametros:
    if bolas is None or len(bolas) == 0 or decenario is None or len(decenario) == 0:
        return

    for num in bolas:
        decenario[get_decenario(num)] += 1


def count_colunarios(bolas: tuple[int, ...], colunario: list[int]):
    # valida os parametros:
    if bolas is None or len(bolas) == 0 or colunario is None or len(colunario) == 0:
        return

    for num in bolas:
        colunario[get_colunario(num)] += 1


def list_espacos(bolas: tuple[int, ...]) -> list[int]:
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


def merge_listas_dezenas(list1: list[int], list2: list[int], list3: list[int]) -> list[int]:
    list_merge: list[int] = []

    has_dezena: bool = True
    len_ausencias: int = len(list1)
    idx_ausencias: int = 0
    len_frequencias: int = len(list2)
    idx_frequencias: int = 0
    len_jogos: int = len(list3)
    idx_jogos: int = 0
    while has_dezena:
        while idx_ausencias < len_ausencias:
            dezena: int = list1[idx_ausencias]
            if dezena not in list_merge:
                list_merge.append(dezena)
                break
            else:
                idx_ausencias += 1

        while idx_frequencias < len_frequencias:
            dezena: int = list2[idx_frequencias]
            if dezena not in list_merge:
                list_merge.append(dezena)
                break
            else:
                idx_frequencias += 1

        while idx_jogos < len_jogos:
            dezena: int = list3[idx_jogos]
            if dezena not in list_merge:
                list_merge.append(dezena)
                break
            else:
                idx_jogos += 1
        # verifica se ainda tem dezenas para adicionar:
        has_dezena = idx_ausencias < len_ausencias or \
            idx_frequencias < len_frequencias or \
            idx_jogos < len_jogos

    return list_merge


# ----------------------------------------------------------------------------
# FUNCOES UTILITARIAS PARA MEGA-SENA
# ----------------------------------------------------------------------------

def rank(c):
    # Rank for C(60, 6). 'c' must be sorted.
    # https://en.wikipedia.org/wiki/Combinatorial_number_system
    return 50063860 - (qtd_combinacoes(60 - c[0], 6) + qtd_combinacoes(60 - c[1], 5) +
                       qtd_combinacoes(60 - c[2], 4) + qtd_combinacoes(60 - c[3], 3) +
                       qtd_combinacoes(60 - c[4], 2) + (60 - c[5]))


def partial_matches(s, n):
    # All winning combinations for 's' set with 'n' matches. 'n' must be less than 6.

    def new_set_with(st, x):
        result = set(st)
        result.update(x)
        return sorted(result)

    remainder = {x for x in range(1, 61) if x not in s}
    wrongs = [x for x in itertools.combinations(remainder, 6 - n)]
    rights = [x for x in itertools.combinations(s, n)]
    return [new_set_with(r, w) for r in rights for w in wrongs]


def all_combinations(s):
    # All combinations for 's' set with 6 elements. 's' must have at least 6 elements
    return [x for x in itertools.combinations(s, 6)]

# ----------------------------------------------------------------------------
