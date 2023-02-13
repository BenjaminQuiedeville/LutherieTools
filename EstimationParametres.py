import numpy as np
from scipy.linalg import hankel, svd, pinv, eig


#import matplotlib.pyplot as plt


def ESTER(W: np.ndarray, nbPolesMax: int) -> np.ndarray:
        
    J: np.ndarray = np.zeros(nbPolesMax)
    
    for poles in range(nbPolesMax):
        
        Ws: np.ndarray = W[:, 0: poles+1]
        Wup: np.ndarray = Ws[1::, :]
        Wdown: np.ndarray = Ws[0: -1, :]
        
        E: np.ndarray = Wup - Wdown @ np.linalg.pinv(Wdown) @ Wup
        
        J[poles] = 1/(np.linalg.norm(E, 2)**2)
        
    return J
    

def ESPRIT(signal: np.ndarray, nbPoles: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Appel de l'algorithme ESPRIT pour la détermination des paramêtres du signal
    Appelle également l'algorithme d'estimation ESTER pour déterminer l'ordre du modèle

    Args:
        signal (np.ndarray): Signal à étudier 
        nbPoles (int): nombre de pôles à déterminer

    Returns:
        np.ndarray, np.ndarray: les matrices Z (ESPRIT) et J (ESTER)
    """    
    # contient également l'implémentation du critère ESTER 
    
    N: int = signal.shape[0]
    M: int = int(N/3)
    L: int = N - M + 1 # M vaut N /3 et l vaut horizon - M + 1

    H: np.ndarray = hankel(signal[0 : M], signal[M : -1])
    C: np.ndarray =  1/L * H @ H.T
  
    W,_,_ = svd(C, full_matrices=False, overwrite_a=True)
    
    W = W[:, 0: nbPoles]
    Wup: np.ndarray = W[1: -1, :]
    Wdown: np.ndarray = W[0: -2, :]
    
    Z: np.ndarray = eig(
        pinv(Wdown, check_finite=False) @ Wup, 
        right = False
        )
    
    # Calcul du critère ESTER    
    J = ESTER(W, int(nbPoles/2))
    
    return Z, J


def parametersEstimation(
        signal: np.ndarray, 
        samplerate: float, 
        nbPoles: int
        ) -> dict:


    poles, J = ESPRIT(signal, 2*nbPoles)
        
    # f : fréquences estimées
    # b : amplitudes
    # ksi : amortissement 

    f: np.ndarray = np.angle(poles) * samplerate/(2*np.pi)
    b: np.ndarray = leastSquares(poles, signal)    
    ksi: np.ndarray = (-np.log(abs(poles))*samplerate)/(2*np.pi*f)
    
    f = f[f > 0] 
    b = np.abs(b[np.imag(b) > 0])
    ksi = ksi[ksi > 0] 
    
    f.resize(nbPoles)
    b.resize(nbPoles)
    ksi.resize(nbPoles)
    
    # tri des vecteurs de parameteres
    indexes = np.argsort(f)
    f = f[indexes]
    b = b[indexes]
    ksi = ksi[indexes]
    
    maxJ = np.ceil(np.nan_to_num(J, posinf=0.0).argmax())

    return {"f": f, "b": b, "ksi": ksi, "J": maxJ}


def leastSquares(vecPoles: np.ndarray, signal: np.ndarray) -> np.ndarray:
    return pinv(
        vandermonde(vecPoles, signal.size), 
        check_finite = False
        ) @ signal


def vandermonde(poles: np.ndarray, size: int) -> np.ndarray:
    return np.nan_to_num(
        np.exp(
            np.arange(0, size)[:, np.newaxis] @
            np.log(poles[:, np.newaxis]).T))