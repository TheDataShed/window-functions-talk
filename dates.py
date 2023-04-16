from datetime import (
    datetime,
    timedelta,
)
import random
from dataclasses import (
    asdict,
    dataclass,
)
from typing import List
import pandas
from matplotlib import pyplot as plt


NUM_USERS = 4

websites = ["Cat Pictures", "Stack Overflow", "PyData", "Reddit"]
NUM_WEBSITES = len(websites)

random.seed("PyData Leeds")


@dataclass
class Event:
    customer_id: int
    website_id: int
    event_datetime: datetime

    def csv_row(self) -> str:
        return ",".join(
            [
                str(event.customer_id),
                str(event.website_id),
                event.event_datetime.isoformat(),
            ]
        )


Events = List[Event]


def random_dates(start: datetime, l: int) -> List[datetime]:
    current = start
    for _ in range(l):
        # Add a gap of up to 14 minutes
        extra_minutes = random.randint(1, 14)

        # 1/10 times add a bigger gap of up to 2 hours
        if random.random() < 0.1:
            extra_minutes += 10 * random.randint(1, 12)

        current += timedelta(minutes=extra_minutes)
        current += timedelta(seconds=random.randint(0, 59))

        yield current


def events_to_df(events: Events) -> pandas.DataFrame:
    return pandas.DataFrame.from_records([asdict(e) for e in events])


events: Events = []

for cust_id in range(NUM_USERS):
    # Offset the starting hours by one hour per customer
    start_hour = 10 + cust_id
    num_rows = random.randint(20, 40)
    website_ids = list(range(NUM_WEBSITES))
    for dt in random_dates(datetime(2022, 10, 1, 8), num_rows):
        event = Event(
            customer_id=cust_id,
            website_id=random.choices(
                population=website_ids, weights=website_ids.reverse()
            )[0],
            event_datetime=dt,
        )
        events.append(event)

# csv_data = "customer_id,website_id,event_datetime\n" + "\n".join(
#     [event.csv_row() for event in events]
# )

events_df = events_to_df(events)

# Shed colours:
# Orange: #f98c2a
# Teal: #5ddbc2
# Dark purple: #5c5aa6
# Darker grey: #d8d7d6
# Light purple: #8c8bc0
# Grey: #e2e2e3

colours = [
    "#f98c2a",
    "#5ddbc2",
    "#5c5aa6",
    "#d8d7d6",
    "#8c8bc0",
    "#e2e2e3",
]

# Different colours for each website
# create an axis with the first website, then append to that axis afterwards
cust_df = events_df[events_df["website_id"] == 0]
axis = cust_df.plot(
    x="event_datetime", y="customer_id", kind="scatter", c=colours[0], label=websites[0]
)

for website_id in range(1, NUM_WEBSITES):
    cust_df = events_df[events_df["website_id"] == website_id]
    cust_df.plot(
        x="event_datetime",
        y="customer_id",
        kind="scatter",
        ax=axis,
        c=colours[website_id],
        label=websites[website_id],
    )


min_date = events_df["event_datetime"].min().replace(microsecond=0, second=0, minute=0)
max_date = events_df["event_datetime"].max().replace(
    microsecond=0, second=0, minute=0
) + timedelta(hours=1)

date_to_add = min_date
dates = [date_to_add]
while date_to_add <= max_date:
    date_to_add += timedelta(hours=2)
    dates.append(date_to_add)

plt.yticks(range(NUM_USERS))
plt.xticks(dates)

plt.ylabel("Customer ID", fontsize=8)
plt.xlabel("Time", fontsize=8)

plt.tick_params(axis="x", which="major", labelsize=8)
plt.tick_params(axis="y", which="major", labelsize=8)

plt.show()
