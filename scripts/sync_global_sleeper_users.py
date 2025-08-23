from pathlib import Path
import json

local_path = Path("sleeper_data/user_data_local.json")
global_path = Path("sleeper_data/user_data_global.json")

# Load local data
if local_path.exists():
    with local_path.open("r", encoding="utf-8") as f:
        local_data = json.load(f)
else:
    local_data = {}

# Load global data
if global_path.exists():
    with global_path.open("r", encoding="utf-8") as f:
        global_data = json.load(f)
else:
    global_data = {}

# Add missing key-value pairs from local to global
updated = False
for key, value in local_data.items():
    if key not in global_data:
        global_data[key] = value
        updated = True

# Save if updated
if updated:
    with global_path.open("w", encoding="utf-8") as f:
        json.dump(global_data, f, indent=4, ensure_ascii=False)
