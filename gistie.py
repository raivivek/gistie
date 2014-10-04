#!/usr/bin/python3

__description__ = """
Gistie - A tiny script to generate quick pasties from terminal stdout
         and stdin output.
         Requires requests module, and xclip (optional).
"""

__author__ = "Vivek Rai"
__date__ = "18th July, 2014"


import requests
import json
import getpass
import sys
import argparse
from subprocess import Popen, PIPE


MAX_RETRIES = 2
BANNER = """\n---\nGenerated by gistie (gh://vivekiitkgp/gistie)."""

def copy(link):
    """Copy given link into system clipboard.
    """
    check_xclip = Popen(['which', 'xclip'], stdout=PIPE)
    out, _ = check_xclip.communicate()

    if out:
        process = Popen(['xclip', '-selection', 'c'], stdin=PIPE)
        # works on Python 3 (bytes() requires an encoding)
        process.communicate(input=bytes(link, 'utf-8'))
        print("Copied to keyboard!")
    else:
        "xclip must be installed \
        On ubuntu, \
        $ sudo apt-get install xclip"

    return

def init():
    """ Set parser arguments, read redirected input from the command line.
    """
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument('-u', action='store',
                        dest='user',
                        help='Set username')
    parser.add_argument('-p', action='store',
                        dest='password',
                        help='Set password')

    credentials = prompt(parser.parse_args())
    return credentials

def create_gist():
    """ The main function which reads input data from terminal, prompts for
    user password and uploads the content.
    """

    read_data = sys.stdin.readlines()
    data_to_string = ''.join(read_data)

    if not read_data:
        print("No gist created due to bad input.")
        exit()

    payload = {
        'description': read_data[0],
        'public': False,
        'files': {
            "": {
                'content': ''.join([data_to_string, BANNER])
            }
        }
    }

    login = init()
    attempts = 0
    for attempts in range(MAX_RETRIES):
        post = requests.post('https://api.github.com/gists',
                             auth=(login.user, login.password),
                             data=json.dumps(payload))
        response = json.loads(post.text)
        response_message = response.get('message', 'Unknown Error')

        if post.status_code == 401:
            print("Error: {}, Please try again.".format(response_message))
            login = prompt(login, True)
            continue
        elif post.ok:
            print("URL: {}".format(response['html_url']))
            copy(response['html_url'])
            return

    # If everything fails, print an error message in the end.
    if attempts == 2:
        print("Error: Too many retries")
    else:
        print("Error: {}".format(response_message))

def prompt(login, bad_try=False):
    """ Prompt only for those fields which are not already known, and if
    previous attempt is failed, prompt for both fields.
    """
    if bad_try:
        login.user = getpass.getpass('Username (not shown): ')
        login.password = getpass.getpass('Password (not shown): ')
    else:
        if not login.user:
            login.user = getpass.getpass('Username (not shown): ')
        if not login.password:
            login.password = getpass.getpass('Password (not shown): ')

    return login

if __name__ == '__main__':
    exit(create_gist())
