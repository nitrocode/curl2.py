# curl2.py
Converts curl statements to python

I was inspired to write a commandline version after seeing [Nick Carneiro's web version](http://curl.trillworks.com/)

# Usage

    python curl2.py 'curl "http://localhost:8080/api/v1/test" -H "Pragma: no-cache"'
    
    python curl2.py 'curl "http://localhost:8080/api/v1/test" -H "Pragma: no-cache"' > runme.py
