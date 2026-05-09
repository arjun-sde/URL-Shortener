from app.core.config import settings
from app.utils.base62 import decode_base62, encode_base62
from app.utils.snowflake import SnowflakeIDGenerator

_generator = SnowflakeIDGenerator(
    machine_id=settings.SNOWFLAKE_MACHINE_ID,
    epoch_ms=settings.SNOWFLAKE_EPOCH_MS,
)


def generate_url_id() -> int:
    return _generator.generate()


def id_to_code(id_: int) -> str:
    return encode_base62(id_, min_length=settings.SHORT_CODE_MIN_LENGTH)


def code_to_id(code: str) -> int:
    return decode_base62(code)
