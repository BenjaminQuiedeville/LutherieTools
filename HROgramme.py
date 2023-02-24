import numpy as np
from copy import deepcopy

from EstimationParametres import parametersEstimation
from Classes import Params, Matrices 


def HROgramme(signal: np.ndarray, params: Params) -> Matrices:

    signalLength: int = signal.size
    
    echParHorizon: int = int(params.horizon * params.samplerate)
    echParRecouvrement: int = int(echParHorizon * params.overlap)
    pointer: int = 0
    
    nbFenetres: int = int(signalLength/(echParHorizon*(1 - params.overlap)))
    
    matrices = Matrices(params.nbPoles, nbFenetres)
    
    print(f"taille de fenetre (samples) = {echParHorizon}")
    print(f'nbFenetres = {nbFenetres}')
    
    for k in range(nbFenetres):
        
        if k % 10 == 0 : print(f'{k}/{nbFenetres}') 
            
        pointer = int(k*(echParHorizon - echParRecouvrement) + 1)
        
        if (pointer + echParHorizon) > signalLength: break 
        
        fenetre: np.ndarray = deepcopy(signal[pointer : pointer + echParHorizon])
        
        parametresEstimes = parametersEstimation(fenetre, params.samplerate, params.nbPoles)
        matrices.F[:, k] = parametresEstimes["f"]
        matrices.B[:, k] = parametresEstimes["b"] 
        matrices.Ksi[:, k] = parametresEstimes["ksi"]
        matrices.J[k] = parametresEstimes["J"]
        
    antialiasingFilter(matrices, params.samplerate)
        
    return matrices


def antialiasingFilter(matrices: Matrices, samplerate: int) -> None:

    matrices.F[matrices.F > 0.5*samplerate] = np.nan
    matrices.B[matrices.F is np.nan] = np.nan
    matrices.Ksi[matrices.F is np.nan] = np.nan