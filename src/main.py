from tile import *
from valid_words import *
from constants import *

import itertools
import re
import sys
import time
import math


class WordResult:
    """A class representing a valid word result found from the rack & board and its associated score. 
    Used for sorting and displaying results.
    Letters in the word are case-sensitive, with uppercase letters representing normal tiles and lowercase letters representing blank tiles.
    """
    def __init__(self, word: str, mode: Mode = DEFAULT_MODE):
        self.word = word
        self.value = getWordScore(word, mode)
        self.length = sum(1 for c in word if c.isalpha())

    def __lt__(self, other) -> bool:
        """Sorts primarily by word score (descending), then alphabetically (ascending) if word scores are equal."""
        if self.value == other.value:
            return self.word.upper() < other.word.upper()
        
        return self.value > other.value

    def __repr__(self) -> str:
        """String representation of the WordResult in the format: WORD - SCORE"""
        return f"{self.word} - {self.value}"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, WordResult):
            return [l for l in self.word if l.isalpha()] == [l for l in other.word if l.isalpha()]
        return False

    def __hash__(self) -> int:
        return hash(self.__repr__())
    

def extractAlphaFromRegex(boardRegex: str) -> list:
    """Extracts all alphabetic characters from a board regex, ignoring escaped characters. Returns them as a string."""
    output = []
    for index, char in enumerate(boardRegex):
        if char.isalpha() and (index == 0 or boardRegex[index-1] != "\\"):
            output.append("(" + char + ")")
    return output

def wordFitsRegex(word: str, boardRegex: str) -> bool:
    """Checks if a word fits the given board regex in general and in specific placement of board letters."""
    if not re.search(boardRegex, word.replace("(", "").replace(")", "")):
        return False
        
    dumbRegex = boardRegex.replace("\\w", " ")
    dumbWord = ""
    letterComesFromBoard = False
    for letter in word:
        if letter == "(":
            letterComesFromBoard = True
        elif letter == ")":
            letterComesFromBoard = False
        elif letterComesFromBoard:
            dumbWord += letter
        else :
            dumbWord += " "
    return re.search(dumbRegex, dumbWord) is not None

def getWordsByIteratingOverRacks(rack: str, boardRegex: str = "", mode: Mode = DEFAULT_MODE) -> set:
    """
    Finds words by generating all possible permutations of the rack + letters from the board regex, 
    then filtering them based on validity and board regex matching.
    """

    print("Iterating over words on rack")

    # TODO: Optimize this to avoid generating duplicate permutations when there are duplicate letters on the rack
    # TODO: Optimize this to avoid generating permutations that don't match the board regex (whether by length or fixed letter positions)
    # Generate all possible permutations of the rack + fixed letters from the board regex
    playableWords = [''.join(p) for r in range(1, len(rack)+len(extractAlphaFromRegex(boardRegex))+1) for p in itertools.permutations(list(rack)+extractAlphaFromRegex(boardRegex), r)]    

    # Remove permutations that are not valid words or don't match the board regex
    validPlayableWords = set([WordResult(word.replace(")(", ""), mode) for word in playableWords if isWordValid(word, mode) and wordFitsRegex(word, boardRegex)])

    return validPlayableWords


def iter_overlapping_regex_matches(boardRegex, word):
    """
    Yield overlapping matches of boardRegex in the string word.
    """
    pattern = re.compile(boardRegex)
    pos = 0
    while True:
        m = pattern.search(word, pos)
        if not m:
            break
        yield m
        pos = m.start() + 1   # advance only 1 char for overlaps

