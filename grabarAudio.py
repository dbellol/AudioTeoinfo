import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

def grabar_audio(duracion=5, sr=44100, archivo_salida="grabacion.wav"):
    print("Grabando... 🎤")
    audio = sd.rec(int(duracion * sr), samplerate=sr, channels=1, dtype=np.int16)
    sd.wait()  # Espera a que termine la grabación
    print("Grabación finalizada. 🎶")

    # Guardar el audio grabado
    wav.write(archivo_salida, sr, audio)
    print(f"Archivo guardado como {archivo_salida}")

# Grabar 5 segundos de audio
grabar_audio()
