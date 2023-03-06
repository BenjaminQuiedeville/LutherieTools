import numpy as np
from typing import Literal


# signaux tests

# 1 diapason                            
# 2 corde idéale (somme de sinusoide)     
# 3 guitare simulée (somme de sinusoide amorties)
# 4 guitare simulée + modes de corps 
# 5 guitatre simulée + modes de corps + modes doubles 
# (modes séparés par un epsilon de frequence pour faire des battements)
# 6 (5) + bruit
# 
# si l'algorithme réussit tout ca on admet qu'il fonctionne


def creationSignauxTest(dureeSecondes: float,
                        samplerate: int,
                        presetSignal: Literal["diapason",
                                            "cordeIdeale",
                                            "guitareSimulee", 
                                            "guitareCorps",
                                            "guitareModesDoubles", 
                                            "guitareBruit"]
                        ) -> np.ndarray:
    """Fonction créant les signaux de synthèse pour les test de l'algorithme

    Args:
        dureeSecondes (float): 

        samplerate (int): fréquence d'échantillonnage

        presetSignal (str): 
            diapason : simple diapason
            
            cordeIdeale : corde idéale (somme de sinusoide)   
            
            guitareSimulee :guitare simulée (ajout d'une enveloppe d'amplitude exponentielle)
            
            guitareCorps : guitare simulée + modes de corps
            
            guitareModesDoubles : guitare simulée + modes doubles 
            
            guitareBruit : guitareModesDoubles + bruit

    Returns:
        np.ndarray: signal synthétisé
    """
    
    preDelay = 50 #ms
    prePad = np.zeros(int(0.001*50*samplerate))

    dureeSecondes = dureeSecondes - 0.001* preDelay
    t = np.arange(0, dureeSecondes, 1/samplerate)

    diapason: int = 440 #Hz
    freqMiGrave: float = 82.0 #Hz
    nHarmoniques:int = 40
    vecFrequences = np.arange(freqMiGrave, nHarmoniques*freqMiGrave, freqMiGrave)
    damping: float = 1E-2
    bodyDamping: float = 0.1
    inharmonicDamping: float = 5*damping
    modesCorps = [90, 200, 250]
    inharmonicCoefficient: float = 1E-4

    # diapason simple
    if presetSignal == "diapason":
        signal = np.sin(2*np.pi*diapason*t)
    

    # corde ideale : empilement de sinusoides
    elif presetSignal == "cordeIdeale":
        signal = np.zeros_like(t)

        for freq in vecFrequences:
            signal += np.sin(2*np.pi*freq*t)


    # guitare simulee : sinusoides ammorties exponentiellement
    elif presetSignal == "guitareSimulee":
        signal = np.zeros_like(t)

        for freq in vecFrequences:
            signal += np.sin(2*np.pi*freq*t) * np.exp(-damping*freq*t)


    # guitare simulee avec les modes de corps
    elif presetSignal == "guitareCorps":
        signal = np.zeros_like(t)

        for freq in vecFrequences:
            signal += np.sin(2*np.pi*freq*t) * np.exp(-damping*freq*t)

        for freq in modesCorps:
            signal += np.sin(2*np.pi*freq*t) * np.exp(-bodyDamping*freq*t)


    # guitare simulee avec les modes inharmoniques
    elif presetSignal == "guitareModesDoubles":
        signal = np.zeros_like(t)

        for freq in vecFrequences:
            signal += np.sin(2*np.pi*freq*t) * np.exp(-damping*freq*t)
            signal += np.sin(2*np.pi*freq*np.sqrt(1 + inharmonicCoefficient**2)*t) * np.exp(-inharmonicDamping*freq*t)

        # for freq in modesCorps:
        #     signal += np.sin(2*np.pi*freq*t) * np.exp(-bodydamping*freq*t)


    # guitare avec bruit additif
    elif presetSignal == "guitareBruit":
        signal = np.zeros_like(t)

        for freq in vecFrequences:
            signal += np.sin(2*np.pi*freq*t) * np.exp(-damping*freq*t)
            signal += np.sin(2*np.pi*freq * np.sqrt(1 + inharmonicCoefficient**2) * t) * np.exp(-inharmonicDamping*freq*t)

        for freq in modesCorps:
            signal += np.sin(2*np.pi*freq*t) * np.exp(-bodyDamping*freq*t)

        SNR: int = -10
        SNRLin = 10**(SNR/20)
        noise = SNRLin * (2*np.random.rand(t.size) - 1)

        signal += noise


    else:
        print("mauvais parametre")
        signal = np.zeros_like(t)

    signal = np.concatenate((prePad, signal))
    return signal