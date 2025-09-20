from datetime import date, datetime, timedelta

import pytz
import streamlit as st

import repo


def main():
    recs = repo.get_all_recs()
    st.button('Add new record', key='add_btn', on_click=render_new_rec_dialog, args=(recs,))
    st.divider()

    for rec in recs:
        draw_progress_bar(rec)
        cols = st.columns(8, vertical_alignment="bottom")

        with cols[0]:
            st.button('Reset', key=f'reset_{rec['id']}', on_click=render_dt_picker, args=(rec,))
        with cols[1]:
            st.button('Edit', key=f'edit_{rec['id']}', on_click=render_edit_dialog, args=(rec,))
        with cols[2]:
            st.button('Delete', key=f'delete_{rec['id']}', on_click=render_del_rec_dialog, args=(rec['id'],))

        st.write('')
        st.write('')


@st.dialog('Add new record')
def render_new_rec_dialog(recs):
    desc = st.text_input('Enter the description:').strip()
    period = st.number_input('Enter the period:', value=None, min_value=1)
    reset_dt = st.date_input(f'Pick a reset date:', max_value=date.today()).isoformat()

    if st.button('Confirm'):
        if not desc or not period:
            st.toast('Description and period cannot be empty!', icon='🚨')
            return
        repo.add_rec(recs, desc, period, reset_dt)
        st.rerun()


def draw_progress_bar(rec):
    reset_dt = rec['reset_dt']
    period = rec['period']
    desc = rec['desc']

    date_delta = compute_date_delta(reset_dt)
    progress_val = min(float(date_delta / period), 1.0)
    rounded_progress_val = round(progress_val * 100)
    due_date = date.fromisoformat(reset_dt) + timedelta(days=int(period))

    txt = f'{desc} ({rounded_progress_val}%) 〰️ reset on {reset_dt} 〰️ period {period} 〰️ due date {due_date}'
    overdue = False
    if date_delta > period:
        overdue = True
        txt += f' 〰️ ⚠️ {date_delta - period} day(s) overdue'
    color = get_color(rounded_progress_val, overdue)

    st.markdown(f"""
        <div style="margin-bottom:8px;">
            <div style="font-size: 0.95em; margin-bottom: 4px;">{txt}</div>
            <div style="background-color: #eee; border-radius: 8px; height: 24px; width: 100%;">
                <div style="
                    width: {rounded_progress_val}%;
                    background-color: {color};
                    height: 100%;
                    border-radius: 8px;
                    text-align: right;
                    transition: width 0.5s;">
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def get_color(value, overdue):
    color_scheme = {
        'red': '#ff4b4b',
        'dark_red': '#5E0303',
        'yellow': '#ffd700',
        'green': '#4caf50'
    }

    if overdue:
        return color_scheme['dark_red']

    if value < 50:
        return color_scheme['green'] 
    elif value < 75:
        return color_scheme['yellow']
    else:
        return color_scheme['red']


@st.dialog('Reset Date')
def render_dt_picker(rec):
    new_reset_dt = st.date_input(f'Pick a reset date for {rec['desc']}:', max_value=date.today()).isoformat()
    if st.button('Confirm'):
        repo.update_reset_dt(rec, new_reset_dt)
        st.rerun()


@st.dialog('Edit Record')
def render_edit_dialog(rec):
    new_desc = st.text_input('New description:').strip()
    new_period = st.number_input('New period:', value=None, min_value=1)

    if st.button('Confirm'):
        if not new_desc and not new_period:
            st.toast('Description and period cannot be both empty!', icon='🚨')
            return
        repo.edit_rec(rec, new_desc, new_period)
        st.rerun()


@st.dialog('Are you sure?')
def render_del_rec_dialog(rec_id):
    col1, col2 = st.columns(2)
    if col1.button('No', type='primary'):
        st.rerun()
    if col2.button('Yes'):
        repo.del_rec(rec_id)
        st.rerun()


def compute_date_delta(reset_date_str):
    cst = pytz.timezone('America/Chicago')
    today = datetime.now(cst).date()
    reset_date = date.fromisoformat(reset_date_str)
    return (today - reset_date).days


if __name__ == '__main__':
    main()
