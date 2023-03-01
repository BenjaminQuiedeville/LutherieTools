import numpy as np
from copy import deepcopy

from EstimationParametres import parametersEstimation
from Classes import Params, Matrices 
import Fonctions
from Stability import stability


def HROgramme(signal: np.ndarray, params: Params) -> Matrices:

    signalLengthInSamples: int = signal.size
    signalLengthInSeconds: float = signal.size/params.samplerate

    
    samplesPerHorizon: int = int(params.horizon * params.samplerate)
    samplesPerOverlap: int = int(samplesPerHorizon * params.overlap)
    pointer: int = 0
    
    numWindows: int = int(signalLengthInSamples/(samplesPerHorizon*(1 - params.overlap)))
    
    matrices = Matrices(params.nbPoles, numWindows)
    
    print(f"taille de fenetre (samples) = {samplesPerHorizon}")
    print(f'nbFenetres = {numWindows}')
    
    for k in range(numWindows):
        
        if k % 10 == 0 : print(f'{k}/{numWindows}') 
            
        pointer = int(k*(samplesPerHorizon - samplesPerOverlap) + 1)
        
        if (pointer + samplesPerHorizon) > signalLengthInSamples: break 
        
        window: np.ndarray = deepcopy(signal[pointer : pointer + samplesPerHorizon])
        
        parametresEstimes = parametersEstimation(window, params.samplerate, 
                                                 params.nbPoles)
        matrices.F[:, k] = parametresEstimes["f"]
        matrices.B[:, k] = parametresEstimes["b"] 
        matrices.Ksi[:, k] = parametresEstimes["ksi"]
        matrices.J[k] = parametresEstimes["J"]
        
    Fonctions.antialiasingFilter(matrices, params.samplerate)

    matrices.T = np.tile(np.linspace(0, signalLengthInSeconds, matrices.F.shape[1]), 
                        (params.nbPoles, 1))
    
    # # seuillage de la matrice des B
    # matrices.B = 20*np.log10(matrices.B)
    # Fonctions.seuil(matrices, -70)

    # conditionnement
    # algorithme de stabilité
    toleranceStabilite = 1 # pourcentage
    numColsToVerify = 3
    matrices.FStable = stability(matrices.F, numColsToVerify, 
                                toleranceStabilite)


    return matrices