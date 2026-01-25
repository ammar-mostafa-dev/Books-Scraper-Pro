import logging

def setup_logger(
    name: str,
    log_file: str = "scraper.log",
    level: int = logging.INFO
):
    """
    Configure and return a logger.
    This should be called once per module using:
        logger = setup_logger(__name__)
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if logger is already configured
    if logger.handlers:
        return logger

    # the format that'll be used in console (Level | Message)
    console_formatter = logging.Formatter(
        "%(levelname)s | %(message)s"
    )
    # the format that'll be used in file (Time | Level | Message )
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Console Handler configuring 
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)

    # File Handler configuring
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
        mode="a"
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)

    # Attaching handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Prevent log propagation to parent logger 
    logger.propagate = False

    return logger
