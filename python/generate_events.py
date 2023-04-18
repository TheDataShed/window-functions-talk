from dataclasses import (
    asdict,
    dataclass,
)
from datetime import (
    datetime,
    timedelta,
)
import os
import random
from typing import List

from matplotlib import pyplot as plt
import pandas as pd


NUM_USERS = 4

WEBSITES = ["Cat Pictures", "Stack Overflow", "PyData", "Reddit"]
NUM_WEBSITES = len(WEBSITES)

COLOURS = [
    "#f98c2a",  # Orange
    "#5ddbc2",  # Teal
    "#5c5aa6",  # Dark purple
    "#d8d7d6",  # Darker grey
    "#8c8bc0",  # Light purple
    "#e2e2e3",  # Grey
]

random.seed("PyData!")


@dataclass
class Event:
    user_id: int
    website_id: int
    event_datetime: datetime


Events = List[Event]


def random_dates(start: datetime, l: int) -> List[datetime]:
    current = start
    for _ in range(l):
        # Add a gap of up to 5 minutes
        extra_minutes = random.randint(0, 5)

        # 1/10 times add a bigger gap of up to an hour
        if random.random() < 0.1:
            extra_minutes += random.randint(10, 60)

        current += timedelta(minutes=extra_minutes)
        current += timedelta(seconds=random.randint(0, 59))

        yield current


def random_events() -> pd.DataFrame:
    events: Events = []

    for cust_id in range(NUM_USERS):
        num_rows = random.randint(20, 40)
        website_ids = list(range(NUM_WEBSITES))
        for dt in random_dates(datetime(2022, 10, 1, 8), num_rows):
            event = Event(
                user_id=cust_id,
                website_id=random.choices(
                    population=website_ids, weights=website_ids.reverse()
                )[0],
                event_datetime=dt,
            )
            events.append(event)

    return pd.DataFrame.from_records([asdict(e) for e in events])


def plot_events(events_df: pd.DataFrame):
    # Different colours for each website
    # create an axis with the first website, then append to that axis afterwards
    cust_df = events_df[events_df["website_id"] == 0]
    axis = cust_df.plot(
        x="event_datetime",
        y="user_id",
        kind="scatter",
        c=COLOURS[0],
        label=WEBSITES[0],
    )

    for website_id in range(1, NUM_WEBSITES):
        cust_df = events_df[events_df["website_id"] == website_id]
        cust_df.plot(
            x="event_datetime",
            y="user_id",
            kind="scatter",
            ax=axis,
            c=COLOURS[website_id],
            label=WEBSITES[website_id],
        )

    min_date = (
        events_df["event_datetime"].min().replace(microsecond=0, second=0, minute=0)
    )
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

    plt.ylabel("user ID", fontsize=8)
    plt.xlabel("Time", fontsize=8)

    plt.tick_params(axis="x", which="major", labelsize=8)
    plt.tick_params(axis="y", which="major", labelsize=8)

    plt.show()


if __name__ == "__main__":
    events = random_events()

    base_dir = os.path.dirname(os.path.dirname(__file__))
    events.to_csv(
        os.path.join(base_dir, "data", "website_data.csv"),
        index=False,
        date_format="%Y-%m-%dT%H:%M:%S",
    )

    plot_events(events)
