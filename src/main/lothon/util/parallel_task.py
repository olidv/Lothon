"""
   Package lothon.util
   Module  parallel_task.py

   Funcoes utilitarias para manipulacao de threads.
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging
import threading

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES UTILITARIAS
# ----------------------------------------------------------------------------

# execucao paralela de qualquer job, cada um em sua propria thread:
def run_threaded(job_func, callback_func):
    job_thread = threading.Thread(target=job_func, args=[callback_func])
    job_thread.start()

# ----------------------------------------------------------------------------
