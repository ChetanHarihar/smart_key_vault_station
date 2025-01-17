from settings import CONNECTION_STRING
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Function to establish a connection to the MongoDB database
def get_db_connection(database_name="smart_key_vault"):
    """
    Establishes a connection to the MongoDB database.

    Args:
        database_name (str): The name of the database to connect to.

    Returns:
        db: The database instance.
    """
    try:
        # Create a MongoClient
        client = MongoClient(CONNECTION_STRING)
        # Access the specified database
        db = client[database_name]
        return db
    except Exception as e:
        raise ConnectionError(f"Could not connect to the database: {e}")

# Function to retrieve all the collections in a MongoDB database
def get_all_collections():
    """
    Fetches all collection names from a specified MongoDB database.

    Args:
        database_name (str): The name of the database.

    Returns:
        list: A list of collection names in the database, or None if an error occurs.
    """
    try:
        # Use the existing get_db_connection function to connect to the database
        db = get_db_connection()

        # Get a list of all collection names
        collections = db.list_collection_names()

        return collections

    except PyMongoError as e:
        print(f"An error occurred with MongoDB: {e}")
        return None
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        return None