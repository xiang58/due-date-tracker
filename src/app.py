import pytz
import streamlit as st
from datetime import date, datetime


def main():
    draw_progress_bar('bath towel', '2025-03-14', 4)


def draw_progress_bar(desc, reset_date_str, period):
    date_delta = compute_date_delta(reset_date_str)
    progress_val = date_delta / period
    st.progress(progress_val, f'{desc} ({progress_val * 100}%)')


def compute_date_delta(reset_date_str):
    cst = pytz.timezone('America/Chicago')
    today = datetime.now(cst).date()
    reset_date = date.fromisoformat(reset_date_str)
    return (today - reset_date).days


if __name__ == '__main__':
    main()
