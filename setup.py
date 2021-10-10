import setuptools
import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PipeRT",
    version=get_version("pipert2/__init__.py"),
    author="digitalTevel",
    author_email="digitalTevel@gmail.com",
    description="Real-time pipeline 4 analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OperationalBina/PipeRT2",
    project_urls={
        "Bug Tracker": "https://github.com/OperationalBina/PipeRT2/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=["posix-ipc", "numpy"],
    python_requires=">=3.6",
)
