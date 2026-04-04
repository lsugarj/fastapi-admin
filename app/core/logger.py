from loguru import logger as loguru_logger
from pathlib import Path

from app.core.config import get_settings
from app.utils.context import get_trace_id, get_span_id


def setup_logger():
    logger_config = get_settings().logger
    Path(logger_config.dir).mkdir(exist_ok=True)

    loguru_logger.remove()

    # 自动补充字段
    def _inject_context(record):
        record["extra"].setdefault("user_id", "-")

        current_trace_id = record["extra"].get("trace_id")
        if not current_trace_id or current_trace_id == "-":
            record["extra"]["trace_id"] = get_trace_id()

        current_span_id = record["extra"].get("span_id")
        if not current_span_id or current_span_id == "-":
            record["extra"]["span_id"] = get_span_id()

    logger = loguru_logger.patch(_inject_context)

    # 控制台（人类可读）
    logger.add(
        lambda msg: print(msg, end=""),
        level=logger_config.level,
        format=(
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "trace={extra[trace_id]} | "
            "{message}"
        ),
        colorize=True,
        enqueue=True,
    )

    # ⭐ 文件（JSON标准，关键）
    logger.add(
        f"{logger_config.dir}/{logger_config.file}",
        level=logger_config.level,
        rotation=logger_config.rotation,
        retention=logger_config.retention,
        compression="zip",
        serialize=True,   # ✅ 核心
        enqueue=True,
    )

    return logger


logger = setup_logger()
