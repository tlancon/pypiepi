# pypiepi

## Summary

A library for everything you need to simulate pi on pictures of pies in Python.

## Examples

For a perfect circle, we can simulate pi by plotting points inside a unit circle inscribed within a square and counting 
the ratio of points that fall within/without the circle. This ratio is related to pi by solving the relationship between
the area of the circle and the area of the square. See this
[GeeksforGeeks](https://www.geeksforgeeks.org/estimating-value-pi-using-monte-carlo/) article for an overview of the
algorithm.

Actual pies are rarely perfect circles since the dough is pinched, typically in a pattern, all around the circumference.
This pinching is also sometimes exaggerated when the pie is baked and those edges get all delicious and crispy.

Let's use pypiepi to test how pi-like and an actual pie is! Consider the example using `data/pi-pie.jpg`:

![A pi pie.](data/pi-pie.jpg)

1. Download and unzip the project to a directory, and with a terminal or CMD window inside that directory, install using
pip:

    `pip install .`

2. Import the package into a Python console:

    `import pypiepi as ppp`

3. 

## Attributions
- All images in data/ are from [Pixabay](https://pixabay.com) and are part of the [public domain](https://pixabay.com/service/license/).
    - pi-pie.jpg: Image by [Andrew Martin](https://pixabay.com/users/aitoff-388338)
    - cherry-pie.jpg: Image by [skeeze](https://pixabay.com/users/skeeze-272447)
    - oblique-cake.jpg: Image by [俊哉 佐伯](https://pixabay.com/users/la-fontaine-22289)
    - gold-coin.jpg: Image by [Tim C. Gundert](https://pixabay.com/users/timcgundert-3157574)
