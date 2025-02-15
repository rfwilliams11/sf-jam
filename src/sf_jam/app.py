import sqlite3
import threading

import pandas as pd
import streamlit as st
from main import run_scraper


def load_concerts_from_db():
    """Load concerts from local SQLite database."""
    conn = sqlite3.connect("concerts.db")
    query = "SELECT * FROM concerts"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def create_venue_link(row):
    """Create a clickable venue link using the ticket URL"""
    return (
        f'<a href="{row["ticket_url"]}" target="_blank">{row["venue"]}</a>'
        if pd.notna(row["ticket_url"])
        else row["venue"]
    )


def main():
    # Run scraper in a separate thread
    # TODO: Separate the scraping from the app
    scraper_thread = threading.Thread(target=run_scraper)
    scraper_thread.daemon = True
    scraper_thread.start()

    st.title("SF Jam 🌉 🎸")
    st.write("Check out a list of concerts at local Bay Area venues")

    # Add custom CSS to make the table responsive
    st.markdown(
        """
    <style>
    .block-container {
        padding-top: 50px !important;
        padding-bottom: 10px !important;
        padding-right: 5px !important;
        padding-left: 10px !important;
    }
    .table-container {
        max-width: 100%;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        margin: 0;
        padding: 0;
    }

    table {
        width: 100%
    }

    /* Responsive table styling */
    @media screen and (max-width: 768px) {
        table {
            font-size: 15.5px;
        }

        th, td {
            padding: 8px 4px !important;
            min-width: 80px;
        }

        th {
            text-align: left !important;  /* Force left alignment */
            padding: 8px 4px !important;
            font-weight: 800;
        }

        /* Adjust column widths for mobile */
        th:nth-child(1), td:nth-child(1) { width: 40%; }  /* Artist/Event */
        th:nth-child(2), td:nth-child(2) { width: 35%; }  /* Date */
        th:nth-child(3), td:nth-child(3) { width: 27%; }  /* Venue */
    }

    th {
            text-align: left !important;  /* Force left alignment */
            padding: 12px 8px !important;
            font-weight: 800;
    }

    /* Search form improvements */
    .search-form {
        # margin-bottom: 1rem;
    }

    /* Improve button styling */
    .stButton > button {
        width: 100%;
        margin: 0;
    }

    /* Improve multiselect on mobile */
    .stMultiSelect {
        max-width: 100%;
    }

    /* Add spacing between elements */
    .spacer {
        margin: 1rem 0;
    }

    .footer {
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        margin-top: 75px;
        border-top: 1px solid #ddd;  /* Optional: add a top border */
    }

    .footer img {
        height: 20px;  /* Adjust the height of the image */
        vertical-align: middle;  /* Align the image vertically with the text */
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    events = load_concerts_from_db()

    # Initialize session state if it doesn't exist
    if "search_term" not in st.session_state:
        st.session_state.search_term = ""

    # Create a form for the search
    with st.form(key="search_form", clear_on_submit=False):
        # Create a horizontal layout for search input and buttons
        # search_cols = st.columns(3)  # Adjust ratios as needed

        search_term = st.text_input(
            "Search artists/events:",
            value=st.session_state.search_term,
            key="search_bar",
        )

        # Create buttons for searching and clearing
        col1, col2 = st.columns([1, 1])  # Ratio to adjust button widths
        with col1:
            search_submitted = st.form_submit_button("Search", use_container_width=True)

        with col2:
            clear_submitted = False
            if st.session_state.search_term != "":
                clear_submitted = st.form_submit_button(
                    "Clear", use_container_width=True
                )

    # Handle the search submissions
    if search_submitted:
        st.session_state.search_term = search_term
        st.rerun()

    if clear_submitted:
        st.session_state.search_term = ""  # Clear the search term
        st.rerun()  # Rerun the app to reflect the changes
    # Get unique venues for the filter
    all_venues = sorted(events["venue"].unique())
    selected_venues = st.multiselect(
        "Select venues:", options=all_venues, default=[], key="venue_filter"
    )

    # Define columns to show and their display names
    column_mapping = {
        "headliner": "Artist/Event",
        "date": "Date",
        "venue_link": "Tickets",
    }

    # Create a copy of the DataFrame with selected columns
    df_display = events[["headliner", "date", "venue", "ticket_url"]].copy()

    # Filter the DataFrame based on selected venues
    if selected_venues:
        df_display = df_display[df_display["venue"].isin(selected_venues)]

    # Filter by search term
    if search_term:
        df_display = df_display[
            df_display["headliner"].str.contains(search_term, case=False, na=False)
        ]

    # Convert date strings to datetime for sorting
    df_display["date_for_sorting"] = pd.to_datetime(df_display["date"])

    # Sort the DataFrame by the datetime column
    df_display = df_display.sort_values("date_for_sorting")

    # Create the venue links
    df_display["venue_link"] = df_display.apply(create_venue_link, axis=1)

    # Keep only the columns we want to display
    df_display = df_display[["headliner", "date", "venue_link"]]

    # Rename the columns
    df_display = df_display.rename(columns=column_mapping)

    # Show results or no results message
    if len(df_display) > 0:
        event_string = "events" if len(df_display) > 1 else "event"
        st.write(f"Showing {len(df_display)} {event_string}")
        # Wrap table in a container div and display
        table_html = f"""
        <div class="table-container">
            {df_display.to_html(escape=False, index=False)}
        </div>
        """
        st.write(table_html, unsafe_allow_html=True)
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

        # Add the footer at the bottom
    st.markdown(
        """
        <div class="footer">
            <p>
                Made by rfwilliams11
                <a href="https://github.com/rfwilliams11/sf-jam">
                    <img src="https://banner2.cleanpng.com/20180421/die/kisspng-github-computer-icons-node-js-circle-pack-5adb933cc5ffc2.914040391524339516811.jpg" alt="GitHub" />  # noqa: E501
                </a>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
