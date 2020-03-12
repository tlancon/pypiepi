import tkinter as tk
import numpy as np
from PIL import ImageTk, Image
from skimage.io import imread
from skimage.segmentation import slic, mark_boundaries
from skimage.morphology import flood_fill
from skimage.util import img_as_ubyte


class SLICPainterApp:
    def __init__(self, master, image_path):
        self.master = master

        self.input_image = imread(image_path)
        max_segments = int(0.01 * (self.input_image.shape[0] * self.input_image.shape[1]))

        self.segments = tk.Scale(master, label='Segments', orient=tk.VERTICAL, from_=10, to=max_segments, resolution=1)
        self.segments.set(300)
        self.segments.grid(row=0, column=0, sticky=tk.W)

        self.compactness = tk.Scale(master, label='Compactness', orient=tk.VERTICAL, from_=0.01, to=100,
                                    resolution=0.01)
        self.compactness.set(20)
        self.compactness.grid(row=1, column=0, sticky=tk.W)

        self.clear = tk.Button(master, text='Clear', command=self.clear_mask)
        self.clear.grid(row=2, column=0, sticky=tk.S)

        self.image_label = tk.Label(master)
        self.image_label.grid(row=0, column=1, rowspan=2)

        self.superpixels = slic(self.input_image, n_segments=self.segments.get(), compactness=self.compactness.get())
        self.boundaries = img_as_ubyte(mark_boundaries(self.input_image, self.superpixels))
        self.mask = np.zeros_like(self.boundaries)
        self.display_image = np.copy(self.boundaries)

        self.update_image()

        master.bind('<B1-Motion>', self.add_region)
        master.bind('<B3-Motion>', self.remove_region)
        master.bind('<ButtonRelease-1>', self.update_superpixels)
        master.bind('<Button-2>', self.flood_fill)

    def update_image(self):
        """
        DO DOCSTRING
        """
        self.display_tk = ImageTk.PhotoImage(Image.fromarray(self.display_image))
        self.image_label.configure(image=self.display_tk)
        self.image_label.image = self.display_tk

    def clear_mask(self):
        """
        DO DOCSTRING
        """
        self.mask = np.zeros_like(self.boundaries)
        self.display_image = np.copy(self.boundaries)
        self.update_image()

    def update_superpixels(self, event):
        """
        DO DOCSTRING
        """
        if event.widget in [self.segments, self.compactness]:
            self.superpixels = slic(self.input_image, n_segments=self.segments.get(),
                                    compactness=self.compactness.get())
            self.boundaries = img_as_ubyte(mark_boundaries(self.input_image, self.superpixels))
            self.mask = np.zeros_like(self.boundaries)
            self.display_image = np.copy(self.boundaries)
            self.update_image()

    def add_region(self, event):
        """
        Adds a superpixel to the segmentation.
        """
        if event.widget is self.image_label:
            chosen_region = self.superpixels[event.y, event.x]
            for i in range(3):
                self.mask[:, :, i] = np.where(self.superpixels == chosen_region, 255, self.mask[:, :, i])
                self.display_image[:, :, i] = np.where(self.mask[:, :, i] == 255, 255, self.display_image[:, :, i])
            self.update_image()

    def remove_region(self, event):
        """
        Removes a superpixel from the segmentation.
        """
        if event.widget is self.image_label:
            chosen_region = self.superpixels[event.y, event.x]
            for i in range(3):
                self.mask[:, :, i] = np.where(self.superpixels == chosen_region, 0, self.mask[:, :, i])
                self.display_image[:, :, i] = np.where(self.mask[:, :, i] == 0, self.boundaries[:, :, i],
                                                       self.display_image[:, :, i])
            self.update_image()

    def flood_fill(self, event):
        """
        DO DOCSTRING
        """
        if event.widget is self.image_label:
            for i in range(3):
                self.mask[:, :, i] = flood_fill(self.mask[:, :, i], seed_point=(event.y, event.x), new_value=255,
                                                tolerance=1)
                self.display_image[:, :, i] = np.where(self.mask[:, :, i] == 255, 255, self.display_image[:, :, i])
            self.update_image()