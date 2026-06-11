"""Настройка логгера."""

from logging import DEBUG, Filter, Formatter, LogRecord, StreamHandler, getLogger


class SensitiveDataFilter(Filter):
    """Фильтрует логи с конфиденциальной информации."""

    def filter(self, record: LogRecord) -> bool:
        return not any(
            word in record.getMessage().lower()
            for word in ["password", "token", "secret"]
        )


logger = getLogger("ShiftTest")
logger.setLevel(DEBUG)

formatter = Formatter(
    fmt="%(name)s - %(asctime)s - %(pathname)s:%(lineno)d - %(levelname)s - %(message)s",  # noqa: E501
    datefmt="%Y-%m-%d %H:%M:%S",
)

console_handler = StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addFilter(SensitiveDataFilter())

__all__ = ["logger"]

if __name__ == "main":
    logger.debug("Дебаг")
    logger.info("Информирование")
    logger.warning("Внимание")
    logger.error("Ошибка")
    logger.critical("Критичное")
