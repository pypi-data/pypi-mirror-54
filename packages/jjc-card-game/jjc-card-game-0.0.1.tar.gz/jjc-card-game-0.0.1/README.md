# JJC's Card Game
This is a simple card played over a series of round. Each round, players draw one card. The player with the highest card received 2 points. Players with penalty cards lose a point. First player to 21 points wins.

## Installation
Make sure you have python 3.6 or higher installed, then:
```powershell
pip install jjc-card-game
```

## Play
Simply:
```powershell
jjc-card-game
```
Then follow the on-screen rules and instructions.

Or try these more advanced options:
- `jjc-card-game -d Jonathan Nicholas Austin` to play a game with these three players. The `-d` speeds up gameplay by dealing all the cards at once.
- `jjc-card-game --help` to see even more options

## Development
Development tools: Windows 10, PowerShell, and PyCharm.
```powershell
git clone https://github.com/jonathanchukinas/card_game.git
cd card_game
pip install flit            # for build, packaging
python -m venv .venv        # create virtual environment
.venv\scripts\activate      # activate virtual environment
flit install --pth-file     # editable install 

# modify source code
jjc-card-game               # to run modified app
# repeat

deactivate                  # exit virtual environment
```

## Running the tests
Test are written for `pytest` and automated by `tox`.
They cover most of the game logic, but less than 50%
of the command-line interface / ouput.

To run all the tests:
```powershell
pip install tox, pytest
cd path\to\project\directory
tox
```
Tests will be run against all these python versions, if you have them:
- v3.6
- v3.7
- v3.8

For a faster way to run tests:
```powershell
pytest
``` 

## Built With
[python](https://www.python.org/) and python packages:
- [click](https://click.palletsprojects.com) for created command line interface
- [PTable]() for generating pretty scorecard tables

## Authors
- **Jonathan Chukinas** - *initial release*

## License
This project is licensed under the MIT License - see the
[LICENSE.md](https://github.com/jonathanchukinas/card_game/blob/master/LICENSE) file for details

## Acknowledgements
- **Brian Okken** for his [Test & Code](https://testandcode.com/81) podcast and [Python Testing with pytest](https://pragprog.com/book/bopytest/python-testing-with-pytest) book, which jump-started my testing knowledge early in 2019 and recently helped me integrate pytest, flit, and tox together.
- **Luciano Ramalho** for his outstanding [Fluent Python](http://shop.oreilly.com/product/0636920032519.do), which taught me much of what I know about python under the hood, dunder methods, lru cache, etc.