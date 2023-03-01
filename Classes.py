import numpy as np

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