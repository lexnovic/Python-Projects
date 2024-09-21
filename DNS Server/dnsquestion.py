from enum import Enum
import struct
from io import BytesIO
from dnsutilities import DNSUtilities

class QType(Enum):
    A = 1       # host addr
    NS = 2      # authoritative domain
    MD = 3      # mail destination
    MF = 4      # mail forwarder
    CNAME = 5   # the canonical name
    SOA = 6     # start of authority
    MB = 7      # mailbox domain name
    MG = 8      # mail group member
    MR = 9      # mail raname domain name
    NULL = 10   # null RR
    WKS = 11    # well known service descriptor
    PTR = 12    # domain name pointer
    HINFO = 13  # host info
    MINFO = 14  # mailbox/maillist information
    MX = 15     # mail exchange
    TXT = 16    # text strings
    AXFR = 252  # request to transfer zone
    MAILB = 253 # request for mailbox-related records (MB,MG,MR)
    MAILA = 254 # request for mail agent RRs
    ALL = 255   # all records

class QClass(Enum):
    IN = 1      # Internet
    CS = 2      # CSNET
    CH = 3      # CHAOS
    HS = 4      # Hesiod [Dyer 87]
    ALL = 255   # any class

class DNSQuestion():
    qname: str
    qtype: QType
    qclass: QClass

    def __init__(self) -> None:
        pass

    def set_values(self, name: str, qtype: QType, qclass: QClass) -> "DNSQuestion":
        self.qname = name
        self.qtype = qtype
        self.qclass = qclass
        return self

    def from_bytes(self, reader: BytesIO) -> "DNSQuestion":
        self.qname = DNSUtilities.decode_name(reader).decode("ascii")
        data = reader.read(4)
        type_, class_ = struct.unpack("!HH", data)
        self.qtype = QType(type_)
        self.qclass = QClass(class_)
        return self

    def to_bytes(self) -> bytes:
        encoded = DNSUtilities.encode_dns_name(self.qname)
        return encoded + struct.pack("!H", self.qtype.value) + struct.pack("!H", self.qclass.value)

