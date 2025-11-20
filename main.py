from tile import *
from valid_words import *
import itertools
import re
import sys
import time
import math

BLANK_INDICATOR = " "

class WordResult:
    def __init__(self, word, mode = "wwf"):
        self.word = word
        self.value = getWordScore(word, mode)
        self.length = len(word)

    def __lt__(self, other):
        if self.value == other.value:
            return self.word.upper() < other.word.upper()
        
        return self.value > other.value

    def __repr__(self):
        return f"{self.word} - {self.value}"
    
    def __eq__(self, other):
        if isinstance(other, WordResult):
            return self.word == other.word
        return False

    def __hash__(self):
        return hash(self.__repr__())
    

def getWordScore(word: str, mode = "wwf") -> int:
    value = 0
    for letter in word:
        if letter.isupper():
            value += tiles[letter].getValue(mode)
    return value

def validateWord(word: str, mode = "wwf") -> bool:
    if mode == "scrabble":
        return word.upper() in scrabbleWords
    return word.upper() in wwfWords

def extractAlphaFromRegex(boardRegex: str):
    output = ""
    for index, char in enumerate(boardRegex):
        if char.isalpha() and (index == 0 or boardRegex[index-1] != "\\"):
            output += char
    return output

def getWordsByIteratingOverRacks(rack: str, boardRegex = "", mode = "wwf"):

    playableWords = [''.join(p) for r in range(1, len(rack+extractAlphaFromRegex(boardRegex))+1) for p in itertools.permutations(rack+extractAlphaFromRegex(boardRegex), r)]

    validPlayableWords = set([WordResult(word, mode) for word in playableWords if validateWord(word, mode) and re.search(boardRegex, word)])

    return validPlayableWords


def wordIsOnRack(validWord: str, numBlanks: int, rack: list):
    output = ""
    remainingBlanks = numBlanks
    for letter in validWord:
        if letter not in rack:
            if remainingBlanks > 0:
                remainingBlanks -= 1
                output += letter.lower()
            else:
                return ""
        
        else:
            output += letter
            rack.remove(letter)

    return output


def getWordsByIteratingOverValidWords(rack: str, boardRegex = "", mode = "wwf"):
    """
    Iterates over valid words to find ones that are on our rack
    """

    wordList = wwfWords
    if mode == "scrabble":
        wordList = scrabbleWords
    
    numBlanks = rack.count(BLANK_INDICATOR)
    trueRack = sorted(rack+extractAlphaFromRegex(boardRegex))

    output = set()
    for word in wordList:
        # Skip words that wouldn't fit in the board constraints
        if not re.search(boardRegex, word):
            continue

        word = wordIsOnRack(word, numBlanks, trueRack.copy())
        if word != "":
            output.add(WordResult(word, mode))

    return output


def getNumValidWords(mode = "wwf"):
    if mode == "scrabble":
        return len(scrabbleWords)
    return len(wwfWords)

def getNumWordsOnRack(rack: str, boardRegex = "", mode = "wwf"):
    numBlanks = rack.count(BLANK_INDICATOR)
    numAlpha = len(rack+ extractAlphaFromRegex(boardRegex)) - numBlanks 

    total = 0
    for i in range(1, numAlpha+1):
        for j in range(0, numBlanks+1):
            total += 26**j * math.factorial(i+j) * math.comb(numAlpha, i) * math.comb(numBlanks, j)
    
    return total


def _findWords(rack: str, boardRegex = "", mode = "wwf"):
    blank_index = rack.find(BLANK_INDICATOR)
    
    if getNumWordsOnRack(rack, boardRegex, mode) < getNumValidWords(mode):
        """
        Iterate over words in all possible rack permutations and check each one
        """

        if blank_index == -1:
            # No blank found
            return sorted(getWordsByIteratingOverRacks(rack, boardRegex, mode))

        print("iterating over words on rack")

        # Get racks for all values of blank
        output = set()
        for i in range(97, 97+26): # iterates over lowercase letters
            newRack = rack[:blank_index] + chr(i) + rack[blank_index+1:]
            output.update(_findWords(newRack, boardRegex, mode))
                
        return sorted(output)
    
    else:
        print("iterating over valid words")
        if blank_index == -1:
            # No blank found
            return sorted(getWordsByIteratingOverRacks(rack, boardRegex, mode))
    
        """
        Iterate over valid words and see which ones are on our rack
        """
        # Get racks for all values of blank
        return sorted(getWordsByIteratingOverValidWords(rack, boardRegex, mode))
    

def findWords(rack: str, boardRegex = "", mode = "wwf"):
    return _findWords(rack.upper(), boardRegex, mode)

if __name__ == "__main__":
    rack = str.replace(str.replace(sys.argv[1], "_", BLANK_INDICATOR), "?", BLANK_INDICATOR).upper()

    boardRegex = ""
    if (len(sys.argv) > 2):
        boardRegex = str.replace(sys.argv[2], " ", "\w")
        if boardRegex.startswith("\\w"):
            boardRegex = "^" + boardRegex
        if boardRegex.endswith("\\w"):
            boardRegex += "$"

    mode = "scrabble"
    if (len(sys.argv) > 3):
        mode = sys.argv[3]

    t0 = time.time()
    results = findWords(rack, boardRegex, mode)
    t1 = time.time()

    result_limit = 100
    for result in results[:result_limit]:
        print(result)
    print(f"{min(result_limit, len(results))} of {len(results)} results shown")