from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime, timedelta, timezone
import pytz
import os

# Database connection string
DB_CONN_STRING = os.environ.get('DB_CONN_STRING')
# Define the IST timezone
IST_TIMEZONE = pytz.timezone('Asia/Kolkata')

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

# Function to fetch completed logs for a specific station
def fetch_completed_logs(
    collection_name="log",
    station_name=None,
    projection=None,
    offset=0,
    limit=0,
    history=None
):
    # Ensure the station name is provided
    if not station_name:
        print("Error: Station name is required.")
        return []

    # Base query
    query = {
        "station": station_name,
        "status": "Completed"  # Target logs with 'Completed' status
    }

    # Add time-based filter if history is provided
    if history:
        try:
            # Get the current IST time
            current_time = datetime.now(IST_TIMEZONE)
            if history == "1 week":
                start_time = current_time - timedelta(weeks=1)
            elif history == "2 weeks":
                start_time = current_time - timedelta(weeks=2)
            elif history == "1 month":
                start_time = current_time - timedelta(days=30)
            else:
                raise ValueError("Invalid history value. Use '1 week', '2 weeks', or '1 month'.")
            
            # Convert timestamps to UTC for MongoDB query
            start_time_utc = start_time.astimezone(pytz.utc)
            query["issued_timestamp"] = {"$gte": start_time_utc}
        except ValueError as ve:
            print(f"Error: {ve}")
            return []

    try:
        # Connect to the database
        db = get_db_connection()  # This should return the actual database connection
        collection = db[collection_name]

        # Fetch the logs using the query
        documents = list(
            collection.find(query, projection)  # Apply the projection here
                      .sort("issued_timestamp", -1)  # Sort by issued_timestamp in descending order
                      .skip(offset)
                      .limit(limit)
        )

        # Return the result or an empty list if no documents are found
        return documents

    except PyMongoError as e:
        print(f"An error occurred with the MongoDB operation: {e}")
        return []
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        return []
    
# Function to check key availability
def check_key_availability(
    collection_name="log",
    station_name: str = None,
    keys: list = None,
    projection = None
) -> dict:
    """
    Checks the availability of keys for a given station and provides log data for unavailable keys.

    Args:
        collection_name (str): Name of the MongoDB collection.
        station_name (str): Name of the station to filter logs.
        keys (list): List of keys to check availability.

    Returns:
        dict: Dictionary with keys as input keys. If unavailable, the value is the log data; otherwise, None.
    """
    # Validate inputs
    if not station_name:
        raise ValueError("station_name is required.")
    if not keys or not isinstance(keys, list):
        raise ValueError("keys must be a non-empty list.")

    # Base query to find 'On-going' logs for the given station and keys
    query = {
        "station": station_name,
        "status": "On-going",
        "key": {"$in": keys}
    }

    try:
        # Connect to the database
        db = get_db_connection()  # Replace with your database connection
        collection = db[collection_name]

        # Fetch matching documents (retrieve full log data for unavailable keys)
        ongoing_logs_cursor = collection.find(
            query,
            projection
        )
        
        # Extract ongoing logs into a dictionary for quick lookup
        ongoing_logs = {log["key"]: log for log in ongoing_logs_cursor}

        # Build the result dictionary
        result = {key: ongoing_logs.get(key, None) for key in keys}

        return result

    except PyMongoError as e:
        print(f"An error occurred with the MongoDB operation: {e}")
        return {key: None for key in keys}
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        return {key: None for key in keys}
    

# Example usage
if __name__ == "__main__":
    station_name = "Baiyappanahalli"
    keys = ["SER", "TER", "DG"]

    # Call the function
    result = check_key_availability(
        station_name=station_name,
        keys=keys
    )

    print(result)