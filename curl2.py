#!/usr/bin/env python
# Description: converts curl statements to python code
#
# Usage:
#   python curl2.py 'curl "http://localhost:8080/api/v1/test" -H "Pragma: no-cache" etc'
#
# Inspired by http://curl.trillworks.com/

import sys
if len(sys.argv) == 1:
    cmd = 'curl "http://localhost:8080/api/v1/test" -H "Pragma: no-cache" -H "Accept-Encoding: gzip, deflate" -H "Accept-Language: en-US,en;q=0.8"'
else:
    cmd = sys.argv[1]

# remove quotations
cmd = cmd.replace('"', '')
args = cmd.split()
# check for POST
post = 'post' if '-X' in args else 'get'
# gather all the headers
headers = {}
url = args[1]
for i, v in enumerate(args):
    if '-H' in v:
        headers[args[i + 1].replace(':', '')] = args[i + 2]

# print code to stdout
print("#!/usr/bin/env python\nimport requests")

# check for a cookie
bCook = 'Cookie' in headers
if bCook:
    cookie = headers['Cookie']
    del headers['Cookie']
    cook = cookie.split('=')
    print("""
cookies = {{
  '{COOKIEID}': '{COOKIE}'
}}""".format(COOKIEID=cook[0], COOKIE=cook[1]))

# assumes there are headers
print("\nheaders = {")
for k, v in headers.iteritems():
    print("  '{k}': '{v}',".format(k=k, v=v))
print("}")

# if there is a cookie, then attach it to the requests call
if bCook:
    resstr = "\nres = requests.{post}('{url}', headers=headers, cookies=cookies)".format(post=post, url=url)
else:
    resstr = "\nres = requests.{post}('{url}', headers=headers)".format(post=post, url=url)
print(resstr)
