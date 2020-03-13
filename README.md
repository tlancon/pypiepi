# pypiepi

For Kathy

## Summary

A library for everything you need to simulate pi on pictures of pies in Python.

## Example

#### The Long Version

For a perfect circle, we can simulate pi by plotting it within a square such that width = height = diameter, then
counting  the ratio of points randomly distributed throughout the square that fall within/without the circle. This
ratio is related to pi by solving the relationship between the area of the circle and the area of the square. See [this
GeeksforGeeks](https://www.geeksforgeeks.org/estimating-value-pi-using-monte-carlo/) article for an overview of the
algorithm.

Actual pies are rarely perfect circles since the dough is pinched, typically in a pattern, all around the circumference.
This pinching is also sometimes exaggerated when the pie is baked and those edges get all delicious and crispy.

Let's use pypiepi to test how pi-like and an actual pie is! Consider the example using `data/pi-pie.jpg`:

![A pi pie.](data/pi-pie.jpg)

1. Download and unzip the project to a directory, and with a terminal or CMD window inside that directory, install using
pip:

        pip install .

2. Import the package into a Python console along with a function for displaying results:

        import pypiepi as ppp
        from skimage.io import imshow

3. You can either create a mask manually using your favorite segmentation editor, try to create it procedurally
yourself, or take advantage of the `segment_pie_auto()` function from pypiepi, as shown here:

        segmentation = ppp.segment_pie_auto('data/pi-pie.jpg', radius=600, radius_width=25)
        imshow(segmentation)

4. The result is that `segmentation` contains a binary Numpy array containing the mask of the pie. You will need to
adjust the radius and radius_width parameters for each image appropriately.

5. To prepare the mask for simulation, we need to crop the edges of the image as close as possible to the mask so that
our bounding box is as close as possible to a unit square (a key assumption of the algorithm):

        cropped = ppp.just_the_pie(segmentation)
        imshow(cropped)

6. After cropping, we are ready to simulate pi:

        ppp.calculate_pi(cropped)

7. For this image, the result is quite close - about 3.12!

#### TL;DR

1. Download from Github, unzip to a directory, then navigate to that directory in a terminal or CMD window:

        pip install .

2. Import pypiepi and segment, crop, then simulate using a picture of a pie:

        import pypiepi as ppp
        segmentation = ppp.segment_pie_auto('data/pi-pie.jpg', radius=600, radius_width=25)
        cropped = ppp.just_the_pie(segmentation)
        ppp.calculate_pi(cropped)

## Attributions
- All images in data/ are from [Pixabay](https://pixabay.com) and are part of the [public domain](https://pixabay.com/service/license/).
    - pi-pie.jpg: Image by [Andrew Martin](https://pixabay.com/users/aitoff-388338)
    - cherry-pie.jpg: Image by [skeeze](https://pixabay.com/users/skeeze-272447)
    - oblique-cake.jpg: Image by [俊哉 佐伯](https://pixabay.com/users/la-fontaine-22289)
    - gold-coin.jpg: Image by [Tim C. Gundert](https://pixabay.com/users/timcgundert-3157574)
