import Stability
import numpy as np


# matrice = np.array(
#     [[1, 100, 100, 100, 20, 30],
#     [200, 200, 200, 100, 1000, 60]], 
#     dtype = 'float64')

matrice = np.random.rand(5,5)

outMatrice = Stability.stability(matrice, 3, 0.05)

print(matrice)
print("\n")
print(outMatrice)