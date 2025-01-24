import streamlit as st


def main():
    st.title("Hi, Mom!")
    st.write("More like StreamLIT")

    number = st.slider("Pick a number", 0, 100)
    st.write(f"You selected {number}")


if __name__ == "__main__":
    main()
