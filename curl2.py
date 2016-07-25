#!/usr/bin/env python
# Description: converts curl statements to python code
#
# Usage:
#   python curl2.py 'curl "http://localhost:8080/api/v1/test" -H "Pragma: no-cache" etc'
#
# Inspired by http://curl.trillworks.com/

import sys
import shlex

def curlToPython(command):
    """convert curl command to python script"""
    # remove quotations
    args = shlex.split(command)
    # check for method
    if '-X' in args:
        method = args[args.index('-X') + 1]
    else:
        method = 'get'

    url = args[1]
    # TODO: convert to dict comprehension?
    # {args[i + 1].split(':')[0]: args[i + 1].split(':')[1].strip() for i, v in enumerate(args) if v == '-H'}
    # gather all the headers
    headers = {}
    for i, v in enumerate(args):
        if '-H' in v:
            myargs = args[i + 1].split(':')
            headers[myargs[0]] = myargs[1].strip()

    pycode = []

    # print code to stdout
    pycode.append("#!/usr/bin/env python")
    pycode.append("import requests")

    # check for a cookie
    bCook = 'Cookie' in headers
    if bCook:
        cookie = headers['Cookie']
        del headers['Cookie']
        cook = cookie.split('=')
        pycode.append("""cookies = {{
  '{COOKIEID}': '{COOKIE}'
}}""".format(COOKIEID=cook[0], COOKIE=cook[1]))

    # assumes there are headers
    pycode.append("headers = {")
    for k, v in headers.iteritems():
        pycode.append("  '{k}': '{v}',".format(k=k, v=v))
    pycode.append("}")
    pycode.append("url = '{0}'".format(url))
    # if there is a cookie, then attach it to the requests call
    resstr = "res = requests.{method}(url, headers=headers".format(
                method=method)
    if bCook:
        pycode.append("{0}, cookies=cookies)".format(resstr))
    else:
        pycode.append("{0})".format(resstr))
    return pycode

def resToCurl(res):
    """converts a requests response to a curl command

    >>> res = requests.get('http://www.example.com')
    >>> print resToCurl(res)
    curl 'http://www.example.com/' -X 'GET' ...

    Source: http://stackoverflow.com/a/17936634
    """
    req = res.request
    command = "curl '{uri}' -X '{method}' -H {headers}"
    method = req.method
    uri = req.url
    data = req.body
    headers = ["{0}: {1}".format(k, v) for k, v in req.headers.items()]
    headerLine = " -H ".join(['"{0}"'.format(h) for h in headers])
    if method == 'GET':
        return command.format(method=method, headers=headerLine, uri=uri)
    else:
        command += " --data-binary '{data}'"
        return command.format(method=method, headers=headerLine, data=data, uri=uri)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        command = 'curl "http://localhost:8080/api/v1/test" -H "Pragma: no-cache" -H "Accept-Encoding: gzip, deflate" -H "Accept-Language: en-US,en;q=0.8"'
    else:
        command = sys.argv[1]
    code = curlToPython(command)
    print('\n'.join(code))
