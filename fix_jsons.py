import json
import os

workflows_dir = r'c:\Users\mbaigorria\minutas-ia\workflows'
for filename in os.listdir(workflows_dir):
    if filename.endswith('.json'):
        path = os.path.join(workflows_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except:
                continue
        
        # Add required fields for n8n CLI import
        if 'active' not in data:
            data['active'] = False
        if 'settings' not in data:
            data['settings'] = {}
        if 'tags' not in data:
            data['tags'] = []
        if 'versionId' not in data:
            data['versionId'] = 1
        
        # Write back
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Fixed {filename}")
