import customtkinter as ctk
from PIL import Image
import os


# Screen size
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600

# Device data
STATION_NAME = os.environ.get('STATION_NAME')
STATION_LINE = os.environ.get('STATION_LINE')
STATION_REACH = os.environ.get('STATION_REACH')

# Constants for database connection
USERNAME = os.environ.get('DB_USERNAME')
PASSWORD = os.environ.get('DB_PASSWORD')
CLUSTER = os.environ.get('DB_CLUSTER')
CONNECTION_STRING = f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER}/"