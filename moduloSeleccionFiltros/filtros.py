import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.signal import butter, filtfilt, convolve

# Definir la ruta base donde están los audios
BASE_DIR = r"F:\FiltrosTeoinfo"
archivo_audio = os.path.join(BASE_DIR, "grabacion.wav")

# Verificar que el archivo existe antes de cargarlo
if os.path.exists(archivo_audio):
    audio, sr = librosa.load(archivo_audio, sr=None)
    print("Archivo cargado correctamente.")
else:
    raise FileNotFoundError(f"Error: No se encontró el archivo en {archivo_audio}")

# ============================
# FUNCIONES PARA FILTRADO Y EFECTOS
# ============================

def butter_filter(data, cutoff, sr, btype, order=4):
    """ Aplica un filtro Butterworth a la señal de audio. """
    nyquist = 0.5 * sr
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype=btype, analog=False)
    return filtfilt(b, a, data)

def aplicar_eco(audio, sr):
    """ Aplica un efecto de eco a la señal de audio. """
    eco_kernel = np.zeros(sr)
    eco_kernel[::sr//2] = 0.6  # Introducimos retardos cada 0.5s
    return convolve(audio, eco_kernel, mode="full")

def aplicar_reverberacion(audio, sr):
    """ Aplica un efecto de reverberación a la señal de audio. """
    reverb_kernel = np.random.uniform(-0.5, 0.5, sr)
    return convolve(audio, reverb_kernel, mode="full")
