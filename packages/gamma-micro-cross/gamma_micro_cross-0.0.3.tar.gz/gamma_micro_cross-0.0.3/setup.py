import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "gamma_micro_cross",
    version = "0.0.3",
    author = "Albert_Wu",
    author_email = "wulf16@mails.tsinghua.edu.cn",
    description = "A python programm for getting gamma cross section",
    long_description_content_type = "text/markdown",
    url = "https://github.com/AlbertWulf",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3 ",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)