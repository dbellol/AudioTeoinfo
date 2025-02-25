import soundfile as sf
from tkinter import messagebox
from moduloSeleccionFiltros.filtros import butter_filter, aplicar_eco, aplicar_reverberacion

def aplicar_filtro(audio, sr, filtro, cutoff=None):
    """
    Aplica el filtro seleccionado.
    """
    if filtro == "Pasaaltos":
        return butter_filter(audio, cutoff, sr, 'high')
    elif filtro == "Pasabajos":
        return butter_filter(audio, cutoff, sr, 'low')
    elif filtro == "Eco":
        return aplicar_eco(audio, sr)
    elif filtro == "Reverberación":
        return aplicar_reverberacion(audio, sr)
    else:
        messagebox.showerror("❌ Error", "Filtro no válido.")
        return None

def guardar_audio(audio, sr, filename="audio_filtrado.wav"):
    """
    Guarda el audio filtrado en un archivo .wav.
    """
    sf.write(filename, audio, sr)
    messagebox.showinfo("✅ Filtro Aplicado", f"🎶 Audio filtrado guardado en: {filename}")
