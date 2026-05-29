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

import srt
import sys
from datetime import timedelta
from pathlib import Path


def fix_subtitles(input_file, offset_ms):
    '''Fix out of sync subtitles.'''

    # Wrap the input file string in a Path object
    input_path = Path(input_file)
    # Build output path e.g. "movie.srt" → "movie_fixed.srt"
    output_path = input_path.with_stem(input_path.stem + '_fixed')

    # Read the original SRT file
    content = input_path.read_text(encoding='utf-8')

    # Parse into subtitle objects
    subtitles = list(srt.parse(content))

    # Build the time offset
    offset = timedelta(milliseconds=offset_ms)

    # Shift every subtitle's start and end time
    for sub in subtitles:
        sub.start += offset
        sub.end += offset

    # Write corrected SRT to a new file
    output_path.write_text(srt.compose(subtitles), encoding='utf-8')

    print(f"Done! Corrected file saved as: {output_path}")


# Entry point: read arguments from the command line
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fix_subs.py <subtitle_file.srt> <offset_ms>")
        print("Example: python fix_subs.py movie.srt 2500")
        sys.exit(1)

    input_file = sys.argv[1]
    offset_ms = int(sys.argv[2])

    fix_subtitles(input_file, offset_ms)
