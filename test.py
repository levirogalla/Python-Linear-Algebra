from main import Matrix, Vector

# v = Vector(1,0,1)
# A = Matrix([1,1], [2,1])
# B = Matrix([1,1,1,1,1,1,1],[1,1,1,3,1,1,1],[1,1,5,1,-3,1,-1],[-2,1,1,1,7,1,1],[5,1,3,1,1,2,1],[0,1,1,9,1,-8,1],[1,-1,1,9,1,4,1])
C = Matrix(
[1,3,5,-4,1],
[9,4,1, 1,1],
[4,9,2,-2,1],
[1,2,-3,1,1])        

# D = Matrix([1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],)


v = Vector(1,1)
c = Vector(2,1)


print(C.detS())   