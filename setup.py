import setuptools
from botw.__version__ import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="botw-utils",
    version=VERSION,
    author="NiceneNerd",
    author_email="macadamiadaze@gmail.com",
    description="Library containing various utilities for modding The Legend of Zelda: Breath of the Wild",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NiceneNerd/botw-utils",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "License :: Public Domain",
        "Topic :: Software Development :: Libraries",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires='>=3.6',
)