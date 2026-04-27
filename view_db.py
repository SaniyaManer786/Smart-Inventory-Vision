import sqlite3
import pandas as pd

conn = sqlite3.connect('inventory.db')
df = pd.read_sql("SELECT * FROM inventory", conn)
print(df)
conn.close()
