"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
Modified by Madoshakalaka@Github (dependency links added)
"""

from setuptools import setup, find_packages
from os import path

from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bamboodle",
    version="0.1.0",
    description="Retrieve session cookies from a bamboohr session",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sw1nn/bamboodle",
    author="Neale Swinnerton",
    author_email="neale@sw1nn.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="bamboo",
    packages=find_packages(where="src", exclude=["contrib", "docs", "tests"]),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["bamboodle = bamboodle.cookie:main"]},
    python_requires=">=3.10",
    install_requires=[
        "async-generator==1.10",
        "attrs==22.2.0",
        "certifi==2022.12.7",
        "charset-normalizer==3.0.1",
        "h11==0.14.0",
        "idna==3.4",
        "outcome==1.2.0",
        "pexpect==4.8.0",
        "ptyprocess==0.7.0",
        "pysocks==1.7.1",
        "requests==2.28.2",
        "selenium==4.8.0",
        "sniffio==1.3.0",
        "sortedcontainers==2.4.0",
        "trio==0.22.0",
        "trio-websocket==0.9.2",
        "urllib3==1.26.14",
        "wsproto==1.2.0"
    ],
    extras_require={"dev": []},
    dependency_links=[],
    project_urls={
        "Bug Reports": "https://github.com/sw1nn/bamboodle/issues",
        "Funding": "https://donate.pypi.org",
        "Say Thanks!": "http://saythanks.io/to/example",
        "Source": "https://github.com/sw1nn/bamboodle/",
    },
)
