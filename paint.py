import tkinter as tk
import numpy as np
from PIL import ImageTk, Image
from skimage.io import imread
from skimage.segmentation import slic, mark_boundaries, flood_fill
from skimage.util import img_as_ubyte


class PaintThePie:
    """
    An app that the user can use to manually paint their object by dragging their mouse across SLIC superpixels.

    Attributes
    ----------
    input_image : str
        String representing path to the image to segment.

    superpixels : (N, M) array
        Label image containing computed superpixels.

    boundaries : (N, M, 3) array
        RGB image showing the boundaries of the superpixels superimposed with input_image.

    mask : (N, M, 3) array
        RGB image containing the user's selection.

    display_image : (N, M, 3) array
        RGB image showing composite of the input_image, superpixel boundaries, and the mask.

    """
    def __init__(self, master, image_path):
        self.master = master

        self.input_image = imread(image_path)
        max_segments = int(0.01 * (self.input_image.shape[0] * self.input_image.shape[1]))

        user_instructions = 'Drag left mouse button to paint superpixels. Drag right mouse button to erase. ' \
                            'Middle click to fill a contour. Close the app when finished.'
        self.instructions = tk.Label(master, text=user_instructions)
        self.instructions.grid(row=0, column=1, sticky=tk.NW)

        self.segments = tk.Scale(master, label='Segments', orient=tk.VERTICAL, from_=10, to=max_segments, resolution=1)
        self.segments.set(300)
        self.segments.grid(row=1, column=0, sticky=tk.W)

        self.compactness = tk.Scale(master, label='Compactness', orient=tk.VERTICAL, from_=0.01, to=100,
                                    resolution=0.01)
        self.compactness.set(20)
        self.compactness.grid(row=2, column=0, sticky=tk.W)

        self.clear = tk.Button(master, text='Clear', command=self.clear_mask)
        self.clear.grid(row=3, column=0, sticky=tk.S)

        self.image_label = tk.Label(master)
        self.image_label.grid(row=1, column=1, rowspan=3)

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
        Updates the app's displayed image.
        """
        self.display_tk = ImageTk.PhotoImage(Image.fromarray(self.display_image))
        self.image_label.configure(image=self.display_tk)
        self.image_label.image = self.display_tk

    def clear_mask(self):
        """
        Clears the mask and updates the app's displayed image.
        """
        self.mask = np.zeros_like(self.boundaries)
        self.display_image = np.copy(self.boundaries)
        self.update_image()

    def update_superpixels(self, event):
        """
        Recomputes superpixels with the user's selected parameters and displays the boundary image in the app.
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
        Adds superpixels to the segmentation by dragging the left mouse button.
        """
        if event.widget is self.image_label:
            chosen_region = self.superpixels[event.y, event.x]
            for i in range(3):
                self.mask[:, :, i] = np.where(self.superpixels == chosen_region, 255, self.mask[:, :, i])
                self.display_image[:, :, i] = np.where(self.mask[:, :, i] == 255, 255, self.display_image[:, :, i])
            self.update_image()

    def remove_region(self, event):
        """
        Removes superpixels from the segmentation by dragging the right mouse button.
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
        Fills a contour selected by the middle mouse button with the mask.
        """
        if event.widget is self.image_label:
            for i in range(3):
                self.mask[:, :, i] = flood_fill(self.mask[:, :, i], seed_point=(event.y, event.x), new_value=255,
                                                tolerance=1)
                self.display_image[:, :, i] = np.where(self.mask[:, :, i] == 255, 255, self.display_image[:, :, i])
            self.update_image()