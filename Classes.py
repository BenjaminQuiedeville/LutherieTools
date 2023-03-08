import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import json
from codecs import open
from os import mkdir
from os.path import isdir


class Params:
    """Classe contenant les paramêtres utilisés pour l'analyse
    
    samplerate (int) : fréquence d'échantillonnage
    
    horizon (float) : longueur des fenêtres de calcul, équivalent à la taille de fenêtre de la STFT.
    
    overlap (float): taux de recouvrement entre les fenêtres de calcul
    
    nbPoles (int) : nombre de Poles à calculer par la méthodes ESPRIT

    exortFolder (str) : dossier d'export pour les résultats et le retour vers le serveur
    """

    def __init__(self) -> None:
        
        self.samplerate: int = 0
        self.horizon: float = 0.
        self.overlap: float = 0.
        self.nbPoles: int = 0
        self.exportFolder: str = ""


class Matrices:
    """Classe contenant les matrices F, FStable, B, BSeuil, Ksi, J et T des résultats
    """
    def __init__(self, nbPoles: int, nbFenetres: int) -> None:
        """Initialise les matrices de résultats avec les tailles adéquates

        Args:
            nbPoles (int): le nombre de poles dans le résultats est le nombre de lignes des matrices.

            nbFenetres (int): le nombre de fenêtres découpées dans le signal est le nombre de colonnes des matrices.
        """
        self.F: np.ndarray = np.zeros((nbPoles, nbFenetres))
        self.FStable: np.ndarray = np.array([])        

        self.B: np.ndarray = np.zeros((nbPoles, nbFenetres))
        self.BSeuil: np.ndarray = np.array([])

        self.Ksi: np.ndarray = np.zeros((nbPoles, nbFenetres))
        self.J: np.ndarray = np.zeros(nbFenetres)    
        self.T: np.ndarray = np.array([])  


    def antialiasingFilter(self, samplerate: int) -> None:
        """Supprime les modes supérieurs à la fréquence de Nyquist par sécurité"""
        self.F[self.F > 0.5*samplerate] = np.nan
        self.B[np.isnan(self.F)] = np.nan
        self.Ksi[np.isnan(self.F)] = np.nan

    
    def seuil(self, seuildB: float) -> None:
        """Supprime les modes dont l'amplitude en dB est inférieure à seuildB. Supprime égalment les fréquences associées."""
        self.BSeuil = self.B.copy()
        self.BSeuil[self.B < (np.nanmax(self.B) + seuildB)] = np.NaN
        self.F[np.isnan(self.BSeuil)] = np.NaN


    def deNaNination(self) -> None:
        """Supprime les valeurs np.NaN des matrices avant export vers le serveur qui ne peut pas les interpréter."""
        self.F[np.isnan(self.BSeuil)] = -1000
        self.Ksi[np.isnan(self.Ksi) or np.isinf(self.Ksi)] = 0
    

    def export(self,signal: np.ndarray,  samplerate: int, 
                exportFolder: str) -> None:
        """Exporte les matrices des résultats dans un fichier JSON. """

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

        # définition du dictionnaire à stocker sous forme de JSON
        matricesDict: dict = {
            "F" : self.FStable.tolist(),
            "B" : self.BSeuil.tolist(),
            "Ksi" : self.Ksi.tolist(),
            "T" : self.T.tolist()
        }

        exportDir: str= f"exports/{exportFolder}"
        jsonFilePath = f"{exportDir}/matrices.json"

        # si le dossier d'export n'existe pas, on le crée
        if not isdir(exportDir): mkdir(exportDir)

        print(f"données exportées dans : {exportDir}")
        # écriture du de matricesDict dans le JSON
        json.dump(matricesDict, open(jsonFilePath, 'w', encoding='utf-8'), 
                separators=(',', ':'), sort_keys=True, indent=4) 

        # export du spectrogramme pour fournir une image de fond
        exportSpectrogramme(spectrogramme(signal, samplerate), 
                            exportDir)