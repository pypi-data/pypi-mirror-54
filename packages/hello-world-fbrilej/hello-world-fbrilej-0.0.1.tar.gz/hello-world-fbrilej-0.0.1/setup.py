import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    required = fh.read().splitlines()

setuptools.setup(
    name="hello-world-fbrilej",
    version="0.0.1",
    author="Felix Brilej",
    author_email="felix.brilej@smaato.com",
    description="A hello world package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smaato",

    include_package_data=True,
    package_data = {
        'data': ['index.html']
    },

    packages=setuptools.find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
