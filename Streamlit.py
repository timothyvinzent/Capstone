import streamlit as st
import streamlit.components.v1 as components

def main():
    st.title("Streamlit Multipage App")

    menu = ["Home", "About"]
    choice = components.html(
        """
        <div style="display:flex; justify-content:space-between">
        <a href="https://www.streamlit.io/" target="_blank"><button>Home</button></a>
        <a href="https://www.streamlit.io/about" target="_blank"><button>About</button></a>
        </div>
        """
    )

if __name__ == "__main__":
    main()