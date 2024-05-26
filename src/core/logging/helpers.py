import logging
import colorlog


def create_logger(base_logger_name: str, base_logger_level=logging.INFO):
    """

    :param base_logger_name: Имя логгера
    :type base_logger_name: str
    :rtype: logging.Logger
    """
    logger = logging.getLogger(base_logger_name)
    logger.setLevel(base_logger_level)
    
    logging.addLevelName(logging.WARNING, 'WARN')
    logging.addLevelName(logging.CRITICAL, 'CRIT')

    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s%(reset)s:\t%(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARN': 'yellow',
            'ERROR': 'red',
            'CRIT': 'red,bg_white',
        },
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger

