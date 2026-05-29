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


# ── Tests ──────────────────────────────────────────────────────────────────

def test_positive_offset_shifts_timestamps_forward(srt_file, output_file):
    '''Positive offset should delay all subtitles (shift forward in time).'''
    offset = 2_500
    fix_subtitles(srt_file, offset)

    result = read_srt_file(output_file)
    original = make_subtitles()

    for original_sub, result_sub in zip(original, result):
        assert result_sub.start == (
            original_sub.start + timedelta(milliseconds=offset)
        )
        assert result_sub.end == (
            original_sub.end + timedelta(milliseconds=offset)
        )


def test_negative_offset_shifts_timestamps_backward(srt_file, output_file):
    '''Negative offset should advance all subtitles (shift backward in time).'''
    offset = -2_000
    fix_subtitles(srt_file, offset)

    result = read_srt_file(output_file)
    original = make_subtitles()

    for original_sub, result_sub in zip(original, result):
        assert result_sub.start == (
            original_sub.start + timedelta(milliseconds=offset)
        )
        assert result_sub.end == (
            original_sub.end + timedelta(milliseconds=offset)
        )


def test_zero_offset_leaves_timestamps_unchanged(srt_file, output_file):
    """Zero offset should produce identical timestamps to the original."""
    offset = 0
    fix_subtitles(srt_file, offset)

    result = read_srt_file(output_file)
    original = make_subtitles()

    for original_sub, result_sub in zip(original, result):
        assert result_sub.start == original_sub.start
        assert result_sub.end == original_sub.end


def test_output_file_is_created_with_fixed_suffix(srt_file, output_file):
    """Output file should exist and be named <original>_fixed.srt."""
    fix_subtitles(srt_file, 1_000)

    assert output_file.exists()
    assert '_fixed.srt' in str(output_file)


def test_original_file_is_not_modified(srt_file):
    """
    The original SRT file should remain unchanged after running the script.
    """
    original = read_srt_file(srt_file)
    fix_subtitles(srt_file, 3_000)
    after = read_srt_file(srt_file)

    for original_sub, after_sub in zip(original, after):
        assert after_sub.start == original_sub.start
        assert after_sub.end == original_sub.end
