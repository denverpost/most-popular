#!/usr/bin/env python
# Class for common Google sheet operations.
import os
import sys
import json
import doctest
import csv
import gspread
import string
from h1 import h1
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
        i = 0
        for row in cell_list:
            i += 1
            # If row[0] has 'http://' in it then we're dealing with a GA row
            # that needs to be fixed.
            # row[0] should contain the title, row[1] the PVs, row[2] the URL.
            if 'http://' in row[0]:
                print row

                # Fix PVs
                # Note that update_cell is 1-indexed.
                worksheet.update_cell(i, 2, row[1].replace(',', ''))

                # Get title.
                # If we have a blog post then it's a h1.
                # If we have an article it's some weird element in a printer-friendly page.
                extract = h1()
                extract.content = extract.request(row[0])

                # Blogs have "blogs." in row[0], articles have "www."
                element = 'h1'
                if 'www.' in row[0]:
                    element = 'h1\ id="articleTitle"\ class="articleTitle",h1'

                value = extract.extract(element)
                if value:
                    worksheet.update_cell(i, 1, value.group(1))

                # Move URL to the third column
                worksheet.update_cell(i, 3, row[0])

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
