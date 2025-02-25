import tkinter as tk
from cargar_audio import cargar_audio
from grabar_audio import grabar_audio, detener_grabacion, actualizar_tiempo_label
import sys
sys.stdout.reconfigure(encoding='utf-8')

def iniciar_interfaz():
    """Crea la interfaz gráfica de la aplicación."""
    root = tk.Tk()
    root.title("🎵 Cargar o Grabar Audio")

    def actualizar_estado(texto, color="black"):
        """Actualiza el estado en la interfaz."""
        estado_label.config(text=texto, fg=color)

    def actualizar_tiempo(tiempo=0, reset=False):
        """Actualiza el tiempo en la interfaz."""
        if reset:
            tiempo_label.config(text="⏳ Tiempo: 0s")
        else:
            tiempo_label.config(text=f"⏳ Tiempo: {tiempo}s")

    def actualizar_botones(grabar: bool, detener: bool):
        """Habilita o deshabilita los botones de grabar y detener."""
        btn_grabar.config(state=tk.NORMAL if grabar else tk.DISABLED)
        btn_detener.config(state=tk.NORMAL if detener else tk.DISABLED)

    # Etiqueta de estado
    estado_label = tk.Label(root, text="🎤 Estado: Esperando acción...", font=("Arial", 12), fg="black")
    estado_label.pack(pady=5)

    # Etiqueta de cronómetro
    tiempo_label = tk.Label(root, text="⏳ Tiempo: 0s", font=("Arial", 12), fg="black")
    tiempo_label.pack(pady=5)

    # Botones de la interfaz
    btn_cargar = tk.Button(root, text="📂 Cargar Audio", command=lambda: cargar_audio(actualizar_estado))
    btn_cargar.pack(pady=10)

    btn_grabar = tk.Button(root, text="🎙️ Grabar Audio", command=lambda: grabar_audio(actualizar_estado, actualizar_tiempo, actualizar_botones))
    btn_grabar.pack(pady=10)

    btn_detener = tk.Button(root, text="🛑 Detener Grabación", command=lambda: detener_grabacion(actualizar_estado, actualizar_botones, actualizar_tiempo), state=tk.DISABLED)
    btn_detener.pack(pady=10)

    # Iniciar la interfaz
    root.mainloop()
