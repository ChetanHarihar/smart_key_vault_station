import customtkinter as ctk
import tkinter as tk

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

purple = "#800080"
white = "#FFFFFF"
platinum = "#E5E4E2"

class TopLevelWindow:
    def __init__(self, toplevel_width, toplevel_height, title, color, message, button1=None, button2=None, callback_function=None):
        self.top_level = tk.Toplevel()
        
        # Calculate position to center the window
        position_top = int((WINDOW_HEIGHT - toplevel_height) / 2)
        position_left = int((WINDOW_WIDTH - toplevel_width) / 2)
        
        self.top_level.geometry(f"{toplevel_width}x{toplevel_height}+{position_left}+{position_top}")
        self.top_level.overrideredirect(True)
        self.top_level.protocol("WM_DELETE_WINDOW", lambda: None)
        self.top_level.configure(bg=platinum, bd=5, relief='groove')
        self.top_level.resizable(False, False)
        self.top_level.focus_set()
        self.top_level.after(100, self.top_level.grab_set)

        # Add widgets
        self.title_label = ctk.CTkLabel(self.top_level, text=title, font=("Arial", 22, 'bold'), fg_color=color, text_color=white, corner_radius=5)
        self.title_label.pack(padx=5, pady=5, fill='x')

        self.msg_label = ctk.CTkLabel(self.top_level, text=message, font=("Arial", 20))
        self.msg_label.pack(pady=30)

        self.btn_frame = ctk.CTkFrame(self.top_level, fg_color='transparent')
        self.btn_frame.pack(pady=10)

        if button1:
            self.button1 = ctk.CTkButton(self.btn_frame, text=button1, font=("Arial", 22, 'bold'), fg_color=purple, height=40, hover=False, command=self.destroy)
            self.button1.pack(side='left', padx=20)
        
        if button2:
            self.button2 = ctk.CTkButton(self.btn_frame, text=button2, font=("Arial", 22, 'bold'), fg_color=purple, height=40, hover=False, command=self.callback_and_destroy)
            self.button2.pack(side='left', padx=20)
        
        self.callback_function = callback_function
    
    def destroy(self):
        self.top_level.destroy()
    
    def callback_and_destroy(self):
        if self.callback_function:
            self.callback_function()
        self.destroy()