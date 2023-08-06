# -*- coding: utf-8 -*-

"""
To upload to PyPI, PyPI test, or a local server:
python setup.py bdist_wheel upload -r <server_identifier>
"""

import setuptools
import os

setuptools.setup(
    name="nionswift-experimental",
    version="0.6.0",
    author="Nion Software",
    author_email="swift@nion.com",
    description="Experimental tools package for Nion Swift.",
    packages=["nionswift_plugin.nion_experimental_tools", "nionswift_plugin.nion_experimental_4dtools"],
    install_requires=["nionswift>=0.14.0"],
    license='GPLv3',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
    ],
    include_package_data=True,
    python_requires='~=3.6',
    zip_safe=False,
)
