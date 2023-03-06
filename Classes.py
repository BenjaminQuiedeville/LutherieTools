import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import json
from codecs import open
from os import mkdir
from os.path import isdir


class Params:

    def __init__(self) -> None:
        
        self.samplerate: int = 0
        self.horizon: float = 0.
        self.overlap: float = 0.
        self.nbPoles: int = 0
        self.exportfolder: str = ""


class Matrices:
    def __init__(self, nbPoles, nbFenetres) -> None:
        self.F: np.ndarray = np.zeros((nbPoles, nbFenetres))
        self.FStable: np.ndarray = np.array([])        

        self.B: np.ndarray = np.zeros((nbPoles, nbFenetres))
        self.BSeuil: np.ndarray = np.array([])

        self.Ksi: np.ndarray = np.zeros((nbPoles, nbFenetres))
        self.J: np.ndarray = np.zeros(nbFenetres)    
        self.T: np.ndarray = np.array([])  


    def antialiasingFilter(self, samplerate: int) -> None:

        self.F[self.F > 0.5*samplerate] = np.nan
        self.B[np.isnan(self.F)] = np.nan
        self.Ksi[np.isnan(self.F)] = np.nan

    
    def seuil(self, seuil: float) -> None:
        self.BSeuil = self.B.copy()
        self.BSeuil[self.B < (np.nanmax(self.B) + seuil)] = np.NaN
        self.F[np.isnan(self.BSeuil)] = np.NaN


    def deNaNination(self) -> None:
        self.F[self.BSeuil == -200] = -1000
        self.Ksi[np.isnan(self.Ksi) or self.Ksi == np.Inf] = 0
        self.Ksi[:, 0] = np.zeros_like(self.Ksi[:,0])
    

    def export(self,
            signal: np.ndarray,  
            samplerate: int, 
            exportFolder: str
            ) -> None:

        """
        pour matrices.F, si f == NaN : f = -1000
        pour matrices.BdBSeuil, si b == NaN : b = nanmin(dBSeuil) et f = -1000
        pour matrices.Ksi, si ksi == Nan : ksi = 0 
        """
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


        self.deNaNination()

        matricesDict: dict = {
            "F" : self.FStable.tolist(),
            "B" : self.BSeuil.tolist(),
            "Ksi" : self.Ksi.tolist(),
            "T" : self.T.tolist()
        }

        exportDir: str= f"exports/{exportFolder}"
        jsonFilePath = f"{exportDir}/matrices.json"

        if not isdir(exportDir): mkdir(exportDir)

        print(f"données exportées dans : {exportDir}")
        # this saves the array in .json format
        json.dump(matricesDict, open(jsonFilePath, 'w', encoding='utf-8'), 
                separators=(',', ':'), sort_keys=True, indent=4) 

        exportSpectrogramme(spectrogramme(signal, samplerate), 
                            exportDir)