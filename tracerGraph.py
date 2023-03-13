import numpy as np
import matplotlib.pyplot as plt

from HROgramme import HROgramme
import Preset
from Affichage import displayHROgramme

"""Script itérants sur différents signaux déterminé
"""

listPreset = ["diapason", "cordeIdeale", "guitareSimulee", 
              "guitareCorps", "guitareModesDoubles", "guitareBruit"]


for signalPreset in listPreset:

    signal, params = Preset.preset("sample", "", signalPreset)

    print(f"preset : {signalPreset}")
    matrices = HROgramme(signal, params)
   

    displayHROgramme(matrices.FStable, matrices.BSeuil, matrices.T, signalPreset, "", False)

    plt.show(block = False)

plt.show(block = True)