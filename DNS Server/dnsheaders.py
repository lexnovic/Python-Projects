import struct
from enum import Enum

class RCode(Enum):
    NO_ERROR = 0
    FORMAT_ERROR = 1
    SERVER_FAILURE = 2
    NAME_ERROR = 3
    NOT_IMPLEMENTED = 4
    REFUSED = 5

class HeaderFlags:
    qr: int = 0             # 1 bit
    opcode: int = 0         # 4 bit
    aa: int = 0             # 1 bit
    tc: int = 0             # 1 bit
    rd: int = 0             # 1 bit
    ra: int = 0             # 1 bit
    z: int = 0              # 3 bit
    rcode = RCode.NO_ERROR  # 4 bits

    def __init__(self, is_response: bool = True):
        if is_response:
            self.qr = 1

    def update_rcode(self, rcode = RCode) -> None:
        self.rcode = rcode

    def from_bytes(self, value_bytes:bytes) -> "HeaderFlags":
        value = int.from_bytes(value_bytes)
        self.qr = (value >> 15) & 0x01
        self.opcode = (value >> 11) & 0x0F
        self.aa = (value >> 10) & 0x01
        self.tc = (value >> 9) & 0x01
        self.rd = (value >> 8) & 0x01
        self.ra = (value >> 7) & 0x07
        self.z = (value >> 4) & 0x07
        rcode_value = value & 0x0F
        self.rcode = RCode(rcode_value)
        return self

class DNSHeader():
    packid: int = 0         # 16 bit
    flags: HeaderFlags      # Combined 16 bit
    qdcount: int = 0        # 16 bit
    ancount: int = 0        # 16 bit
    nscount: int = 0        # 16 bit
    arcount: int = 0        # 16 bit

    def __init__(self, packid:int = 0, is_response: bool = True) -> None:
        self.pack_id = packid
        self.flags = HeaderFlags(is_response)

    def create_response(self, other):
        if not isinstance(other, DNSHeader):
            raise ValueError("Can only copy from another DNS Header.")

        self.packid = other.packid
        self.flags.qr = 1
        self.flags.opcode = other.flags.opcode
        self.flags.rd = other.flags.rd

        if self.flags.opcode != 0:
            self.flags.update_rcode(RCode.NOT_IMPLEMENTED)

    def from_bytes(self, header: bytes) -> "DNSHeader":
        try:
            self.packid = int.from_bytes(header[:2])
            self.flags.from_bytes(header[2:4])
            self.qdcount = int.from_bytes(header[4:6])
            self.ancount = int.from_bytes(header[6:8])
            self.nscount = int.from_bytes(header[8:10])
            self.arcount = int.from_bytes(header[10:12])
        except Exception as e:
            print(f"Error parsing DNS Header: {e}")

        return self

    # increment methods
    def increment_question(self) -> None:
        self.qdcount += 1

    def increment_answer(self) -> None:
        self.ancount += 1

    def increment_authority(self) -> None:
        self.nscount += 1

    def increment_ar(self) -> None:
        self.arcount += 1

    def update_rcode(self, rcode: RCode) -> None:
        self.flags.update_rcode(rcode)

    def to_bytes(self) -> bytes:
        header = struct.pack(
            "!HHHHHH",
            self.packid,
            self.flags.to_byte(),
            self.qdcount,
            self.ancount,
            self.nscount,
            self.arcount,
        )
        return header

