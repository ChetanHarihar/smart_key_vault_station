import customtkinter as ctk
from tkinter import ttk

class TreeView(ttk.Treeview):
    def __init__(self, parent, tags=('oddrow', 'evenrow'), *args, **kwargs):
        super().__init__(parent, selectmode='browse', *args, **kwargs)

        # Set tags and their configurations
        for tag in tags:
            self.tag_configure(tag, background='#ECECEC' if tag == 'oddrow' else '#CFCFCF', foreground='#000000')

        # Create and place the vertical scrollbar
        self.vertical_scrollbar = ctk.CTkScrollbar(parent, orientation="vertical", width=20, command=self.yview)
        self.vertical_scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

        # Create and place the horizontal scrollbar
        self.horizontal_scrollbar = ctk.CTkScrollbar(parent, orientation="horizontal", height=20, command=self.xview)
        self.horizontal_scrollbar.pack(side=ctk.BOTTOM, fill=ctk.X)

        # Configure the Treeview's yscroll and xscroll commands
        self.configure(yscrollcommand=self.vertical_scrollbar.set, xscrollcommand=self.horizontal_scrollbar.set)

        # Pack the Treeview widget last so it fills the remaining space after scrollbars have been placed
        self.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

# Example usage:
if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Options: "System", "Light", "Dark"
    ctk.set_default_color_theme("blue")  # Options: "blue", "dark-blue", "green"

    root = ctk.CTk()
    root.title("Custom TreeView Example")
    root.geometry("500x300")

    # Create a custom frame for better alignment
    frame = ctk.CTkFrame(root)
    frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

    # Create and configure the custom treeview
    custom_treeview = TreeView(frame)

    # Create columns
    custom_treeview["columns"] = ("SL.no", "ID", "Category", "Size", "Quantity", "Quantity_selected")
    custom_treeview.column("#0", width=0, stretch=ctk.NO)  # Hide the item_tree column
    custom_treeview.column("SL.no", width=40)
    custom_treeview.column("ID", width=0, stretch=ctk.NO)
    custom_treeview.column("Category", width=180, anchor=ctk.CENTER)
    custom_treeview.column("Size", width=250)
    custom_treeview.column("Quantity", width=0, stretch=ctk.NO)
    custom_treeview.column("Quantity_selected", width=0, stretch=ctk.NO)

    # Create headings
    custom_treeview.heading("SL.no", text="SL.no")
    custom_treeview.heading("Category", text="Category")
    custom_treeview.heading("Size", text="Size")

    # Inserting categories/items in the Treeview
    for i in range(1, 11):
        if i % 2 == 0:
            custom_treeview.insert('', ctk.END, values=(f"{i}", f"ID_{i}", f"Category {i}", f"Size {i}", f"Quantity {i}", f"Selected {i}"), tags=('evenrow',))
        else:
            custom_treeview.insert('', ctk.END, values=(f"{i}", f"ID_{i}", f"Category {i}", f"Size {i}", f"Quantity {i}", f"Selected {i}"), tags=('oddrow',))

    root.mainloop()