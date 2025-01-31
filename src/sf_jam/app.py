import json
import streamlit as st
import pandas as pd
from datetime import datetime


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


def create_clickable_link(url):
    """Create a clickable link with 'Buy Tickets' text"""
    return f'<a href="{url}" target="_blank">Tickets</a>'


def main():
    st.title("Welcome to SF Jam 🌉 🎸")
    st.write("Check out a list of concerts at local Bay Area venues")

    # Add custom CSS to style the table
    st.markdown(
        """
        <style>
        table {
            width: 100% !important;
            white-space: nowrap !important;
        }
        th {
            text-align: left !important;
            padding: 8px !important;
            white-space: nowrap !important;
            # background-color: #f0f2f6 !important;
        }
        td {
            text-align: left !important;
            padding: 8px !important;
            white-space: nowrap !important;
        }
        a {
            color: #1E88E5 !important;
            text-decoration: none !important;
        }
        a:hover {
            text-decoration: underline !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    events = load_json_file()
    df = pd.DataFrame(events)

    # Create a layout with columns for the filters
    col1, col2 = st.columns([2, 1])

    # Add search bar in the first (wider) column
    with col1:
        search_term = st.text_input("Search artists/events:", key="search_bar")

    # Add venue filter in the second column
    with col2:
        # Get unique venues for the filter
        all_venues = sorted(df["venue"].unique())
        selected_venues = st.multiselect(
            "Select venues:", options=all_venues, default=[], key="venue_filter"
        )

    # Define columns to show and their display names
    column_mapping = {
        "headliner": "Artist/Event",
        "date": "Date",
        "venue": "Venue",
        "show_time": "Show Time",
        "ticket_url": "",
    }

    columns_to_show = list(column_mapping.keys())

    # Create a copy of the DataFrame with selected columns
    df_display = df[columns_to_show].copy()

    # Filter the DataFrame based on selected venues
    if selected_venues:
        df_display = df_display[df_display["venue"].isin(selected_venues)]

    # Filter by search term
    if search_term:
        df_display = df_display[
            df_display["headliner"].str.contains(search_term, case=False, na=False)
        ]

    # Convert date strings to datetime for sorting
    # First, create a copy of the date column for sorting
    df_display["date_for_sorting"] = pd.to_datetime(df_display["date"])

    # Sort the DataFrame by the datetime column
    df_display = df_display.sort_values("date_for_sorting")

    # Remove the sorting column as we don't need to display it
    df_display = df_display.drop("date_for_sorting", axis=1)

    # Convert ticket URLs to clickable links
    df_display["ticket_url"] = df_display["ticket_url"].apply(create_clickable_link)

    # Rename the columns
    df_display = df_display.rename(columns=column_mapping)

    # Display the table with HTML rendering enabled
    # st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Show results or no results message
    if len(df_display) > 0:
        st.write(f"Showing {len(df_display)} events")
        # Display the table with HTML rendering enabled
        st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        # If search term was used, include it in the message
        if search_term:
            st.markdown(
                f"""<div class="no-results">
                    <h3>No events found</h3>
                    <p>No events match your search for "{search_term}"</p>
                    <p>Try adjusting your search terms or selected venues</p>
                </div>""",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """<div class="no-results">
                    <h3>No events found</h3>
                    <p>No events match the selected filters</p>
                    <p>Try selecting different venues</p>
                </div>""",
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
