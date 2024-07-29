from cryptes import *
import socket
import struct

class IP(Structure):
    _fields_ = [
        ("version", c_ubyte, 4),         # 4 bit unsigned char
        ("ihl", c_ubyte, 4),             # 4 bit unsigned char
        ("tos", c_ubyte, 8),             # 1 byte char
        ("len", c_ushort, 16),           # 2 byte unsigned char
        ("id", c_ushort, 16),            # 2 byte unsigned char
        ("offset", c_ushort, 16),        # 1 byte char
        ("ttl", c_ubyte, 8),             # 1 byte char
        ("protocol_num", c_ubytem, 8),   # 1 byte char
        ("sum", c_uint32, 32),           # 2 byte unsigned char
        ("src", c_uint32, 32),           # 4 byte unsigned char
        ("dst". c_unit32, 32)            # 4 byte unsigned char
    ]
    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        # human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.src))