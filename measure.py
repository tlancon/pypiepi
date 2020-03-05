import tkinter as tk
from PIL import ImageTk, Image


class MeasureRadiusApp:
    def __init__(self, master, image_path):
        self.master = master

        self.center_label = tk.Label(master, text='Center (left-click to select): ')
        self.center_label.grid(row=0, column=0, sticky=tk.E)

        self.center_coords = tk.Entry(master)
        self.center_coords.grid(row=0, column=1, sticky=tk.W)

        self.edge_label = tk.Label(master, text='Edge (right-click to select): ')
        self.edge_label.grid(row=0, column=2, sticky=tk.E)

        self.edge_coords = tk.Entry(master)
        self.edge_coords.grid(row=0, column=3, sticky=tk.W)

        self.radius_label = tk.Label(master, text='Radius: ')
        self.radius_label.grid(row=0, column=4, sticky=tk.E)

        self.radius_distance = tk.Entry(master)
        self.radius_distance.grid(row=0, column=5, sticky=tk.W)

        self.img = ImageTk.PhotoImage(Image.open(image_path))
        self.image_label = tk.Label(master, image=self.img)
        self.image_label.image = self.img
        self.image_label.grid(row=1, column=0, columnspan=8)

        master.bind("<Button-1>", self.set_center)
        master.bind("<Button-3>", self.set_edge)

    def set_center(self, event):
        """
        Sets the center coordinate of the Measure Radius app using a left click.
        """
        current = self.center_coords.get()
        self.center_coords.delete(0, len(current) + 1)
        self.center_coords.insert(0, f"{event.x}, {event.y}")
        self.set_radius()

    def set_edge(self, event):
        """
        Sets the edge coordinate of the Measure Radius app using a right click.
        """
        current = self.edge_coords.get()
        self.edge_coords.delete(0, len(current) + 1)
        self.edge_coords.insert(0, f"{event.x}, {event.y}")
        self.set_radius()

    def set_radius(self):
        """
        Automatically computes the distance between the center and edge coordinates if they are populated.
        """
        if self.center_coords.get() == '' or self.edge_coords.get() == '':
            pass
        else:
            current = self.radius_distance.get()
            p1 = tuple(map(int, self.center_coords.get().split(',')))
            p2 = tuple(map(int, self.edge_coords.get().split(',')))
            self.radius_distance.delete(0, len(current) + 1)
            self.radius_distance.insert(0, self.distance_2d(p1, p2))

    def distance_2d(self, p1, p2):
        """
        Calculates the Euclidean distance between two Cartesian points in 2D.

        Parameters
        ----------
        p1 : tuple or list
            Coordinates of the first point.

        p2 : tuple or list
            Coordinates of the second point.

        Returns
        -------
        float
            Euclidean distance between the two points.
        """
        return round(((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** (1 / 2), 2)
