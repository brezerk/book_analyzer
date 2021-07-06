
Test assigment
***********************************************

Your task is to write a program, BookAnalyzer, that analyzes such a log file.
BookAnalyzer takes one command line argument: target‐size. BookAnalyzer then
reads a market data log on standard input. As the book is modified,
BookAnalyzer prints (on standard output) the total expense you would incur if
you bought target‐size shares (by taking as many asks as necessary, lowest
first), and the total income you would receive if you sold target‐size shares
(by hitting as many bids as necessary, highest first). Each time the income or
expense changes, it prints the changed value.

In addition to supplying us with your source code, please answer these questions
***********************************************

> How did you choose your implementation language?

Python is the best language for fast prototyping (But not the fastest one, yeah);

> How did you arrive at your final implementation? Were there other approaches that you
considered or tried first?

Data analysis discovered following items:

* There are two types of messages: A, R
** A message brings two data streams: S, B
** R can modify data state for each data stream: S, B
* Desired output is based on data state for two data streams: S, B

Two things I hate about this:
* R message seem to be capabe not only to remove, but to reduce the size of order: so we need ability to map ID -> recorded order size;
* R message can affect both S, B data streams state;
* Data state can be changed with each message;

So, simple solution like just keeping the sum for S, B streams incrementing with A and reducing with R messages won't work:
* S, B needs to arranged by price;
* R can change values in the "middle";
* A can insert values in the "front" causeung entire sum to be recalculated in regards to desired target size;

-_-

So we need to have some kind of DB (or map) to keep actual data state.
There is no need to keep entire message, but the required data only.

So this is where the code.db.metadata comes into play.

Data to be stored:
 * side (init) -- S or B will control the orders insert logic based on desired price trend (lower frst, highest first);
 * index       -- just a list of "known" order ids, it will serve as an index for orders list as well (some kind of 1-level cache);
 * orders      -- a list of orders in format [<price>, <count>]
 * count       -- the sum of counts for all okders in the orders array (some kind of 1-level cache);

The obvoius "design" issue: the need to iterate over a list to sumup the final price: this will trigger a bunch of float point operations. And yes, Python is not good in it.

This is the core. The rest is just build around metadata engine.

> How does your implementation scale with respect to the target size?

With the need to keep a list of orders -- badly. Perfomance drops exponentially i think.
The obvious suggeston is to split S and B calculation into two threads (this is done btw).

> How does your implementation scale with respect to the number of orders in the book?

In regards to the requirement: "As the book is modified, BookAnalyzer prints the total expense you would incur*": this limits implimentation, so perfomance scales linearly more or less.
There is an a room to implement central DB support like redis (see: core.db.base. core.db.memory, core.book) you will need to split the incoming feed and pass it to multimple workers as well as split the logic into 'loader' and 'processor'.
Howover this probaably won't feet into the requirement as the suggestions would be done on data snapshot which can be not accurate;


Notes
***********************************************
This software comes with absolutely no warranty.

Dependencies:
***********************************************
python3-virtualenv
make

Installation
***********************************************

1. $ make dev
2. $ make test
3. $ source .venv/bin/activate
4. $ cat test/e2e/data/book_analyzer.small.stdin | python ./main.py --target‐size 200
5. ???
6. ...
5. PROFIT

Known Issues:
***********************************************

