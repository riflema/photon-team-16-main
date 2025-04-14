import tkinter as tk
from PIL import Image, ImageTk
from PIL.Image import Resampling
from typing import Dict, Optional, Union

class Game_Start_Countdown:
    def __init__(self, parent:Optional[Union[tk.Tk, tk.Toplevel]] = None) -> None:
        self.image_main_path = "countdown_images/"
        self.image_scale_factor = 0.5
        self.title = "Countdown"
        self.current_num = 0
        # Store as class variable to prevent garbage collection
        self.photos: Dict[str, ImageTk.PhotoImage] = {}
        self.num = 31
        self.parent = parent
        
    def create_countdown_window(self) -> None:
        print("Counting down")
        # Create the main window
        if self.parent:
            root = tk.Toplevel(self.parent)
        else:
            root = tk.Toplevel()

        root.title(self.title)
        root.attributes('-topmost', True)
        root.attributes('-fullscreen', True)
        
        # Create a frame to hold all content
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Load initial background
        try:
            bg_img = Image.open(f"{self.image_main_path}background.tif")
            bg_resized = bg_img.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
            bg_photo = ImageTk.PhotoImage(bg_resized)
            # Store reference to prevent garbage collection
            self.photos["bg"] = bg_photo
            
            # Create a label for displaying images
            label = tk.Label(frame, image=bg_photo)
            label.pack(fill=tk.BOTH, expand=True)

            # Define the update function inside where we have access to label and root
            def update_image() -> None:
                self.num -= 1
                if self.num < 0:
                    root.destroy()
                    return
                
                try:
                    # Load background for composite
                    bg = Image.open(f"{self.image_main_path}background.tif")
                    
                    # Try to load number image
                    try:
                        num_img = Image.open(f"{self.image_main_path}{self.num}.tif")
                        
                        # Calculate position to center the number
                        pos_x = ((bg.width - num_img.width) // 2) + 1
                        pos_y = ((bg.height - num_img.height) // 2) + 37
                        
                        # Paste the number onto background
                        if num_img.mode == 'RGBA':
                            bg.paste(num_img, (pos_x, pos_y), num_img)
                        else:
                            bg.paste(num_img, (pos_x, pos_y))
                    except Exception as e:
                        print(f"Error loading number image {self.num}: {e}")
                    
                    # Create new PhotoImage
                    bg_resized = bg.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
                    new_photo = ImageTk.PhotoImage(bg_resized)
                    # Store reference
                    self.photos[f"img_{self.num}"] = new_photo
                    
                    # Update label with new image
                    label.config(image=new_photo)
                    root.update()
                    
                    # Schedule next update
                    root.after(1000, update_image)
                except Exception as e:
                    print(f"Error in update_image: {e}")
                    root.destroy()
            
            # Start the countdown after a short delay
            root.after(10, update_image)
            
            
        except Exception as e:
            print(f"Error in create_countdown_window: {e}")
            if root:
                root.destroy()

def run_countdown(parent_window:Optional[Union[tk.Tk, tk.Toplevel]] = None) -> bool:
    try:
        countdown = Game_Start_Countdown(parent = parent_window)
        countdown.create_countdown_window()
        return True
    except Exception as e:
        print(f"Error in run_countdown: {e}")
        return False
