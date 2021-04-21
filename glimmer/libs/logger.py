import logging
from rich.logging import RichHandler

from glimmer.libs.core.exceptions import LoggerExceptions


class WrapLogger(object):
    def init(self, logger):
        self._logger = logger

    def __getattr__(self, name):
        if not hasattr(self, "_logger"):
            raise LoggerExceptions.NotInitError()
        return getattr(self._logger, name)


def init_logger(debug):
    global logger
    FORMAT = "%(message)s"
    if debug:
        level = logging.DEBUG
    else:
        level = logging.CRITICAL
    logging.basicConfig(
        level=level, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    logger.init(logging.getLogger("rich"))


logger = WrapLogger()
