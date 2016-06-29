# curl2.py

Converts curl statements from Chrome's DevTools or Firefox's Tools to python.

I was inspired to write a commandline version after seeing [Nick Carneiro's web version](http://curl.trillworks.com/)

# Usage

1. Open Chrome's DevTools or Firefox's Tools

2. Click on the Network tab

3. Navigate to a website

4. Right click on a call and click _Copy to curl_ or something similar

5. Run this script

    ```
    python curl2.py 'curl "http://localhost:8080/api/v1/test" -H "Pragma: no-cache"'
    
    python curl2.py 'curl "http://localhost:8080/api/v1/test" -H "Pragma: no-cache"' > runme.py
    chmod +x runme.py
    ./runme.py
    ```
