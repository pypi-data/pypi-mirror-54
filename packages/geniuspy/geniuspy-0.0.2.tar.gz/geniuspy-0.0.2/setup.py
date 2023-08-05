import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geniuspy",
    version="0.0.2",
    author="Rafael Sánchez Sánchez",
    author_email="lletfrix@gmail.com",
    description="A Python wrapper around the Genius API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lletfrix/geniuspy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
