import tkinter as tk
from tkinter import filedialog, messagebox
from moduloCargarAudio.cargar_audio import cargar_audio
from moduloCargarAudio.grabar_audio import grabar_audio, detener_grabacion
from moduloSeleccionFiltros.procesador_audio import aplicar_filtro, guardar_audio
import os
import soundfile as sf  # Para leer el archivo de audio grabado

import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf
import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from moduloCargarAudio.cargar_audio import cargar_audio
from moduloCargarAudio.grabar_audio import grabar_audio, detener_grabacion
from moduloSeleccionFiltros.procesador_audio import aplicar_filtro, guardar_audio

# Ruta base de los audios
BASE_DIR = r"F:\FiltrosTeoinfo"

def iniciar_interfaz():
    """Crea la interfaz gráfica de la aplicación."""
    root = tk.Tk()
    root.title("🎵 Procesador de Audio")

    audio_data = {"audio": None, "sr": None}  # Diccionario para almacenar el audio en memoria

    def actualizar_estado(texto, color="black"):
        """Actualiza el estado en la interfaz."""
        estado_label.config(text=texto, fg=color)

    def cargar_audio_ui():
        """Carga un audio desde un archivo seleccionado manualmente."""
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=[("Archivos de audio", "*.wav *.mp3 *.ogg")]
        )
        if not filepath:
            actualizar_estado("⚠ No se seleccionó un archivo.", "red")
            return

        try:
            audio, sr = librosa.load(filepath, sr=None)
            audio_data["audio"], audio_data["sr"] = audio, sr
            actualizar_estado(f"✅ Audio cargado: {os.path.basename(filepath)}", "green")
            mostrar_onda(audio, sr, "Forma de Onda - Audio Original")  # 📊 Mostrar onda tras cargar
        except Exception as e:
            actualizar_estado(f"⚠ Error al cargar el archivo: {str(e)}", "red")

    def aplicar_filtro_ui():
        """Aplica el filtro seleccionado al audio cargado y muestra la forma de onda."""
        if audio_data["audio"] is None or audio_data["sr"] is None:
            actualizar_estado("⚠ No hay audio cargado.", "red")
            return

        filtro = filtro_var.get()
        ambiente = ambiente_var.get() if filtro == "Ambientes" else None

        if filtro in ["Pasaaltos", "Pasabajos"]:
            try:
                cutoff = int(entry_frec.get())
                if cutoff < 20 or cutoff > 20000:
                    actualizar_estado("⚠ La frecuencia debe estar entre 20 Hz y 20,000 Hz.", "red")
                    return
            except ValueError:
                actualizar_estado("⚠ Ingresa una frecuencia válida.", "red")
                return
        else:
            cutoff = None

        resultado = aplicar_filtro(audio_data["audio"], audio_data["sr"], filtro, cutoff, ambiente)
        if resultado is not None:
            guardar_audio(resultado, audio_data["sr"])
            audio_data["audio"] = resultado
            actualizar_estado("✅ Filtro aplicado con éxito 🎛", "green")
            mostrar_onda(resultado, audio_data["sr"], f"Forma de Onda - {filtro}")  # 📊 Mostrar onda tras aplicar filtro

    def mostrar_onda(audio, sr, titulo):
        """Muestra la forma de onda del audio procesado en la interfaz."""
        fig, ax = plt.subplots(figsize=(6, 3))
        tiempo = np.linspace(0, len(audio) / sr, num=len(audio))
        ax.plot(tiempo, audio, color='purple')
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.set_title(titulo)
        
        # Limpiar gráfico anterior y actualizar con el nuevo
        for widget in frame_onda.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=frame_onda)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # INTERFAZ VISUAL 🎛 (NO SE TOCÓ NADA AQUÍ)
    estado_label = tk.Label(root, text="🎤 Estado: Esperando acción...", font=("Arial", 12))
    estado_label.pack(pady=5)

    btn_cargar = tk.Button(root, text="📂 Cargar Audio", command=cargar_audio_ui)
    btn_cargar.pack(pady=10)

    btn_grabar = tk.Button(root, text="🎙️ Grabar Audio", command=grabar_audio)
    btn_grabar.pack(pady=10)

    btn_detener = tk.Button(root, text="🛑 Detener Grabación", command=detener_grabacion, state=tk.DISABLED)
    btn_detener.pack(pady=10)

    filtro_var = tk.StringVar(value="Selecciona un filtro")
    opciones = ["Pasaaltos", "Pasabajos", "Eco", "Reverberación", "Ambientes"]
    menu_filtros = tk.OptionMenu(root, filtro_var, *opciones)
    menu_filtros.pack()

    ambiente_var = tk.StringVar(value="Selecciona un ambiente")
    opciones_ambientes = ["Sala pequeña", "Iglesia", "Estadio", "Cueva"]
    menu_ambientes = tk.OptionMenu(root, ambiente_var, *opciones_ambientes)
    menu_ambientes.pack()

    entry_frec = tk.Entry(root)
    entry_frec.pack()

    btn_aplicar = tk.Button(root, text="🎛 Aplicar Filtro", command=aplicar_filtro_ui)
    btn_aplicar.pack(pady=10)

    # Marco para la gráfica de la forma de onda
    frame_onda = tk.Frame(root)
    frame_onda.pack(pady=10)

    root.mainloop()
