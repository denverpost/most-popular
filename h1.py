#!/usr/bin/env python
# Extract the text of a particular element from a URL
import os
import sys
import doctest
import string
import argparse
import httplib2
import re


class h1:
    """ """

    def __init__(self):
        self.options = None

    def set_options(self, options):
        """ Set the objects options var.
            """
        self.options = options
        return options

    def request(self, url, action='GET', headers={}, request_body=''):
        """ Download the asset.
            """
        h = httplib2.Http('')
        response, content = h.request(url, action, headers=headers, body=request_body)
        if response.status > 299:
            print 'ERROR: HTTP response %s' % response.status
            sys.exit(1)
        return content

    def extract(self, element):
        """ Return the first matching element.
            """
        pass

def main(args):
    """ 
        Example command:
        $ python h1.py --url http://www.denverpost.com/ h1 title meta.robots
        """
    if args:
        extract = h1()
        extract.set_options(args)
        print args
        #extract.content = extract.request
        for element in args.elements[0]:

            sheet.worksheet = sheet.open_worksheet(worksheet)
            sheet.fix()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='$ python h1.py',
                                     description='',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("-u", "--url", dest="url", default=False)
    parser.add_argument("elements", action="append", nargs="*")
    args = parser.parse_args()

    if args.verbose:
        doctest.testmod(verbose=args.verbose)

    main(args)
