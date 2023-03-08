import numpy as np
from scipy.io.wavfile import read
from scipy.signal import decimate
import json
from typing import Literal

from Classes import Params
from SignauxTest import creationSignauxTest


def preset(creationPreset: str,
           paramsPath: str,
           signalPreset: Literal["diapason",
                                 "cordeIdeale",
                                 "guitareSimulee", 
                                 "guitareCorps",
                                 "guitareModesDoubles", 
                                 "guitareBruit"]
           ) -> tuple[np.ndarray, Params]:
    """
    Fonction déterminant quel signal et paramètres on utilisera : 
    - "gen" : signal généré
    - "sample" : un fichier déterminé par son chemin
    - "json" : comme "json" mais utilisé pour appeler le programme depuis le terminal du serveur 

    Args:
        preset (str): "gen", "sample", "json"
        signalPreset (str): preset pour le signal à générer
        paramsPath (str): le chemin vers le fichier .json contenant les paramètres 

    Returns:
        tuple[np.ndarray, Params, str]:
        signal, params, exportfolder
    """    
    params = Params()

    if creationPreset == "gen":
        
        params.samplerate = 48000
        duree: float = 2.0
        signal = creationSignauxTest(duree, params.samplerate, signalPreset)
            
        params.horizon = 0.05
        params.overlap = 0.
        params.nbPoles = 50

    elif creationPreset == "sample":
        
        [params.samplerate, signal] = read(f"clips_audio/{signalPreset}.wav")
        
        params.horizon = 0.05
        params.overlap = 0.50
        params.nbPoles = 50
        
    elif creationPreset == 'json': 
        
        argsDict = json.load(open(paramsPath))
        
        [params.samplerate, signal] = read(argsDict["filepath"])
        
        params.horizon = argsDict["horizon"]
        params.overlap = argsDict["overlap"]
        params.nbPoles = argsDict["nbPoles"]
        params.exportFolder = "export_" + argsDict["exportfolder"]
            

    signal, params = preparation(signal, params)

    return signal, params


def preparation(signal: np.ndarray, params: Params):

    if signal.ndim > 1 : signal = signal[:, 0]

    signal = signal/np.max(signal)

    if params.samplerate > 40000: 
        downSamplingFactor:int = 4
        signal = decimate(signal, downSamplingFactor)
        params.samplerate //= downSamplingFactor

    return signal, params