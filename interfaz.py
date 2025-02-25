import tkinter as tk
from moduloCargarAudio.cargar_audio import cargar_audio
from moduloCargarAudio.grabar_audio import grabar_audio, detener_grabacion
from moduloSeleccionFiltros.procesador_audio import aplicar_filtro, guardar_audio
import os
import soundfile as sf  # Importamos soundfile para leer el archivo de audio grabado

def iniciar_interfaz():
    """Crea la interfaz gráfica de la aplicación."""
    root = tk.Tk()
    root.title("🎵 Procesador de Audio")

    # Variables globales para almacenar el audio cargado o grabado
    audio_data = {"audio": None, "sr": None}  # Diccionario para evitar problemas con 'nonlocal'

    def actualizar_estado(texto, color="black"):
        """Actualiza el estado en la interfaz."""
        estado_label.config(text=texto, fg=color)

    def actualizar_tiempo(tiempo=0, reset=False):
        """Actualiza el tiempo en la interfaz."""
        tiempo_label.config(text=f"⏳ Tiempo: {tiempo}s" if not reset else "⏳ Tiempo: 0s")

    def actualizar_botones(grabar: bool, detener: bool):
        """Habilita o deshabilita los botones de grabar y detener."""
        btn_grabar.config(state=tk.NORMAL if grabar else tk.DISABLED)
        btn_detener.config(state=tk.NORMAL if detener else tk.DISABLED)

    def cargar_audio_ui():
        """Carga un audio desde un archivo seleccionado manualmente."""
        resultado = cargar_audio(actualizar_estado)  # Intentamos cargar el audio

        if resultado is None:  # Si no se seleccionó archivo, no hacer nada
            actualizar_estado("⚠ No se seleccionó un archivo.", "red")
            return

        audio_data["audio"], audio_data["sr"] = resultado  # Guardamos en el diccionario
        actualizar_estado("✅ Audio cargado con éxito 🎵", "green")

    def grabar_audio_ui():
        """Inicia la grabación del audio sin abrir la ventana de carga."""
        actualizar_estado("🔴 Grabando... 🎙", "red")
        grabar_audio(actualizar_estado, actualizar_tiempo, actualizar_botones)

    def detener_grabacion_ui():
        """Detiene la grabación y carga automáticamente el audio sin abrir la ventana de carga."""
        detener_grabacion(actualizar_estado, actualizar_botones, actualizar_tiempo)

        grabacion_path = "grabacion.wav"  # Ruta fija para la grabación
        if os.path.exists(grabacion_path):
            try:
                audio, sr = sf.read(grabacion_path)
                audio_data["audio"], audio_data["sr"] = audio, sr
                actualizar_estado("✅ Grabación guardada y cargada 🎙", "green")
            except Exception as e:
                actualizar_estado(f"⚠ Error al cargar la grabación: {str(e)}", "red")
        else:
            actualizar_estado("⚠ Error: Archivo de grabación no encontrado.", "red")

    def aplicar_filtro_ui():
        """Aplica el filtro seleccionado al audio cargado."""
        if audio_data["audio"] is None or audio_data["sr"] is None:
            actualizar_estado("⚠ No hay audio cargado.", "red")
            return

        filtro = filtro_var.get()

        try:
            cutoff = int(entry_frec.get()) if filtro in ["Pasaaltos", "Pasabajos"] else None
        except ValueError:
            actualizar_estado("⚠ Ingresa una frecuencia de corte válida.", "red")
            return

        resultado = aplicar_filtro(audio_data["audio"], audio_data["sr"], filtro, cutoff)
        if resultado is not None:
            guardar_audio(resultado, audio_data["sr"])
            audio_data["audio"] = resultado  # Guardamos el audio filtrado en memoria
            actualizar_estado("✅ Filtro aplicado con éxito 🎛", "green")

    # INTERFAZ VISUAL 🎛
    estado_label = tk.Label(root, text="🎤 Estado: Esperando acción...", font=("Arial", 12))
    estado_label.pack(pady=5)

    tiempo_label = tk.Label(root, text="⏳ Tiempo: 0s", font=("Arial", 12))
    tiempo_label.pack(pady=5)

    btn_cargar = tk.Button(root, text="📂 Cargar Audio", command=cargar_audio_ui)
    btn_cargar.pack(pady=10)

    btn_grabar = tk.Button(root, text="🎙️ Grabar Audio", command=grabar_audio_ui)
    btn_grabar.pack(pady=10)

    btn_detener = tk.Button(root, text="🛑 Detener Grabación", command=detener_grabacion_ui, state=tk.DISABLED)
    btn_detener.pack(pady=10)

    filtro_var = tk.StringVar(value="Selecciona un filtro")
    opciones = ["Pasaaltos", "Pasabajos", "Eco", "Reverberación"]
    menu_filtros = tk.OptionMenu(root, filtro_var, *opciones)
    menu_filtros.pack()

    entry_frec = tk.Entry(root)
    entry_frec.pack()

    btn_aplicar = tk.Button(root, text="🎛 Aplicar Filtro", command=aplicar_filtro_ui)
    btn_aplicar.pack(pady=10)

    root.mainloop()
