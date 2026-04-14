import os
import subprocess
import time

solutionPath = '.\\Solutions\\' # path to .py files of solutions(BruteForce.py, Solve.py, etc)
testPath = '.\\test\\'# path to .in and .out files of test cases

# name of the solution file to run, without extension
solveFileName =  'SegmentTree'
# solveFileName =  'BruteForce'

TIME_LIMIT = 10 # seconds

if __name__ == '__main__':
    # make sure solve file exists
    solvefilepath = os.path.join(solutionPath, solveFileName + '.py')
    if not os.path.exists(solvefilepath):
        print('Solution file not found:', solveFileName + '.py')
        exit(1)
    # find all file in test folder end with .in
    testFiles = [f for f in os.listdir(testPath) if f.endswith('.in')]
    for testFile in testFiles:
        print('Running test case:',  testFile, end='|')
        # run the solution file with input and check output vs expected output, if time is more than TIME_LIMIT second print "Time limit exceeded"
        solutionFile = os.path.join(solutionPath, solveFileName + '.py')
        testinputFile = os.path.join(testPath, testFile)
        testoutputFile = os.path.join(testPath, testFile.replace('.in', '.out'))
        # make sure testoutputFile exists, if not quit with error
        if not os.path.exists(testoutputFile):
            print('Expected output file not found:', testoutputFile)
            exit(1)
        with open(testinputFile, 'r') as input_f, open(testoutputFile, 'r') as expected_output:
            try:
                starttime = time.time()
                process = subprocess.Popen(['python', solutionFile],stdin=input_f, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, text=True, bufsize=1)
                for i, expected in enumerate(expected_output, 1):
                    # skip empty line in expected output
                    if not expected.strip(): continue
                    # timeout check
                    if time.time() - starttime > TIME_LIMIT:
                        process.kill()
                        print(f"TLE line {i} time {time.time() - starttime:.4f}")
                        exit(1)
                    
                    output = process.stdout.readline() if process.stdout else ""

                    if not output:
                        print(f"FAILED: thiếu output ở line {i}, expected: '{expected.strip()}'")
                        process.kill()
                        exit(1)

                    if output.strip() != expected.strip():
                        print(f"FAILED at line {i}, expected: '{expected.strip()}', got: '{output.strip()}'")
                        process.kill()
                        exit(1)
                else:
                    # kiểm tra dư output
                    extra = process.stdout.read() if process.stdout else ""
                    if extra.strip():
                        print("FAILED: dư output")
                        process.kill()
                        exit(1)
                    # check exit code
                    process.wait()
                    if process.returncode != 0:
                        print("RE (Runtime Error)")
                    else:
                        print(f"PASSED in {time.time() - starttime:.4f} seconds")
            except subprocess.TimeoutExpired:
                print("Time limit exceeded! Try others solution or optimize your code!")
                exit(1)
            except Exception as e:
                print("Error while running the solution:", e)
                exit(1)