import logging
import argparse
import sys
import psycopg2


# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets'")
logging.debug("Database connection established.")

def put(name, snippet):
    """
    Store a snippet with an associated name.

    """
    logging.debug("Storing snippet - put({!r}, {!r})".format(name, snippet))
    #cursor=connection.cursor() #this will establish a conection to the psql table
    with connection,connection.cursor() as cursor:
        try:
            command="insert into snippets (keyword,message) values (%s,%s)"
            cursor.execute(command,(name,snippet)) 
        except:
            connection.rollback()
            command="update snippets set message=%s where keyword=%s"
            cursor.execute(command,(snippet,name)) 
        #connection.commit() 
        logging.debug('snippet stored succesfully')
        return name, snippet
    
def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return "ERROR: Snippet not found , try with a different keyword."

    Returns the snippet.
    """
    logging.debug("Searching for the snippet -  get({!r})".format(name))
    with connection,connection.cursor() as cursor:
        #cursor=connection.cursor()
        command="select * from snippets where keyword = %s"
        cursor.execute(command,(name,))
        snippet=cursor.fetchone() 
        #connection.commit()
    if not snippet:
        snippet="ERROR: Snippet not found , try with a different keyword."
        logging.debug('Snippet not found')
    else:logging.debug('snippet retrieved')
    return snippet

def search(name):
    """Retrieve the snippets which contain the letters of the name.

    If there is no such snippet, return "ERROR: Snippet not found , try with a different keyword."

    Returns the snippet.
    """
    logging.debug("Searching for the snippet -  search({!r})".format(name))
    with connection,connection.cursor() as cursor:
        #cursor=connection.cursor()
        name2='%'+name+'%'
        command="select * from snippets where keyword like {!r} and not hidden order by keyword;".format(name2)
        logging.debug("DEBUGGING : Checking how the string is concatenated : {!r}".format(command))
        cursor.execute(command,)
        snippet=cursor.fetchall()
        logging.debug("DEBUGGING : Checking the result of search {!r}".format(snippet))
        #connection.commit()
    if not snippet:
        snippet="ERROR: Snippet not found , try with a different keyword."
        logging.debug('Snippets not found')
    else:logging.debug('snippets retrieved')
    return snippet
    
def catalog():
    """Retrieve the names available.

    Returns the name list .
    """
    logging.debug("loading all snippets -  catalog()")
    cursor=connection.cursor()
    command="select keyword  from snippets where not hidden order by keyword;"
    cursor.execute(command,)
    snippetList=cursor.fetchall() 
    #logging.debug("{!r}".format(snippetList))
    #logging.debug("{!r}".format(type(snippetList)))
    logging.debug('all snippets retrieved')
    return snippetList
    
def main():
    """Main function"""
    logging.info("Constructing parsers")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    #put_parser.add_argument("--hide", help="The snippet will be hidden from search functions.")
    
    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet with a name")
    get_parser.add_argument("name",help="name of the snippet to retrieve.")

    # Subparser for the get command
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="Retrieve all snippets similar to name")
    search_parser.add_argument("name",help="name of the snippet to search for.")
    
    # Subparser for the catalog command
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Retrieve all names loaded.")
    arguments = parser.parse_args(sys.argv[1:])
    
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        if snippet=="ERROR: Snippet not found , try with a different keyword.":
            print("{!r}".format(snippet))
        else:print("Retrieved snippet: {!r}".format(snippet))
    elif command == "search":
        snippet = search(**arguments)
        if snippet=="ERROR: Snippet not found , try with a different keyword.":
            print("{!r}".format(snippet))
        else:print("Retrieved snippet: {!r}".format(snippet))
    elif command =="catalog":
        snipdict=catalog()
        #print("Retrieved snippet: {!r}".format(snipdict))
        print("The catalog list is :")
        for keyword in snipdict:
            print("{!r} ").format(keyword)

if __name__ == "__main__":
    main()