#!/usr/bin/env python
# Description: converts curl statements to python code
# Inspired by http://curl.trillworks.com/
import sys
import shlex

INDENT = 4

def dict_to_code(name, simple_dict):
    """Converts a dictionary to a python compatible key value pair

    >>> code = dict_to_code("cookies", cookies)

    :param name: name of the variable
    :param simple_dict: dictionary to iterate
    :return: python compatible code in a list
    """
    code = []
    if simple_dict:
        code.append("{} = {{".format(name))
        # check for python3
        try:
            for k, v in simple_dict.items():
                code.append("{i}'{k}': '{v}',".format(i=" " * INDENT, k=k, v=v))
        except:
            for k, v in simple_dict.iteritems():
                code.append("{i}'{k}': '{v}',".format(i=" " * INDENT, k=k, v=v))
        code.append("}\n")
    return code


def create_request(url, method, cookies, headers, data=None):
    """Create request code from params

    >>> code = create_request("https://localhost:8080", None, "get", None,
    None)

    :param url: url requested
    :param method: method used e.g. get, post, delete, put
    :param cookies: dict of each cookie
    :param headers: dict of each header
    :param data: optional param to provided data to the request
    :return: python compatible code in a list
    """
    code = []
    key_value = "{i}'{k}': '{v}'"
    # check for cookies
    code += dict_to_code("cookies", cookies)
    # check for headers
    code += dict_to_code("headers", headers)
    code.append("url = '{}'".format(url))
    resstr = "res = requests.{}(url, ".format(method)
    append = "headers=headers"
    # if there are cookies / data, then attach it to the requests call
    if cookies:
        append += ", cookies=cookies"
    if data:
        code.append("data = '{}'".format(data))
        append += ", data=data"
    code.append(resstr + append + ")")
    code.append("print(res.content)\n")
    return code


def curl_to_python(command):
    """Convert curl command to python script.

    >>> code = curl_to_python(command)
    >>> print('\n'.join(code))

    :param command: curl command exported from Chrome's Dev Tools
    :return: python compatible code in a list
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

    cookies = {}
    # gather all the cookies
    if 'Cookie' in headers:
        cookie = headers['Cookie']
        # remove cookies from headers because it will be added separately
        del headers['Cookie']
        cookies = dict([c.strip().split('=') for c in cookie.split(';')])

    code = []
    code.append("#!/usr/bin/env python")
    code.append("import requests\n")
    code += create_request(url, method, cookies, headers, data)
    return code


def res_to_curl(res):
    """converts a requests response to a curl command

    >>> res = requests.get('http://www.example.com')
    >>> print res_to_curl(res)
    curl 'http://www.example.com/' -X 'GET' ...

    Source: http://stackoverflow.com/a/17936634

    :param res: request object
    """
    req = res.request
    command = "curl '{uri}' -X '{method}' -H {headers}"
    headers = ["{}: {}".format(k, v) for k, v in req.headers.items()]
    header_line = " -H ".join(['"{}"'.format(h) for h in headers])
    if req.method == "GET":
        return command.format(method=req.method, headers=header_line,
                              uri=req.url)
    else:
        command += " --data-binary '{data}'"
        return command.format(method=req.method, headers=header_line,
                              data=req.body, uri=req.url)


def main():
    """Main entry point.

    Purposely didn't use argparse or another command line parser to keep this
    script simple.
    """
    if len(sys.argv) == 1:
        command = 'curl "http://www.example.com" ' + \
                  '-H "Pragma: no-cache" ' + \
                  '-H "Accept-Encoding: gzip, deflate" ' + \
                  '-H "Accept-Language: en-US,en;q=0.8"'
    else:
        command = sys.argv[1]
    code = curl_to_python(command)
    print('\n'.join(code))


if __name__ == "__main__":
    main()
