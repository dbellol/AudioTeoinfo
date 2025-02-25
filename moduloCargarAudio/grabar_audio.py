import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time
import threading
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Variables globales
grabando = False
sr = 44100  # Frecuencia de muestreo
duracion_maxima = 60  # Máximo 60 segundos
audio_buffer = []
tiempo_inicio = 0

def grabar_audio(actualizar_estado, actualizar_tiempo, actualizar_botones):
    """Inicia la grabación y actualiza la interfaz."""
    global grabando, audio_buffer, tiempo_inicio
    if grabando:
        return

    grabando = True
    audio_buffer = []
    tiempo_inicio = time.time()
    
    actualizar_botones(grabar=False, detener=True)
    actualizar_estado("🎙️ Grabando... (Máx. 60s)", "blue")
    actualizar_tiempo(0)  # Iniciar cronómetro

    def grabacion():
        """Ejecuta la grabación en un hilo separado."""
        with sd.InputStream(samplerate=sr, channels=1, dtype=np.int16, callback=callback_audio):
            sd.sleep(duracion_maxima * 1000)
        detener_grabacion(actualizar_estado, actualizar_botones, actualizar_tiempo)

    threading.Thread(target=grabacion, daemon=True).start()
    actualizar_tiempo_label(actualizar_tiempo)  # Iniciar actualización del cronómetro

def callback_audio(indata, frames, time, status):
    """Almacena fragmentos de audio."""
    if grabando:
        audio_buffer.append(indata.copy())

def detener_grabacion(actualizar_estado, actualizar_botones, actualizar_tiempo):
    """Detiene la grabación y guarda el archivo."""
    global grabando, audio_buffer
    if not grabando:
        return

    grabando = False
    sd.stop()
    print("🛑 Grabación detenida.")


    if audio_buffer:
        audio_final = np.concatenate(audio_buffer, axis=0)
        archivo_salida = "grabacion.wav"
        wav.write(archivo_salida, sr, audio_final)
        print(f"✅ Grabación guardada: {archivo_salida} ({len(audio_final)/sr:.2f} segundos)")
        actualizar_estado(f"✅ Grabación guardada: {archivo_salida}", "green")
    else:
        actualizar_estado("⚠️ No se grabó audio.", "red")

    actualizar_botones(grabar=True, detener=False)
    actualizar_tiempo(reset=True)

def actualizar_tiempo_label(actualizar_tiempo):
    """Actualiza el cronómetro en la interfaz."""
    if grabando:
        tiempo_actual = int(time.time() - tiempo_inicio)
        actualizar_tiempo(tiempo_actual)

        # Si llega al límite de tiempo, detener grabación automáticamente
        if tiempo_actual >= duracion_maxima:
            detener_grabacion()
        else:
            threading.Timer(1, lambda: actualizar_tiempo_label(actualizar_tiempo)).start()

