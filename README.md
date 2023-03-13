# LutherieTools

Ce code comprend tous les algorithmes de traitement de l'application [LutherieTools](https://lutherietools.ideesculture.fr/) développée dans le cadre d'un projet de fin d'études par des étudiants de l'ENSIM au Mans. Les principaux acteurs sont : Clément LARCADE, Benjamin QUIEDEVILLE et Andréas AUTIN. Ils one étés encadrés par François GAUTIER et Frédéric ABLITZER, chercheurs au LAUM et Gautier MICHELIN développeur chez [idéesculture](https://www.ideesculture.com/).

Ces algotirhmes nécessitent python >= 3.9. ([python.org/downloads/](https://www.python.org/downloads/))

Arguments optionnels de ligne de commandes : args.json. Spécifie le nom du fichier de paramètres à utiliser pour les algorithmes.

Une version alternative écrite sous [Matlab ](https://github.com/BenjaminQuiedeville/LutherieToolsMatlab)est disponible. Le code de l'application de l'application est disponible dans un dépot [Github ](https://github.com/ideesculture/lutherietools)de Gautier MICHELIN

Pour modifier le projet : 

- Envoyer une demande de colaboration


# Fichiers

HROgramme.py : Comprend la fonction principale de tout le procédé. Initialise les matrices de résultats, découpe le signal en fenêtres temporelles et executes les algorithmes de EstimationParametres.py.

EstimationParametres.py : Comprend l'analyse par la méthode ESPRIT du signal considéré et l'estimation de l'ordre par le critère ESTER.

Preset.py : Importe le signal ou le génère par la fonction signauxTest. Importe les paramètres de l'analyse ou les génère. Décime le signal pour réduire les temps de calcul.

SignauxTest.py : Génère les signaux de synthèse servant à tester les algorithmes.

Classes.py : Comprend les définitions des classes Params et Matrices. Params sert à stocker les paramètres de l'analyse en un même endroit. Matrices initialise et stocke les matrices de résultats et définie les méthodes *antialiasingFilter*, *seuil*, *deNaNisation* et *export.*

Stability.py : Comprend l'algorithme de stabilité, filtrant les modes jugés instables après analyse par ESPRIT.
