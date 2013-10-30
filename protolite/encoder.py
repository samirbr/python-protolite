import struct


def decode_varint(data, index):
    "return an int32, int64, uint32, uint64, sint32, sint64, bool, or enum"

    item = 128
    num = 0
    left = 0
    while item & 128:
        item = data[index]
        index += 1
        value = (item & 127) << left
        num += value
        left += 7
    return num, index


def decode_key(key):
    "return a tuple containing the field and the wire type"

    return key >> 3, key & 7


def decode_struct(data, index, bits, fmt):
    last = index
    index += bits
    values = [chr(i) for i in data[last:index]]
    values = ''.join(values)
    num = struct.unpack(fmt, values)
    return num[0], index


def decode_delimited(data, index):
    "return a string, bytes, embedded messages, or packed repeated fields"

    length, index = decode_varint(data, index)
    last = index
    index += length
    res = data[last:index]
    return res, index