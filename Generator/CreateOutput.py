import os
import subprocess
import time

solutionPath = '.\\Solutions\\' # path to .py files of solutions(BruteForce.py, Solve.py, etc)
testPath = '.\\test\\'# path to .in and .out files of test cases
# name of the solution file to run, without extension
# solveFileName =  'BruteForce'
solveFileName =  'Solve'

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
        # run the solution file and redirect input and output
        solutionFile = os.path.join(solutionPath, solveFileName + '.py')
        testinputFile = os.path.join(testPath, testFile)
        testoutputFile = os.path.join(testPath, testFile.replace('.in', '.out'))
        with open(testoutputFile, 'w') as output_f, open(testinputFile, 'r') as input_f:
            try:
                starttime = time.time()
                subprocess.run(['python', solutionFile], stdin=input_f, stdout=output_f, timeout=5)
                endtime = time.time()
                print(f' Time: {endtime - starttime:.4f} seconds')
            except subprocess.TimeoutExpired:
                print("Time limit exceeded 5 seconds! Try others solution or optimize your code!")
                exit(1)
        