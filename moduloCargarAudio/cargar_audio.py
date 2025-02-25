from tkinter import filedialog

def cargar_audio(actualizar_estado):
    """Permite al usuario seleccionar un archivo de audio .wav."""
    archivo = filedialog.askopenfilename(filetypes=[("Archivos WAV", "*.wav")])
    if archivo:
        print(f"📂 Archivo cargado: {archivo}")
        actualizar_estado(f"📂 Archivo cargado: {archivo}", "purple")
