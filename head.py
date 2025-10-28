#!/usr/bin/env python3
"""
myhead.py - A simplified reimplementation of the Unix `head` command.

Features:
- Base functionality: print the first 10 lines of a file or stdin.
- Flags:
    -n NUM : print the first NUM lines.
    -c NUM : print the first NUM bytes.
Author: Aaron Wulff
"""

import sys
import argparse


def head_lines(file, num_lines):
    """Print the first num_lines lines from file (or stdin)."""
    count = 0
    for line in file:
        sys.stdout.write(line)
        count += 1
        if count >= num_lines:
            break


def head_bytes(file, num_bytes):
    """Print the first num_bytes bytes from file (or stdin)."""
    content = file.read(num_bytes)
    if isinstance(content, bytes):
        sys.stdout.buffer.write(content)
    else:
        sys.stdout.write(content)


def main():
    parser = argparse.ArgumentParser(
        description="A simplified implementation of the `head` command."
    )
    parser.add_argument(
        "-n", "--lines", type=int, help="Number of lines to display (default 10)"
    )
    parser.add_argument(
        "-c", "--bytes", type=int, help="Number of bytes to display"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="File to read from (default: standard input)"
    )

    args = parser.parse_args()

    # Determine input source
    if args.file:
        try:
            mode = "rb" if args.bytes else "r"
            with open(args.file, mode) as f:
                if args.bytes:
                    head_bytes(f, args.bytes)
                else:
                    head_lines(f, args.lines or 10)
        except FileNotFoundError:
            print(f"myhead: cannot open '{args.file}' for reading: No such file or directory", file=sys.stderr)
            sys.exit(1)
    else:
        # Reading from stdin
        if args.bytes:
            head_bytes(sys.stdin.buffer, args.bytes)
        else:
            head_lines(sys.stdin, args.lines or 10)


if __name__ == "__main__":
    main()
