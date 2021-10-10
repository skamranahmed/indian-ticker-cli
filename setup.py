from setuptools import setup, find_packages
from io import open
from os import path

import pathlib

from ind_ticker.ind_ticker import version

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# automatically captured required modules for install_requires in requirements.txt
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

setup(
    name="ind-ticker",
    version=version,
    author="Syed Kamran Ahmed",
    author_email="syedkamranahmed14@gmail.com",
    description="CLI tool to get data of Indian Stocks and Mutual Funds",
    long_description=README,      
    long_description_content_type="text/markdown",
    url="https://github.com/skamranahmed/indian-ticker-cli",
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
    python_requires='>=3.7.0',
    license="MIT",
    entry_points="""
        [console_scripts]
        ind-ticker=ind_ticker.ind_ticker:main
    """,
    dependency_links=dependency_links
)