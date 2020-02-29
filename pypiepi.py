import numpy as np
from skimage.segmentation import join_segmentations

test_image = np.array([[0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 4, 2, 0, 0],
                       [0, 2, 6, 5, 6, 0],
                       [0, 0, 3, 2, 0, 0]])


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


def simulate_pi(mask):
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

# TODO Return image showing hits/non-hits
# TODO Create companion function to segment pie
# TODO Force 2D, 8bit, single channel arrays for masks, or define logic to handle them
