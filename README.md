# curltopy

Converts curl statements from Chrome's DevTools or Firefox's Tools to executable python 2 and 3 compatible code.

I was inspired to write a command line version after seeing @NickCarneiro's web app on [curl.trillworks.com](http://curl.trillworks.com/).

## Install

    pip install curltopy

## Usage

1. Open Chrome's DevTools or Firefox's Tools

2. Click on the Network tab

3. Navigate to a website

4. Right click on a call and click _Copy > Copy as cURL_

5. Here is a template. Replace the curl statement with the one captured from the browser.

        curltopy 'curl "http://example.com" -H "Pragma: no-cache"' > runme.py
        chmod +x runme.py
        ./runme.py
