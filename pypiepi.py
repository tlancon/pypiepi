import numpy as np
from skimage.segmentation import join_segmentations


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
        calculated value of pi
    """

    x_len, y_len = mask.shape

    rand_array = np.zeros(shape=(x_len, y_len),dtype=np.uint8)
    rand_array[:, :] = (np.random.randint(low=0, high=255, size=(x_len, y_len)) >= 128).astype(np.uint8)

    result = join_segmentations(rand_array, mask)

    points_inside_pie = np.count_nonzero((result == 3).astype(np.uint8))
    total_points = np.count_nonzero(rand_array.astype(np.uint8))
    calculated_pi = (float(points_inside_pie) / total_points) * 4

    return calculated_pi

# TODO def auto_crop(mask):
# TODO Return image showing hits/non-hits
# TODO Create companion function to segment pie
