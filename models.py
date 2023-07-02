def create_table(conn):
    """ 
    Create the 'streets' table if it doesn't exist
    """ 
    conn.execute('''
        CREATE TABLE IF NOT EXISTS streets (
            u INTEGER,
            v INTEGER,
            key INTEGER,
            osmid BIGINT,
            lanes TEXT,
            ref TEXT,
            name TEXT,
            highway TEXT,
            maxspeed TEXT,
            oneway TEXT,
            reversed TEXT,
            length FLOAT,
            bridge TEXT,
            geometry LINESTRING,
            access TEXT,
            junction TEXT,
            tunnel TEXT
        )
    ''')