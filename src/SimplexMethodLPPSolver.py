if __name__ == '__main__':
   import SimplexMethodLPPSolver
   SimplexMethodLPPSolver.simplex('max', '3x1+2x2', ['2x1+x2<=18', '2x1+3x2<=42', '3x1+x2<=24'])
