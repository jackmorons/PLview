import streamlit as st

"""Simple multi-page Streamlit app with 5 pages: a, b, c, d, e."""


def page_a():
    st.title("Page A")
    st.write("Welcome to page A. Add your content here.")


def page_b():
    st.title("Page B")
    st.write("Welcome to page B. Add your content here.")


def page_c():
    st.title("Page C")
    st.write("Welcome to page C. Add your content here.")


def page_d():
    st.title("Page D")
    st.write("Welcome to page D. Add your content here.")


def page_e():
    st.title("Page E")
    st.write("Welcome to page E. Add your content here.")


PAGES = {
    "a": page_a,
    "b": page_b,
    "c": page_c,
    "d": page_d,
    "e": page_e,
}


def main():
    st.sidebar.title("Navigation")
    page_key = st.sidebar.radio("Choose a page", list(PAGES.keys()))
    st.sidebar.markdown("---")
    st.sidebar.write("Use this sidebar to switch between pages.")

    page = PAGES.get(page_key)
    if page:
        page()
    else:
        st.error(f"Unknown page '{page_key}'")


if __name__ == "__main__":
    main()

