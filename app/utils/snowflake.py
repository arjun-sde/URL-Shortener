import threading
import time


class SnowflakeIDGenerator:
    """
    64-bit, k-ordered ID generator.

    Layout: 41 bits timestamp, 10 bits machine id, 12 bits sequence.
    Configure a unique SNOWFLAKE_MACHINE_ID per pod/replica when running HPA.
    """

    MACHINE_ID_BITS = 10
    SEQUENCE_BITS = 12
    MAX_MACHINE_ID = (1 << MACHINE_ID_BITS) - 1
    MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

    def __init__(self, machine_id: int, epoch_ms: int) -> None:
        if machine_id < 0 or machine_id > self.MAX_MACHINE_ID:
            raise ValueError(f"machine_id must be between 0 and {self.MAX_MACHINE_ID}")

        self.machine_id = machine_id
        self.epoch_ms = epoch_ms
        self._lock = threading.Lock()
        self._last_timestamp_ms = -1
        self._sequence = 0

    def generate(self) -> int:
        with self._lock:
            timestamp_ms = self._current_timestamp_ms()

            if timestamp_ms < self._last_timestamp_ms:
                raise RuntimeError("system clock moved backwards")

            if timestamp_ms == self._last_timestamp_ms:
                self._sequence = (self._sequence + 1) & self.MAX_SEQUENCE
                if self._sequence == 0:
                    timestamp_ms = self._wait_next_millisecond(timestamp_ms)
            else:
                self._sequence = 0

            self._last_timestamp_ms = timestamp_ms

            return (
                ((timestamp_ms - self.epoch_ms) << (self.MACHINE_ID_BITS + self.SEQUENCE_BITS))
                | (self.machine_id << self.SEQUENCE_BITS)
                | self._sequence
            )

    @staticmethod
    def _current_timestamp_ms() -> int:
        return int(time.time() * 1000)

    def _wait_next_millisecond(self, timestamp_ms: int) -> int:
        next_timestamp_ms = self._current_timestamp_ms()
        while next_timestamp_ms <= timestamp_ms:
            next_timestamp_ms = self._current_timestamp_ms()
        return next_timestamp_ms
