import io
import os

from setuptools import setup, find_packages


with io.open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
) as f:
    long_description = f.read()

setup(
    name="piopiy",
    version="1.0.7.1",
    description="PIOPIY SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/telecmi/piopiy_python",
    author="PIOPIY",
    author_email="support@telecmi.com",
    license="MIT",
    packages=find_packages(),
    platforms=["any"],
    install_requires=['requests==2.32.3'],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
