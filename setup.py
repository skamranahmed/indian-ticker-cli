import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ind-ticker",
    version="0.0.1",
    author="Syed Kamran Ahmed",
    author_email="syedkamranahmed14@gmail.com",
    description="CLI tool to get data of Indian Stocks and Mutual Funds",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    url="https://github.com/skamranahmed/indian-stocks-cli",
    packages=setuptools.find_packages(),    
    install_requires=[
        "click",
        "prettytable",
        "requests",
        "termcolor",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
    python_requires='>=3.7.0',
    license="MIT",
    entry_points="""
        [console_scripts]
        ind-ticker=ind_ticker.__main__:main
    """
)