# Flight search

Find flights using `flight-search` & `fast-flights`

## Set up

use `uv init` and `uv sync` to set up environment from `pyproject.toml`

## Usage

Edit the list of `travel_times` in [code/main.py](code/main.py) to reflect desired destination and origin for a range of travel dates. 

Run with `uv run code/main.py`, or use in your REPL of choice. The results are outputted to `out/top_flights.md` in order of leg and price.
