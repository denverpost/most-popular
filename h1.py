#!/usr/bin/env python
# Extract the text of a particular element from a URL
import os
import sys
import doctest
import string
import argparse


def main(args):
    """ 
        Example command:
        $ python h1.py http://www.denverpost.com/
        """
    if args:
        sheet = Sheet('popular')
        sheet.set_options(args)
        for worksheet in args.sheets[0]:
            sheet.worksheet = sheet.open_worksheet(worksheet)
            sheet.fix()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='$ python h1.py',
                                     description='',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("urls", action="append", nargs="*")
    args = parser.parse_args()

    if args.verbose:
        doctest.testmod(verbose=args.verbose)

    main(args)