def wordFromRack(validWord: str, rack: str, boardRegex: str) -> list:
    """
    Checks if a valid word can be formed from the given rack and number of blanks.
    Returns a list of ways to represent the word with tiles on rack and board.
    """
    
    # Ensure the word can be formed from the rack + board letters
    workingRack = list(rack)+[l[1:-1] for l in extractAlphaFromRegex(boardRegex)]
    numBlanks = workingRack.count(BLANK_INDICATOR)
    output = ""
    remainingBlanks = numBlanks
    for letter in validWord:
        if letter in workingRack:
            workingRack.remove(letter)
            output += letter
        else:
            if remainingBlanks > 0:
                remainingBlanks -= 1
                output += letter.lower()
            else:
                return []

    # If there are multiple ways to place the word on the board, return them all
    outputs = []
    for playPosition in iter_overlapping_regex_matches(boardRegex, validWord):
        outputs.append(output[:playPosition.start()] + "(" + playPosition.group() + ")" + output[playPosition.end():])

    return outputs

def getWordsByIteratingOverValidWords(rack: str, boardRegex: str = "", mode: Mode = DEFAULT_MODE) -> set:
    """
    Finds words by iterating over all valid words in the dictionary that match the board regex,
    and then checking if they can be formed from the rack + letters from the board regex.
    """

    print("Iterating over valid words")

    output = set()
    for word in getAllValidWords(mode):
        # Skip words that wouldn't fit in the board constraints
        if not re.search(boardRegex, word):
            continue

        # Check if the word can be formed from the rack + board letters
        for word in wordFromRack(word, rack, boardRegex):
            output.add(WordResult(word, mode))

    return output


def getNumWordsOnRack(rack: str, boardRegex: str = "") -> int:
    """
    Estimates the number of possible words that can be formed from the given rack and board regex.
    """

    numBlanks = rack.count(BLANK_INDICATOR)
    numAlpha = len(rack)+len(extractAlphaFromRegex(boardRegex)) - numBlanks 

    total = 0
    for i in range(1, numAlpha+1):
        for j in range(0, numBlanks+1):
            total += 26**j * math.factorial(i+j) * math.comb(numAlpha, i) * math.comb(numBlanks, j)
    
    return total


def findWords(rack: str, boardRegex: str = "", mode: Mode = DEFAULT_MODE) -> list:
    """
    Finds all valid words that can be formed from the given rack and board regex, based on the game mode.
    Chooses the optimal method (rack iteration or valid words iteration) based on estimated number of words.
    Returns a sorted list of WordResult objects.
    """

    if getNumWordsOnRack(rack, boardRegex) < getNumValidWords(mode):
        # Use rack iteration method
        
        blank_index = rack.find(BLANK_INDICATOR)
        if blank_index == -1:
            # No blank found
            return sorted(getWordsByIteratingOverRacks(rack, boardRegex, mode))

    
        # Get racks for all values of blank
        output = set()
        for i in range(97, 97+26): # iterates over lowercase letters
            newRack = rack[:blank_index] + chr(i) + rack[blank_index+1:]
            output.update(findWords(newRack, boardRegex, mode))
                
        return sorted(output)
    
    else:
        # Use valid words iteration method
        return sorted(getWordsByIteratingOverValidWords(rack, boardRegex, mode))
    

def main(rawRack: str, rawBoardRegex: str = "", rawMode: str = DEFAULT_MODE.value):
    """Command line arguments: rack, board regex (optional), mode (optional, "scrabble" or "wwf")"""

    # Replace "_" and "?" with blank indicator for easier input
    rack = str.replace(str.replace(rawRack, "_", BLANK_INDICATOR), "?", BLANK_INDICATOR).upper()

    # Sanitize board regex input
    boardRegex = ""
    boardRegex = str.replace(rawBoardRegex, " ", "\w")
    if boardRegex.startswith("\\w"):
        boardRegex = "^" + boardRegex
    if boardRegex.endswith("\\w") or boardRegex.endswith("}"):
        boardRegex += "$"

    # Set mode
    mode = Mode(rawMode.lower())

    t0 = time.time()
    results = findWords(rack, boardRegex, mode)
    t1 = time.time()

    result_limit = 100
    for result in results[:result_limit]:
        print(result)
    print(f"{min(result_limit, len(results))} of {len(results)} results shown in {t1 - t0:.4f} seconds.")


if __name__ == "__main__":
    main(*sys.argv[1:])