# -*- coding: utf-8 -*-
# pylint: disable=protected-access
"""decorator functions

`pcapkit.utilities.decorators` contains several useful
decorators, including `seekset` and `beholder`.

"""
import functools
import io
import os
import traceback

###############################################################################
# from pcapkit.foundation.analysis import analyse
# from pcapkit.protocols.raw import Raw
###############################################################################

__all__ = ['seekset', 'seekset_ng', 'beholder', 'beholder_ng']


def seekset(func):
    """[ClassMethod] Read file from start then set back to original."""
    @functools.wraps(func)
    def seekcur(self, *args, **kw):
        seek_cur = self._file.tell()
        self._file.seek(self._seekset, os.SEEK_SET)
        return_ = func(self, *args, **kw)
        self._file.seek(seek_cur, os.SEEK_SET)
        return return_
    return seekcur


def seekset_ng(func):
    """Read file from start then set back to original."""
    @functools.wraps(func)
    def seekcur(file, *args, seekset=os.SEEK_SET, **kw):  # pylint: disable=redefined-outer-name
        # seek_cur = file.tell()
        file.seek(seekset, os.SEEK_SET)
        return_ = func(file, *args, seekset=seekset, **kw)
        # file.seek(seek_cur, os.SEEK_SET)
        return return_
    return seekcur


def beholder(func):
    """[ClassMethod] Behold extraction procedure."""
    @functools.wraps(func)
    def behold(self, proto, length, *args, **kwargs):
        seek_cur = self._file.tell()
        try:
            return func(proto, length, *args, **kwargs)
        except Exception:
            from pcapkit.protocols.raw import Raw
            error = traceback.format_exc(limit=1).strip().split(os.linesep)[-1]
            # error = traceback.format_exc()

            self._file.seek(seek_cur, os.SEEK_SET)
            next_ = Raw(io.BytesIO(self._read_fileng(length)), length, error=error)
            return next_
    return behold


def beholder_ng(func):
    """Behold analysis procedure."""
    @functools.wraps(func)
    def behold(file, length, *args, **kwargs):
        seek_cur = file.tell()
        try:
            return func(file, length, *args, **kwargs)
        except Exception:
            # from pcapkit.foundation.analysis import analyse
            from pcapkit.protocols.raw import Raw
            error = traceback.format_exc(limit=1).strip().split(os.linesep)[-1]
            # error = traceback.format_exc()

            file.seek(seek_cur, os.SEEK_SET)

            # raw = Raw(file, length, error=str(error))
            # return analyse(raw.info, raw.protochain, raw.alias)
            next_ = Raw(file, length, error=error)
            return next_
    return behold
