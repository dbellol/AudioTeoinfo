import numpy as np
from scipy.signal import butter, filtfilt, convolve

def butter_filter(data, cutoff, sr, btype, order=4):
    """
    Aplica un filtro Butterworth a la señal de audio.
    
    Parámetros:
    - data: La señal de audio.
    - cutoff: Frecuencia de corte en Hz.
    - sr: Frecuencia de muestreo.
    - btype: Tipo de filtro ('high' para pasaaltos, 'low' para pasabajos).
    - order: Orden del filtro (por defecto 4).

    Retorna:
    - Señal filtrada.
    """
    nyquist = 0.5 * sr
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype=btype, analog=False)
    return filtfilt(b, a, data)

def aplicar_eco(audio, sr):
    """
    Aplica un efecto de eco a la señal de audio.
    
    Parámetros:
    - audio: Señal de audio.
    - sr: Frecuencia de muestreo.

    Retorna:
    - Señal con eco aplicado.
    """
    eco_kernel = np.zeros(sr)
    eco_kernel[::sr//2] = 0.6  # Introducimos retardos cada 0.5s
    return convolve(audio, eco_kernel, mode="full")

def aplicar_reverberacion(audio, sr):
    """
    Aplica un efecto de reverberación a la señal de audio.
    
    Parámetros:
    - audio: Señal de audio.
    - sr: Frecuencia de muestreo.

    Retorna:
    - Señal con reverberación aplicada.
    """
    reverb_kernel = np.random.uniform(-0.5, 0.5, sr)
    return convolve(audio, reverb_kernel, mode="full")
