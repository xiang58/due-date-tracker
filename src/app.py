import streamlit as st

def main():
    if 'percent_left' not in st.session_state:
        st.session_state.percent_left = 100

    big_to_go_box = '大便当盒'
    st.progress(st.session_state['percent_left'], big_to_go_box)

    st.button('Decrement', on_click=update_precent_left)
    st.button("Reset", on_click=reset_precent_left)

def update_precent_left():
    if st.session_state.percent_left >= 20:
        st.session_state.percent_left -= 20

def reset_precent_left():
    st.session_state.percent_left = 100

if __name__ == '__main__':
    main()
