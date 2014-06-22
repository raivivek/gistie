gistie
======

A tiny gist creation script (**experimental**) which takes an input and creates
a gist on Github-gists and copies the link to clipboard for instant
distribution.

The idea is to take output from install commands through piping and create an
instant gist for loggin or debugging of install commands. No more additions
thoughts as of now.


Requires `requests` module and `xclip` for copying to system clipboard.

### Regrets

I guess this can be easily done through bash scripting and `curl` but I didn't
know how to do that.

Also, this has already been done extensively and probably nicely somewhere that
I may not be aware of. I do not claim originality of code idea or implementation
but hey the name is _my_ invention ;).

### Problems

After having a little bit discussion about the way I originally the script to
work, it seems that code will become only more nastier and hard-coded than the
ease it would be. I am however still looking into the concept and working out
any possible solutions that I could think of. Let's hope for the best. 

_Clue_ : `getpass` module.
