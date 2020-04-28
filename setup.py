import setuptools

from drftmpl import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="drftmpl",
    version=__version__,
    author="Mikele",
    author_email="blive200@gmail.com",
    description="Generate rest framework templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toyourheart163/drftmpl",
    install_requires=["jinja2"],
    packages=["drftmpl/templates"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/drftmpl'],
    python_requires='>=3.6',
)
