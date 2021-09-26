"""
enspired-tool setup file.
"""
from setuptools import find_packages, setup


setup(
    name="enspired-tool",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['enspired-tool=enspired.main:main']
    },
    author="Mohammed Bilal Ansari",
    author_email="mohammedbilalansari.official@gmail.com",
) 
