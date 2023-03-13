import numpy as np

def stability(inMatrix: np.ndarray, numColsToVerify: int, 
              tolerancePourcent: float) -> np.ndarray:
    """stability : parcourt la matrice des fréquences matrices.F pour vérifier la stabilité des modes utilisés. Pour chaque colonne et pour chaque mode, on cherche si le mode apparaît dans les {numColsToVerify} colonnes suivantes. Si le mode apparait dans toutes les colonnes vérifiées, on le garde, sinon on le remplace par np.NaN.

    Args:
        inMatrix (np.ndarray): matrices des Fréquences
        numColsToVerify (int): nombre de colonnes à vérifier
        tolerancePourcent (float): tolérance pour la vérification en pourcents

    Returns:
        np.ndarray: la matrices des Fréquences apres vérification
    """
    def isValid(value: float, arrayToVerify: np.ndarray, 
                tolerance: float) -> bool:
        """isValid : compte le nombre de colonnes pour lesquelles np.isclose renvoie True, si le compte est égal au nombre de colonne à vérifier, renvoie True"""
        return (arrayToVerify.shape[1] 
                <= np.sum(np.isclose(value, arrayToVerify, 
                                     atol = tolerance, rtol = 0.)))
    
    # on vérifie si on est pas à la fin de la matrice
    # puis si le isValid renvoie True 
    # sinon le mode devient np.NaN
    # et ce pour tous les modes
    return np.array([
        mode 
        if ((inMatrix.shape[1] - col) > numColsToVerify
        and isValid(mode, 
                    inMatrix[:, (col+1):(col+numColsToVerify+1)],
                    mode * tolerancePourcent))
        else np.NaN
        for (row, col), mode in np.ndenumerate(inMatrix)])