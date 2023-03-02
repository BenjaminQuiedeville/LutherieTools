import matplotlib.pyplot as plt
import numpy as np

from Preset import preset


signal, params = preset("sample", "", "sampleSoutenance")


fig, ax = plt.subplots(figsize = (8,6), tight_layout = True)

NFFT = 2048
ax.specgram(signal, NFFT = NFFT, Fs = params.samplerate,
            noverlap = NFFT//2)

ax.set_ylim((0, 500))
ax.set_xlim((0.75, 2))
ax.set_ylabel("Fréquences (Hz)")
ax.set_xlabel("Temps (s)")
ax.set_title("Spectrogramme d'un échantillon de Udu")
plt.show()