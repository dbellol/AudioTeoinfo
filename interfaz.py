import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf
import tkinter as tk
from tkinter import filedialog, messagebox, Scale
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
            mostrar_onda(audio, sr, "Forma de Onda - Audio Original")  
            mostrar_espectrograma(audio, sr, "Espectrograma - Audio Original")  
        except Exception as e:
            actualizar_estado(f"⚠ Error al cargar el archivo: {str(e)}", "red")

    def aplicar_filtro_ui():
        """Aplica el filtro seleccionado al audio cargado y muestra la forma de onda y el espectrograma."""
        if audio_data["audio"] is None or audio_data["sr"] is None:
            actualizar_estado("⚠ No hay audio cargado.", "red")
            return

        filtro = filtro_var.get()
        ambiente = ambiente_var.get() if filtro == "Ambientes" else None
        cutoff = None
        intensidad = scale_intensidad.get()

        if filtro in ["Pasaaltos", "Pasabajos"]:
            cutoff = scale_frec.get()

        if filtro in ["Eco", "Reverberación"]:
            resultado = aplicar_filtro(audio_data["audio"], audio_data["sr"], filtro, cutoff, ambiente, intensidad)
        elif filtro == "Ambientes":
            resultado = aplicar_filtro(audio_data["audio"], audio_data["sr"], filtro, cutoff, ambiente)
        else:
            resultado = aplicar_filtro(audio_data["audio"], audio_data["sr"], filtro, cutoff)

        if resultado is None:
            actualizar_estado("⚠ El filtro no generó cambios en el audio.", "red")
            return

        guardar_audio(resultado, audio_data["sr"])
        audio_data["audio"] = resultado
        actualizar_estado("✅ Filtro aplicado con éxito 🎛", "green")
        mostrar_onda(resultado, audio_data["sr"], f"Forma de Onda - {filtro}")  
        mostrar_espectrograma(resultado, audio_data["sr"], f"Espectrograma - {filtro}")  

    def mostrar_onda(audio, sr, titulo):
        """Muestra la forma de onda del audio procesado en la interfaz."""
        fig, ax = plt.subplots(figsize=(7, 3))
        tiempo = np.linspace(0, len(audio) / sr, num=len(audio))

        ax.plot(tiempo, audio, color='purple')
        ax.set_xlabel("Tiempo (s)", fontsize=10, fontweight='bold')
        ax.set_ylabel("Amplitud", fontsize=10, fontweight='bold')
        ax.set_title(titulo, fontsize=12, fontweight='bold')
        ax.set_xlim([0, max(tiempo)])
        ax.grid(True, linestyle='--', alpha=0.7)

        plt.tight_layout()

        for widget in frame_onda.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame_onda)
        canvas.draw()
        canvas.get_tk_widget().pack()
        plt.close(fig)

    def mostrar_espectrograma(audio, sr, titulo):
        """Muestra el espectrograma del audio procesado en la interfaz."""
        fig, ax = plt.subplots(figsize=(7, 3))
        espectrograma = np.abs(librosa.stft(audio))
        espectrograma_db = librosa.amplitude_to_db(espectrograma, ref=np.max)

        mappable = librosa.display.specshow(espectrograma_db, sr=sr, x_axis='time', y_axis='log', cmap='inferno', ax=ax)
        ax.set_title(titulo, fontsize=12, fontweight='bold')
        ax.set_xlabel("Tiempo (s)", fontsize=10, fontweight='bold')
        ax.set_ylabel("Frecuencia (Hz)", fontsize=10, fontweight='bold')
        ax.set_xlim([0, len(audio) / sr])
        plt.colorbar(mappable, ax=ax, format="%+2.0f dB")

        plt.tight_layout()

        for widget in frame_espectrograma.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame_espectrograma)
        canvas.draw()
        canvas.get_tk_widget().pack()
        plt.close(fig)

    estado_label = tk.Label(root, text="🎤 Estado: Esperando acción...", font=("Arial", 12))
    estado_label.pack(pady=5)

    tiempo_label = tk.Label(root, text="⏳ Esperando grabación...", font=("Arial", 10))
    tiempo_label.pack(pady=5)

    def actualizar_tiempo(texto=None, reset=False):
        if reset:
            tiempo_label.config(text="⏳ Esperando grabación...")
        elif texto:
            tiempo_label.config(text=texto)


    def actualizar_botones(grabar=True, detener=False):
        btn_grabar.config(state=tk.NORMAL if grabar else tk.DISABLED)
        btn_detener.config(state=tk.NORMAL if detener else tk.DISABLED)

    btn_cargar = tk.Button(root, text="📂 Cargar Audio", command=cargar_audio_ui)
    btn_cargar.pack(pady=10)

    btn_grabar = tk.Button(root, text="🎙️ Grabar Audio", command=lambda: grabar_audio(actualizar_estado, actualizar_tiempo, actualizar_botones))
    btn_grabar.pack(pady=10)

    btn_detener = tk.Button(root, text="🛑 Detener Grabación", command=lambda: detener_grabacion(actualizar_estado, actualizar_botones, actualizar_tiempo), state=tk.DISABLED)
    btn_detener.pack(pady=10)

    filtro_var = tk.StringVar(value="Selecciona un filtro")
    opciones = ["Pasaaltos", "Pasabajos", "Eco", "Reverberación", "Ambientes"]
    menu_filtros = tk.OptionMenu(root, filtro_var, *opciones)
    menu_filtros.pack()

    ambiente_var = tk.StringVar(value="Selecciona un ambiente")
    opciones_ambientes = ["Sala pequeña", "Iglesia", "Estadio", "Cueva"]
    menu_ambientes = tk.OptionMenu(root, ambiente_var, *opciones_ambientes)
    menu_ambientes.pack()

    scale_frec = Scale(root, from_=20, to=20000, orient="horizontal", label="Frecuencia de Corte (Hz)")
    scale_frec.pack()

    scale_intensidad = Scale(root, from_=0.0, to=1.0, resolution=0.01, orient="horizontal", label="Intensidad del Efecto")
    scale_intensidad.pack()

    btn_aplicar = tk.Button(root, text="🎛 Aplicar Filtro", command=aplicar_filtro_ui)
    btn_aplicar.pack(pady=10)

    frame_onda = tk.Frame(root)
    frame_onda.pack(pady=10)

    frame_espectrograma = tk.Frame(root)
    frame_espectrograma.pack(pady=10)

    root.mainloop()
