CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INTEGER PRIMARY KEY,
    inventory_name TEXT NOT NULL,
    current_stock INTEGER DEFAULT 0 CHECK (current_stock >= 0),
    max_stock INTEGER DEFAULT 0 CHECK (max_stock >= 0),
    CHECK (current_stock <= max_stock)
);

INSERT INTO inventory (inventory_name, current_stock, max_stock)
VALUES ('大打包盒', 200, 200), ('小打包盒', 300, 300), ('叉子', 500, 500)
