""" Module containing methods to profile the code.
Ex : Keep track of memory or the time of execution.
"""
import numpy as np
import logging
import os
import time
import tracemalloc
from functools import wraps
from inspect import getframeinfo, stack

LOG_PATH = "."

# sys.getsizeof(variable)  # to get the size in bytes of a variable


# TODO: Ajouter une vraie mesure du temps d'éxécution de la fonction
def memory_tracer():
    """ Function returning the total amount of memory (in bytes) used by the programm """
    tracemalloc.start()
    snapshot = tracemalloc.take_snapshot()
    stats = snapshot.statistics("filename")  # autres options : "lineno" (gives filename and line number) and traceback
    tot_memory_used = np.sum([stat.size for stat in stats])
    return tot_memory_used


# Examples adapted from Corey Schafer's tutorial on decorators
def sayen_logger(func):
    """ Function writing information on :
        - how a function has been called
        - the time it took to run
        - the total amount of memory used by the programm when the function has been called (in kB)
    """
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                        format="%(levelname)s: %(message)s : %(asctime)s")
    start = time.perf_counter()

    @wraps(func)  # If we want to chain decorators
    def wrapper(*args, **kwargs):
        resultat = func(*args, **kwargs)
        caller = getframeinfo(stack()[1][0])  # get info on where te script is executed
        filename = os.path.basename(caller.filename)
        logging.info(f"File {filename} line {caller.lineno}, Function: {func.__name__}, "
                     f"Memory: {memory_tracer()/1024: .2f} kB, Ran in : {time.perf_counter() - start} s, at :")
        return resultat

    return wrapper