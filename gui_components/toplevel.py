import customtkinter as ctk
import tkinter as tk


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

purple = "#800080"
white = "#FFFFFF"
platinum = "#E5E4E2"


def open_toplevel_window(toplevel_width, toplevel_height, title, color, message, button1=None, button2=None, callback_function=None):
        # Create a Toplevel window
        top_level = tk.Toplevel()  # Using Toplevel from tkinter

        # Calculate the position for the center of the screen based on custom screen size
        position_top = int((WINDOW_HEIGHT - toplevel_height) / 2)
        position_left = int((WINDOW_WIDTH - toplevel_width) / 2)
        
        # Set the geometry of the Toplevel window (position + size)
        top_level.geometry(f"{toplevel_width}x{toplevel_height}+{position_left}+{position_top}")

        # Remove the close, minimize, and maximize buttons
        top_level.overrideredirect(True)  # Removes window decorations (title bar, buttons)
            
        # Optionally prevent closing the window (X button)
        top_level.protocol("WM_DELETE_WINDOW", lambda: None)

        # Add a border to the Toplevel window
        top_level.configure(bg=platinum, bd=5, relief='groove')
        
        # Set window to be non-resizable
        top_level.resizable(False, False)

        # Focus on the Toplevel window
        top_level.focus_set()

        # Delay the grab_set() call to after the window is visible
        top_level.after(100, top_level.grab_set)  # Call grab_set after 100ms

        # add widgets
        title_label = ctk.CTkLabel(top_level, text=title, font=("Arial", 22, 'bold'), fg_color=color, text_color=white, corner_radius=5)
        title_label.pack(padx=5, pady=5, fill='x')

        msg_label = ctk.CTkLabel(top_level, text=message, font=("Arial", 20))
        msg_label.pack(pady=30)

        def destroy_toplevel():
            top_level.destroy()

        def callback_and_destroy():
            if callback_function:
                callback_function()
            top_level.destroy()

        btn_frame = ctk.CTkFrame(top_level, fg_color='transparent')
        btn_frame.pack(pady=10)

        if button1:
            button1 = ctk.CTkButton(btn_frame, text=button1, font=("Arial", 22, 'bold'), fg_color=purple, height=40, hover=False, command=destroy_toplevel)
            button1.pack(side='left', padx=20)

        if button2:
            button2 = ctk.CTkButton(btn_frame, text=button2, font=("Arial", 22, 'bold'), fg_color=purple, height=40, hover=False, command=callback_and_destroy)
            button2.pack(side='left', padx=20)