import os 
import subprocess
import time
from pathlib import Path

problem_folder_path = os.path.dirname(os.path.abspath(__file__))
problem_name = r'pine' # problem name, used to find solution file and test files
# problem_name = r'X' # problem name, used to find solution file and test files
IS_BRUTE_FORCE = 0
TIME_LIMIT = 4 # seconds
ONLY_1_OUTPUT = 1 # set to True if the problem has only one valid output, so we can check the output without comparing with expected output
# path to solution file, should be in the same folder as this file name {problem_name}.py
solution_path = os.path.join(problem_folder_path, f"{problem_name}.py")
# input and output test files should be in the same folder as this file, with name format test.in and test.out
input_path = os.path.join(problem_folder_path, "test.in")
output_path = os.path.join(problem_folder_path, "test.out")
# run subprocess to execute solution file with input and check output vs expected output, if time is more than TIME_LIMIT seconds print "TLE"

print(f"Run '{solution_path}' with {input_path}")

with open(input_path, 'r') as f:
    INPUT: list[str] = f.read().split("EOF\n")
INPUT = [i for i in INPUT if i.strip()]
OUTPUT_EXPECTED = open(output_path, 'r')
LOG_OUT, LOG_ERR, NOT_PASS, RUNTIME = [], [], [], []
for TEST in range(1, len(INPUT) + 1):
    start_time = time.time()
    out = subprocess.run(['python', solution_path], input=INPUT[TEST - 1], 
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=TIME_LIMIT)
    RUNTIME.append(time.time() - start_time)
    if out.returncode != 0:
        print("Runtime error:", out.stderr)
        exit(1)
    print(f"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print(f">>>TEST:{TEST}>>>STDERR>>>:\n{out.stderr.strip()}")
    print(f">>>TEST:{TEST}>>>STDOUT>>>\n{out.stdout.strip()}")
    print(f"Time: {RUNTIME[-1]:.2f} seconds")
    LOG_ERR.append(out.stderr.strip())
    LOG_OUT.append(out.stdout.strip())
    if IS_BRUTE_FORCE: continue
    # compare output with expected output or check the output if ONLY_1_OUTPUT is True
    if ONLY_1_OUTPUT:
        # comparing output with expected output line by line to find the first line where they differ and print it
        output_lines = out.stdout.strip().split('\n')
        for i in range(len(output_lines)):
            expected_line = OUTPUT_EXPECTED.readline().strip()
            if output_lines[i].strip() != expected_line:
                print("Wrong Answer")
                print(f"First difference at line {i+1}:")
                print(f"Output: {output_lines[i]} || Expected: {expected_line}")
                NOT_PASS.append(TEST)
                break
        else:
            print("Accepted")
        continue
    # for problems with multiple satisfying solutions we must check it by itself
    # logic check more here
    input_data = list(map(int, INPUT[TEST - 1].split()))
    output_data = out.stdout.strip().splitlines()
    t = input_data[0]
    ptr = 1
    ptr2 = 0
    for i in range(t):
        n, m = input_data[ptr: ptr + 2]
        ptr += 2
        k = input_data[ptr: ptr + m]
        ptr += m
        result = list(map(int, output_data[ptr2].split()))
        ptr2 += 1
        expected_line = OUTPUT_EXPECTED.readline().strip()
        wrong = False
        if expected_line == '-1':
            if len(result) != 1 or result[0] != -1:
                wrong = True
        else:       
            if len(set(result)) != n or min(result) != 0 or max(result) != n - 1:
                wrong = True
            if not wrong:
                for j in range(1, n):
                    for ki in k:
                        if abs(result[j - 1] - result[j]) % ki == 0:
                            break# find 1 is ok
                    else:
                        wrong = True
                        break
                
        if wrong:
            print("Wrong Answer")
            print(f"First difference at line {i+1}:")
            print(f"Output: {result} || Expected: a{j} - a{j-1} = {abs(result[j - 1] - result[j])}")
            NOT_PASS.append(TEST)
            break
    else:
        print("Accepted")
        



if IS_BRUTE_FORCE:
    OUTPUT_EXPECTED.close()
    with open(output_path, 'w') as OUTPUT:
        OUTPUT.write('\n'.join(LOG_OUT))
    exit()
# after that we need check OUTPUT_EXPECTED is EOF
if len(NOT_PASS) == 0:
    line = OUTPUT_EXPECTED.readline()
    while line == '\n':
        line = OUTPUT_EXPECTED.readline()
    if line != "": print(f'Output is missing')

ROOT = Path(__file__).resolve().parent
with open(ROOT / "log.txt", 'w') as l:
    l.write('\n'.join(LOG_OUT))
    l.write('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
    l.write('\n'.join(LOG_ERR))

print(f"PASS: {len(INPUT) - len(NOT_PASS)} | NOT PASS: {NOT_PASS}")
print(f"BEST TIME: {min(RUNTIME):.2f} WORST TIME: {max(RUNTIME):.2f}")