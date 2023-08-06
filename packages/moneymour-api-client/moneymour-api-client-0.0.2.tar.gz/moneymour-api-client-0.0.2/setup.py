import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="moneymour-api-client",
    version="0.0.2",
    author="Antonio Trapani",
    author_email="antonio.trapani@gmail.com",
    description="The library offers easy access to Moneymour APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moneymour/api-client-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests',
        'pycrypto',
    ],
)
