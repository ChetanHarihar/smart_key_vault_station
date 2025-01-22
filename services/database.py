from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os

DB_CONN_STRING = os.environ.get('DB_CONN_STRING')

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
        client = MongoClient(DB_CONN_STRING)
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

# Function to authenticate the user
def auth_user(collection_name="employee", UID=None, projection=None):
    """
    Authenticates a user by validating the card scanned.

    Parameters:
        collection_name (str): The name of the collection within the database.
        UID (str): The card ID for authentication.
        projection (dict): Optional. Specifies fields to include or exclude in the result.

    Returns:
        dict or None: A single document matching the filter if found, else None.
    """
    if not UID:
        print("Card ID is required for authentication.")
        return None

    filter_criteria = {'UID': UID, 'active_status': True}

    try:
        # Connect to the database
        db = get_db_connection()
        
        # Access the specified collection
        collection = db[collection_name]
        
        # Query for a single matching document
        document = collection.find_one(filter_criteria, projection)
        
        return document

    except ConnectionError as conn_err:
        print(f"Failed to connect to MongoDB: {conn_err}")
        return None
    except PyMongoError as e:
        print(f"An error occurred with the MongoDB operation: {e}")
        return None
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        return None