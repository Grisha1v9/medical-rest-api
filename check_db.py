import sqlite3

con = sqlite3.connect("medical.db")
cur = con.cursor()

print("schema")
for row in cur.execute("SELECT sql FROM sqlite_master WHERE name='results'"):
    print(row[0])

print("\nrows")
for row in cur.execute("SELECT id, age, risk_level, created_at FROM results"):
    print(row)