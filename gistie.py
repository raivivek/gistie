#!/usr/bin/python3

"""
Gistie - A tiny script to generate quick pasties from terminal stdout
         and stdin output.
         Requires xclip, requests module.
"""

__author__ = "Vivek Rai"
__date__ = "18th July, 2014"


import requests
import json
import getpass
from sys import stdin, stdout
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
    """ Read redirected input from the command line.
        TODO : Not properly tested. May not work well. Possibl
    """
    inp = input()
    make_request(inp)

    return


def make_request(inp):
    """ Make a POST request for creation of gist given by the payload
    parameters.
    """
    payload = {
        "description": inp[:20],
        "public": False,
        "files": {
            "{}_gistie.txt".format(inp[:5]): {
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
        print("Error : {}".format(err))
        exit()

    if post_request.ok:
        print("URL : {}".format(j['html_url']))
        set_clipboard(j['html_url'])
        print("Copied to keyboard!")
    return


def authorization():
    """ Handling authorization through github v3 API
    """
    user, passwd = ("", "")
    if not user:
        user = input("Username: ")
    if not passwd:
        passwd = getpass.getpass("Password: ")

    return user, passwd


if __name__ == '__main__':
    exit(catch_input())
