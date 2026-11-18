from flight_search import search_flights
import pandas as pd

"""
In portland 23-(28|29)
In SD ~ 7days
"""
# in_portland = (pd.Timestamp("2026-12-23"),pd.Timestamp("2026-12-28"))
# in_sd = pd.Timestamp("2026-12-28") + pd.Timedelta(7, 'days')

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
            max_results=100,
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

print("***Flight Summary***")
for k,leg in flight_d.sort_values("price").groupby(['origin','destination']).head(1).iterrows():
    org,dest = leg['origin'],leg['destination']
    print(f"Flying {leg['airline']} {org}->{dest} at {leg['departure_time']} to arrive at {leg['arrival_time']}. ${leg['price']} for {n_adults} adults")
