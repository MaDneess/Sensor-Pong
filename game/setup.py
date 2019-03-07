
from setuptools import setup

with open("README.md") as f:
    long_desc = f.read()

setup(
    name="SensorPong",
    version="1.2",
    description="Ping-Pong Game Controlled By Sensors",
    long_description=long_desc,
    author="Aleksej Zaicev",
    author_email="alex.zaicef@gmail.com",
    install_requires=["pyserial", "pygame"]
)