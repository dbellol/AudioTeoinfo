import numpy as np
import scipy.signal as signal
import soundfile as sf
import librosa
from tkinter import messagebox
import tempfile

def butter_filter(data, cutoff, sr, btype, order=4):
    """Aplica un filtro pasaaltos o pasabajos usando Butterworth."""
    nyquist = 0.5 * sr
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype=btype, analog=False)
    return signal.filtfilt(b, a, data)

def aplicar_eco(audio, sr, intensidad=0.5, retardo_s=0.3, repeticiones=5):
    """Aplica un efecto de eco con retardos múltiples, sin salirse del rango permitido."""
    retardo = int(sr * retardo_s)  # Convertir retardo a muestras
    kernel_size = retardo * repeticiones  # Tamaño del kernel de eco

    # Asegurar que el tamaño del kernel no supere el tamaño del audio
    kernel = np.zeros(min(len(audio), kernel_size))

    for i in range(1, repeticiones + 1):
        idx = i * retardo
        if idx < len(kernel):  # ✅ Evita acceder a un índice fuera de rango
            kernel[idx] = intensidad / (i + 1)  # Atenuar con cada repetición

    audio_eco = np.convolve(audio, kernel, mode="full")
    return audio_eco[:len(audio)]  # Ajustar al tamaño original

def aplicar_reverberacion(audio, sr, intensidad=0.5):
    """Aplica reverberación generando un kernel de respuesta al impulso."""
    kernel_size = sr // 2  # Tamaño de la IR sintética (~0.5s de reverb)
    reverb_kernel = np.exp(-np.linspace(0, intensidad, kernel_size))  # Decaimiento exponencial

    # Añadir pequeñas reflexiones aleatorias
    reverb_kernel += np.random.uniform(-0.05, 0.05, kernel_size) * intensidad
    
    audio_reverb = np.convolve(audio, reverb_kernel, mode="full")
    return audio_reverb[:len(audio)]  # Ajustar al tamaño original
