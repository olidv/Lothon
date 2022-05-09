"""
   Package lothon.domain.basico
   Module  time.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from enum import Enum

# Libs/Frameworks modules
# Own/Project modules
from lothon.conf import app_config


# ----------------------------------------------------------------------------
# CLASSE ENUMERACAO
# ----------------------------------------------------------------------------

class Time(Enum):
    """
    Implementacao de classe para .
    """

    # --- VALORES ENUMERADOS -------------------------------------------------
    ABC_RN = 1
    AMERICA_RN = 2
    AMERICA_MG = 3
    AMERICA_RJ = 4
    AMERICANO_RJ = 5
    ATLETICO_GO = 6
    ATLETICO_MG = 7
    ATLETICO_PR = 8
    AVAI_SC = 9
    BAHIA_BA = 10
    BANGU_RJ = 11
    BARUERI_SP = 12
    BOTAFOGO_PB = 13
    BOTAFOGO_RJ = 14
    BRAGANTINO_SP = 15
    BRASILIENSE_DF = 16
    CEARA_CE = 17
    CORINTHIANS_SP = 18
    CORITIBA_PR = 19
    CRB_AL = 20
    CRICIUMA_SC = 21
    CRUZEIRO_MG = 22
    CSA_AL = 23
    DESPORTIVA_ES = 24
    FIGUEIRENSE_SC = 25
    FLAMENGO_RJ = 26
    FLUMINENSE_RJ = 27
    FORTALEZA_CE = 28
    GAMA_DF = 29
    GOIAS_GO = 30
    GREMIO_RS = 31
    GUARANI_SP = 32
    INTER_DE_LIMEIRA_SP = 33
    INTERNACIONAL_RS = 34
    IPATINGA_MG = 35
    ITUANO_SP = 36
    JI_PARANA_RO = 37
    JOINVILLE_SC = 38
    JUVENTUDE_RS = 39
    JUVENTUS_SP = 40
    LONDRINA_PR = 41
    MARILIA_SP = 42
    MIXTO_MT = 43
    MOTO_CLUBE_MA = 44
    NAUTICO_PE = 45
    NACIONAL_AM = 46
    OLARIA_RJ = 47
    OPERARIO_MS = 48
    PALMAS_TO = 49
    PALMEIRAS_SP = 50
    PARANA_PR = 51
    PAULISTA_SP = 52
    PAYSANDU_PA = 53
    PONTE_PRETA_SP = 54
    PORTUGUESA_SP = 55
    REMO_PA = 56
    RIO_BRANCO_AC = 57
    RIO_BRANCO_ES = 58
    RIVER_PI = 59
    RORAIMA_RR = 60
    SAO_CAETANO_SP = 61
    SAO_PAULO_SP = 62
    SAO_RAIMUNDO_AM = 63
    SAMPAIO_CORREA_MA = 64
    SANTA_CRUZ_PE = 65
    SANTO_ANDRE_SP = 66
    SANTOS_SP = 67
    SERGIPE_SE = 68
    SPORT_PE = 69
    TREZE_PB = 70
    TUNA_LUSO_PA = 71
    UBERLANDIA_MG = 72
    UNIAO_BARBARENSE_SP = 73
    UNIAO_SAO_JOAO_SP = 74
    VASCO_DA_GAMA_RJ = 75
    VILA_NOVA_GO = 76
    VILLA_NOVA_MG = 77
    VITORIA_BA = 78
    XV_DE_PIRACICABA_SP = 79
    YPIRANGA_AP = 80

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_str(value: str):
        if value is not None:
            value = value.strip().lower()

        if value in app_config.MAP_TIMES.keys():
            numero = app_config.MAP_TIMES[value]
            return Time(numero)
        else:
            raise ValueError(f"Valor invalido para criar instancia de Time: {value}.")

    # ----------------------------------------------------------------------------
