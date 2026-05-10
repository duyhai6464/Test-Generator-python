import subprocess
import sys
from pathlib import Path
import problem

ROOT = Path(__file__).resolve().parent
SOL = [sys.executable, str(ROOT / "solution.py")]
LOG_FILE = ROOT / "log.txt"

def run_solution(input_data: str):
    p = subprocess.run(
        SOL,
        input=input_data.encode(),
        stdout=subprocess.PIPE,
        stderr=sys.stderr
    )
    return p.returncode, p.stdout.decode().strip()


def main():
    with open(LOG_FILE, 'w') as logg:
        test_data = problem.generate_test()

        # phase 1
        inp1 = problem.make_input_phase1(test_data)
        logg.write(f">>>INPUT1>>>\n{inp1}\n")
        code, out1 = run_solution(inp1)
        logg.write(f"<<<OUTPUT1<<<\n{out1}\n")

        if code != 0:
            print("Crash phase1")
            print(inp1)
            return

        ok, processed = problem.validate_phase1(test_data, out1)
        if not ok:
            print("Invalid phase1")
            print(out1)
            return

        # phase 2
        inp2 = problem.make_input_phase2(test_data, processed)
        logg.write(f">>>INPUT2>>>\n{inp2}\n")
        code, out2 = run_solution(inp2)
        logg.write(f"<<<OUTPUT2<<<\n{out2}\n")

        if code != 0:
            print("Crash phase2")
            return

        ok = problem.validate_phase2(test_data, out2)

        if not ok:
            print("Wrong answer")
            print(test_data)
            print(out1)
            print(out2)
            return
        print("AC")


if __name__ == "__main__":
    main()