# utils.py
# helper functions: parse input and compute metrics

from typing import List, Dict

def parse_requests(text: str) -> List[int]:
    """
    Accepts comma or space separated numbers, e.g.
    "98, 183, 37"  or  "98 183 37"
    """
    if text is None:
        return []
    txt = text.strip()
    if txt == "":
        return []
    # replace commas with spaces, split on whitespace
    parts = txt.replace(',', ' ').split()
    nums = []
    for p in parts:
        try:
            nums.append(int(p))
        except ValueError:
            raise ValueError(f"Invalid request value: {p}")
    return nums

def compute_disk_metrics(path: List[int], requests_count: int, seek_time_per_cylinder_ms: float = 1.0) -> Dict:
    """
    path: list of cylinder positions visited (including starting head)
    requests_count: number of actual requests (not counting artificial ends)
    seek_time_per_cylinder_ms: estimated time to move one cylinder in milliseconds
    """
    total_movement = 0
    for i in range(1, len(path)):
        total_movement += abs(path[i] - path[i-1])

    avg_seek = total_movement / requests_count if requests_count > 0 else 0.0
    total_time_seconds = (total_movement * seek_time_per_cylinder_ms) / 1000.0
    throughput = (requests_count / total_time_seconds) if total_time_seconds > 0 else 0.0

    return {
        "total_head_movement": int(total_movement),
        "average_seek_distance": round(avg_seek, 3),
        "total_time_seconds": round(total_time_seconds, 5),
        "throughput_req_per_sec": round(throughput, 3)
    }
