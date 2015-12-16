#!/usr/bin/env python
# Class for common Google sheet operations.
import os
import sys
import json
import doctest
import csv
import gspread
import string
from oauth2client.client import SignedJwtAssertionCredentials
from collections import defaultdict
try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict
import argparse


class Sheet:
    """ Handle google spreadsheet read and flatfile write operations.
        >>> sheet = Sheet('test-sheet', 'worksheet-name')
        >>> sheet.publish()
        True
        """

    def __init__(self, sheet_name, worksheet=None):
        self.options = None
        self.directory = os.path.dirname(os.path.realpath(__file__))
        if not os.path.isdir('%s/output' % self.directory):
            os.mkdir('%s/output' % self.directory)

        scope = ['https://spreadsheets.google.com/feeds']
        self.credentials = SignedJwtAssertionCredentials(
            os.environ.get('ACCOUNT_USER'),
            string.replace(os.environ.get('ACCOUNT_KEY'), "\\n", "\n"),
            scope)
        self.spread = gspread.authorize(self.credentials)
        self.sheet_name = sheet_name
        self.filters = None
        if worksheet:
            self.worksheet = self.open_worksheet(worksheet)

    def set_options(self, options):
        """ Set the objects options var.
            """
        self.options = options
        return options

    def slugify(self, slug):
        return slug.lower().replace(' ', '-')

    def open_worksheet(self, worksheet):
        """ Open a spreadsheet, return a sheet object.
            >>> sheet = Sheet('test-sheet')
            >>> sheet.open_worksheet('worksheet-name')
            <Worksheet 'worksheet-name' id:od6>
            """
        self.sheet = self.spread.open(self.sheet_name).worksheet(worksheet)
        return self.sheet

    def fix(self, worksheet=None):
        """ Publish the data in whatever permutations we need.
            This assumes the spreadsheet's key names are in the first row.
            >>> sheet = Sheet('test-sheet', 'worksheet-name')
            >>> sheet.fix()
            True
            """
        if not self.sheet or worksheet:
            self.sheet = self.open_worksheet(worksheet)

        if not worksheet:
            worksheet = self.worksheet

        cell_list = worksheet.get_all_values()
        for row in cell_list:
            print row

        return True


def main(args):
    """ Take args as key=value pairs, pass them to the add_filter method.
        Example command:
        $ python writesheet.py test
        """
    if args:
        sheet = Sheet('popular')
        sheet.set_options(args)
        for worksheet in args.sheets[0]:
            sheet.worksheet = sheet.open_worksheet(worksheet)
            sheet.fix()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='$ python writesheet.py',
                                     description='',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("sheets", action="append", nargs="*")
    args = parser.parse_args()

    if args.verbose:
        doctest.testmod(verbose=args.verbose)

    main(args)