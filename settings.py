import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os


# Screen size
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

# Colors
purple = "#800080"
white = "#FFFFFF"
black = "#000000"
green = "#36A211"
red = "#FF0000"
blue = "#0096FF"
gray = "#A9A9A9"
platinum = "#E5E4E2"
lavender = "#E6E6FA"
vl_green = "#D1FFBD"

# Device data
STATION_NAME = os.environ.get('STATION_NAME')
STATION_LINE = os.environ.get('STATION_LINE')
STATION_REACH = os.environ.get('STATION_REACH')

# Key data 
s_and_t_ups = "S & T UPS"
ser = "SER"
ter= "TER"
ass_and_tss= "ASS/TSS"
dg = "DG"
pump = "PUMP"

# Key and department mapping
KEY_MAP = {"Signalling": [s_and_t_ups, ser], 
           "Telecom & AFC": [s_and_t_ups, ter], 
           "Traction": [ass_and_tss], 
           "E & M": [ass_and_tss, dg, pump], 
           "Fire": [s_and_t_ups, ser, ter, ass_and_tss, dg, pump],
           "All": [s_and_t_ups, ser, ter, ass_and_tss, dg, pump]
           }