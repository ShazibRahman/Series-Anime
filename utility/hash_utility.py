import hashlib


def order_independent_hash(lst):
    # Sort the list to normalize order
    sorted_lst = sorted(lst)

    # Optional: use deterministic string representation
    serialized = "".join(str(x) for x in sorted_lst)

    # Hash it using SHA-256 (or any algorithm you prefer)
    return hashlib.sha256(serialized.encode()).hexdigest()
