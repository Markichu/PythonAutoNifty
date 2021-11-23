import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyautonifty",
    version="0.0.1",
    author="Markichu, Davidryan59, EL-S",
    author_email="EL.S13337@gmail.com",
    description="Automatically and programmatically generate drawing instructions for Nifty.Ink",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Markichu/PythonAutoNifty",
    project_urls={
        "Bug Tracker": "https://github.com/Markichu/PythonAutoNifty/issues",
    },
    keywords = ["nifty.ink", "NFT", "drawing"],
    install_requires=[
        "fonttools==4.28.2",
        "numpy==1.21.4",
        "pygame==2.1.0",
        "scipy==1.7.2",
        "pillow==8.4.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
)