import functools
import logging
import time
import traceback
import tracemalloc
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable

# Configuration du logger
def setup_logger(name: str, log_file: Optional[str] = None, level=logging.INFO) -> logging.Logger:
    """Configure et retourne un logger personnalisé."""
    logger = logging.getLogger(name)
    
    # Éviter les handlers en double
    if logger.hasHandlers():
        logger.handlers.clear()
    
    logger.setLevel(level)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (optionnel)
    if log_file:
        log_path = Path("logs")
        log_path.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_path / log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    # Éviter la propagation aux loggers parents
    logger.propagate = False

    return logger

def log_function(
    name: Optional[str] = None,
    log_file: Optional[str] = None,
    track_memory: bool = False,
    level: int = logging.INFO
) -> Callable:
    """
    Décorateur pour logger l'exécution d'une fonction.
    
    Args:
        name: Nom du logger (par défaut: nom du module)
        log_file: Fichier de log (optionnel)
        track_memory: Active le suivi mémoire
        level: Niveau de logging
    
    Usage:
        @log_function(track_memory=True)
        def ma_fonction(arg1, arg2):
            ...
    """
    def decorator(func: Callable) -> Callable:
        logger_name = name or func.__module__
        logger = setup_logger(logger_name, log_file, level)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            if track_memory:
                tracemalloc.start()
                start_memory = tracemalloc.get_traced_memory()[0]

            # Log début d'exécution
            logger.info(f"Début de {func.__name__}")
            logger.debug(f"Arguments: args={args}, kwargs={kwargs}")

            try:
                # Exécution de la fonction
                result = func(*args, **kwargs)

                # Calcul du temps d'exécution
                execution_time = time.time() - start_time
                
                # Log mémoire si activé
                if track_memory:
                    current, peak = tracemalloc.get_traced_memory()
                    memory_diff = current - start_memory
                    logger.info(
                        f"Mémoire: différence={memory_diff/1024:.2f}KB, "
                        f"pic={peak/1024:.2f}KB"
                    )
                    tracemalloc.stop()

                # Log succès
                logger.info(
                    f"Fin de {func.__name__} - "
                    f"Temps d'exécution: {execution_time:.2f}s"
                )
                return result

            except Exception as e:
                # Log erreur
                logger.error(
                    f"Erreur dans {func.__name__}: {str(e)}\n"
                    f"Traceback: {traceback.format_exc()}"
                )
                raise

        return wrapper
    return decorator