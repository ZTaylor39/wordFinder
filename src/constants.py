from enum import Enum

# Scrabble dictionary paths
SCRABBLE_DICTIONARY_PATH = "../libs/scrabbleDictionary/dictionary.txt"
DEFAULT_SCRABBLE_DICTIONARY_PATH = "../defaultDictionaries/defaultScrabbleDictionary.txt"

# WWF dictionary paths
# TODO: Update with actual WWF dictionary path when available
WWF_DICTIONARY_PATH = DEFAULT_SCRABBLE_DICTIONARY_PATH
DEFAULT_WWF_DICTIONARY_PATH = DEFAULT_SCRABBLE_DICTIONARY_PATH

# Character representing a blank tile
# Not much reason to change this from a single space character
BLANK_INDICATOR = " "

# Game modes
class Mode(Enum):
    SCRABBLE = "scrabble"
    WWF = "wwf"
    
DEFAULT_MODE = Mode.WWF