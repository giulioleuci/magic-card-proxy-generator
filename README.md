# magic-card-proxy-generator
Magic: The Gathering card proxy generator written in Python.

Using APIs from https://scryfall.com/ this script generates proxy on A4 paper, ready for cut and play.

This script makes .pdf with nanDECK (https://www.nandeck.com/) made by Andrea “Nand” Nini

# Instructions

This script uses a `.xlsx` file with this columns:
- quantity: copies of card
- name: the name that this script search on Scryfall
- image: do not use

Launch this script with command similar to `python3 deck_generator.py -e cardlist.xlsx -n 60`.

Parameters:

`-e` Excel file with card infos.

`-n` total card to generate

`-f` not use in this version

In case of errors, this script prints a warning: you can manually correct the `.xlsx` updated file (and/or manually search for card images) and launch nanDECK.
