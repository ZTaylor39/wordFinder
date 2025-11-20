from constants import *

def getWords(filepath) -> set:
    validWords = set() # Prevent duplicates
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip() # Remove whitespace characters
            if word:
                validWords.add(word.upper())
    
    return validWords

try:
    scrabbleWords = getWords(SCRABBLE_DICTIONARY_PATH)
except FileNotFoundError:
    scrabbleWords = getWords(DEFAULT_SCRABBLE_DICTIONARY_PATH)

try:
    wwfWords = getWords(WWF_DICTIONARY_PATH)
except FileNotFoundError:
    wwfWords = getWords(DEFAULT_WWF_DICTIONARY_PATH)

def getAllValidWords(mode: Mode = DEFAULT_MODE) -> set:
    """Returns the set of valid words based on the game mode."""
    if mode == Mode.SCRABBLE:
        return scrabbleWords
    return wwfWords

def getNumValidWords(mode: Mode = DEFAULT_MODE) -> int:
    """Returns the number of valid words based on the game mode."""
    return len(getAllValidWords(mode))

def isWordValid(word: str, mode: Mode = DEFAULT_MODE) -> bool:
    """Checks if a word is valid based on the game mode."""
    if mode == Mode.SCRABBLE:
        return word.upper() in scrabbleWords
    return word.upper() in wwfWords