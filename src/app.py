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
    item_id, item_name, current_stock, max_stock = item
    percent = current_stock / max_stock
    st.progress(percent, item_name)
    num_consumed = st.number_input(key=f'num_input_{item_id}', label='Enter how many used:', min_value=0)
    st.button(key=f'btn_confirm_{item_id}', label='Confirm', 
        on_click=update_inventory, args=(item_id, current_stock - num_consumed))
    st.button(key=f'btn_reset_{item_id}', label='Reset', on_click=reset_inventory, args=(item_id,))


@db_connector
def update_inventory(db_cursor, item_id, num_consumed):
    db_cursor.execute(sql_queries.UPDATE_INVENTORY, (num_consumed, item_id))


@db_connector
def reset_inventory(db_cursor, item_id):
    db_cursor.execute(sql_queries.RESET_INVENTORY, (item_id,))


def main():
    draw_progress_bars()


if __name__ == '__main__':
    main()
