from datetime import date, datetime, timedelta

import pytz
import streamlit as st

import helper


def main():
    recs = helper.get_all_recs()
    for rec in recs:
        draw_progress_bar(rec)
        st.button('Reset', key=rec['id'], on_click=render_dt_picker, args=(rec,))
        st.write('')
        st.write('')


def draw_progress_bar(rec):
    reset_dt = rec['reset_dt']
    period = rec['period']
    desc = rec['desc']

    date_delta = compute_date_delta(reset_dt)
    progress_val = min(float(date_delta / period), 1.0)
    due_date = date.fromisoformat(reset_dt) + timedelta(days=int(period))

    txt = f'{desc} ({round(progress_val * 100)}%) 〰️ reset on {reset_dt} 〰️ period {period} 〰️ due date {due_date}'
    if date_delta > period:
        txt += f' 〰️ ⚠️ {date_delta - period} day(s) overdue'

    st.progress(progress_val, txt)


@st.dialog('Reset Date')
def render_dt_picker(rec):
    new_reset_dt = st.date_input(f'Pick a reset date for {rec['desc']}:', max_value=date.today()).isoformat()
    if st.button('Confirm'):
        helper.update_reset_dt(rec, new_reset_dt)
        st.rerun()


def compute_date_delta(reset_date_str):
    cst = pytz.timezone('America/Chicago')
    today = datetime.now(cst).date()
    reset_date = date.fromisoformat(reset_date_str)
    return (today - reset_date).days


if __name__ == '__main__':
    main()
