"""
In portland 23-(28|29)
In SD ~ 7days
"""
from flight_search import search_flights
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
# in_portland = (pd.Timestamp("2026-12-23"),pd.Timestamp("2026-12-28"))
# in_sd = pd.Timestamp("2026-12-28") + pd.Timedelta(7, 'days')

if __name__ == "__main__":

    os.chdir(Path.home() / "dev/py_stuff/flight_search")

    travel_times = [
        ('DEN', 'PDX', '2026-12-21'),
        ('DEN', 'PDX', '2026-12-23'),
        ('DEN', 'PDX', '2026-12-22'),

        ('PDX', 'SAN', '2026-12-27'),
        ('PDX', 'SAN', '2026-12-28'),
        ('PDX', 'SAN', '2026-12-29'),
        ('PDX', 'SAN', '2026-12-30'),

        ('SAN', 'DEN', '2027-01-03'),
        ('SAN', 'DEN', '2027-01-04'),
        ('SAN', 'DEN', '2027-01-05'),
        ('SAN', 'DEN', '2027-01-06'),
        ('SAN', 'DEN', '2027-01-07'),
    ]

    n_adults = 2
    flights = []
    for org,dest,dt in travel_times:
        try:
            result = search_flights(
                origin=org,
                destination=dest,
                date=dt,
                adults=n_adults,
                seat_class="economy",
                max_results=200,
            )
        except:
            print(f"No flights found for {org} -> {dest}")
            continue
        print(dt,org,'->',dest)
        res = pd.concat([pd.Series(result.flights[i].to_dict()) for i in range(len(result.flights))], axis = 1).T
        res['origin'] = org
        res['destination'] = dest
        flights.append(res)


    flight_d = pd.concat(flights)
    flight_d['price'] = flight_d.price.astype(float)
    for x in ['origin', 'destination']:
        flight_d[x] = flight_d[x].astype('category').cat.reorder_categories(["DEN", "PDX", "SAN"])
    flight_d['duration'] =[int(p[0]) + int(p[2])/60 if len(p := x.split()) == 4 else int(p[0]) for x in flight_d['duration']]
    flight_d.to_csv("out/flights.csv")

    # plot
    fig, ax = plt.subplots()
    for i,(k,G) in enumerate(flight_d.groupby(['origin', 'destination'])):
        ax.scatter(G["duration"],G["price"], label = " ".join(k), color = f'C{i}', alpha = .3)
    ax.legend()
    plt.tight_layout()

    flight_d['departure_date']  = [x[1] for x in flight_d['departure_time'].str.split(" on ")]

    plt.figure(figsize = (10,5))
    flight_d.groupby(["origin", 'destination', 'departure_date']).price.plot.kde()
    plt.legend()
    plt.savefig('out/departure_flight_price_kde.pdf')


    # find best flights under certain duration and price
    best = flight_d[flight_d.duration.lt(5)&flight_d.price.lt(400)].sort_values(['origin',"price",'duration'], ascending = [True, True, True]).groupby(['origin','destination']).head(10)
    best=best.drop_duplicates(subset = ['airline', 'origin', 'destination', 'departure_time', 'arrival_time'])

    x = "DEN"
    with open("out/top_flights.md", 'wt') as f:
        print("# Flight Summary\n", file = f)
        for k,leg in best.iterrows():
            org,dest = leg['origin'],leg['destination']
            if org != x:
                print("\\ \n\\", file = f)
            print(f"Flying {leg['airline']} {org}->{dest} at **{leg['departure_time']}** to arrive at **{leg['arrival_time']}** ({leg['duration']:.2f} hrs). **${leg['price']:.0f}** for {n_adults} adults\n", file = f)
            x=org
