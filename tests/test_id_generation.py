import pytest

from app.utils.base62 import decode_base62, encode_base62
from app.utils.snowflake import SnowflakeIDGenerator


def test_base62_round_trip_with_min_length():
    code = encode_base62(123456789, min_length=10)

    assert len(code) == 10
    assert decode_base62(code) == 123456789


def test_snowflake_generates_unique_monotonic_ids():
    generator = SnowflakeIDGenerator(machine_id=17, epoch_ms=1704067200000)

    ids = [generator.generate() for _ in range(1000)]

    assert len(ids) == len(set(ids))
    assert ids == sorted(ids)


def test_snowflake_rejects_invalid_machine_id():
    with pytest.raises(ValueError):
        SnowflakeIDGenerator(machine_id=1024, epoch_ms=1704067200000)
