import numpy as _np
import tkinter as tk
from skimage.util import img_as_ubyte as _img_as_ubyte
from skimage.color import rgb2gray as _rgb2gray
from skimage.io import imread as _imread
from skimage.feature import canny as _canny
from skimage.transform import hough_circle as _hough_circle
from skimage.transform import hough_circle_peaks as _hough_circle_peaks
from skimage.draw import circle as _circle
from skimage.morphology import disk as _disk
from skimage.morphology import watershed as _watershed
from skimage.filters.rank import median as _median
from skimage.filters.rank import gradient as _gradient
from skimage.segmentation import join_segmentations as _join_segmentations
from measure import MeasureRadiusApp


def measure_radius(image):
    """
    Calls the MeasureRadiusApp window for the user to interactively determine radius of an object.

    Parameters
    ---------
    image : string
        Path to the image.
    """
    root = tk.Tk()
    root.title('Measure Radius')
    MeasureRadiusApp(root, image_path=image)
    root.mainloop()


def hough_seeded_watershed(image, radius, radius_width, edge_size=3):
    """
    Performs a high-level combination of the Hough transform and watershed to segment the true edge of the most
    prominent circular object in an image.

    Approximate the radius of the object you wish to segment (in pixels) for the "radius" parameter. The "radius_width"
    parameter is the approximate error in that radius. For example, your thought process might be as follows:

    1. It looks like the circular object is about 650 pixels in diameter,
    2. so a radius of about 325 should work, but
        2a. it looks like the edge of the object is a bit wavy, so the radius varies by about 50 pixels
        OR
        2b. it looks like the object is elliptical and the radius may be up to about 50 less than 325 at some angles,
    3. so I will use a "radius_width" of 50.

    The algorithm would then look for 5 different radii between (325-50) and (325+50) and return the most appropriate
    one. Therefore, your radius estimation does not need to be exact, and the algorithm aims to be robust despite
    some error in this approximation.

    "edge_size" probably does not need to change for most cases, but can be increased from 3 for higher resolution
    images, and decreased for lower resolution images.

    Attributes
    ----------
    image : string
        Filepath to the image of a circular object.

    radius : int
        Estimated radius of the object in pixels.

    radius_width : int
        Width of the edge of the object in pixels (you are recommended to overestimate this somewhat).

    edge_size : int
        Size in pixels used for smoothing, edge detection, and morphological structuring elements.

    Returns
    -------
    (N, M) array
        Binary segmentation of the circular object.
    """

    input_image = _img_as_ubyte(_rgb2gray(_imread(image)))
    inside_seed = _np.zeros(shape=input_image.shape, dtype=_np.uint8)
    outside_seed = _np.zeros(shape=input_image.shape, dtype=_np.uint8)
    radii = _np.arange(radius - radius_width, radius + radius_width, 5)
    gradient_disk = _disk(edge_size)

    # high_threshold hard-coded to 100 since ubyte type is enforced:
    edge_image = _canny(input_image, sigma=edge_size, high_threshold=100)

    hough_result = _hough_circle(edge_image, radii)
    peak, cx, cy, r = _hough_circle_peaks(hough_result, radii, num_peaks=1, total_num_peaks=1, normalize=True)
    # cx, cy, and r are returned as arrays, but circle_perimeter requires ints:
    cy, cx, r = map(int, [cy, cx, r])

    rr, cc = _circle(cy, cx, r-int(radius_width/2), shape=input_image.shape)
    inside_seed[rr, cc] = 1

    rr, cc = _circle(cy, cx, r + int(radius_width / 2), shape=input_image.shape)
    outside_seed[rr, cc] = 1
    outside_seed = _np.logical_not(outside_seed)

    seeds = (inside_seed + 2*outside_seed).astype(_np.uint8)
    # separate seeds are no longer needed and are best removed here to save memory in case of a large image
    del inside_seed, outside_seed

    gradient_image = _gradient(_median(input_image, gradient_disk), gradient_disk)
    segmentation = _np.where(_watershed(gradient_image, seeds) == 1, 1, 0).astype(_np.uint8)

    return segmentation


def auto_crop(mask):
    """
    Removes columns and rows of zeros inward from the bounding box until values are reached. For a binary image, this
    results in the smallest possible bounding box containing the labeled pixels.

    Attributes
    ----------
    mask : (N, M) array
        2D array of mask of pie.

    Returns
    -------
    (N, M) array
        Cropped image
    """

    xbounds = _np.where(mask.any(axis=1))[0]
    xmin = _np.min(xbounds)
    xmax = _np.max(xbounds)

    ybounds = _np.where(mask.any(axis=0))[0]
    ymin = _np.min(ybounds)
    ymax = _np.max(ybounds)

    return mask[xmin:xmax+1, ymin:ymax+1]


def calculate_pi(mask, export_image=False):
    """
    Calculates circularity of an object by simulating pi on its mask. Ideal circles will return values close to 3.14etc.

    Attributes
    ----------
    mask : (N, M) array
        Binary, 2D array of mask of pie.

    Returns
    -------
    float
        Calculated value of pi
    """

    x_len, y_len = mask.shape

    rand_array = _np.zeros(shape=(x_len, y_len), dtype=_np.uint8)
    rand_array[:, :] = (_np.random.randint(low=0, high=255, size=(x_len, y_len)) >= 128).astype(_np.uint8)

    result = _join_segmentations(rand_array, mask)

    points_inside_pie = _np.count_nonzero((result == 3).astype(_np.uint8))
    total_points = _np.count_nonzero(rand_array.astype(_np.uint8))
    calculated_pi = (float(points_inside_pie) / total_points) * 4

    return calculated_pi


class SimulatePi:
    """
    Perform a converging simulation of pi.
    """
    def __init__(self, mask=None, histories=314, criterion=0.0314, verbose=True):
        self.mask = mask
        self.simulation_image = None
        self.max_histories = histories
        self.convergence_criterion = criterion
        self.verbose = verbose
        self.simulated_pi = None
        self.convergence_history = _np.array([])
        self.pi_history = _np.array([])

    def run(self):
        """
        DO DOCSTRING
        """
        if self.mask is None:
            return 'Please set SimulatePi.mask to the binary image on which to simulate pi.'

        x_len, y_len = self.mask.shape

        self.simulation_image = _np.copy(self.mask)

        convergence = 314
        histories = 0
        hits = 0
        self.verbosity_print("History | Convergence | pi")
        while convergence > self.convergence_criterion and histories < self.max_histories:
            dart_x = _np.random.randint(0, x_len)
            dart_y = _np.random.randint(0, y_len)
            if self.mask[dart_x, dart_y] == 1:
                hits += 1
                self.simulation_image[dart_x, dart_y] = 2
            else:
                self.simulation_image[dart_x, dart_y] = 3
            histories += 1
            self.simulated_pi = (float(hits) / histories) * 4
            convergence = abs(_np.pi - self.simulated_pi)
            self.convergence_history = _np.append(self.convergence_history, convergence)
            self.pi_history = _np.append(self.pi_history, self.simulated_pi)
            self.verbosity_print(f"{histories} | {convergence} | {self.simulated_pi}")

    def verbosity_print(self, message):
        if self.verbose is True:
            print(message)
