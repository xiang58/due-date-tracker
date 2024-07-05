import streamlit as st

import sql_queries
from db_connector import db_connector


@db_connector
def get_all_inventory(db_cursor):
    return list(db_cursor.execute(sql_queries.GET_ALL_INVENTORY))


def draw_progress_bars():
    inventory = get_all_inventory()
    for item in inventory:
        draw_progress_bar(item)


def draw_progress_bar(item):
    item_name, current_stock, max_stock = item[0], item[1], item[2]
    percent = current_stock / max_stock
    st.progress(percent, item_name)


def main():
    draw_progress_bars()


if __name__ == '__main__':
    main()
