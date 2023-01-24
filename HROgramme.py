from concurrent.futures import thread
import numpy as np
import matplotlib.pyplot as plt
import threading

from EstimationParametres import parametres
from Classes import Params, Matrices 


def HROgramme(signal: np.ndarray, params: Params) -> Matrices:

    signalLength: int = signal.size
    
    echParHorizon: int = int(params.horizon * params.samplerate)
    echParRecouvrement: int = int(echParHorizon * params.overlap)
    pointer: int = 0
    
    nbFenetres: int = int(signalLength/(echParHorizon*(1 - params.overlap)))
    
    matrices = Matrices()
    matrices.F: np.ndarray =     np.zeros((params.nbPoles, nbFenetres))
    matrices.Ksi: np.ndarray =   np.zeros((params.nbPoles, nbFenetres))
    matrices.B: np.ndarray =     np.zeros((params.nbPoles, nbFenetres))
    matrices.J: np.ndarray =     np.zeros((params.nbPoles, nbFenetres))    
    
    print(f"taille de fenetre (samples) = {echParHorizon}")
    print(f'nbFenetres = {nbFenetres}')
    
    for k in range(nbFenetres, 2):
        
        if k %  10 == 0:    
            print(f'{k}/{nbFenetres}')
            
        pointer1 = int(k*(echParHorizon - echParRecouvrement) + 1)
        pointer2 = int((k+1) * (echParHorizon - echParRecouvrement) +1)

        if ((pointer1 + echParHorizon) > signalLength or 
            (pointer2 + echParHorizon) > signalLength):
            print("sortie de boucle")
            break
        

        fenetre1: np.ndarray = signal[pointer1 : pointer1 + echParHorizon]
        fenetre2: np.ndarray = signal[pointer2 : pointer2 + echParHorizon]

        thread1 = threading.Thread(target = parametres, args = (fenetre1, params.samplerate, params.nbPoles))
        thread2 = threading.Thread(target = parametres, args = (fenetre2, params.samplerate, params.nbPoles))
        
        parametresEstimes1 = thread1.start()
        parametresEstimes2 = thread2.start()

        thread1.join()
        thread2.join()

        matrices.F[:, k] = parametresEstimes1[0]
        matrices.B[:, k] = parametresEstimes1[1] 
        matrices.Ksi[:, k] = parametresEstimes1[2]
        matrices.J[:, k] = parametresEstimes1[3]

        matrices.F[:, k + 1] = parametresEstimes2[0]
        matrices.B[:, k + 1] = parametresEstimes2[1] 
        matrices.Ksi[:, k + 1] = parametresEstimes2[2]
        matrices.J[:, k + 1] = parametresEstimes2[3]
        
    antialiasingfilter(matrices, params.samplerate)
        
    return matrices


def antialiasingfilter(matrices, samplerate):

    # for (i,j), x in np.ndenumerate(matrices.F):
    #     # Supprimer les frequences calculées au delà de F nyquist
    #     if x > 0.5*samplerate:
            
    #         matrices.F[i,j] = np.NaN
    #         matrices.B[i,j] = np.NaN

    matrices.F[matrices.F > 0.5*samplerate] = np.nan
    matrices.B[matrices.F is np.nan] = np.nan
    matrices.Ksi[matrices.F is np.nan] = np.nan

    return matrices
