# -*- coding: utf-8 -*-
"""authentication header

`pcapkit.protocols.internet.ah` contains `AH` only,
which implements extractor for Authentication Header (AH),
whose structure is described as below.

 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Next Header   |  Payload Len  |          RESERVED             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 Security Parameters Index (SPI)               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Sequence Number Field                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
+                Integrity Check Value-ICV (variable)           |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

"""
from pcapkit.corekit.infoclass import Info
from pcapkit.protocols.internet.ipsec import IPsec
from pcapkit.utilities.exceptions import (ProtocolError, UnsupportedCall,
                                          VersionError)

__all__ = ['AH']


class AH(IPsec):
    """This class implements Authentication Header.

    Properties:
        * name -- str, name of corresponding protocol
        * info -- Info, info dict of current instance
        * alias -- str, acronym of corresponding protocol
        * layer -- str, `Internet`
        * length -- int, header length of corresponding protocol
        * protocol -- str, name of next layer protocol
        * protochain -- ProtoChain, protocol chain of current instance

    Methods:
        * read_ah -- read Authentication Header (AH)

    Attributes:
        * _file -- BytesIO, bytes to be extracted
        * _info -- Info, info dict of current instance
        * _protos -- ProtoChain, protocol chain of current instance

    Utilities:
        * _read_protos -- read next layer protocol type
        * _read_fileng -- read file buffer
        * _read_unpack -- read bytes and unpack to integers
        * _read_binary -- read bytes and convert into binaries
        * _read_packet -- read raw packet data
        * _decode_next_layer -- decode next layer protocol type
        * _import_next_layer -- import next layer protocol extractor

    """
    ##########################################################################
    # Properties.
    ##########################################################################

    @property
    def name(self):
        """Name of corresponding protocol."""
        return 'Authentication Header'

    @property
    def length(self):
        """Info dict of current instance."""
        return self._info.length  # pylint: disable=E1101

    @property
    def payload(self):
        """Payload of current instance."""
        if self._extf:
            raise UnsupportedCall(f"'{self.__class__.__name__}' object has no attribute 'payload'")
        return self._next

    @property
    def protocol(self):
        """Name of next layer protocol."""
        return self._info.next  # pylint: disable=E1101

    ##########################################################################
    # Methods.
    ##########################################################################

    def read_ah(self, length, version, extension):
        """Read Authentication Header.

        Structure of AH header [RFC 4302]:
             0                   1                   2                   3
             0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            | Next Header   |  Payload Len  |          RESERVED             |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |                 Security Parameters Index (SPI)               |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |                    Sequence Number Field                      |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |                                                               |
            +                Integrity Check Value-ICV (variable)           |
            |                                                               |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets      Bits        Name                    Description
              0           0     ah.next                 Next Header
              1           8     ah.length               Payload Length
              2          16     -                       Reserved (must be zero)
              4          32     ah.spi                  Security Parameters Index (SPI)
              8          64     ah.seq                  Sequence Number Field
              12         96     ah.icv                  Integrity Check Value (ICV)

        """
        if length is None:
            length = len(self)

        _next = self._read_protos(1)
        _plen = self._read_unpack(1)
        _resv = self._read_fileng(2)
        _scpi = self._read_unpack(4)
        _dsnf = self._read_unpack(4)

        # ICV length & value
        _tlen = _plen * 4 - 2
        _vlen = _tlen - 12
        _chkv = self._read_fileng(_vlen)

        ah = dict(
            next=_next,
            length=_tlen,
            spi=_scpi,
            seq=_dsnf,
            icv=_chkv,
        )

        if version == 6:
            _plen = 8 - (_tlen % 8)
        elif version == 4:
            _plen = 4 - (_tlen % 4)
        else:
            raise VersionError(f'Unknown IP version {version}')

        if _plen:   # explicit padding in need
            padding = self._read_binary(_plen)
            if any((int(bit, base=2) for bit in padding)):
                raise ProtocolError(f'{self.alias}: invalid format')

        length -= ah['length']
        ah['packet'] = self._read_packet(header=ah['length'], payload=length)

        if extension:
            self._protos = None
            return ah
        return self._decode_next_layer(ah, _next, length)

    ##########################################################################
    # Data models.
    ##########################################################################

    def __init__(self, _file, length=None, *, version=4, extension=False, **kwargs):
        self._file = _file
        self._extf = extension
        self._info = Info(self.read_ah(length, version, extension))

    def __length_hint__(self):
        return 20

    @classmethod
    def __index__(cls):
        return cls.__name__
