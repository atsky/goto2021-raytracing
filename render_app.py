import time
import tkinter as tk

import tqdm

import numpy as np
import threading
import matplotlib.pyplot as plt

from skimage.transform import resize

from PIL import Image, ImageTk


class RenderApp:
    def __init__(self, draw_function, width, height, result_file=None):
        self.draw_function = draw_function
        self.width = width
        self.height = height
        self.result_file = result_file
        self.root = tk.Tk()

        self.image_data = np.zeros((height, width, 3))

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
            array = self.image_data.astype(np.uint8)
        self.img = ImageTk.PhotoImage(image=Image.fromarray(array))
        self.c_image = self.canvas.create_image(0, 0, anchor="nw", image=self.img)

        self.root.after(100, self.do_update)

    def generate_pairs(self, step):
        for j in range(0, self.height, step):
            for i in range(0, self.width, step):
                yield i, j

    def generate_triples(self):
        for step in [16, 4, 1]:
            for i, j in self.generate_pairs(step):
                yield step, i, j

    def draw_all(self):
        start_time = time.time()

        width = self.width
        height = self.height

        mask = np.zeros((height, width))
        triples = list(self.generate_triples())
        for step, i, j in tqdm.tqdm(triples):
            c = self.draw_function(i, j, width, height)
            if mask[j, i] == 1:
                continue
            with self.lock:
                self.image_data[j:j + step, i:i + step, :] = (c.clip(0, 0.9999) * 256)
                mask[j, i] = 1

        elapsed_time = time.time() - start_time
        print('Rendering finished in {:.2f} s'.format(elapsed_time))

        if self.result_file is not None:
            plt.imsave('image.png', self.image_data.astype(np.uint8))


def run_render(draw_pixel, width, height, result_file):
    RenderApp(draw_pixel, width, height, result_file)
