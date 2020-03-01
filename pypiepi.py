import numpy as np
from scipy.ndimage import binary_fill_holes
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.util import img_as_ubyte
from skimage.draw import circle_perimeter
from skimage.feature import canny
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.morphology import disk, binary_erosion, binary_dilation, watershed
from skimage.filters.rank import median, gradient
from skimage.segmentation import join_segmentations

test_image = np.array([[0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 4, 2, 0, 0],
                       [0, 2, 6, 5, 6, 0],
                       [0, 0, 3, 2, 0, 0]])


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

    input_image = img_as_ubyte(rgb2gray(imread(image)))
    mask = np.zeros(shape=input_image.shape, dtype=np.uint8)
    radii = np.arange(radius - radius_width, radius + radius_width, 5)
    # high_threshold hard-coded to 100 since ubyte type is enforced:
    edge_image = canny(input_image, sigma=edge_size, high_threshold=100)
    hough_result = hough_circle(edge_image, radii)
    peak, cx, cy, r = hough_circle_peaks(hough_result, radii, num_peaks=1, total_num_peaks=1, normalize=True)
    # cx, cy, and r are returned as arrays, but circle_perimeter requires ints:
    cy, cx, r = map(int, [cy, cx, r])
    rr, cc = circle_perimeter(cy, cx, r, shape=input_image.shape)
    mask[rr, cc] = 1
    mask = binary_fill_holes(mask)
    inside_seed = binary_erosion(mask, disk(2*radius_width))
    outside_seed = ~binary_dilation(mask, disk(2*radius_width))
    seeds = (inside_seed + 2*outside_seed).astype(np.uint8)
    # separate seeds are no longer needed and are best removed here to save memory in case of a large image
    del inside_seed, outside_seed
    gradient_image = gradient(median(input_image, disk(edge_size)), disk(edge_size))
    segmentation = np.where(watershed(gradient_image, seeds) == 1, 1, 0).astype(np.uint8)
    return segmentation

    # TODO Test using gradient image instead of Canny to save a computation
    # TODO Attempt to parallelize hough_circle


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

    xbounds = np.where(mask.any(axis=1))[0]
    xmin = np.min(xbounds)
    xmax = np.max(xbounds)

    ybounds = np.where(mask.any(axis=0))[0]
    ymin = np.min(ybounds)
    ymax = np.max(ybounds)

    return mask[xmin:xmax+1, ymin:ymax+1]

    # TODO Add optional "square" parameter, make compatible with 3D arrays, then submit to scikit-image


def simulate_pi(mask, export_image=False):
    """
    Calculates pie-ness by simulating pi on a 2D mask.

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

    rand_array = np.zeros(shape=(x_len, y_len),dtype=np.uint8)
    rand_array[:, :] = (np.random.randint(low=0, high=255, size=(x_len, y_len)) >= 128).astype(np.uint8)

    result = join_segmentations(rand_array, mask)

    points_inside_pie = np.count_nonzero((result == 3).astype(np.uint8))
    total_points = np.count_nonzero(rand_array.astype(np.uint8))
    calculated_pi = (float(points_inside_pie) / total_points) * 4

    return calculated_pi

    # TODO Optionally return image showing hits/non-hits

# TODO Handle cases where wedge is cut from pie
# TODO Make tests
# TODO Explore possibility to segment using morphological closing/filling of the Canny image
# TODO Add algorithm to simulate pi using small packets of "darts" until convergence
