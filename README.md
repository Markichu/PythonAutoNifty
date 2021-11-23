# PythonAutoNifty

## Installation

pyautonifty is available from PyPI:

``` sh
pip install --upgrade pyautonifty
```

## Purpose
- Nifty.Ink (https://nifty.ink) allows you to create NFTs using a Microsoft-Paint-like tool, and mint the NFTs on the xDai blockchain
- This Python3 code allows you to automatically generate drawing instructions for Nifty.Ink
- This code can generate more complex and accurate patterns than it is possible to do by hand
- Your Nifty Ink NFTs may look better!

## Instructions
- Check your Python3 environment is set up correctly (see below)
- Run: `pip install pyautonifty`
- Edit `main.py` file to draw something nice (see examples for inspiration) or create your own file
- Run: `python3 main.py`
- Output file `output.txt` is created
- Open this file, copy the text
- Go to https://nifty.ink
- Hit `Create` button
- Open Developer Console in web browser
- Paste the text from `output.txt` into the console, hit Enter
- Nifty.Ink should draw something nice!

## Set up a Python virtualenv

Set up and activate the env in your local PythonAutoNifty folder, so this project dependencies are separate from your other projects:

``` sh
python3 -m venv ~/.virtualenvs/PythonAutoNifty
source ~/.virtualenvs/PythonAutoNifty/bin/activate
pip3 install -r requirements.txt
pip3 list
```

Deactivate the env:

``` sh
deactivate
```

## Development Environment
- Clone this repo
- Setup a virtual environment if you prefer
- Run: `pip3 install -r requirements.txt`
- Create a branch or fork the repository if you do not have permissions
- Make edits to the repo (usually in the pyautonifty directory)
- Create a pull request
- Get a review + approval from another contributor
- Squash and merge typically
- Run: `py -m pip install --upgrade build`
- Run: `py -m build`
- Your freshly built .whl will be in the dist directory!

## Credits
- Original code by `Markichu`
- Contributions from `davidryan59` (aka `niftymaestro`) and `EL-S`
- Thanks to the developers behind Nifty Ink website
