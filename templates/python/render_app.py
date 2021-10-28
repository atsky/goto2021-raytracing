import tkinter as tk

import numpy as np
import threading
from skimage.transform import resize

from PIL import Image, ImageTk


class RenderApp:
    def __init__(self, draw_function, width, height, result_file=None):
        self.draw_function = draw_function
        self.root = tk.Tk("Ray Tracing")

        self.array = np.zeros([400, 600, 3]).astype(np.uint8)
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.array))

        self.canvas = tk.Canvas(self.root, width=600, height=400)
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
        local_image = np.zeros((200, 300, 3))
        while True:
            for j in range(200):
                for i in range(300):
                    c = self.draw_function(i, j, 300, 200)
                    local_image[j, i, :] = (c.clip(0, 0.9999) * 256)

                with self.lock:
                    self.array = resize(local_image, (400, 600), order=1).astype(np.uint8)


def run_render(draw_pixel, width, height, result_file):
    RenderApp(draw_pixel, width, height, result_file)
