import hashlib
import riemann
from riemann import blake256 as b256


def i2le(number: int) -> bytes:
    '''
    Convert int to little endian (LE) bytes

    Args:
        number: int value to convert to bytes in LE format
    Returns:
        LE-encoded number
    '''
    if number == 0:
        return b'\x00'
    return number.to_bytes((number.bit_length() + 7) // 8, 'little')


def i2le_padded(number: int, length: int) -> bytes:
    '''
    Convert int to little endian (LE) bytes with specified length

    Args:
        number: int value to convert to LE bytes
        length: length of resulting bytes
    Returns:
        LE-encoded number with fixed length
    '''
    return number.to_bytes(length, 'little')


def i2le_script(number: int) -> str:
    '''
    Convert int to signed little endian (LE) hex for use within scripts

    Args:
        number: int value to convert to bytes in LE format
    Returns:
        the hex-encoded signed LE number
    '''
    if number == 0:
        return '00'
    for i in range(520):
        try:  # this is stupid
            return number.to_bytes(
                length=i,  # minimal bytes lol
                byteorder='little',
                signed=True).hex()
        except OverflowError:
            continue
    raise ValueError(
        'Number cannot be expressed in 520 bytes or less')  # pragma: nocover


def le2i(b: bytes, signed: bool = False) -> int:
    '''
    Convert little endian (LE) bytes to int

    Args:
        b: LE bytes to convert to int
        signed: two's complement flag
    Returns:

    '''
    return int.from_bytes(b, 'little', signed=signed)


def be2i(b: bytes, signed: bool = False) -> int:
    '''
    Convert big endian (b.e.) bytes to int

    Args:
        b: BE bytes to convert to int
        signed: two's complement flag
    Returns:

    '''
    return int.from_bytes(b, 'big', signed=signed)


def i2be(number: int) -> bytes:
    '''
    Convert int to big endian (b.e.) bytes

    Args:
        number: int value to convert to bytes in BE format
    Returns:
        bytes in BE format
    '''
    if number == 0:
        return b'\x00'
    return number.to_bytes((number.bit_length() + 7) // 8, 'big')


def i2be_padded(number: int, length: int) -> bytes:
    '''
    Convert int to big endian (b.e.) bytes with specified length

    Args:
        number: int value to convert to bytes in BE format
        length: length of resulting bytes
    Returns:
        bytes in BE format with specified length
    '''
    return number.to_bytes(length, 'big')


def change_endianness(b: bytes) -> bytes:
    '''Reverse a bytestring'''
    return b[::-1]


def rmd160(msg_bytes: bytes) -> bytes:
    '''
    ripemd160 digest of a messge
    '''
    h = hashlib.new('ripemd160')
    h.update(msg_bytes)
    return h.digest()


def sha256(msg_bytes: bytes) -> bytes:
    '''sha256 digest of a message'''
    return hashlib.sha256(msg_bytes).digest()


def hash160(msg_bytes: bytes) -> bytes:
    '''rmd160 of sha256 of message'''
    h = hashlib.new('ripemd160')
    if 'decred' in riemann.get_current_network_name():
        h.update(blake256(msg_bytes))
        return h.digest()
    h.update(sha256(msg_bytes))
    return h.digest()


def hash256(msg_bytes: bytes) -> bytes:
    '''sha256 of sha256 of message'''
    if 'decred' in riemann.get_current_network_name():
        return blake256(blake256(msg_bytes))
    return hashlib.sha256(hashlib.sha256(msg_bytes).digest()).digest()


def blake256(msg_bytes: bytes) -> bytes:
    '''blake256 digest of a message'''
    return b256.blake_hash(msg_bytes)


def blake2b(data: bytes = b'', **kwargs) -> bytes:
    '''blake2b digest of a message'''
    b2 = hashlib.blake2b(**kwargs)
    b2.update(data)
    return b2.digest()


def blake2s(data: bytes = b'', **kwargs) -> bytes:
    '''blake2s digest of a message'''
    b2 = hashlib.blake2s(**kwargs)
    b2.update(data)
    return b2.digest()
