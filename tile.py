class Tile:
    
    def __init__(self, letter: str, scrabbleValue: int, scrabbleNum: int, wwfValue: int, wwfNum: int):
        self.letter = letter
        self.scrabbleValue = scrabbleValue
        self.scrabbleNum = scrabbleNum
        self.wwfValue = wwfValue
        self.wwfNum = wwfNum

    def getValue(self, mode = "wwf") -> int:
        if mode == "scrabble":
            return self.scrabbleValue
        return self.wwfValue


tiles = {
    'A' : Tile('A', 1, 9, 1, 9),
    'B' : Tile('B', 3, 2, 4, 2),
    'C' : Tile('C', 3, 2, 4, 2),
    'D' : Tile('D', 2, 4, 2, 5),
    'E' : Tile('E', 1, 12, 1, 13),
    'F' : Tile('F', 4, 2, 4, 2),
    'G' : Tile('G', 2, 3, 3, 3),
    'H' : Tile('H', 4, 2, 3, 4),
    'I' : Tile('I', 1, 9, 1, 8),
    'J' : Tile('J', 8, 1, 10, 1),
    'K' : Tile('K', 5, 1, 5, 1),
    'L' : Tile('L', 1, 4, 2, 4),
    'M' : Tile('M', 3, 2, 4, 2),
    'N' : Tile('N', 1, 6, 2, 5),
    'O' : Tile('O', 1, 8, 1, 8),
    'P' : Tile('P', 3, 2, 4, 2),
    'Q' : Tile('Q', 10, 1, 10, 1),
    'R' : Tile('R', 1, 6, 1, 6),
    'S' : Tile('S', 1, 4, 1, 5),
    'T' : Tile('T', 1, 6, 1, 7),
    'U' : Tile('U', 1, 4, 2, 4),
    'V' : Tile('V', 4, 2, 5, 2),
    'W' : Tile('W', 4, 2, 4, 2),
    'X' : Tile('X', 8, 1, 8, 1),
    'Y' : Tile('Y', 4, 2, 3, 2),
    'Z' : Tile('Z', 10, 1, 10, 1),
    ' ' : Tile('_', 0, 2, 0, 2)
}