#!/usr/bin/python3

"""
Gistie - A tiny script to generate quick pasties from terminal stdout
         and stdin output.
         Requires xclip, requests module.

  TODO : The current behavior is tested only for very simple outputs
         and may not work well. I think it would be suitable to work
         with stdin/stdout directly.
"""

__author__ = "Vivek Rai"
__date__ = "18th July, 2014"


import requests
import json
import getpass
import sys
from subprocess import Popen, PIPE


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
    """ Read redirected input from the command line. See related note.
    """
    inp = "".join(sys.stdin.readlines())
    make_request("".join([inp.rstrip(), BANNER]))
    return


def make_request(inp):
    """ Make a POST request for creation of gist given by the payload
    parameters (GitHub v3 API).
    TODO: The file name generation and description could be made more
          meaningful.
    """
    payload = {
        "description": inp[:20],
        "public": False,
        "files": {
            "{}.txt".format(inp[:8]): {
                "content": inp
            }
        }
    }
    user, passwd = authorization()
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


def authorization():
    """ Handling user, password input using getpass. This is the only
    workaround that I have found to accept non blocking input from
    terminal.
    """
    user, passwd = ("", "")
    if not user:
        user = getpass.getpass("Username: ")
    if not passwd:
        passwd = getpass.getpass("Password: ")

    return user, passwd


if __name__ == '__main__':
    exit(catch_input())
