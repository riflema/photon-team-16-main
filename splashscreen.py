import tkinter as tk
from PIL import Image, ImageTk
from player_entry_gui import Player_Entry_GUI as Player_Entry_GUI

root = tk.Tk()

def create_player_entry() -> None:
    root.destroy()
    player_entry_gui = Player_Entry_GUI()

def show_image() -> None:
    # Create the main window
    root.title("Image Display")

    # Set the window size to be full screen
    root.attributes("-fullscreen", True)

    # Load the image using PIL
    img = Image.open("gui_sprites/logo.jpg")
    resized_image = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    photo = ImageTk.PhotoImage(resized_image)

    # Create a label to display the image
    label = tk.Label(root, image=photo).pack(expand=True)

    # Close the window after 3 seconds (3000 ms)
    root.after(3000, create_player_entry)

    # Run the Tkinter main loop
    root.mainloop()

show_image()
