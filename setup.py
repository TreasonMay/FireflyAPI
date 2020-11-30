import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FireflyAPI",
    version="0.0.1",
    author="TreasonMay",
    author_email="55131032+TreasonMay@users.noreply.github.com",
    description="An API for interacting withe Firefly Learning systems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TreasonMay/FireflyAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)