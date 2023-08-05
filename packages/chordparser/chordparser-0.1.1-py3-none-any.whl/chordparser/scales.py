from .notes import Note, Key
from typing import Union
import re


class Scale:
    """
    Scale class that composes of a Key and Notes.

    Arguments:
    key -- the key of the Scale (Key)

    The Scale class accepts a Key and generates a 2-octave Note tuple in its 'notes' attribute. The Scale can be changed by setting its 'key' attribute, or by transposing it using the 'transpose' method.

    The 'notes' attribute can also be set manually with a sequence (e.g. tuple).
    """
    _heptatonic_base = (2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1)
    _SCALES = {
        "major": 0,
        "ionian": 0,
        "dorian": 1,
        "phrygian": 2,
        "lydian": 3,
        "mixolydian": 4,
        "aeolian": 5,
        "minor": 5,
        "locrian": 6,
        }
    _SCALE_DEGREE = {
        0: "ionian",
        1: "dorian",
        2: "phrygian",
        3: "lydian",
        4: "mixolydian",
        5: "aeolian",
        6: "locrian",
    }
    _submodes = {
        None: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        "natural": (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        "melodic": (0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 1, 0, -1),
        "harmonic": (0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 1, -1),
    }
    _notes_tuple = (
        'C', 'D', 'E', 'F', 'G', 'A', 'B',
        'C', 'D', 'E', 'F', 'G', 'A', 'B')

    def __init__(self, key: Key):
        self.key = key

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        if not isinstance(value, Key):
            try:
                self._key = Key(value)
            except TypeError:
                raise TypeError("Only Keys, Notes and strings are accepted")
        self._key = value
        self._refresh()

    def _refresh(self):
        self.notes = self._get_notes()
        self.diatonic_chords = self._get_chords()

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        notelist = []
        for note in value:
            if isinstance(note, Note):
                notelist.append(note)
            else:
                notelist.append(Note(note))
        self._notes = tuple(notelist)

    def _get_notes(self):
        self.scale_intervals = self._get_scale_intervals()
        note_no_symbol = Note(self.key.letter())
        self._idx = Scale._notes_tuple.index(note_no_symbol)
        self._note_order = self._get_note_order()
        notes = self._shift_notes()
        return notes

    def _get_scale_intervals(self):
        intervals = self._get_intervals(self.key.mode)
        submode_intervals = Scale._submodes.get(self.key.submode)
        scale_intervals = []
        for scale, subm in zip(intervals, submode_intervals):
            scale_intervals.append(scale + subm)
        return tuple(scale_intervals)

    def _get_intervals(self, mode):
        shift = Scale._SCALES[mode]
        intervals = (
            Scale._heptatonic_base[shift:]
            + Scale._heptatonic_base[:shift]
            )
        return intervals

    def _get_note_order(self):
        note_order = (
            Scale._notes_tuple[self._idx:]
            + Scale._notes_tuple[:self._idx]
            )
        return note_order

    def _shift_notes(self):
        base_intervals = self._get_intervals(
                Scale._SCALE_DEGREE[self._idx]
                )
        symbol_increment = self.key.symbolvalue()
        note_list = []
        for num, note in enumerate(self._note_order):
            new_note = Note(note)
            total_increment = (
                symbol_increment
                + sum(self.scale_intervals[:num])
                - sum(base_intervals[:num])
                )
            new_note.shift(total_increment)
            note_list.append(new_note)
        return tuple(note_list)

    def _get_chords(self):
        chords = []
        for i in range(7):
            chords.append((self.notes[i], self.notes[i+2], self.notes[i+4]))
        return tuple(chords)

    def transpose(self, value: int = 0, use_flats: bool = False):
        if not isinstance(value, int):
            raise TypeError("Only integers are accepted")
        self.key.transpose(value, use_flats=use_flats)
        return self

    def __repr__(self):
        return f'{self.key} scale'
