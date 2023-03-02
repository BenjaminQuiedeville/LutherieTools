import numpy as np
import matplotlib.pyplot as plt

from HROgramme import HROgramme
import Preset
from Affichage import affichage



listPreset = ["diapason", "cordeIdeale", "guitareSimulee", 
              "guitareCorps", "guitareModesDoubles", "guitareBruit"]

listTitres = ["Diapason", "Corde idéale", "Guitare Simulée", 
              "Guitare avec modes de corps",
              "Guitare avec modes de corde doubles", 
              "Guitare avec bruit"]

for signalPreset, titre in zip(listPreset, listTitres):

    signal, params = Preset.preset("sample", "", signalPreset)

    print(f"preset : {signalPreset}")
    matrices = HROgramme(signal, params)
   
    plt.close("all")

    affichage(matrices.FStable, matrices.BSeuil, matrices.T, signalPreset, 
                titre, "", True)


# plt.show(block = True)