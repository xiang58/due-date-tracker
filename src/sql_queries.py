GET_ALL_INVENTORY = 'SELECT * FROM inventory'

UPDATE_INVENTORY = '''
    UPDATE inventory SET current_stock = ?
    WHERE inventory_id = ?
'''

RESET_INVENTORY = '''
    UPDATE inventory SET current_stock = max_stock
    WHERE inventory_id = ?
'''
