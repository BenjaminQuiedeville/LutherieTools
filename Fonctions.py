from copy import deepcopy
import numpy as np
import json
from codecs import open
from os import mkdir, path

from Classes import Matrices


def export(matrices: Matrices, exportfolder: str) -> None:

    """
    pour matrices.F, si f == NaN : f = -1000
    pour matrices.BdBSeuil, si b == NaN : b = nanmin(dBSeuil) et f = -1000
    pour matrices.Ksi, si ksi == Nan : ksi = 0 
    """

    deNaNination(matrices)

    matricesDict: dict = {
        "F" : matrices.F.tolist(),
        "B" : matrices.BdBSeuil.tolist(),
        "Ksi" : matrices.Ksi.tolist(),
        "T" : matrices.T.tolist()
    }

    filePath = "exports/" + exportfolder + "/matrices.json"
    exportdir: str= "exports/" + exportfolder

    if not path.isdir(exportdir):
        mkdir(exportdir)

    print(filePath)
    json.dump(
        matricesDict, 
        open(filePath, 'w', encoding='utf-8'), 
        separators=(',', ':'), 
        sort_keys=True, 
        indent=4
        ) # this saves the array in .json format

    return


def deNaNination(matrices: Matrices) -> None:

    matrices.F[matrices.BdBSeuil == -200] = -1000
    matrices.Ksi[matrices.Ksi is np.NaN or matrices.Ksi == np.Inf] = 0
    matrices.Ksi[:, 0] = np.zeros_like(matrices.Ksi[:,0])
            
    return


def seuil(matrices: Matrices, seuil: float) -> None:
    
    matrices.BdBSeuil = deepcopy(matrices.BdB)
    matrices.BdBSeuil[matrices.BdB < seuil] = -200

    return 