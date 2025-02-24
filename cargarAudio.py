import tkinter as tk
from tkinter import filedialog
import librosa
import soundfile as sf

def cargar_audio():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos WAV", "*.wav")])
    if archivo:
        audio, sr = librosa.load(archivo, sr=None)  # Carga el audio con la tasa de muestreo original
        print(f"Archivo cargado: {archivo}")
        print(f"Duración: {len(audio)/sr:.2f} segundos, Frecuencia de muestreo: {sr} Hz")
        return audio, sr, archivo
    return None, None, None

# Crear ventana Tkinter
root = tk.Tk()
root.withdraw()  # Oculta la ventana principal

# Ejecutar función de carga
audio, sr, archivo = cargar_audio()
