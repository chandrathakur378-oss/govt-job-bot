import json
import os

FILE = "data/seen.json"

def load_seen():
    if not os.path.exists(FILE):
        return []
    return json.load(open(FILE))

def save_seen(data):
    json.dump(data, open(FILE, "w"))

def is_new(job, seen):
    return job["url"] not in seen

def mark_seen(job, seen):
    seen.append(job["url"])