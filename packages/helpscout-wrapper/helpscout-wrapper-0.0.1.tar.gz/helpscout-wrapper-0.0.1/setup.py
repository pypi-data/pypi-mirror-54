import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="helpscout-wrapper",
    version="0.0.1",
    description="HelpScout api wrapper",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Gogen120/helpscout",
    author="Armand Kulsh",
    author_email="armand.kulsh@gmail.com",
    licence="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests"],
)
