import sqlite3
import json

db_path = r"c:\Users\mbaigorria\minutas-ia\n8n_data\database.sqlite"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT name, nodes, connections FROM workflow_entity WHERE name LIKE '%chunking%';")
rows = cursor.fetchall()
for row in rows:
    data = {
        "name": row['name'],
        "nodes": json.loads(row['nodes']),
        "connections": json.loads(row['connections'])
    }
    with open(r"c:\Users\mbaigorria\minutas-ia\workflow_chunking_dump.json", "w") as f:
        json.dump(data, f, indent=2)
        print("Workflow dumped to workflow_chunking_dump.json")

conn.close()
