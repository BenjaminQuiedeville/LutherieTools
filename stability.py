import numpy as np

def stability(inMatrix: np.ndarray, numColsToVerify: int, 
              tolerancePourcent: float) -> np.ndarray:
    """stability : parcourt la matrice des fréquences matrices.F pour vérifier la stabilité des modes utilisés. Pour chaque colonne et pour chaque mode, on cherche si le mode apparaît dans les {numColsToVerify} colonnes suivantes. Si le mode n'apparait pas dans toutes les colonnes vérifiées, on le remplace par np.NaN, sinon on le conserve.

    isInIntervalle : 


    Args:
        inMatrix (np.ndarray): matrices des Fréquences
        numColsToVerify (int): nombre de colonnes à vérifier
        tolerancePourcent (float): tolérance pour la vérification en pourcents

    Returns:
        np.ndarray: la matrices des Fréquences apres vérification
    """
    def isValid(value: float, arrayToVerify: np.ndarray, 
                tolerance: float) -> bool:
        """isValid : compte le nombre de colonnes pour lesquelles isInInterval renvoie True, si le compte est égal au nombre de colonne à vérifier, renvoie True"""

        return ((numcols := arrayToVerify.shape[1]) 
            == np.sum([isInInterval(value, arrayToVerify[:, i], tolerance) 
                      for i in range(numcols)]))
    

    def isInInterval(value: float, vector: np.ndarray, 
                     tolerance: float) -> bool:
        """Recherche si {value} apparait dans {vector} à {tolerance} près."""
        return ((value >= vector - tolerance) 
              & (value <= vector + tolerance)).any()


    numcols = inMatrix.shape[1]
    outMatrix = inMatrix.copy()

    for (rowIndex, colIndex), mode in np.ndenumerate(inMatrix):

        tolerance = mode * tolerancePourcent
        
        # on arrête la boucle avant la fin pour 
        # éviter le dépacement hors de la matrice
        if not ((numcols - colIndex) > numColsToVerify 
            and isValid(mode, inMatrix[:, (colIndex+1):numColsToVerify], 
                        tolerance)):
            outMatrix[rowIndex, colIndex] = np.nan
                        
    return outMatrix