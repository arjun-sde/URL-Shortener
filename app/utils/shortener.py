from hashids import Hashids
import random
import string
from app.core.config import settings

hashids = Hashids(salt=settings.HASHIDS_SALT, min_length=settings.HASHIDS_MIN_LENGTH)
ALPHABET = string.ascii_letters + string.digits

def id_to_code(id_: int) -> str:
    try:
        return hashids.encode(id_)
    except Exception:
        return ""

def code_to_id(code: str):
    decoded = hashids.decode(code)
    return decoded[0] if decoded else None

def random_code(length: int = 6) -> str:
    return ''.join(random.choices(ALPHABET, k=length))
