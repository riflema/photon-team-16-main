import tkinter as tk
from PIL import Image, ImageTk
from player_entry_gui import Player_Entry_GUI as Player_Entry_GUI

class Game_Start_Countdown:
  def __init__(self) -> None:
    self.root = tk.TK()
    self.countdown()

  def countdown() -> None:
    # Create the main window
    root.title("Countdown")

    # Set the window size to be full screen
    root.attributes("-fullscreen", True)

    # Load the image using PIL
    img = Image.open("countdown_images/background.tif")
    resized_image = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    photo = ImageTk.PhotoImage(resized_image)

    # Create a label to display the image
    label = tk.Label(root, image=photo).pack(expand=True)

    # Close the window after 3 seconds (3000 ms)
    # root.after(3000, create_player_entry)

    # Run the Tkinter main loop
    root.mainloop()
