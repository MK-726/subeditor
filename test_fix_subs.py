"""
test_fix_subs.py — Tests for fix_subs.py
-----------------------------------------
Run with:
    pytest test_fix_subs.py
 
Or for more detailed output:
    pytest test_fix_subs.py -v
"""

import srt
import pytest
from pathlib import Path
from datetime import timedelta
from fix_subs import fix_subtitles


# ── Helpers ────────────────────────────────────────────────────────────────

def make_srt_file(path, subtitles):
    """Write a list of srt.Subtitle objects to a file."""
    Path(path).write_text(srt.compose(subtitles), encoding='utf-8')


def read_srt_file(path):
    """Read and parse an SRT file, return list of srt.Subtitle objects."""
    content = Path(path).read_text(encoding='utf-8')
    return list(srt.parse(content))


def make_subtitles():
    """Return a small sample subtitle list to use across tests."""
    return [
        srt.Subtitle(index=1, start=timedelta(seconds=10),
                     end=timedelta(seconds=13), content="Hello!"),
        srt.Subtitle(index=2, start=timedelta(seconds=20),
                     end=timedelta(seconds=24), content="How are you?"),
        srt.Subtitle(index=3, start=timedelta(seconds=30),
                     end=timedelta(seconds=35), content="Goodbye!"),
    ]


# ── Fixtures ───────────────────────────────────────────────────────────────

@pytest.fixture
def srt_file(tmp_path):
    """Create a temporary SRT file and return its path."""
    path = str(tmp_path / 'test.srt')
    make_srt_file(path, make_subtitles())
    return path


@pytest.fixture
def output_file(srt_file):
    """Return the expected output file path for a given input."""
    path = Path(srt_file)
    return path.with_stem(path.stem + '_fixed')
