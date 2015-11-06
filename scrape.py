#!/usr/bin/env python3

from argparse import ArgumentParser
from time import sleep

from bs4 import BeautifulSoup
from requests import get


class TranscriptScraper:
    """
    URLs for chat pages are of the form:

    http://chat.stackexchange.com/transcript/<ID>/<Y>/<M>/<D>[/<H>]

    There are two important things to note about the URL structure:

     - the numbers aren't zero-padded ("6", not "06")
     - the first part of the day has two URLs - one with and without the hours

    Each page contains the following information:

     - "a[rel=next]" contains the next day to fetch
     - ".pager" (if present) contains the links for other pages for the day
     - "a" after ".current" in ".pager" are remaining pages for the day
     - ".monologue" (a block) contains ".signature" and ".messages"
     - ".signature" contains a single link with the user's name in the "title"
       attribute and their user ID in the URL of the link
     - ".messages" contains one or more ".message"
     - ".message" has an ID of the form "message-xxx" where "xxx" is the ID
     - ".message" content is found in ".content"
     - oneboxed posts contain a ".onebox" child
     - stars are in ".flash" container with class ".times" (empty otherwise)
     - edited messages have a child with class ".edits"
     - deleted messages have a child with class ".deleted" in ".content"
    """

    def __init__(self, args):
        self._args = args

    def _next_page(self, s):
        """
        Given a copy of the DOM, determine the next page to fetch.
        """
        pager = s.find(class_='pager')
        if pager:
            sibling = pager.find(class_='current').next_sibling
            if sibling:
                return sibling['href']
        next = s.find('a', rel='next')
        if next:
            return next['href']

    def _pages(self):
        """
        Continue to yield pages until the end page is reached or an error
        occurs.
        """
        url = self._args.start
        while True:
            r = get('http://chat.stackexchange.com{}'.format(url))
            s = BeautifulSoup(r.text)
            yield s
            url = self._next_page(s)
            if url:
                if self._args.end.startswith(url):
                    break
                else:
                    sleep(self._args.delay)
            else:
                break

    def scrape(self):
        for p in self._pages():
            print(p.title.string)


if __name__ == '__main__':
    parser = ArgumentParser(description="Scrape information from Stack Exchange chat transcripts")
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
    parser_group = parser.add_argument_group('parser')
    parser_group.add_argument(
        '-d', '--delay',
        metavar='SECONDS',
        type=int,
        default=5,
        help="delay between page requests",
    )
    parser_group.add_argument(
        '-s', '--start',
        metavar='/transcript/Y/M/D[/H-H]',
        required=True,
        help="starting date for parsing (inclusive)",
    )
    parser_group.add_argument(
        '-e', '--end',
        metavar='/transcript/Y/M/D[/H-H]',
        help="ending date for parsing (exclusive)",
    )
    TranscriptScraper(parser.parse_args()).scrape()
