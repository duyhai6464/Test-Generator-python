import os
import subprocess


def runCpp(fileIn, fileOut, file_name='solve.exe'):
    with open('test/' + fileOut, 'w'):
        os.system(file_name + ' < ' + fileIn + ' > '+fileOut)


def runPy():
    pass


if __name__ == '__main__':
    CppSolve = 'solve.cpp'

    ListFile = [f[:-3] for f in os.listdir('test/') if f.endswith('.in')]

    if CppSolve.endswith('.cpp'):
        ExeSolve = CppSolve[:-4] + '.exe'
        os.system('g++ ' + CppSolve + ' -o ' + ExeSolve)
        print(CppSolve + ' -> ' + ExeSolve)

        for name in ListFile:
            runCpp(name + '.in', name + '.out', ExeSolve)
            print('Created ' + name + '.out' + '  <----  ' + name + '.in')

    elif CppSolve.endswith('.py'):
        pass
