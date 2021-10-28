import tkinter as tk

import numpy as np
import threading
from skimage.transform import resize

from PIL import Image, ImageTk


class RenderApp:
    def __init__(self, draw_function, width, height, result_file=None):
        self.draw_function = draw_function
        self.width = width
        self.height = height
        self.root = tk.Tk()

        self.array = np.zeros([height, width, 3]).astype(np.uint8)
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.array))

        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.pack()
        self.c_image = self.canvas.create_image(0, 0, anchor="nw", image=self.img)

        self.root.after(100, self.do_update)

        self.lock = threading.Lock()

        self.thread = threading.Thread(target=self.draw_all, args=(), daemon=True)
        self.thread.start()

        self.root.mainloop()

    def do_update(self):
        with self.lock:
            self.img = ImageTk.PhotoImage(image=Image.fromarray(self.array))
            self.c_image = self.canvas.create_image(0, 0, anchor="nw", image=self.img)

        self.root.after(100, self.do_update)

    def draw_all(self):
        width = self.width
        height = self.height

        local_image = np.zeros((height, width, 3))
        mask = np.zeros((height, width))
        for step in [16, 4, 1]:
            for j in range(0, height, step):
                for i in range(0, width, step):
                    c = self.draw_function(i, j, width, height)
                    if mask[j, i] != 1:
                        local_image[j:j+step, i:i+step, :] = (c.clip(0, 0.9999) * 256)
                        mask[j, i] = 1

                with self.lock:
                    self.array = local_image.astype(np.uint8)


def run_render(draw_pixel, width, height, result_file):
    RenderApp(draw_pixel, width, height, result_file)
