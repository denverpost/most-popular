# Most Popular
Generate the markup for our year-end most-pop lists. Also, Google Analytics doesn't publish headlines with its PVs, so we need to be able to add that data to the spreadsheet.

# Dev notes
When figuring out Oauth2 access, always always use http://gspread.readthedocs.org/en/latest/oauth2.html

Be sure to share the spreadsheet with the email address stored in the ACCOUNT_USER env var.

# Workflow

1. Get the report for all articles
2. Use writesheet.py to get the headlines into the spreadsheet (if you put all articles in the tab named "all," `python writesheet.py all` will do that. Unicode errors will output to the command line, just add those into the spreadsheet by hand. When the script stops and is restarted, it picks up where it left off (it starts at the first empty title row).
3. Currently we don't have a way to get the article section, so that work needs to be done by hand.

# License
The MIT License (MIT)

Copyright © 2015-2016 The Denver Post 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

