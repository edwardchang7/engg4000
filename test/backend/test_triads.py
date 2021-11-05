from src.backend.triads import gen_triad

def test_majorTriad_one():
    assert gen_triad('C', 'M')==['C', 'E', 'G']

def test_majorTriad_two():
    assert gen_triad("a'", 'M')==["a'", "c#''", "e''"]

def test_majorTriad_three():
    assert gen_triad('D#,,', 'M')==['D#,,', 'G,,', 'A#,,']


def test_minorTriad_one():
    assert gen_triad('C', 'm')==['C', 'D#', 'G']

def test_minorTriad_two():
    assert gen_triad("a'", 'm')==["a'", "c''", "e''"]

def test_minorTriad_three():
    assert gen_triad('D#,,', 'm')==['D#,,', 'F#,,', 'A#,,']


def test_diminishedTriad_one():
    assert gen_triad('C', 'D')==['C', 'D#', 'F#']

def test_diminshedTriad_two():
    assert gen_triad("a'", 'D')==["a'", "c''", "d#''"]

def test_diminishedTriad_three():
    assert gen_triad('D#,,', 'D')==['D#,,', 'F#,,', 'A,,']


def test_sus2Triad_one():
    assert gen_triad('C', 's2')==['C', 'D', 'G']

def test_sus2Triad_two():
    assert gen_triad("a'", 's2')==["a'", "b''", "e''"]

def test_sus2Triad_three():
    assert gen_triad('D#,,', 's2')==['D#,,', 'E#,,', 'A#,,']


def test_sus4Triad_one():
    assert gen_triad('C', 's4')==['C', 'F', 'G']

def test_sus4Triad_two():
    assert gen_triad("a'", 's4')==["a'", "d''", "e''"]

def test_sus4Triad_three():
    assert gen_triad('D#,,', 's4')==['D#,,', 'G#,,', 'A#,,']