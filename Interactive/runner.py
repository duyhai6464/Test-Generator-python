import subprocess
import threading
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SOLVER = [sys.executable, str(ROOT / "solution.py")]
INTERACTOR = [sys.executable, str(ROOT / "interactor.py")]
LOG_FILE = ROOT / "log.txt"
TIME_LIMIT = 10


def bridge(src, dst, tag, log_file):
    try:
        while True:
            data = src.readline()
            if not data:
                break
            log_file.write(f"[{tag}] {data.decode()}")
            log_file.flush()
            dst.write(data)
            dst.flush()
    except:
        pass


def main():
    sol = subprocess.Popen(
        SOLVER,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr
    )

    itr = subprocess.Popen(
        INTERACTOR,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr
    )
    
    with open(LOG_FILE, 'w') as logg:
        t1 = threading.Thread(target=bridge, args=(sol.stdout, itr.stdin, ">>>S>>I>>>", logg), daemon=True)
        t2 = threading.Thread(target=bridge, args=(itr.stdout, sol.stdin, "<<<S<<I<<<", logg), daemon=True)

        t1.start()
        t2.start()

        start = time.time()

        while True:
            if sol.poll() is not None or itr.poll() is not None:
                break

            if time.time() - start > TIME_LIMIT:
                print("TLE - killing processes")
                sol.kill()
                itr.kill()
                break

            time.sleep(0.01)

        t1.join(timeout=1)
        t2.join(timeout=1)

        print("DONE")
    


if __name__ == "__main__":
    main()