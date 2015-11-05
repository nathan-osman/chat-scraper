#!/usr/bin/env python3

from argparse import ArgumentParser


class TranscriptParser:
    """
    Parse a chain of pages from the chat transcript.
    """


if __name__ == '__main__':
    parser = ArgumentParser(description="Scrape information from Stack Exchange chat transcripts")
    parser.add_argument(
        'room',
        metavar='ID',
        type=int,
        help="room to scrape",
    )
    output_group = parser.add_argument_group('output')
    output_group.add_argument(
        '-o', '--output',
        metavar='FILENAME',
        default='output.json',
        help="JSON file to output information to",
    )
    output_group.add_argument(
        '-a', '--append',
        action='store_true',
        help="don't truncate output file if it exists",
    )
    output_group.add_argument(
        '-p', '--pretty',
        action='store_true',
        help="pretty-print the JSON",
    )
    date_group = parser.add_argument_group('date')
    date_group.add_argument(
        '-s', '--start',
        metavar='YYYY-MM-DD',
        help="starting date for parsing (inclusive)",
    )
    date_group.add_argument(
        '-e', '--end',
        metavar='YYYY-MM-DD',
        help="ending date for parsing (inclusive)",
    )
    args = parser.parse_args()
