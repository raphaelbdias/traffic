import sqlite3
from models import create_table

# Connect to the SQLite database
conn = sqlite3.connect("streets_data.db")

# Execute the create_table function
create_table(conn)

# Close the connection to the database
conn.close()
