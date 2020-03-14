import setuptools

with open('requirements.txt', 'r') as fc:
    requirements = [line.strip() for line in fc]

setuptools.setup(
    name='pypiepi',
    version='1.0.1',
    author='Trevor Lancon',
    description='A library for everything you need to simulate pi on pictures of pies in Python.',
    long_description='A library for everything you need to simulate pi on pictures of pies in Python.',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
    install_requires=requirements
)
