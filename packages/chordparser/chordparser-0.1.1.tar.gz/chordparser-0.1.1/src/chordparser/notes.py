from typing import Union
import re


class Note:
    """
    Create a Note.

    Arguments:
    value -- the Note value (str)

    The Note class consists of notation a-g or A-G, with optional accidental symbols. The symbols that can be used are b (flat), bb (doubleflat), # (sharp), ## (doublesharp) and their respective unicode characters.

    Notes can have accidentals set using the 'accidental' method, and can be shifted by semitones using the 'shift' method. Notes also have 'letter', 'symbol', and 'symbolvalue' methods to get their respective values.
    """
    _flat = '\u266d'
    _sharp = '\u266f'
    _doubleflat = '\U0001D12B'
    _doublesharp = '\U0001D12A'
    _symbols = {
        _flat: -1, _doubleflat: -2,
        _sharp: +1, _doublesharp: +2,
        -1: _flat, -2: _doubleflat,
        +1: _sharp, +2: _doublesharp,
        0: '', None: 0,
        }
    _symbol_converter = {
        _flat: _flat, _doubleflat: _doubleflat,
        _sharp: _sharp, _doublesharp: _doublesharp,
        'b': _flat, 'bb': _doubleflat,
        '#': _sharp, '##': _doublesharp,
        None: '',
    }
    _note_values = {
        ('C' + _doubleflat): 10,
        ('C' + _flat): 11,
        'C': 0,
        ('C' + _sharp): 1,
        ('C' + _doublesharp): 2,
        ('D' + _doubleflat): 0,
        ('D' + _flat): 1,
        'D': 2,
        ('D' + _sharp): 3,
        ('D' + _doublesharp): 4,
        ('E' + _doubleflat): 2,
        ('E' + _flat): 3,
        'E': 4,
        ('E' + _sharp): 5,
        ('E' + _doublesharp): 6,
        ('F' + _doubleflat): 3,
        ('F' + _flat): 4,
        'F': 5,
        ('F' + _sharp): 6,
        ('F' + _doublesharp): 7,
        ('G' + _doubleflat): 5,
        ('G' + _flat): 6,
        'G': 7,
        ('G' + _sharp): 8,
        ('G' + _doublesharp): 9,
        ('A' + _doubleflat): 7,
        ('A' + _flat): 8,
        'A': 9,
        ('A' + _sharp): 10,
        ('A' + _doublesharp): 11,
        ('B' + _doubleflat): 9,
        ('B' + _flat): 10,
        'B': 11,
        ('B' + _sharp): 0,
        ('B' + _doublesharp): 1,
        }
    _sharp_scale = (
        'C', 'C\u266f', 'D', 'D\u266f', 'E', 'F', 'F\u266f',
        'G', 'G\u266f', 'A', 'A\u266f', 'B'
        )
    _flat_scale = (
        'C', 'D\u266d', 'D', 'E\u266d', 'E', 'F',
        'G\u266d', 'G', 'A\u266d', 'A', 'B\u266d', 'B'
        )

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Only strings are accepted")
        pattern = (
            '^([a-gA-G])(\u266F|\u266D|\U0001D12B|\U0001D12A'
            '|bb|##|b|#){0,1}$'
            )
        rgx = re.match(pattern, value, re.UNICODE)
        if not rgx:
            raise ValueError("Note is invalid")
        letter_ = rgx.group(1).upper()
        symbol_ = Note._symbol_converter.get(rgx.group(2))
        self._value = letter_ + symbol_

    def accidental(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Only integers are accepted")
        if value not in {-2, -1, 0, 1, 2}:
            raise ValueError(
                "Only integers between -2 and 2 are accepted"
                )
        self.value = self.letter() + Note._symbols.get(value)
        return self

    def shift(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Only integers are accepted")
        value += self.symbolvalue()
        if value not in {-2, -1, 0, 1, 2}:
            raise ValueError(
                "Only symbols up to doublesharps and doubleflats are accepted"
                )
        self.value = self.letter() + Note._symbols.get(value)
        return self

    def letter(self) -> str:
        return self.value[0]

    def symbol(self) -> str:
        if len(self.value) > 1:
            return self.value[1]
        return None

    def symbolvalue(self) -> int:
        if len(self.value) > 1:
            symbol = self.value[1]
        else:
            symbol = None
        return Note._symbols.get(symbol)

    def transpose(self, value=0, use_flats: bool = False):
        if not isinstance(value, int):
            raise TypeError("Only integers are accepted")
        number = Note._note_values.get(self.value)
        number += value
        if use_flats:
            dic = Note._flat_scale
        else:
            dic = Note._sharp_scale
        self.value = dic[number % 12]
        return self

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, Note):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            return NotImplemented


class Key:
    """
    Create a Key.

    Arguments:
    value -- the note of the Key (str)

    Keyword arguments:
    mode -- the mode of the Key (default 'major') (str)
    submode -- the submode (default None) (str)

    The Key class composes of a Note class with the additional attributes 'mode' and 'submode' (e.g. types of minor keys). Keys have the same methods as Notes, with an additional 'transpose' and 'use_flats'/'use_sharps' methods for transposing.

    The Key class only accepts the western heptatonic modes and submodes for now.
    """
    _modes = (
        'major', 'minor', 'ionian', 'dorian', 'phrygian',
        'lydian', 'mixolydian', 'aeolian', 'locrian'
        )
    _submodes = {'minor': ('harmonic', 'melodic', 'natural')}

    def __init__(
            self, value, mode: str = 'major',
            submode: Union[str, None] = None):
        self.root = value
        self.mode = mode
        self.submode = submode

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        if not isinstance(value, Note):
            try:
                self._root = Note(value)
            except TypeError:
                raise TypeError("Only Notes and strings are accepted")
        else:
            self._root = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if not isinstance(value, str):
            raise TypeError("Only strings are accepted")
        if value.lower() not in Key._modes:
            raise KeyError("Mode could not be found")
        self._mode = value.lower()

    @property
    def submode(self):
        return self._submode

    @submode.setter
    def submode(self, value):
        if value is None:
            self._submode = value
            return
        if not isinstance(value, str):
            raise TypeError("Only strings are accepted")
        submode_tuple = Key._submodes.get(self.mode)
        if submode_tuple is None:
            raise KeyError("Mode does not have any submodes")
        if value.lower() not in submode_tuple:
            raise KeyError("Submode could not be found")
        self._submode = value.lower()

    def __getattr__(self, attribute):
        # So Note methods can be used on Key
        if attribute in Note.__dict__:
            return getattr(self.root, attribute)

    def __repr__(self):
        if not self.submode:
            return f'{self.root} {self.mode}'
        return f'{self.root} {self.submode} {self.mode}'

    def __eq__(self, other):
        if not isinstance(other, Key):
            return NotImplemented
        return (
                self.root == other.root
                and self.mode == other.mode
                and self.submode == other.submode
                )
