# PythonAutoNifty

## Purpose
- Nifty Ink website (https://nifty.ink) allows you to create NFTs using a Microsoft-Paint-like tool, and mint the NFTs on the xDai blockchain
- This Python3 code allows you to automatically generate drawing instructions for Nifty Ink website
- This code can generate more complex and accurate patterns than it is possible to do by hand
- Your Nifty Ink NFTs may look better!

## Instructions
- Check your Python3 environment is set up correctly (see below)
- Edit `main.py` file to draw something nice (see examples for inspiration)
- Run: `python3 main.py`
- Output file `output.txt` is created
- Open this file, copy the text
- Go to https://nifty.ink
- Hit `Create` button
- Open Developer Console in web browser
- Paste the text from `output.txt` into the console, hit Enter
- Nifty.Ink website should draw something nice

## Set up Python virtualenv

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

## Credits
- Original code by `Markichu`
- Contributions from `davidryan59` (aka `niftymaestro`) and `EL-S`
- Thanks to the developers behind Nifty Ink website