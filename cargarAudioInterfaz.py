import tkinter as tk
from tkinter import filedialog
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import sys
import threading

# Configurar UTF-8 en la salida para evitar errores de codificación
sys.stdout.reconfigure(encoding='utf-8')

# Variables globales
grabando = False  # Estado de grabación
duracion_maxima = 60  # Tiempo máximo de grabación en segundos
sr = 44100  # Frecuencia de muestreo
audio_grabado = None  # Para almacenar la grabación

def grabar_audio():
    global grabando, audio_grabado
    if grabando:  # Evitar múltiples grabaciones a la vez
        return

    grabando = True
    archivo_salida = "grabacion.wav"

    # Deshabilitar botón de grabar y habilitar detener
    btn_grabar.config(state=tk.DISABLED)
    btn_detener.config(state=tk.NORMAL)

    print("Grabando... [MIC] (Máx. 60s)")

    def grabacion():
        global audio_grabado
        audio_grabado = sd.rec(int(duracion_maxima * sr), samplerate=sr, channels=1, dtype=np.int16)
        sd.wait()  # Esperar a que termine la grabación o se detenga manualmente

        if grabando:  # Solo guardar si no se detuvo antes
            wav.write(archivo_salida, sr, audio_grabado)
            print(f"Grabación guardada como {archivo_salida}")

        detener_grabacion()  # Asegurar que se reactive el botón de grabar

    # Iniciar grabación en un hilo para evitar que bloquee la interfaz
    thread = threading.Thread(target=grabacion)
    thread.start()

def detener_grabacion():
    global grabando
    if grabando:
        grabando = False
        sd.stop()  # Detener grabación inmediatamente
        print("Grabación detenida. 🎶")

        # Habilitar botón de grabar y deshabilitar detener
        btn_grabar.config(state=tk.NORMAL)
        btn_detener.config(state=tk.DISABLED)

def cargar_audio():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos WAV", "*.wav")])
    if archivo:
        print(f"Archivo cargado: {archivo}")

# Crear la ventana de Tkinter
root = tk.Tk()
root.title("Cargar o Grabar Audio")

# Botón para cargar audio
btn_cargar = tk.Button(root, text="Cargar Audio", command=cargar_audio)
btn_cargar.pack(pady=10)

# Botón para grabar audio (Se bloquea mientras se graba)
btn_grabar = tk.Button(root, text="Grabar Audio", command=grabar_audio)
btn_grabar.pack(pady=10)

# Botón para detener grabación (Empieza desactivado)
btn_detener = tk.Button(root, text="Detener Grabación", command=detener_grabacion, state=tk.DISABLED)
btn_detener.pack(pady=10)

# Iniciar la interfaz gráfica
root.mainloop()
