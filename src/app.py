from datetime import date, datetime

import pytz
import streamlit as st

import helper


def main():
    recs = helper.get_all_recs()
    for rec in recs:
        draw_progress_bar(rec['desc'], rec['reset_dt'], rec['period'])


def draw_progress_bar(desc, reset_date_str, period):
    date_delta = compute_date_delta(reset_date_str)
    progress_val = float(date_delta / period)
    st.progress(progress_val, f'{desc} ({round(progress_val * 100)}%)')


def compute_date_delta(reset_date_str):
    cst = pytz.timezone('America/Chicago')
    today = datetime.now(cst).date()
    reset_date = date.fromisoformat(reset_date_str)
    return (today - reset_date).days


if __name__ == '__main__':
    main()
