import numpy as np

from EstimationParametres import estimation
from Classes import Params, Matrices 
from Stability import stability


def HROgramme(signal: np.ndarray, params: Params) -> Matrices:
    """Fonction principale du programme, détermine les matrices de HROgrammes pour un signal {signal} donné et un jeu de paramêtres d'analyse {params}.
    """
    
    seuil: int = -40 #(dB)
    # algorithme de stabilité
    toleranceStabilite = 0.5 
    numColsToVerify = 2

    signalLengthInSamples: int = signal.size
    signalLengthInSeconds: float = signal.size/params.samplerate
    
    samplesPerHorizon: int = int(params.horizon * params.samplerate)
    samplesPerOverlap: int = int(samplesPerHorizon * params.overlap)
    pointer: int = 0
    
    numWindows: int = int(signalLengthInSamples/(samplesPerHorizon*(1 - params.overlap)))
    
    matrices = Matrices(params.nbPoles, numWindows)
    matrices.T = np.tile(
        np.linspace(0, signalLengthInSeconds, matrices.F.shape[1]), 
        (params.nbPoles, 1))
    
    print(f"taille de fenetre (samples) = {samplesPerHorizon}")
    print(f'nbFenetres = {numWindows}')
    
    for k in range(numWindows):
        
        if k % 10 == 0 : print(f'{k}/{numWindows}') 
            
        pointer = int(k*(samplesPerHorizon - samplesPerOverlap) + 1)
        
        if (pointer + samplesPerHorizon) > signalLengthInSamples: break 
        
        window: np.ndarray = signal[pointer : pointer + samplesPerHorizon].copy()
        
        parametresEstimes = estimation(window, params.samplerate, 
                                                 params.nbPoles)
        matrices.F[:, k] = parametresEstimes["f"]
        matrices.B[:, k] = parametresEstimes["b"] 
        matrices.Ksi[:, k] = parametresEstimes["ksi"]
        matrices.J[k] = parametresEstimes["J"]
        
    matrices.antialiasingFilter(params.samplerate)
    
    # seuillage de la matrice des B
    matrices.B[matrices.B <= 0] = np.nan
    matrices.B = 20*np.log10(matrices.B)
    matrices.seuil(seuil)

    matrices.FStable = stability(matrices.F, numColsToVerify, 
                                toleranceStabilite)

    return matrices