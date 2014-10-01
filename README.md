gistie
======

A tiny gist creation script which takes an input and creates
a gist on Github-gists and copies the link to clipboard for instant
distribution.

The idea is to take output from install commands through piping and create an
instant gist for loggin or debugging of install commands. No more additions
thoughts as of now.


Requires `requests` module, and `xclip` (optional).

## Installation

    $ curl -L https://raw.githubusercontent.com/vivekiitkgp/gistie/master/gistie.py -o /usr/local/bin/gistie
    $ chmod +x /usr/local/bin/gistie

Please provide appropriate permission when needed according to your platform.

## Usage

`$ command <options> ... | gistie`

Alternatively,

`$ command <options> ... | gistie -u <username> -p <password>`

In other words, pipe the output to the script.

Update
------
I have finally decided to use `getpass.getpass()` for username as well since
this was neater than implementing the getpass method in the script itself. It
works for the time being but, we must further test it rigorously.
