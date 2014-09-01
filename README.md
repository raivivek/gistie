gistie
======

A tiny gist creation script (**experimental**) which takes an input and creates
a gist on Github-gists and copies the link to clipboard for instant
distribution.

The idea is to take output from install commands through piping and create an
instant gist for loggin or debugging of install commands. No more additions
thoughts as of now.


Requires `curl`, `requests` module, and `xclip`.

## Installation

    curl -L https://raw.githubusercontent.com/vivekiitkgp/gistie/master/gistie.py -o /usr/local/bin/gistie
    chmod +x /usr/local/bin/gistie

## Usage

`command <options> ... | gistie`

Alternatively,

`command <options> ... | gistie -u <username> -p <password>`

In other words, pipe the output to the script.

### Regrets

I guess this can be easily done through bash scripting and `curl` but I didn't
know how to do that.

Also, this has already been done extensively and probably nicely somewhere that
I may not be aware of.

````
.. ARCHIVE

### Problems
After having a little bit discussion about the way, I originally the script to
work, it seems that the code will become only nastier and hard-coded than the
ease it would be. I am however still looking into the concept and working out
any possible solutions that I could think. Let's hope for the best.
````

Update
------
I have finally decided to use `getpass.getpass()` for username as well since
this was neater than implementing the getpass method in the script itself. It
works for the time being but, we must further test it rigorously.
