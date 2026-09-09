from client import SS2PLManager

def main():
    print("=== SS2PL Concurrency Manager & Deadlock Detector ===")
    mgr = SS2PLManager()
    mgr.acquire_exclusive(1, "resA")
    mgr.acquire_exclusive(2, "resB")
    mgr.acquire_exclusive(1, "resB") # Tx 1 waits for Tx 2
    mgr.acquire_exclusive(2, "resA") # Tx 2 waits for Tx 1

    res = mgr.detect_deadlock()
    print("Deadlock Detection Result:", res)
    assert res["deadlock"] is True

    print("SS2PL Deadlock Detector verified successfully!")

if __name__ == "__main__":
    main()
