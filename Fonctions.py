from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import json
from codecs import open
from os import mkdir, path

from Classes import Matrices


def export(signal: np.ndarray, 
        matrices: Matrices, 
        samplerate: int, 
        exportFolder: str
        ) -> None:

    """
    pour matrices.F, si f == NaN : f = -1000
    pour matrices.BdBSeuil, si b == NaN : b = nanmin(dBSeuil) et f = -1000
    pour matrices.Ksi, si ksi == Nan : ksi = 0 
    """

    deNaNination(matrices)

    matricesDict: dict = {
        "F" : matrices.FStable.tolist(),
        "B" : matrices.BdBSeuil.tolist(),
        "Ksi" : matrices.Ksi.tolist(),
        "T" : matrices.T.tolist()
    }

    exportDir: str= f"exports/{exportFolder}"
    jsonFilePath = f"{exportDir}/matrices.json"

    if not path.isdir(exportDir): mkdir(exportDir)

    print(f"données exportées dans : {exportDir}")
    # this saves the array in .json format
    json.dump(matricesDict, open(jsonFilePath, 'w', encoding='utf-8'), 
            separators=(',', ':'), sort_keys=True, indent=4) 

    exportSpectrogramme(spectrogramme(signal, samplerate), 
                        exportDir)


def deNaNination(matrices: Matrices) -> None:
    matrices.F[matrices.BdBSeuil == -200] = -1000
    matrices.Ksi[matrices.Ksi is np.NaN or matrices.Ksi == np.Inf] = 0
    matrices.Ksi[:, 0] = np.zeros_like(matrices.Ksi[:,0])
            

def seuil(matrices: Matrices, seuil: float) -> None:
    matrices.BdBSeuil = deepcopy(matrices.BdB)
    matrices.BdBSeuil[matrices.BdB < seuil] = -200


def spectrogramme(signal: np.ndarray, samplerate: int) -> Figure:

    nfft = 1024
    fig, ax = plt.subplots(frameon = False)
    ax.specgram(signal, NFFT = nfft, noverlap=nfft//2, Fs = samplerate)
    ax.set_ylim([0, 3500])
    ax.set_axis_off()

    return fig


def exportSpectrogramme(fig: Figure, exportFolder: str) -> None:

    fig.savefig(f"{exportFolder}/spectrogram.png", 
                bbox_inches = "tight", dpi = 1500)
    plt.close(fig)
