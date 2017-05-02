# Most Popular
Generate the markup for our year-end most-pop lists. Also, Google Analytics doesn't publish headlines with its PVs, so we need to be able to add that data to the spreadsheet.

# Dev notes
When figuring out Oauth2 access, always always use http://gspread.readthedocs.org/en/latest/oauth2.html

Be sure to share the spreadsheet with the email address stored in the ACCOUNT_USER env var.

# Workflow

1. In GA, export the most-pop articles (I usually do the top 1,000) as a CSV.
1. Rename the previous year's Google sheets document "popular-PREVIOUSYEAR"
1. Duplicate the previous year's Google sheets document, name it "popular"
1. Empty out the contents of the sheets document's tabs.
1. Paste the exported GA CSV into the "all" tab. Paste the CSV starting at the second column -- the first column should be left blank for the headline, which we import programmatically.
1. The section field is generated by hand (haha / sob)
2. *Add the headlines*. Use writesheet.py to get the headlines into the spreadsheet (if you put all articles in the tab named "all," `python writesheet.py all` will do that. Unicode errors will output to the command line, just add those into the spreadsheet by hand. When the script stops and is restarted, it picks up where it left off (it starts at the first empty title row).
3. Currently we don't have a way to get the article section, so that work needs to be done by hand.
4. Create section-specific spreadsheets, one sheet per section. Add the section's items from the "all" spreadsheet to that section-specific sheet.
5. To turn the section-specific spreadsheet into markup, run `$ python writesheet.py news --publish | head -n 100` (change the "news" to whichever section you're running this on). The `| head -n 100` means "Show only the first 100 lines." That will output something like
```html
<li><a href="http://www.denverpost.com/2016/11/05/there-is-no-such-thing-as-the-denver-guardian/">There is no such thing as the Denver Guardian, despite that Facebook post you saw</a></li>
<li><a href="http://www.denverpost.com/2016/06/02/thunderbird-crash-colorado-springs/">Thunderbirds fighter jet crashes in Colorado Springs after flyover at Air Force Academy graduation</a></li>
<li><a href="http://www.denverpost.com/2016/06/28/downtown-denver-shooting-wynkoop/">One woman in critical condition, gunman dead after shooting at 15th &amp; Wynkoop in Denver</a></li>
```

# License
The MIT License (MIT)

Copyright © 2015-2017 The Denver Post 

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

