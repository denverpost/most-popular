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

    def extract(self, pattern):
        """ Return the text first matching element.
            *** What if we just want an attribute value?
            """
        regex = '.*<%s>([^<]+)<\/%s>' % ( pattern, pattern )
        if ',' in pattern:
            items = pattern.split(',')
            regex = '.*<%s>([^<]+)<\/%s>' % ( items[0], items[1] )
        print regex
        result = re.match(regex, self.content, re.MULTILINE|re.VERBOSE|re.IGNORECASE|re.DOTALL)
        return result

def main(args):
    """ 
        Example command:
        $ python h1.py --url http://www.denverpost.com/ "h1 class='articleTitle',h1" "title,title"
        """
    if args:
        extract = h1()
        extract.set_options(args)
        extract.content = extract.request(args.url)
        for pattern in args.patterns[0]:
            value = extract.extract(pattern)
            if value:
                print value.group(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='$ python h1.py',
                                     description='Pass h1 a url and a series of comma-separated patterns to search for.',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("-u", "--url", dest="url", default=False)
    parser.add_argument("patterns", action="append", nargs="*")
    args = parser.parse_args()

    if args.verbose:
        doctest.testmod(verbose=args.verbose)

    main(args)
