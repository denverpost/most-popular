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

    def publish(self, worksheet=None):
        """ Print out markup for a list.
            """
        if not self.sheet or worksheet:
            self.sheet = self.open_worksheet(worksheet)

        if not worksheet:
            worksheet = self.worksheet

        cell_list = worksheet.get_all_values()
        i = 0
        for row in cell_list:
            i += 1
            try:
                print '<li><a href="%s">%s</a></li>' % ( row[2], row[0] )
            except:
                pass

    def adddupe(self, worksheet=None):
        """ Find sheets that have the same url in there twice, and
            add their PVs together.
            """
        if not self.sheet or worksheet:
            self.sheet = self.open_worksheet(worksheet)

        if not worksheet:
            worksheet = self.worksheet

        cell_list = worksheet.get_all_values()
        urls = []
        dupes = []
        dupecounts = {}
        # Get the dupes
        i = 0
        for row in cell_list:
            i += 1
            if row[2] in urls:
                dupes.append(row[2])
                dupecounts[row[2]] = 0
            else:
                urls.append(row[2])

        # Tally up the counts of the dupes
        i = 0
        for row in cell_list:
            i += 1
            if row[2] in dupes:
                dupecounts[row[2]] += int(row[1])

        print dupecounts
        # Update the sheet with the totals
        dupekills = []
        i = 0
        for row in cell_list:
            i += 1
            if row[2] in dupekills:
                # We've already added it to the sheet. Kill it.
                index = dupekills.index(row[2])
                del dupekills[index]
                worksheet.update_cell(i, 1, '')
                worksheet.update_cell(i, 2, '')
                worksheet.update_cell(i, 3, '')
            elif row[2] in dupes:
                worksheet.update_cell(i, 2, dupecounts[row[2]])
                dupekills.append(row[2])

        print 'done'
    
    def dedupe(self, worksheet=None):
        """ Find sheets that have the same url in there twice, and
            kill the other one.
            """
        if not self.sheet or worksheet:
            self.sheet = self.open_worksheet(worksheet)

        if not worksheet:
            worksheet = self.worksheet

        cell_list = worksheet.get_all_values()
        urls = []
        dupes = []

        # Get the dupes
        i = 0
        for row in cell_list:
            i += 1
            if row[2] in urls:
                dupes.append(row[2])
                worksheet.update_cell(i, 1, '')
                worksheet.update_cell(i, 2, '')
                worksheet.update_cell(i, 3, '')
            else:
                urls.append(row[2])

        print 'done'
        
        
        
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
            # If row[0] is blank then we're dealing with a GA row
            # that needs to be fixed.
            # row[0] should contain the title, row[1] the URL, row[2] the PVs.
            #if 'http://' in row[0]:
            if row[0] == '' and row[2] != '':

                # Get title.
                # If we have a blog post then it's a h1.
                # If we have an article it's some weird element in a printer-friendly page.
                extract = h1()

                if 'newsfuze.com' in row[1]:
                    row[1] = row[1].replace('newsfuze', 'denverpost')
                    worksheet.update_cell(i, 3, row[1])
                elif 'dailycamera.com' in row[1]:
                    row[1] = row[1].replace('dailycamera', 'denverpost')
                    worksheet.update_cell(i, 3, row[1])
                elif 'mercurynews.com' in row[1]:
                    row[1] = row[1].replace('mercurynews', 'denverpost')
                    worksheet.update_cell(i, 3, row[1])
                elif 'timescall.com' in row[1]:
                    row[1] = row[1].replace('timescall', 'denverpost')
                    worksheet.update_cell(i, 3, row[1])
                elif row[1][0] == '/':
                    row[1] = 'http://www.denverpost.com%s' % row[1]
                    worksheet.update_cell(i, 3, row[1])

                extract.content = extract.request(row[1])

                # Blogs have "blogs." in row[0], articles have "www."
                element = 'h1'
                if 'www.denverpost.com' in row[1]:
                    element = 'h1\ id="articleTitle"\ class="articleTitle",h1'
                elif 'cannabist.co' in row[1]:
                    element = 'h1\ class="entry-title",h1'
                elif 'heyreverb' in row[1]:
                    element = 'h1\ class="entry-title",h1'

                value = extract.extract(element)
                if value:
                    try:
                        worksheet.update_cell(i, 2, value.group(1))
                    except:
                        print value.group(1)

                # Move URL to the third column
                #worksheet.update_cell(i, 3, row[0])

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
            if args.publish == True:
                sheet.publish()
            else:
                print worksheet
                sheet.dedupe()
                sheet.fix()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='$ python writesheet.py',
                                     description='',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("-d", "--dupes", dest="dupes", default=False, action="store_true")
    parser.add_argument("-p", "--publish", dest="publish", default=False, action="store_true")
    parser.add_argument("sheets", action="append", nargs="*")
    args = parser.parse_args()

    if args.verbose:
        doctest.testmod(verbose=args.verbose)

    main(args)
