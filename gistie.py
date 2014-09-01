#!/usr/bin/python3

__description__ = """
Gistie - A tiny script to generate quick pasties from terminal stdout
         and stdin output.
         Requires curl, xclip, and requests module.
"""

__author__ = "Vivek Rai"
__date__ = "18th July, 2014"


import requests
import json
import getpass
import sys
import argparse
from subprocess import Popen, PIPE


BANNER = """\n\nGenerated by gistie (gh://vivekiitkgp/gistie)."""

def set_clipboard(text):
    """Automatically copies the obtained gist URL to system clipboard.
    Reference taken from a very simple Python script - Pyperclip.
    """
    process = Popen(['xclip', '-selection', 'c'], stdin=PIPE)
    try:
        # works on Python 3 (bytes() requires an encoding)
        process.communicate(input=bytes(text, 'utf-8'))
    except TypeError:
        pass

    return


def catch_input():
    """ Read redirected input from the command line.
    """
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument('-u', action='store', dest='user',
                        help='Set username')
    parser.add_argument('-p', action='store', dest='password',
                        help='Set password')

    credentials = parser.parse_args()

    inp = "".join(sys.stdin.readlines())
    make_request("".join([inp.rstrip(), BANNER]), credentials)
    return


def make_request(inp, credentials):
    """ Make a POST request for creation of gist given by the payload
    parameters (GitHub v3 API).
    TODO: The file name generation and description could be made more
          meaningful.
    """
    payload = {
        "description": inp[:20].strip(),
        "public": False,
        "files": {
            "{}.txt".format(inp[:8].strip()): {
                "content": inp
            }
        }
    }
    user, passwd = authorization(credentials)
    post_request = requests.post("https://api.github.com/gists",
                                 auth=(user, passwd), data=json.dumps(payload))
    j = (json.loads(post_request.text))

    if post_request.status_code >= 400:
        err = j.get('message', 'Undefined Error - No message from server.')
        print("Error: {}".format(err))
        exit()

    if post_request.ok:
        print("URL: {}".format(j['html_url']))
        set_clipboard(j['html_url'])
        print("Copied to keyboard!")
    return


def authorization(credentials):
    """ Handling user, password input using getpass. This is the only
    workaround that I have found to accept non blocking input from
    terminal.
    """
    user, passwd = (credentials.user, credentials.password)

    if not user:
        user = getpass.getpass("Username: ")
    if not passwd:
        passwd = getpass.getpass("Password: ")

    return user, passwd


if __name__ == '__main__':
    exit(catch_input())
