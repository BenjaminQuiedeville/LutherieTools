from sys import argv
from time import perf_counter

from HROgramme import HROgramme
from Preset import preset

# VERSION DE PYTHON > 3.9.2

# trouver des plages de variations pour les params d'étude

def main(argv: list[str]) -> None:

    argvPreset: str = "sample"
    # "gen","sample" ou "json" 
    signalPreset: str = "guitareBruit"
    # Diapason, cordeIdeale, guitareSimulee, 
    # guitareCorps, guitareModesDoubles, guitareBruit

    paramsPath: str = ''
    afficher: bool = True
    # forme d'appel : python main.py args.json 

    if len(argv) > 1:
        paramsPath = argv[1]
        argvPreset: str = "json"
        afficher = False    

    signal, params = preset(argvPreset, paramsPath, signalPreset)
    print(f"samplerate = {params.samplerate}")
    print(f"horizon = {params.horizon}")
    print(f"overlap = {params.overlap}")
    print(f"nbPoles = {params.nbPoles}")
    print(f'duree du signal = {signal.size/params.samplerate :.2f}')


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
        matrices.export(signal, params.samplerate, 
                        params.exportFolder)

    # affichage
    if afficher:
        from Affichage import display
        display(signal, params.samplerate, matrices, 
                signalPreset, "Stabilité", False)
        

if __name__ == "__main__":
    main(argv)