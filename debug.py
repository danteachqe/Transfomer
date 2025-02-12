import json
import os

json_file = "playwright_files.json"

if not os.path.exists(json_file):
    print(f"[DEBUG] JSON file not found: {json_file}")
else:
    with open(json_file, "r", encoding="utf-8") as f:
        raw = f.read()
        print("[DEBUG] Raw JSON read:\n", raw)
        try:
            data = json.loads(raw)
            print("[DEBUG] type(data) =", type(data))
        except Exception as e:
            print("[DEBUG] JSON decode error:", e)