import logging

LOGS_LEVEL = {
    'CRITICAL': 50,
    'ERROR' : 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10,
    'NOTSET': 0
}


def setup_logger(log_file, log_level):
    _log_level = LOGS_LEVEL.get(log_level.upper())
    if not _log_level:
        _log_level = LOGS_LEVEL.get("INFO")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
