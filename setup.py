from setuptools import setup
from os import path

setup(
    name="tcp_logger",
    version="1.0.0",
    description="the tcp logger for ports",
    license="MIT",
    packages="tcp_logger",
    author="Synarcs",
    install_requires=[
        "socket",
        "requests",
        "nmap",
        "docopt",
        "python-nmap"
    ]
)
