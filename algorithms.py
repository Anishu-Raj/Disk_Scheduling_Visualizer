# algorithms.py
from typing import List, Dict

def fcfs(requests: List[int], head: int) -> Dict:
    path = [head]
    total = 0
    for r in requests:
        total += abs(r - path[-1])
        path.append(r)
    return {"name": "FCFS", "order": requests, "path": path, "total_head_movement": total}

def sstf(requests: List[int], head: int) -> Dict:
    remaining = requests.copy()
    pos = head
    path = [pos]
    total = 0
    while remaining:
        nearest = min(remaining, key=lambda x: abs(x - pos))
        total += abs(nearest - pos)
        pos = nearest
        path.append(pos)
        remaining.remove(nearest)
    return {"name": "SSTF", "order": [p for p in path[1:]], "path": path, "total_head_movement": total}

def scan(requests: List[int], head: int, direction: str = "right",
         disk_start: int = 0, disk_end: int = 199) -> Dict:
    path = [head]
    total = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])
    if direction == "right":
        for r in right:
            total += abs(r - path[-1]); path.append(r)
        if path[-1] != disk_end:
            total += abs(disk_end - path[-1]); path.append(disk_end)
        for r in reversed(left):
            total += abs(r - path[-1]); path.append(r)
    else:
        for r in reversed(left):
            total += abs(r - path[-1]); path.append(r)
        if path[-1] != disk_start:
            total += abs(path[-1] - disk_start); path.append(disk_start)
        for r in right:
            total += abs(r - path[-1]); path.append(r)
    serviced = [x for x in path[1:] if x in requests]
    return {"name": "SCAN", "order": serviced, "path": path, "total_head_movement": total}

def look(requests: List[int], head: int, direction: str = "right") -> Dict:
    path = [head]
    total = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])
    if direction == "right":
        for r in right:
            total += abs(r - path[-1]); path.append(r)
        for r in reversed(left):
            total += abs(r - path[-1]); path.append(r)
    else:
        for r in reversed(left):
            total += abs(r - path[-1]); path.append(r)
        for r in right:
            total += abs(r - path[-1]); path.append(r)
    serviced = [x for x in path[1:] if x in requests]
    return {"name": "LOOK", "order": serviced, "path": path, "total_head_movement": total}

def c_scan(requests: List[int], head: int, disk_start: int = 0, disk_end: int = 199) -> Dict:
    path = [head]
    total = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])
    for r in right:
        total += abs(r - path[-1]); path.append(r)
    if path[-1] != disk_end:
        total += abs(disk_end - path[-1]); path.append(disk_end)
    if left:
        path.append(disk_start)
        for r in left:
            total += abs(r - path[-1]); path.append(r)
    serviced = [x for x in path[1:] if x in requests]
    return {"name": "C-SCAN", "order": serviced, "path": path, "total_head_movement": total}

def c_look(requests: List[int], head: int) -> Dict:
    path = [head]
    total = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])
    for r in right:
        total += abs(r - path[-1]); path.append(r)
    if left:
        path.append(min(left))
        for r in left:
            total += abs(r - path[-1]); path.append(r)
    serviced = [x for x in path[1:] if x in requests]
    return {"name": "C-LOOK", "order": serviced, "path": path, "total_head_movement": total}
