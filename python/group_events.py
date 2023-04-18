import csv
from datetime import datetime, timedelta
import hashlib
import os

from matplotlib import pyplot as plt
import pandas as pd


SESSION_TIMEOUT_SECS = 1800

CSV_FILE = "website_data_20230418_012558.csv"

base_dir = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(base_dir, "data", CSV_FILE)


def read_events() -> list[str]:
    with open(file_path) as f:
        csv_reader = csv.DictReader(f)
        return list(csv_reader)


def sequential_grouping(events: list[str]) -> list[dict]:
    current_user = None
    for event in events:
        current_website = event["website_id"]
        current_time = datetime.fromisoformat(event["event_datetime"])

        if current_user != event["user_id"]:
            current_user = event["user_id"]
            sessions = {}

        # Is this a new website or has the session timed out?
        if current_website not in sessions or current_time >= sessions.get(
            current_website
        ).get("max_session_time"):
            hash_string = f"{current_user}-{current_website}-{event['event_datetime']}"
            # create a new session in the 'memory'
            sessions[current_website] = {
                "session_id": hashlib.md5(hash_string.encode("utf-8")).hexdigest(),
            }

        # update the max_session_time for the session
        sessions[current_website]["max_session_time"] = current_time + timedelta(
            seconds=SESSION_TIMEOUT_SECS
        )

        # Output the row with session information
        session_id = sessions.get(current_website).get("session_id")
        yield {
            "user_id": current_user,
            "website_id": current_website,
            "event_datetime": datetime.fromisoformat(event["event_datetime"]),
            "session_id": session_id,
        }


def plot_events(events_df: pd.DataFrame):
    # Different colours for each session_id
    # get all the session_ids
    session_ids = events_df["session_id"].unique()

    # create an axis with the first website, then append to that axis afterwards
    cust_df = events_df[events_df["session_id"] == session_ids[0]]
    axis = cust_df.plot(
        x="event_datetime",
        y="user_id",
        kind="scatter",
        c=f"#{session_ids[0][:6]}",
        label=session_ids[0][:6],
    )

    for session_id in session_ids:
        cust_df = events_df[events_df["session_id"] == session_id]
        cust_df.plot(
            x="event_datetime",
            y="user_id",
            kind="scatter",
            ax=axis,
            c=f"#{session_id[:6]}",
            label=session_id[:6],
        )

    num_users = events_df["user_id"].unique().size

    plt.yticks(range(num_users))

    plt.gcf().autofmt_xdate()

    plt.ylabel("user ID", fontsize=8)
    plt.xlabel("Time", fontsize=8)

    plt.tick_params(axis="x", which="major", labelsize=8)
    plt.tick_params(axis="y", which="major", labelsize=8)

    axis.get_legend().remove()

    plt.show()


if __name__ == "__main__":
    events = read_events()

    events_df = pd.DataFrame.from_records(sequential_grouping(events))

    plot_events(events_df)
