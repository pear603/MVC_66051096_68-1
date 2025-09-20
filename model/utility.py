import json

def load_data(file_path='model/data.json'):
    import os, json
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return []
    
    toStore = []
    with open(file_path, 'r') as f:
        data = json.load(f)

    for item in data:
        toStore.append(item)
        # to appened in array
    return toStore

def save_data(toStore, file_path='Model/data.json'):
    with open(file_path, 'w') as f:
        json.dump([toStore.to_dict() for f in toStore], f, indent=4)

# other generic utility functions can be added here