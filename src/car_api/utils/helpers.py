from typing import Iterable

def next_id(existing_ids: Iterable[int]) -> int:
    """Return the next integer ID greater than max(existing_ids), starting at 1."""
    maximum = max(existing_ids) if existing_ids else 0
    return maximum + 1
