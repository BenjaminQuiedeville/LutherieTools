import numpy as np
from copy import deepcopy

def stability(inMatrix: np.ndarray, numcolstoverify: int, 
            tolerancePourcent: float) -> np.ndarray:
    
    modesValides = []
    numcols = inMatrix.shape[1]
    outMatrix = deepcopy(inMatrix)

    for (rowIndex, colIndex), mode in np.ndenumerate(inMatrix):

        tolerance = mode * tolerancePourcent

        # if mode in modesValides: 
        #     continue 
        
        if ((numcols - colIndex) > numcolstoverify 
        and isValid(mode, inMatrix[:, (colIndex+1):numcolstoverify], tolerance)):

            # modesValides.append(mode)
            continue
            
        else: 
            outMatrix[rowIndex, colIndex] = np.nan

    return outMatrix


def isValid(value: float, arrayToVerify: np.ndarray, tolerance: float) -> bool:

    numcols: int = arrayToVerify.shape[1]
    numOfValidCols: int = 0

    for colIndex in range(numcols):

        if isInInterval(value, arrayToVerify[:, colIndex], tolerance):
            numOfValidCols += 1

    return numOfValidCols == numcols

    
def isInInterval(value: float, vector: np.ndarray, tolerance: float) -> bool:

    result: bool = False

    for _, vectorelem in np.ndenumerate(vector):
        if (value >= vectorelem - tolerance and 
            value <= vectorelem + tolerance):

            result = True

    return result