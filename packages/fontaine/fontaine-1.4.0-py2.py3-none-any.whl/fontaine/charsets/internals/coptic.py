# -*- coding: utf-8 -*-
class Charset:
    common_name = u'Coptic'
    native_name = u"Ⲙⲉⲧⲣⲉⲙ̀ⲛⲭⲏⲙⲓ"
    key = 0x03E2
    abbreviation = 'COPT'
    glyphs = \
        list(range(0x03e2, 0x03ef)) + \
        list(range(0x2c80, 0x2cb1)) + \
        list(range(0x2cb2, 0x2cdb)) + \
        list(range(0x2cdc, 0x2ce3)) + \
        list(range(0x2ce4, 0x2cea)) + \
        list(range(0x2cf9, 0x2cfc)) + \
        [
            0x2cfd,
            0x2cfe,
            0x2cff
        ]
