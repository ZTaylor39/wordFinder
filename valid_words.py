def getWords(filepath = "scrabbleDictionary.txt") -> set:
    validWords = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word:
                validWords.add(word)
    
    return validWords

scrabbleWords = getWords()
wwfWords = getWords()