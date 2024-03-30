from string import ascii_uppercase, digits

from shortuuid import ShortUUID


def shortid(prefix: str, length: int = 10):
    return prefix + ShortUUID(alphabet=ascii_uppercase + digits).random(length=length)
