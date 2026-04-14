import os
import subprocess

problem_folder_path = os.path.dirname(os.path.abspath(__file__))
problem_name = 'D' # problem name, used to find solution file and test files
DEBUG = 1 # set to True to print debug information
TIME_LIMIT = 1 # seconds
ONLY_1_OUTPUT = 1 # set to True if the problem has only one valid output, so we can check the output without comparing with expected output

# path to solution file, should be in the same folder as this file name {problem_name}.py
solution_path = os.path.join(problem_folder_path, f"{problem_name}.py")
# input and output test files should be in the same folder as this file, with name format test.in and test.out
input_path = os.path.join(problem_folder_path, "test.in")
output_path = os.path.join(problem_folder_path, "test.out")
# run subprocess to execute solution file with input and check output vs expected output, if time is more than TIME_LIMIT seconds print "TLE"
out = subprocess.run(['python', solution_path], stdin=open(input_path, 'r'), 
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=TIME_LIMIT)
if out.returncode != 0:
    print("Runtime error:", out.stderr)
    exit(1)
expected_output = open(output_path, 'r').read().strip()
# if DEBUG is True, print the output only
if DEBUG:
    print(out.stdout.strip())
    exit(0)
# compare output with expected output or check the output if ONLY_1_OUTPUT is True
if ONLY_1_OUTPUT:
    if out.stdout.strip() == expected_output:
        print("Accepted")
        exit(0)
    print("Wrong Answer")
    # comparing output with expected output line by line to find the first line where they differ and print it
    output_lines = out.stdout.strip().split('\n')
    expected_lines = expected_output.split('\n')
    for i in range(min(len(output_lines), len(expected_lines))):
        if output_lines[i] != expected_lines[i]:
            print(f"First difference at line {i+1}:")
            print(f"Output: {output_lines[i]}")
            print(f"Expected: {expected_lines[i]}")
            break
    exit(0)

# for problems with multiple satisfying solutions we must check it by itself
# logic check more here
