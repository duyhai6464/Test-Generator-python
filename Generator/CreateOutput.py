from CreateInput import N
import os
import subprocess

solutionPath = '.\\Solutions\\'
testPath = '.\\test\\'


def runCpp(fileIn, fileOut, file_name):
    os.system(file_name + ' < ' + fileIn + ' > '+fileOut)


def runPy():
    pass


if __name__ == '__main__':
    CppSolve = 'solve.cpp'

    if CppSolve.endswith('.cpp'):
        ExeSolve = CppSolve[:-4]
        os.system('g++ ' + solutionPath + CppSolve +
                  ' -o ' + solutionPath + ExeSolve)

        print(CppSolve + ' ----> ' + ExeSolve + '.exe')

        for name in [str(i + 1) for i in range(N)]:
            runCpp(testPath + name + '.in',
                   testPath + name + '.out', solutionPath + ExeSolve)
            print('Created ' + name + '.out' + '  <----  ' + name + '.in')

    elif CppSolve.endswith('.py'):
        pass
