# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Destination Options and Hop-by-Hop Options"""

from aenum import IntEnum, extend_enum


class Option(IntEnum):
    """Enumeration class for Option."""
    _ignore_ = 'Option _'
    Option = vars()

    # Destination Options and Hop-by-Hop Options
    Option['PAD'] = 0x00                                                        # [IPV6]
    Option['PADN'] = 0x01                                                       # [IPV6]
    Option['JUMBO'] = 0xC2                                                      # [RFC 2675]
    Option['RPL Option'] = 0x23                                                 # [RFC -ietf-roll-useofrplinfo-31]
    Option['RPL'] = 0x63                                                        # [RFC 6553][RFC -ietf-roll-useofrplinfo-31]
    Option['TUN'] = 0x04                                                        # [RFC 2473]
    Option['RA'] = 0x05                                                         # [RFC 2711]
    Option['QS'] = 0x26                                                         # [RFC 4782][RFC  Errata            2034]
    Option['CALIPSO'] = 0x07                                                    # [RFC 5570]
    Option['SMF_DPD'] = 0x08                                                    # [RFC 6621]
    Option['HOME'] = 0xC9                                                       # [RFC 6275]
    Option['DEPRECATED'] = 0x8A                                                 # [CHARLES LYNN]
    Option['ILNP'] = 0x8B                                                       # [RFC 6744]
    Option['LIO'] = 0x8C                                                        # [RFC 6788]
    Option['Deprecated'] = 0x4D                                                 # [RFC 7731]
    Option['MPL'] = 0x6D                                                        # [RFC 7731]
    Option['IP_DFF'] = 0xEE                                                     # [RFC 6971]
    Option['PDM'] = 0x0F                                                        # [RFC 8250]
    Option['Path MTU Record Option \nTEMPORARY - registered 2019-09-03, expires 2020-09-03'] = 0x30
                                                                                # [draft-ietf-6man-mtu-option]
    Option['RFC3692-style Experiment [0x1E]'] = 0x1E                            # [RFC 4727]
    Option['RFC3692-style Experiment [0x3E]'] = 0x3E                            # [RFC 4727]
    Option['RFC3692-style Experiment [0x5E]'] = 0x5E                            # [RFC 4727]
    Option['RFC3692-style Experiment [0x7E]'] = 0x7E                            # [RFC 4727]
    Option['RFC3692-style Experiment [0x9E]'] = 0x9E                            # [RFC 4727]
    Option['RFC3692-style Experiment [0xBE]'] = 0xBE                            # [RFC 4727]
    Option['RFC3692-style Experiment [0xDE]'] = 0xDE                            # [RFC 4727]
    Option['RFC3692-style Experiment [0xFE]'] = 0xFE                            # [RFC 4727]

    @staticmethod
    def get(key, default=-1):
        """Backport support for original codes."""
        if isinstance(key, int):
            return Option(key)
        if key not in Option._member_map_:  # pylint: disable=no-member
            extend_enum(Option, key, default)
        return Option[key]

    @classmethod
    def _missing_(cls, value):
        """Lookup function used when value is not found."""
        if not (isinstance(value, int) and 0x00 <= value <= 0xFF):
            raise ValueError('%r is not a valid %s' % (value, cls.__name__))
        extend_enum(cls, 'Unassigned [0x%s]' % hex(value)[2:].upper().zfill(2), value)
        return cls(value)
