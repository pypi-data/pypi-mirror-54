#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["matplotlib>=3.1.0"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Andrei Berceanu",
    author_email="andreicberceanu@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 3.6",
    ],
    description="thin wrapper on top of matplotlib's imshow for 2D plotting with attached slice plots",
    install_requires=requirements,
    python_requires=">= 3.6",
    license="BSD license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="slice plot plotting",
    name="sliceplots",
    packages=find_packages(include=["sliceplots"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/berceanu/sliceplots",
    version="0.3.2",
    zip_safe=False,
)
