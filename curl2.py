#!/usr/bin/env python
# Description: converts curl statements to python code
# Inspired by http://curl.trillworks.com/
import sys
import shlex

INDENT = 4


def create_request(url, data, method, cookies, headers):
    """Create request code from params

    :param url: url requested
    :param method: method used e.g. get, post, delete, put
    :param cookies: dict of each cookie
    :param headers: dict of each header
    """
    pycode = []
    # check for a cookie
    if cookies:
        pycode.append("cookies = {")
        for k, v in cookies.iteritems():
            pycode.append("{I}'{k}': '{v}'".format(I=" " * INDENT, k=k, v=v))
        pycode.append("}\n")
    # assumes there are headers
    pycode.append("headers = {")
    for k, v in headers.iteritems():
        pycode.append(" " * INDENT + "'{k}': '{v}',".format(k=k, v=v))
    pycode.append("}\n")
    pycode.append("url = '{0}'".format(url))
    # if there is a cookie, then attach it to the requests call
    resstr = "res = requests.{method}(url, ".format(method=method)
    append = "headers=headers"
    if cookies:
        append += ", cookies=cookies"
    if data:
        pycode.append("data = '{0}'".format(data))
        append += ", data=data"
    pycode.append(resstr + append + ")")
    pycode.append("print res.content\n")
    return pycode


def curlToPython(command):
    """Convert curl command to python script.

    :param command: curl command exported from Chrome's Dev Tools
    """
    # remove quotations
    args = shlex.split(command)
    data = None
    # check for method
    if '-X' in args:
        method = args[args.index('-X') + 1]
    elif '--data' in args:
        method = 'post'
        data = args[args.index('--data') + 1]
    else:
        method = 'get'

    url = args[1]
    # gather all the headers
    headers = {}
    for i, v in enumerate(args):
        if '-H' in v:
            myargs = args[i + 1].split(':')
            headers[myargs[0]] = ''.join(myargs[1:]).strip()

    # gather all the cookies
    if 'Cookie' in headers:
        cookie = headers['Cookie']
        # remove cookies from headers because it will be added separately
        del headers['Cookie']
        cookies = dict([c.strip().split('=') for c in cookie.split(';')])

    pycode = []
    pycode.append("#!/usr/bin/env python")
    pycode.append("import requests\n")
    pycode += create_request(url, data, method, cookies, headers)
    return pycode


def resToCurl(res):
    """converts a requests response to a curl command

    >>> res = requests.get('http://www.example.com')
    >>> print resToCurl(res)
    curl 'http://www.example.com/' -X 'GET' ...

    Source: http://stackoverflow.com/a/17936634

    :param res: request object
    """
    req = res.request
    command = "curl '{uri}' -X '{method}' -H {headers}"
    headers = ["{0}: {1}".format(k, v) for k, v in req.headers.items()]
    headerLine = " -H ".join(['"{0}"'.format(h) for h in headers])
    if req.method == 'GET':
        return command.format(method=req.method, headers=headerLine,
                              uri=req.url)
    else:
        command += " --data-binary '{data}'"
        return command.format(method=req.method, headers=headerLine,
                              data=req.body, uri=req.url)


def main():
    if len(sys.argv) == 1:
        command = 'curl "http://localhost:8080/api/v1/test" ' + \
                  '-H "Pragma: no-cache" ' + \
                  '-H "Accept-Encoding: gzip, deflate" ' + \
                  '-H "Accept-Language: en-US,en;q=0.8"'
    else:
        command = sys.argv[1]
    code = curlToPython(command)
    print('\n'.join(code))


if __name__ == "__main__":
    main()
