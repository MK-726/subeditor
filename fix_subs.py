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


def fix_subtitles(input_file, offset_ms):
    '''Fix out of sync subtitles.'''

    # Read the original SRT file
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse into subtitle objects
    subtitles = list(srt.parse(content))

    # Build the time offset
    offset = timedelta(milliseconds=offset_ms)

    # Shift every subtitle's start and end time
    for sub in subtitles:
        sub.start += offset
        sub.end += offset

    # Write corrected SRT to a new file
    output_file = input_file.replace(".srt", "_fixed.srt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(srt.compose(subtitles))

    print(f"Done! Corrected file saved as: {output_file}")


# Entry point: read arguments from the command line
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fix_subs.py <subtitle_file.srt> <offset_ms>")
        print("Example: python fix_subs.py movie.srt 2500")
        sys.exit(1)

    input_file = sys.argv[1]
    offset_ms = int(sys.argv[2])

    fix_subtitles(input_file, offset_ms)
