import numpy as np
import matplotlib.pyplot as plt
from sys import argv
from time import perf_counter

from HROgramme import HROgramme
import Fonctions
from Preset import preset
from Affichage import affichage

# VERSION DE PYTHON > 3.9.2

# tester les signaux tests
# trouver des plages de variations pour les params d'étude
# exporter un spectrogram pour afficher en fond 
# dimension : 1500 pixels en largeur

def main(argv: list) -> None:

    argvPreset: str = "sample"
    # "gen","sample" ou "json" 
    signalPreset: str = "guitareSimulee"
    # Envelope, battements, sinusAleatoires, diapason, cordeIdeale
    # guitareSimulee, guitareCorps, guitareModesDoubles, guitareBruit

    paramsPath: str = ''
    afficher: bool = True
    # forme d'appel : python mainHROgramme.py args.json 

    if len(argv) > 1:
        paramsPath = argv[1]
        argvPreset: str = "json"
        afficher = False    

    signal, params = preset(argvPreset, paramsPath, signalPreset)

    # Process

    print(f"samplerate = {params.samplerate}")
    print(f"horizon = {params.horizon}")
    print(f"overlap = {params.overlap}")
    print(f"nbPoles = {params.nbPoles}")

    # Calcul du HROgramme
    timeDebut = perf_counter()
    matrices = HROgramme(signal, params)

    # Calcul des performances

    timeFin: float = perf_counter()
    timeTotal: float = timeFin - timeDebut
    print(f"temps d'execution du 1er tour = {timeTotal}")


    # deuxième tour de post process
    deuxiemeTour: bool = False
    # Le deuxième tour basé sur les résultats de ESTER est désactivé
    # les résultats étant non satisfaisants, on désactive le 2e tour 
    # dans la version actuelle

    if deuxiemeTour:

        params.nbPoles = int(max(matrices.J))
        timeDebut2 = perf_counter()
        matrices2 = HROgramme(signal, params)
        
        # Calcul des perfs
        timeFin2: float = perf_counter()
        timeTotal2: float = timeFin2 - timeDebut2
        print(f"temps d'execution du 2e tour = {timeTotal2}")

    # Export en json des matrices 
    if argvPreset == "json": 
        Fonctions.export(signal, matrices, params.samplerate, 
                        params.exportfolder)

    # affichage
    if afficher:
        
        plt.close("all")
        
        # plt.figure(tight_layout = True, figsize = (8, 6))
        # plt.specgram(signal, NFFT = 4096, 
        #              Fs = params.samplerate, noverlap= 2048)
        # plt.ylim([0, 1000])
        # plt.ylabel("Fréquence (Hz)")
        # plt.xlabel("Temps (s)")
        # plt.colorbar(label = "Amplitude (dB)")

        affichage(matrices.F, matrices.BSeuil, matrices.T, signalPreset, 
                  "Amplitude (dB)", "sans critere", False)
        
        affichage(matrices.FStable, matrices.BSeuil, matrices.T, signalPreset, 
                  "Amplitude (dB)", "Stabilité", False)
        
    
        plt.show(block = True)


if __name__ == "__main__":
    main(argv)