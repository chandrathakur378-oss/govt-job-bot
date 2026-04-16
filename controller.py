import json

FILE = "data/control.json"

def get_status():
    try:
        with open(FILE, "r") as f:
            return json.load(f).get("status", "running")
    except:
        return "running"

def set_status(status):
    with open(FILE, "w") as f:
        json.dump({"status": status}, f)