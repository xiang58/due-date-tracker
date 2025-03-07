import streamlit as st
import time


def draw_progress_bar():
    st.title("Streamlit Progress Bar Example")

    # Create a progress bar object
    progress_bar = st.progress(0)

    # Simulate a task progressing
    for percent_complete in range(101):
        time.sleep(0.05)  # Simulating work
        progress_bar.progress(percent_complete)  # Update progress

    st.success("Task Completed! 🎉")


def main():
    draw_progress_bar()


if __name__ == '__main__':
    main()
