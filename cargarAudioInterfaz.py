import tkinter as tk
from tkinter import filedialog
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import sys
import threading
import time

# Configurar UTF-8 para evitar problemas de codificación en la terminal
sys.stdout.reconfigure(encoding='utf-8')

# Variables globales
grabando = False  # Indica si la grabación está en curso
sr = 44100  # Frecuencia de muestreo
duracion_maxima = 60  # Máximo 60 segundos de grabación
audio_buffer = []  # Almacena fragmentos de audio grabados
tiempo_inicio = 0  # Tiempo de inicio de la grabación

def grabar_audio():
    """Inicia la grabación y deshabilita el botón de grabar hasta que termine."""
    global grabando, audio_buffer, tiempo_inicio
    if grabando:
        return  # Evitar grabaciones simultáneas

    grabando = True
    audio_buffer = []  # Reiniciar buffer de audio
    tiempo_inicio = time.time()  # Guardar el tiempo de inicio
    actualizar_botones(grabar=False, detener=True)
    actualizar_estado("🎙️ Grabando... (Máx. 60s)", "blue")
    actualizar_tiempo()  # Iniciar actualización del cronómetro

    print("🎙️ Grabando... (Máx. 60s)")

    def grabacion():
        """Ejecuta la grabación en un hilo separado."""
        with sd.InputStream(samplerate=sr, channels=1, dtype=np.int16, callback=callback_audio):
            sd.sleep(duracion_maxima * 1000)  # Esperar hasta 60s o hasta que se detenga manualmente
        detener_grabacion()  # Cuando termine, asegurar que se detenga correctamente

    # Iniciar grabación en un hilo para no bloquear la interfaz
    threading.Thread(target=grabacion, daemon=True).start()

def callback_audio(indata, frames, time, status):
    """Almacena los fragmentos de audio grabados en tiempo real."""
    if grabando:
        audio_buffer.append(indata.copy())

def detener_grabacion():
    """Detiene la grabación y guarda el audio con la duración exacta."""
    global grabando, audio_buffer
    if not grabando:
        return

    grabando = False
    sd.stop()  # Detener la captura de audio
    print("🛑 Grabación detenida.")

    if audio_buffer:
        # Concatenar los fragmentos grabados
        audio_final = np.concatenate(audio_buffer, axis=0)

        # Guardar el archivo solo con la parte grabada (sin silencios adicionales)
        archivo_salida = "grabacion.wav"
        wav.write(archivo_salida, sr, audio_final)
        print(f"✅ Grabación guardada: {archivo_salida} ({len(audio_final)/sr:.2f} segundos)")
        actualizar_estado(f"✅ Grabación guardada: {archivo_salida}", "green")
    else:
        actualizar_estado("⚠️ No se grabó audio.", "red")

    # Restaurar botones y reiniciar cronómetro
    actualizar_botones(grabar=True, detener=False)
    tiempo_label.config(text="⏳ Tiempo: 0s")

def actualizar_tiempo():
    """Actualiza el cronómetro en la interfaz mientras la grabación está en curso."""
    if grabando:
        tiempo_actual = int(time.time() - tiempo_inicio)
        tiempo_label.config(text=f"⏳ Tiempo: {tiempo_actual}s")
        
        # Si llega al límite, detener la grabación automáticamente
        if tiempo_actual >= duracion_maxima:
            detener_grabacion()
        else:
            root.after(1000, actualizar_tiempo)  # Actualizar cada segundo

def cargar_audio():
    """Permite al usuario seleccionar un archivo de audio .wav."""
    archivo = filedialog.askopenfilename(filetypes=[("Archivos WAV", "*.wav")])
    if archivo:
        print(f"📂 Archivo cargado: {archivo}")
        actualizar_estado(f"📂 Archivo cargado: {archivo}", "purple")

def actualizar_botones(grabar: bool, detener: bool):
    """Habilita o deshabilita los botones de grabar y detener."""
    btn_grabar.config(state=tk.NORMAL if grabar else tk.DISABLED)
    btn_detener.config(state=tk.NORMAL if detener else tk.DISABLED)

def actualizar_estado(texto, color="black"):
    """Actualiza el texto y color del estado en la interfaz."""
    estado_label.config(text=texto, fg=color)

# Crear la ventana de Tkinter
root = tk.Tk()
root.title("🎵 Cargar o Grabar Audio")

# Label para mostrar el estado de la grabación
estado_label = tk.Label(root, text="🎤 Estado: Esperando acción...", font=("Arial", 12), fg="black")
estado_label.pack(pady=5)

# Label para mostrar el cronómetro
tiempo_label = tk.Label(root, text="⏳ Tiempo: 0s", font=("Arial", 12), fg="black")
tiempo_label.pack(pady=5)

# Botón para cargar audio
btn_cargar = tk.Button(root, text="📂 Cargar Audio", command=cargar_audio)
btn_cargar.pack(pady=10)

# Botón para grabar audio
btn_grabar = tk.Button(root, text="🎙️ Grabar Audio", command=grabar_audio)
btn_grabar.pack(pady=10)

# Botón para detener grabación (inicialmente deshabilitado)
btn_detener = tk.Button(root, text="🛑 Detener Grabación", command=detener_grabacion, state=tk.DISABLED)
btn_detener.pack(pady=10)

# Iniciar la interfaz gráfica
root.mainloop()
