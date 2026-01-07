import io
import os

from setuptools import setup, find_packages


with io.open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
) as f:
    long_description = f.read()

setup(
    name="piopiy",
    version="1.1.0",
    description="PIOPIY: Complete Voice AI Agent & CPaaS Platform SDK (Voice, Queue, Campaigns, WhatsApp, SMS)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/telecmi/piopiy_python",
    author="PIOPIY",
    author_email="support@telecmi.com",
    license="Apache 2.0",
    packages=find_packages(),
    platforms=["any"],
    install_requires=['requests==2.32.3'],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
