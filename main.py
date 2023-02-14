import numpy as np
from numpy.matlib import repmat
import matplotlib.pyplot as plt
from sys import argv
from time import perf_counter

from HROgramme import HROgramme
import Fonctions
from Preset import preset
from Affichage import affichage
from Stability import stability

# tester les signaux tests
# trouver des plages de variations pour les params d'étude


# exporter un spectrogram pour afficher en fond 
# dimension : 1500 pixels en largeur


argvPreset: str = "sample"     
# "gen","sample" ou "json" 
signalPreset: str = "oudoureduit"
# Envelope, battements, sinusAleatoires, diapason, cordeIdeale
# guitareSimulee, guitareCorps, guitareModesDoubles, guitareBruit

paramsPath: str = ''
afficher: bool = True

signal: np.ndarray = np.array([])

# forme d'appel : python mainHROgramme.py args.json 

if len(argv) > 1:
    paramsPath = argv[1]
    argvPreset: str = "json"
    afficher = False    

    
signal, params = preset(argvPreset, paramsPath, signalPreset)

# Process

signalLength: float = signal.size/params.samplerate

print(f"samplerate = {params.samplerate}")
print(f"horizon = {params.horizon}")
print(f"overlap = {params.overlap}")
print(f"nbPoles = {params.nbPoles}")

#%% Calcul du HROgramme
timeDebut = perf_counter()

matrices = HROgramme(signal, params)

matrices.T = repmat(
    np.linspace(0, signalLength, matrices.F.shape[1]), 
    params.nbPoles, 
    1
    )


# Calcul des perfs

timeFin: float = perf_counter()
timeTotal: float = timeFin - timeDebut
print(f"temps d'execution du 1er tour = {timeTotal}")


#%% conditionnement

# algo de stabilité
toleranceStabilite = 1
numColsToVerify = 2
matrices.FStable = stability(matrices.F, numColsToVerify, toleranceStabilite)


# seuillage de la matrice des B
matrices.BdB = 20*np.log10(matrices.B)
Fonctions.seuil(matrices, -70)

#%% deuxième tour de post process
deuxiemeTour: bool = False

if deuxiemeTour:

    params.nbPoles = int(max(matrices.J))

    timeDebut2 = perf_counter()
    matrices2 = HROgramme(signal, params)
    
    matrices2.T = repmat(
        np.linspace(0, signalLength, matrices2.F.shape[1]), 
        params.nbPoles, 
        1)

    # Calcul des perfs

    timeFin2: float = perf_counter()
    timeTotal2: float = timeFin2 - timeDebut2
    print(f"temps d'execution du 2e tour = {timeTotal2}")

    # algo de stabilité
    toleranceStabilite = 1
    numColsToVerify = 2
    matrices2.FStable = stability(matrices2.F, numColsToVerify, toleranceStabilite)


    # seuillage de la matrice des B
    matrices2.BdB = 20*np.log10(matrices2.B)
    Fonctions.seuil(matrices2, -60)

#%% Export en json des matrices 

if argvPreset == "json": 
    Fonctions.export(
        signal, 
        matrices, 
        params.samplerate, 
        params.exportfolder
        )

#%% affichage

if afficher:
    
    plt.close("all")
    
    plt.figure()
    plt.specgram(signal, NFFT = 2048, Fs = params.samplerate)
    plt.ylim([0, 3500])
    
    affichage(matrices.F, matrices.BdBSeuil, matrices.T, signalPreset,
        "Amplitude (dB)", "sans critere", False)
    
    affichage(matrices.FStable, matrices.BdBSeuil, matrices.T, signalPreset,
        "Amplitude (dB)", "Stabilité", False)


    if deuxiemeTour:
        affichage(matrices2.F, matrices2.BdBSeuil, matrices2.T, signalPreset,
            "Amplitude (dB)", "sans critere 2e tour", False)
        
        affichage(matrices2.FStable, matrices2.BdBSeuil, matrices2.T, signalPreset,
            "Amplitude (dB)", "Stabilité 2e tour", False)
        
    plt.show()