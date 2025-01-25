import json
import streamlit as st
import pandas as pd


def load_json_file():
    venues = [
        "fox_concerts.json",
        "chapel_concerts.json",
        "warfield_concerts.json",
        "fillmore_concerts.json",
    ]

    events = []

    for venue in venues:
        with open(venue, "r") as file:
            # events = json.load(file)
            events.extend(json.load(file))

    return events


def main():
    st.title("Welcome to SF Jam 🌉🎸")
    st.write("Check out a list of concerts at local Bay Area venues")
    events = load_json_file()
    df = pd.DataFrame(events)

    columns_to_show = ["title", "date", "venue", "door_time", "show_time"]

    st.table(df[columns_to_show])

    ## Remove index colum
    # st.markdown(
    #     df[columns_to_show].style.hide(axis="index").to_html(), unsafe_allow_html=True
    # )


if __name__ == "__main__":
    main()
