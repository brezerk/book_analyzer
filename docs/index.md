# Welcome to BookAnalyzer test assigment

The task is to write a program, BookAnalyzer, that analyzes such a log file.
BookAnalyzer takes one command line argument: target‐size. BookAnalyzer then
reads a market data log on standard input. As the book is modified,
BookAnalyzer prints (on standard output) the total expense you would incur if
you bought target‐size shares (by taking as many asks as necessary, lowest
first), and the total income you would receive if you sold target‐size shares
(by hitting as many bids as necessary, highest first). Each time the income or
expense changes, it prints the changed value.

For support visit [brezblock.org.ua](https://brezblock.org.ua).

## Installation

* `make dev`

## Testing

* `make test`

## Running application manually

* `source .venv/bin/activate`
* `python main.py`

## Tech data

# Message format

* [Input format](./format/input.md)
* [Output format](./format/output.md)

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
    data/         # Project data
    test/unit     # Unit tests
    test/e2e      # e2e tests
    test/data     # Unit tests data

## Known Issues

