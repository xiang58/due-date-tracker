from datetime import date, datetime

import pytz
import streamlit as st

import helper


def main():
    if 'show_dialog' not in st.session_state:
        st.session_state['show_dialog'] = None

    recs = helper.get_all_recs()
    for rec in recs:
        draw_progress_bar(rec)

        reset_key = f"reset_{rec['id']}"
        if st.button("Reset", key=reset_key, disabled=is_reset_button_disabled(rec)):
            st.session_state['show_dialog'] = rec['id']
            st.rerun()

        if st.session_state.get('show_dialog') == rec['id']:
            render_dt_picker(rec)

        st.write('')
        st.write('')


def draw_progress_bar(rec):
    date_delta = compute_date_delta(rec['reset_dt'])
    progress_val = min(float(date_delta / rec['period']), 1.0)
    st.progress(progress_val, f'{rec['desc']} ({round(progress_val * 100)}%) - last reset date: {rec['reset_dt']}')


def is_reset_button_disabled(rec):
    return st.session_state['show_dialog'] is not None and st.session_state['show_dialog'] != rec['id']


def render_dt_picker(rec):
    new_reset_dt = st.date_input('Pick a reset date:', key=f"date_{rec['id']}", max_value=date.today()).isoformat()
    if st.button("Confirm", key=f"confirm_{rec['id']}"):
        helper.update_reset_dt(rec, new_reset_dt)
        st.session_state['show_dialog'] = None
        st.rerun()


def compute_date_delta(reset_date_str):
    cst = pytz.timezone('America/Chicago')
    today = datetime.now(cst).date()
    reset_date = date.fromisoformat(reset_date_str)
    return (today - reset_date).days


if __name__ == '__main__':
    main()
