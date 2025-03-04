from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime, timedelta, timezone
from bson import ObjectId
import pytz
import os

# Database connection string
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
            current_time = datetime.now(pytz.utc)
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
    
# Function to insert a log 
def insert_log(collection_name="log", station=None, line=None, reach=None, key=None, purpose=None, key_issuer=None, key_picker=None):
    try:
        # Connect to the database using the get_db_connection function
        db = get_db_connection()
        collection = db[collection_name]

        # Get current UTC time
        current_time_utc = datetime.now(pytz.utc) 

        # convert to IST to display
        # Convert to IST (UTC +5:30)
        ist_offset = timedelta(hours=5, minutes=30)
        current_time_ist = current_time_utc + ist_offset

        # Format date and time as strings
        in_date = current_time_ist.strftime("%d-%m-%Y")  # DD-MM-YYYY format
        in_time = current_time_ist.strftime("%H:%M")     # HH:MM format

        # Prepare the document
        document = {
            "status": "On-going",
            "station": station,
            "line": line,
            "reach": reach,
            "key": key,
            "purpose": purpose,
            "key_picker": {
                "_id": key_picker.get("_id", ""),
                "employee_ID": key_picker.get("employee_ID", ""),
                "name": key_picker.get("name", ""),
                "UID": key_picker.get("UID", ""),
                "active_status": key_picker.get("active_status", ""),
                "department": key_picker.get("department", ""),
                "designation": key_picker.get("designation", ""),
                "role": key_picker.get("role", ""),
                "contact_number": key_picker.get("contact_number", "")
            },
            "issued_timestamp": current_time_utc,
            "issued_date": in_date,
            "issued_time": in_time,
            "key_issuer": {
                "_id": key_issuer.get("_id", ""),
                "employee_ID": key_issuer.get("employee_ID", ""),
                "name": key_issuer.get("name", ""),
                "UID": key_issuer.get("UID", ""),
                "active_status": key_issuer.get("active_status", ""),
                "role": key_issuer.get("role", ""),
                "contact_number": key_issuer.get("contact_number", "")
            }
        }

        # Insert the document
        result = collection.insert_one(document)
        print(f"Document inserted with ID: {result.inserted_id}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Function to update the log
def update_log(collection_name="log", log_id=None, status="Completed", key_returner=None, key_receiver=None):
    try:
        # Connect to the database using the get_db_connection function
        db = get_db_connection()
        collection = db[collection_name]

        # Prepare the current UTC timestamp for the returned timestamp
        current_time_utc = datetime.now(pytz.utc)

        # convert to IST to display
        # Convert to IST (UTC +5:30)
        ist_offset = timedelta(hours=5, minutes=30)
        current_time_ist = current_time_utc + ist_offset

        # Format date and time as strings
        out_date = current_time_ist.strftime("%d-%m-%Y")  # DD-MM-YYYY format
        out_time = current_time_ist.strftime("%H:%M")     # HH:MM format

        # Prepare the updated document
        updated_document = {
            "status": status,
            "returned_timestamp": current_time_utc,  # Convert returned timestamp to UTC
            "returned_data": out_date,
            "returned_time": out_time,
            "key_returner": {
                "_id": key_returner.get("_id", ""),
                "employee_ID": key_returner.get("employee_ID", ""),
                "name": key_returner.get("name", ""),
                "UID": key_returner.get("UID", ""),
                "active_status": key_returner.get("active_status", ""),
                "department": key_returner.get("department", ""),
                "designation": key_returner.get("designation", ""),
                "role": key_returner.get("role", ""),
                "contact_number": key_returner.get("contact_number", "")
            },
            "key_receiver": {
                "_id": key_receiver.get("_id", ""),
                "employee_ID": key_receiver.get("employee_ID", ""),
                "name": key_receiver.get("name", ""),
                "UID": key_receiver.get("UID", ""),
                "active_status": key_receiver.get("active_status", ""),
                "role": key_receiver.get("role", ""),
                "contact_number": key_receiver.get("contact_number", "")
            }
        }

        # Update the document
        result = collection.update_one(
            {"_id": ObjectId(log_id)},
            {"$set": updated_document}
        )

        if result.matched_count > 0:
            print(f"Log with ID: {log_id} updated successfully.")
        else:
            print(f"No log found with ID: {log_id}")

    except Exception as e:
        print(f"An error occurred: {e}")