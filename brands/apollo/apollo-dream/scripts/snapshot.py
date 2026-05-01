#!/usr/bin/env python3
"""snapshot.py - 7天快照"""
import json, os
from datetime import datetime

SNAPSHOT_DIR = "/tmp/snapshots"

def create_snapshot(name, content):
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    path = os.path.join(SNAPSHOT_DIR, f"{name}.json")
    with open(path, 'w') as f:
        json.dump({"name": name, "content": content, "at": datetime.now().isoformat()}, f)
    return path

if __name__ == '__main__':
    path = create_snapshot("test", "测试内容")
    print(f"快照: {path}")
