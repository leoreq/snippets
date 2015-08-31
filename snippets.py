import logging

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet
    
def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return "snippet not found"

    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return "snippet not found"
    
def viewAll():
    """Retrieve the names available.

    Returns the name list .
    """
    snippetList=[]
    logging.error("FIXME: Unimplemented - viewAll({!r})".format(snippetList))
    return snippetList