import os
import random
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance, ImageOps

folder_path = 'C:\\Users\\11User\\Desktop\\slideshow-app\\pics'

class SlideshowApp:
    def __init__(self, root, folder_path, transition_time=1000, display_time=4000, steps=50):
        self.root = root
        self.folder_path = folder_path
        self.transition_time = transition_time  # How long a fade transition lasts (ms)
        self.display_time = display_time        # How long an image stays before changing (ms)
        self.steps = steps                      # How many frames in the fade transition
        self.image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        random.shuffle(self.image_files)
        self.index = 0

        self.label = tk.Label(root)
        self.label.pack()

        self.current_image = self.load_image(self.image_files[self.index])
        self.next_image_obj = None

        self.show_image(self.current_image)
        self.root.after(self.display_time, self.start_transition)

    def load_image(self, filename):
        path = os.path.join(self.folder_path, filename)
        img = Image.open(path).convert('RGBA')  # Always use RGBA mode to allow blending
        img = ImageOps.exif_transpose(img)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        img.thumbnail((screen_width, screen_height), Image.LANCZOS)

        # Create a black background
        background = Image.new('RGBA', (screen_width, screen_height), (0, 0, 0, 255))
        # Paste the image centered on the background
        x = (screen_width - img.width) // 2
        y = (screen_height - img.height) // 2
        background.paste(img, (x, y))

        return background


    def show_image(self, img):
        self.tk_image = ImageTk.PhotoImage(img)
        self.label.config(image=self.tk_image)

    def start_transition(self):
        self.index = (self.index + 1) % len(self.image_files)
        self.next_image_obj = self.load_image(self.image_files[self.index])
        self.fade_step = 0
        self.fade()

    def fade(self):
        alpha = self.fade_step / self.steps
        blended = Image.blend(self.current_image, self.next_image_obj, alpha)
        self.show_image(blended)

        if self.fade_step < self.steps:
            self.fade_step += 1
            delay = self.transition_time // self.steps
            self.root.after(delay, self.fade)
        else:
            self.current_image = self.next_image_obj
            self.root.after(self.display_time, self.start_transition)


print("Starting app...")
root = tk.Tk()
root.configure(bg='black')
root.attributes('-fullscreen', True)  # Make it full screen

app = SlideshowApp(root, folder_path)
print("Running mainloop...")
root.mainloop()
print("App finished.")