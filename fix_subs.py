"""
fix_subs.py — Subtitle Sync Fixer
----------------------------------
Shifts all timestamps in an SRT file forward or backward by a fixed amount.

Usage:
    python fix_subs.py <subtitle_file.srt> <offset_in_milliseconds>

Examples:
    Subs are too early (they appear before the dialogue):
        python fix_subs.py movie.srt 2500       (delay by 2.5 seconds)

    Subs are too late (they appear after the dialogue):
        python fix_subs.py movie.srt -1800      (advance by 1.8 seconds)
"""

import logging
import sys
from datetime import timedelta
from pathlib import Path

import srt


def fix_subtitles(input_file, offset_ms):
    '''Fix out of sync subtitles.'''

    # Wrap the input file string in a Path object
    input_path = Path(input_file)

    validate_file(input_path)

    # Build output path e.g. "movie.srt" → "movie_fixed.srt"
    output_path = input_path.with_stem(input_path.stem + '_fixed')

    subtitles = parse_subtitles(input_path)

    # Build the time offset
    offset = timedelta(milliseconds=offset_ms)

    validate_offset(offset, subtitles, offset_ms)

    subtitles = shift_timestamps(subtitles, offset)

    # Write corrected SRT to a new file
    output_path.write_text(srt.compose(subtitles), encoding='utf-8')

    print(f"Done! Corrected file saved as: {output_path}")


def validate_file(input_path):
    """Check file exists and is an SRT file."""
    # Check if the file exists.
    if not input_path.exists():
        print(f'Error: file not found: {input_path}.')
        sys.exit(1)

    # Check if the file is SRT.
    if input_path.suffix != '.srt':
        print(f"Error: '{input_path.name}' is not a SRT file.")
        sys.exit(1)


def parse_subtitles(input_path):
    """Read and parse the SRT file into subtitle objects."""
    # Read the original SRT file
    content = input_path.read_text(encoding='utf-8')

    # Parse into subtitle objects
    logging.disable(logging.WARNING)
    subtitles = list(srt.parse(content, ignore_errors=True))
    logging.disable(logging.NOTSET)

    # Check for empty files or absence of srt content
    if not subtitles:
        print(
            'Error: the subtitle file is empty '
            'or contains no valid subtitles.'
        )
        sys.exit(1)
    return subtitles


def validate_offset(offset, subtitles, offset_ms):
    """Check offset won't push timestamps below zero."""
    # Check if offset would push the first subtitle below zero.
    if invalid_negative_offset(offset, subtitles):
        display_error_message(offset_ms, subtitles)
        sys.exit(1)


def invalid_negative_offset(offset, subtitles):
    '''Return true if entered negative offset is too large.'''
    first_sub = subtitles[0]
    return first_sub.start + offset < timedelta(0)


def display_error_message(offset_ms, subtitles):
    '''Display error messages for invalid large offsets.'''
    first_sub = subtitles[0]
    offset_timestamp = srt.timedelta_to_srt_timestamp(
        timedelta(milliseconds=abs(offset_ms))
    )
    first_sub_timestamp = srt.timedelta_to_srt_timestamp(first_sub.start)
    message = (
        f"Error: offset of {offset_ms:,}ms ({offset_timestamp}) is larger "
        f"than the first subtitle's start time ({first_sub_timestamp}).\n"
        f"Either the offset is wrong, or this subtitle file needs "
        f"to be replaced."
    )
    print(message)


def shift_timestamps(subtitles, offset):
    """Shift all subtitle timestamps by the given offset."""
    # Shift every subtitle's start and end time
    for sub in subtitles:
        sub.start += offset
        sub.end += offset
    return subtitles


# Entry point: read arguments from the command line
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fix_subs.py <subtitle_file.srt> <offset_ms>")
        print("Example: python fix_subs.py movie.srt 2500")
        sys.exit(1)

    input_file = sys.argv[1]
    offset_ms = int(sys.argv[2])

    fix_subtitles(input_file, offset_ms)
