# algorithms.py
# Disk scheduling algorithm implementations: FCFS, SSTF, SCAN, LOOK

from typing import List, Dict

def fcfs(requests: List[int], head: int) -> Dict:
    """First-Come First-Serve"""
    path = [head]
    total = 0
    for r in requests:
        total += abs(r - path[-1])
        path.append(r)
    return {"name": "FCFS", "order": requests, "path": path, "total_head_movement": total}

def sstf(requests: List[int], head: int) -> Dict:
    """Shortest Seek Time First"""
    remaining = requests.copy()
    pos = head
    path = [pos]
    total = 0
    while remaining:
        # nearest remaining request
        nearest = min(remaining, key=lambda x: abs(x - pos))
        total += abs(nearest - pos)
        pos = nearest
        path.append(pos)
        remaining.remove(nearest)
    return {"name": "SSTF", "order": [p for p in path[1:]], "path": path, "total_head_movement": total}

def scan(requests: List[int], head: int, direction: str = "right",
         disk_start: int = 0, disk_end: int = 199) -> Dict:
    """
    SCAN (elevator). If direction == 'right', head moves right first to disk_end,
    then reverses and moves left to disk_start.
    """
    path = [head]
    total = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])

    if direction == "right":
        # service right side
        for r in right:
            total += abs(r - path[-1])
            path.append(r)
        # travel to disk_end
        if path[-1] != disk_end:
            total += abs(disk_end - path[-1])
            path.append(disk_end)
        # now service left side (in descending)
        for r in reversed(left):
            total += abs(r - path[-1])
            path.append(r)
    else:
        # left first
        for r in reversed(left):
            total += abs(r - path[-1])
            path.append(r)
        if path[-1] != disk_start:
            total += abs(path[-1] - disk_start)
            path.append(disk_start)
        for r in right:
            total += abs(r - path[-1])
            path.append(r)

    # return only the serviced request order (exclude the extra end points if not actual requests)
    serviced = [x for x in path[1:] if x in requests]
    return {"name": "SCAN", "order": serviced, "path": path, "total_head_movement": total}

def look(requests: List[int], head: int, direction: str = "right") -> Dict:
    """
    LOOK algorithm: like SCAN but it reverses at the last request (doesn't go to disk end).
    """
    path = [head]
    total = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])

    if direction == "right":
        for r in right:
            total += abs(r - path[-1])
            path.append(r)
        for r in reversed(left):
            total += abs(r - path[-1])
            path.append(r)
    else:
        for r in reversed(left):
            total += abs(r - path[-1])
            path.append(r)
        for r in right:
            total += abs(r - path[-1])
            path.append(r)

    serviced = [x for x in path[1:] if x in requests]
    return {"name": "LOOK", "order": serviced, "path": path, "total_head_movement": total}
