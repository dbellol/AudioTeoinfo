import os
import sys
import soundfile as sf
import librosa
import numpy as np
from tkinter import messagebox
from scipy.signal import convolve

# 🔹 Agregar manualmente la carpeta "moduloCargarAudio" al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 🔹 Ahora importa los módulos sin problemas
from moduloSeleccionFiltros.filtros import butter_filter, aplicar_eco, aplicar_reverberacion


# Carpeta donde están las respuestas al impulso (IRs)
IR_DIR = os.path.dirname(__file__)

# Diccionario de respuestas al impulso (IRs) para ambientes
RESPUESTAS_IMPULSO = {
    "Sala pequeña": os.path.join(IR_DIR, "ir_sala_pequena.wav"),
    "Iglesia": os.path.join(IR_DIR, "ir_iglesia.wav"),
    "Estadio": os.path.join(IR_DIR, "ir_estadio.wav"),
    "Cueva": os.path.join(IR_DIR, "ir_cueva.wav")
}

def aplicar_filtro(audio, sr, filtro, cutoff=None, ambiente=None):
    """
    Aplica el filtro seleccionado o simula un ambiente específico.
    """
    if filtro == "Pasaaltos":
        return butter_filter(audio, cutoff, sr, 'high')
    elif filtro == "Pasabajos":
        return butter_filter(audio, cutoff, sr, 'low')
    elif filtro == "Eco":
        return aplicar_eco(audio, sr)
    elif filtro == "Reverberación":
        return aplicar_reverberacion(audio, sr)
    elif filtro == "Ambientes" and ambiente:
        return aplicar_filtro_ambiente(audio, sr, ambiente)
    else:
        messagebox.showerror("❌ Error", "Filtro no válido o ambiente no seleccionado.")
        return None

def aplicar_filtro_ambiente(audio, sr_audio, ambiente):
    """
    Aplica un filtro de ambiente usando respuestas al impulso (IRs).
    """
    if ambiente not in RESPUESTAS_IMPULSO:
        messagebox.showerror("❌ Error", "Ambiente no válido.")
        return None

    ir_file = RESPUESTAS_IMPULSO[ambiente]

    try:
        # Cargar la IR
        ir, sr_ir = sf.read(ir_file)

        # Si la IR tiene una frecuencia de muestreo diferente, la convertimos
        if sr_ir != sr_audio:
            ir = librosa.resample(ir, orig_sr=sr_ir, target_sr=sr_audio)
            sr_ir = sr_audio  # Actualizar la frecuencia de muestreo

            # Guardar la IR corregida dentro de la misma carpeta de las IRs
            ir_fixed_file = os.path.join(IR_DIR, f"{ambiente}_fixed.wav")
            sf.write(ir_fixed_file, ir, sr_audio)
            print(f"✅ IR {ambiente} convertida a {sr_audio} Hz y guardada en {ir_fixed_file}")

            # Usar la versión corregida
            ir_file = ir_fixed_file

        # Convertir ambas señales a mono si es necesario
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)  # Convertir a mono
        if len(ir.shape) > 1:
            ir = np.mean(ir, axis=1)  # Convertir a mono

        # Asegurar que ambas señales sean de tipo float32
        audio = audio.astype(np.float32)
        ir = ir.astype(np.float32)

        # Aplicar SOLO la convolución con la IR del ambiente
        audio_filtrado = convolve(audio, ir, mode="full")

        return audio_filtrado

    except Exception as e:
        messagebox.showerror("❌ Error", f"No se pudo aplicar el ambiente: {str(e)}")
        return None

def guardar_audio(audio, sr, filename="audio_filtrado.wav"):
    """
    Guarda el audio filtrado en un archivo .wav.
    """
    sf.write(filename, audio, sr)
    messagebox.showinfo("✅ Filtro Aplicado", f"🎶 Audio filtrado guardado en: {filename}")
