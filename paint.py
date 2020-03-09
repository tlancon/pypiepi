import tkinter as _tk
import numpy as _np
from PIL import ImageTk as _ImageTk
from PIL import Image as _Image
from skimage.io import imread as _imread
from skimage.segmentation import slic as _slic
from skimage.segmentation import mark_boundaries as _mark_boundaries
from skimage.util import img_as_ubyte as _img_as_ubyte


class SLICPainterApp:
    def __init__(self, master, image_path):
        self.master = master

        self.xy_label = _tk.Label(master, text='X, Y: ')
        self.xy_label.grid(row=0, column=0, sticky=_tk.E)

        self.xy_coords = _tk.Entry(master)
        self.xy_coords.grid(row=0, column=1, sticky=_tk.W)

        self.region_label = _tk.Label(master, text='SLIC region: ')
        self.region_label.grid(row=0, column=2, sticky=_tk.E)

        self.region_coords = _tk.Entry(master)
        self.region_coords.grid(row=0, column=3, sticky=_tk.W)

        self.input_image = _imread(image_path)
        self.superpixels = _slic(self.input_image, n_segments=2500, compactness=15)
        self.boundaries = _img_as_ubyte(_mark_boundaries(self.input_image, self.superpixels))
        self.mask = _np.zeros_like(self.boundaries)
        self.display_image = _np.copy(self.boundaries)

        self.display_tk = _ImageTk.PhotoImage(_Image.fromarray(self.display_image))
        self.image_label = _tk.Label(master, image=self.display_tk)
        self.image_label.image = self.display_tk
        self.image_label.grid(row=1, column=0, columnspan=8)

        master.bind("<Button-1>", self.add_region)
        master.bind("<Button-3>", self.remove_region)

    def update_image(self, image_array):
        """
        DO DOCSTRING
        """
        self.display_tk = _ImageTk.PhotoImage(_Image.fromarray(image_array))
        self.image_label.configure(image=self.display_tk)
        self.image_label.image = self.display_tk

    def query_superpixel(self, event):
        """
        DO DOCSTRING
        """
        current = self.xy_coords.get()
        self.xy_coords.delete(0, len(current) + 1)
        self.xy_coords.insert(0, f"{event.x}, {event.y}")
        self.region_coords.delete(0, len(current) + 1)
        chosen_region = self.superpixels[event.y, event.x]
        self.region_coords.insert(0, str(chosen_region))
        return chosen_region

    def add_region(self, event):
        """
        Adds a superpixel to the segmentation.
        """
        chosen_region = self.query_superpixel(event)
        for i in range(3):
            self.mask[:, :, i] = _np.where(self.superpixels == chosen_region, 255, 0)
            self.display_image[:, :, i] = _np.where(self.mask[:, :, i] == 255, 255, self.display_image[:, :, i])
        self.update_image(self.display_image)

    def remove_region(self, event):
        """
        Removes a superpixel from the segmentation.
        """
        chosen_region = self.query_superpixel(event)
        for i in range(3):
            self.mask[:, :, i] = _np.where(self.superpixels == chosen_region, 255, 0)
            self.display_image[:, :, i] = _np.where(self.mask[:, :, i] == 255, self.boundaries[:, :, i],
                                                    self.display_image[:, :, i])
        self.update_image(self.display_image)