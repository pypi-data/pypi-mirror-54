I found this pacakage which did exactly what I needed but in Python2 https://pypi.org/project/urlunshort/. I updated the code and moved the web logic to requests to simplify some things. 

Some URLs for shortening came from https://gist.github.com/ninetyfivenorth/9322bfc20523ba2eb7521d57cf25f265.

This should handle many services reasonably, but I found a few that don't respond normally to a HEAD requests and the tricks=True argument might help with some of those cases.
