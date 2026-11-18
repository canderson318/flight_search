# Flight search

Find flights using `flight-search` & `fast-flights` [(source)](https://github.com/Olafs-World/flight-search/tree/main).
This scrapes the first page of any Google Flights query with out an api.

## Set up

use `uv init` and `uv sync` to set up environment from [pyproject.toml](pyproject.toml)

## Usage

Edit the list of `travel_times` in [code/main.py](code/main.py) to reflect desired destination and origin for a range of travel dates. 

Run with `uv run code/main.py`, or use in your REPL of choice. The top flights are outputted to `out/top_flights.md` in order of leg and price and all flights found are saved as a csv in [out/flights.csv](out/flights.csv).
