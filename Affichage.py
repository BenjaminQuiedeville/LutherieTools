import matplotlib.pyplot as plt
import numpy as np

from Classes import Matrices


def displaySpectrogram(signal: np.ndarray, samplerate: int) -> None:

    NFFT: int = 4096
    plt.figure(tight_layout = True, figsize = (8, 6))
    plt.specgram(signal, NFFT = NFFT, 
                Fs = samplerate, noverlap = NFFT // 2)
    plt.ylim([0, 1000])
    plt.ylabel("Fréquence (Hz)")
    plt.xlabel("Temps (s)")
    plt.colorbar(label = "Amplitude (dB)")



def displayHROgramme(frequences: np.ndarray,
                    BSeuil: np.ndarray, 
                    temps: np.ndarray, 
                    signalPreset: str, 
                    critere: str,
                    save: bool
                    ) -> None:
    """Fonction d'affichage des HROGrammes calculés"""
    
    BSeuil[BSeuil == -200] = np.nan
    
    ylimit = (0, 1000)
    
    fig, ax = plt.subplots(figsize = (8,6), tight_layout = True)
    
    graph = ax.scatter(temps, frequences, s=25, c=BSeuil, cmap = "Reds")
    ax.set_ylim(ylimit)
    ax.set_xlim(0, temps[0, -1])
    ax.set_title(f"Amplitude (dB) - {signalPreset} - {critere}")
    ax.set_xlabel("Temps (s)")
    ax.set_ylabel("Fréquence (Hz)")

    plt.colorbar(graph, label ="Amplitude (dB)")
    ax.grid(True)

    if save: fig.savefig(f"/../Amplitudes-{signalPreset}-{critere}.pdf")


def display(signal: np.ndarray, samplerate: int, 
            matrices: Matrices, signalPreset: str, 
            critere: str, save: bool) -> None:
    
    plt.close("all")
    displaySpectrogram(signal, samplerate)
    displayHROgramme(matrices.FStable, matrices.BSeuil, matrices.T, 
                    signalPreset, critere, save)

    plt.show(block = True)
    