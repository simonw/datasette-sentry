from setuptools import setup
import os

VERSION = "0.3"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-sentry",
    description="Datasette plugin for configuring Sentry",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-sentry",
    license="Apache License, Version 2.0",
    version=VERSION,
    entry_points={"datasette": ["sentry = datasette_sentry"]},
    py_modules=["datasette_sentry"],
    install_requires=["sentry-sdk", "datasette>=0.62"],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
