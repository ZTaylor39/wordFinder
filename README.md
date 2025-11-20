# WordFinder

### Dependencies
Python 3

#### Python Libraries
* itertools
* re
* sys
* time
* math

### Usage
`python3 main.py <RACK> [<REGEX>] [<MODE>]`

#### `<RACK>`
For `<RACK>` , enter the tiles on your rack, in "double-quotes". Use an underscore (`_`), a question mark (`?`), or simply a space to indicate a blank tile. (e.g., "CUR ING" indicates a rack with the tiles "C", "U", "R", "Blank", "I", "N", "G"). The letters are case-insensitive.

#### `<REGEX>`
For `<REGEX>`, optionally enter, in "double-quotes", a regex string that results must match against.
* Letters in `<REGEX>` indicate tiles on the board. (These letters will not come from your rack). Use this with tiles on the board that must be included in the results. 
    * Letters are case sensitive: capital letters indicate normal tiles, lowercase letters indicate blank tiles that are standing in for a particular tile (this affects the calculation of points for a word).
* Regex patterns need not include letters. Using "\w{5}", for instance, will filter the results to show only words that are five-letters long
* A space character in the `<REGEX>` input is treated as convenient shorthand for a "\w". Thus, the following REGEX inputs are all equivalent:
    * `"     "` (five space characters)
    * `"\w\w\w\w\w"`
    * `"\w{5}"`

#### `<MODE>`
For `<MODE>`, optionally enter either (including "double-quotes"):
* "scrabble" (to use the Scrabble word dictionary and tile point values). 
* "wwf" (to use the Scrabble* word dictionary and Words With Friends tile points). If omitted, defaults to "wwf".
    * Yeah, even "wwf" mode uses the Scrabble word dictionary. I haven't found a good word list for Words With Friends yet.

The specific word dictionary that is being used is found [here](https://gist.github.com/deostroll/7693b6f3d48b44a89ee5f57bf750bd32.js).

### Example

* Rack: "CURVING"
* Regex: "\w{5}" (i.e., five-letter words)
* Mode: "scrabble"

`python3 main.py "CURVING" "\w{5}" "scrabble"`

outputs:
```
CUING - 8
INCUR - 7
RUNIC - 7
RUING - 6
UNRIG - 6
5 of 5 results shown
```