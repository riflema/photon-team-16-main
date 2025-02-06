import tkinter as tk
from PIL import Image, ImageTk

def show_image():
    # Create the main window
    root = tk.Tk()
    root.title("Image Display")

    # Set the window size to be full screen
    root.attributes("-fullscreen", True)

    # Load the image using PIL
    image = Image.open("logo.jpg")

    # Get the window dimensions
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()

    # Resize the image to fit the window using the new resampling method
    image = image.resize((window_width, window_height), Image.Resampling.LANCZOS)

    # Convert the image to a format Tkinter can use
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    label = tk.Label(root, image=photo)
    label.pack(fill="both", expand=True)

    # Close the window after 3 seconds (3000 ms)
    root.after(3000, root.destroy)

    # Run the Tkinter main loop
    root.mainloop()

show_image()
