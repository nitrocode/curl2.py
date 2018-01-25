# curl2.py

Converts curl statements from Chrome's DevTools or Firefox's Tools to executable python 2 and 3 compatible code.

I was inspired to write a command line version after seeing Nick Carneiro's web app on  [curl.trillworks.com](http://curl.trillworks.com/).

# Usage

1. Open Chrome's DevTools or Firefox's Tools

2. Click on the Network tab

3. Navigate to a website

4. Right click on a call and click _Copy > Copy as cURL_

5. Create a virtual environment

    ```
    ✗ virtualenv env
    ✗ . env/bin/activate
    (env) ✗ pip install requests
    ```

5. Here is a template. Replace the curl statement with the one captured from the browser.

    ```
    (env) ✗ python curl2.py 'curl "http://example.com" -H "Pragma: no-cache"' > runme.py
    (env) ✗ chmod +x runme.py
    (env) ✗ ./runme.py
    ```
