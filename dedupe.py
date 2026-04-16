import json
import os

FILE = "data/seen.json"


def load_seen():
    if not os.path.exists(FILE):
        return set()

    with open(FILE, "r") as f:
        return set(json.load(f))


def save_seen(seen):
    with open(FILE, "w") as f:
        json.dump(list(seen), f)


def get_id(job):
    return job["url"]


def is_new(job, seen):
    return get_id(job) not in seen


def mark_seen(job, seen):
    seen.add(get_id(job))
