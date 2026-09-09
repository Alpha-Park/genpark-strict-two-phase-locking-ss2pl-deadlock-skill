class SS2PLManager:
    """Strict Two-Phase Locking (SS2PL) with Deadlock Detection."""
    def __init__(self):
        self.locks = {} # item -> (lock_type, tx_id)
        self.wait_for = {} # tx_id -> waiting_for_tx_id

    def acquire_exclusive(self, tx_id: int, item: str) -> dict:
        if item in self.locks:
            holding_tx = self.locks[item][1]
            if holding_tx != tx_id:
                self.wait_for[tx_id] = holding_tx
                return {"granted": False, "waiting_on_tx": holding_tx}
        self.locks[item] = ('X', tx_id)
        if tx_id in self.wait_for:
            del self.wait_for[tx_id]
        return {"granted": True, "item": item, "tx_id": tx_id}

    def detect_deadlock(self) -> dict:
        for start in list(self.wait_for.keys()):
            visited = set()
            curr = start
            path = [curr]
            while curr in self.wait_for:
                curr = self.wait_for[curr]
                if curr in visited:
                    return {"deadlock": True, "cycle_participants": path + [curr]}
                visited.add(curr)
                path.append(curr)
        return {"deadlock": False, "cycle_participants": []}
