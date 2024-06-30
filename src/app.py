import streamlit as st
import time

def main():
    big_to_go_box = '大便当盒'
    big_to_go_box_bar = st.progress(100, big_to_go_box)

    for percent_consumed in range(0, 101, 20):
        big_to_go_box_bar.progress(100 - percent_consumed, text=big_to_go_box)
        time.sleep(3)

    time.sleep(3)
    big_to_go_box_bar.empty()
    st.button("Rerun")

if __name__ == '__main__':
    main()
