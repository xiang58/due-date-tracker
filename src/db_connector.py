import os
import sqlite3

def db_connector(f):

    env = os.getenv('STREAMLIT_ENV', 'local')
    db_path = ''

    if env == 'local':
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'church_inventory_local.db'))
    else:
        raise Exception('Unknown env')
    
    def _with_connection(*args, **kwargs):
        conn = sqlite3.connect(db_path)
        try:
            rv = f(conn, *args, **kwargs)
        except Exception:
            conn.rollback()
            raise
        else:
            conn.commit()
        finally:
            conn.close()
        return rv

    return _with_connection
