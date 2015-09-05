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
    cursor=connection.cursor() #this will establish a conection to the psql table
    command="insert into snippets (keyword,message) values (%s,%s)"
    cursor.execute(command,(name,snippet)) #instructions that are being sent to the database, substituting the values for keyword and message that will be sent
    connection.commit() #save changes to the database
    logging.debug('snippet stores succesfully')
    return name, snippet
    
def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return ""

    Returns the snippet.
    """
    logging.debug("Searching for the snippet -  get({!r})".format(name))
    cursor=connection.cursor()
    command="select * from snippets where keyword = %s"
    cursor.execute(command,(name,))
    snippet=cursor.fetchone() 
    print(type(snippet))
    logging.debug('snippet retrieved')
    return snippet
    
def viewall():
    """Retrieve the names available.

    Returns the name list .
    """
    logging.debug("loading all snippets -  viewall()")
    cursor=connection.cursor()
    command="select * from snippets ;"
    cursor.execute(command,)
    snippetList=cursor.fetchall() 
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

    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet with a name")
    get_parser.add_argument("name",help="name of the snippet to retrieve.")
    
    # Subparser for the viewall command
    logging.debug("Constructing viewall subparser")
    viewall_parser = subparsers.add_parser("viewall", help="Retrieve all names and snippets loaded.")
    arguments = parser.parse_args(sys.argv[1:])
    
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command =="viewall":
        snipdict=viewall()
        #print("Retrieved snippet: {!r}".format(snipdict))
        print("(keyword | text )")
        for keyword,text in snipdict:
            print("({!r} , {!r})").format(keyword,text)

if __name__ == "__main__":
    main()