import sqlite3
import json
import sys

db_path = r"c:\Users\mbaigorria\minutas-ia\n8n_data\database.sqlite"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

try:
    cursor.execute("SELECT name, nodes FROM workflow_entity WHERE name LIKE '%chunking%';")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Workflow: {row['name']}")
        nodes_str = row['nodes']
        try:
            nodes = json.loads(nodes_str)
            for node in nodes:
                if node['type'] == 'n8n-nodes-base.webhook':
                    print("Webhook Node Config:")
                    print(json.dumps(node, indent=2))
        except Exception as e:
            print(f"Error parseando nodes: {e}")
            print(f"Raw: {nodes_str[:200]}...")
except Exception as e:
    print(f"Error querying: {e}")
    # Some versions use 'workflow' instead of 'workflow_entity'
    try:
        cursor.execute("SELECT name, nodes FROM workflow WHERE name LIKE '%chunking%';")
        rows = cursor.fetchall()
        for row in rows:
            print(f"Workflow: {row['name']}")
            nodes_str = row['nodes']
            nodes = json.loads(nodes_str)
            for node in nodes:
                if node['type'] == 'n8n-nodes-base.webhook':
                    print("Webhook Node Config:")
                    print(json.dumps(node, indent=2))
    except Exception as e2:
        print(f"Error queried workflow: {e2}")

conn.close()
