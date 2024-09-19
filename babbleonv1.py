import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import tempfile
import wave
import pyaudio
from openai import OpenAI
from pydub import AudioSegment
import pygame
import time

class VoiceTranscriptionApp:
    def __init__(self, master):
        self.master = master
        master.title("Voice Transcription App")
        master.geometry("700x600")
        master.configure(bg="#f0f0f0")  # Light gray background

        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use 'clam' theme as a base
        self.configure_styles()

        self.api_key = tk.StringVar()
        self.client = None
        self.transcription = ""
        self.audio_file = None
        self.is_recording = False
        self.frames = []
        self.recording_start_time = None

        self.create_widgets()

    def configure_styles(self):
        # Configure modern-looking styles
        self.style.configure('TButton', font=('Segoe UI', 10), padding=10)
        self.style.configure('TEntry', font=('Segoe UI', 10), padding=5)
        self.style.configure('TLabel', font=('Segoe UI', 10), background="#f0f0f0")
        self.style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'), background="#f0f0f0")

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20 20 20 20", style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # API Key input and submit button
        ttk.Label(main_frame, text="OpenAI API Key:", style='Header.TLabel').pack(anchor='w', pady=(0, 5))
        api_frame = ttk.Frame(main_frame)
        api_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(api_frame, textvariable=self.api_key, show="*", width=50).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(api_frame, text="Submit", command=self.submit_api_key).pack(side=tk.LEFT, padx=(10, 0))

        # API key status
        self.api_status = tk.StringVar(value="API Key Status: Not submitted")
        ttk.Label(main_frame, textvariable=self.api_status).pack(anchor='w', pady=(0, 10))

        # Audio input device
        self.audio_device = self.get_default_input_device()
        ttk.Label(main_frame, text=f"Audio Input: {self.audio_device}", style='TLabel').pack(anchor='w', pady=(0, 10))

        # Recording status and duration
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        self.recording_status = tk.StringVar(value="Not recording")
        ttk.Label(status_frame, textvariable=self.recording_status).pack(side=tk.LEFT)
        self.recording_duration = tk.StringVar(value="Duration: 00:00")
        ttk.Label(status_frame, textvariable=self.recording_duration).pack(side=tk.RIGHT)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(button_frame, text="Record", command=self.toggle_recording).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Select File", command=self.select_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Transcribe", command=self.transcribe).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Play Audio", command=self.play_audio).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Copy Text", command=self.copy_text).pack(side=tk.LEFT, padx=5)

        # Transcription display
        ttk.Label(main_frame, text="Transcription:", style='Header.TLabel').pack(anchor='w', pady=(0, 5))
        self.transcription_text = tk.Text(main_frame, wrap=tk.WORD, width=80, height=15, font=('Segoe UI', 10))
        self.transcription_text.pack(fill=tk.BOTH, expand=True)

    def get_default_input_device(self):
        p = pyaudio.PyAudio()
        default_device = p.get_default_input_device_info()
        p.terminate()
        return default_device['name']

    def submit_api_key(self):
        key = self.api_key.get()
        if key:
            try:
                self.client = OpenAI(api_key=key)
                self.client.models.list()
                self.api_status.set("API Key Status: Valid")
                messagebox.showinfo("Success", "API key is valid and has been set.")
            except Exception as e:
                self.api_status.set("API Key Status: Invalid")
                messagebox.showerror("Error", f"Invalid API key: {str(e)}")
        else:
            self.api_status.set("API Key Status: Not submitted")
            messagebox.showerror("Error", "Please enter an API key.")

    def toggle_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.recording_status.set("Recording...")
            self.frames = []
            self.recording_start_time = time.time()
            threading.Thread(target=self.record_audio).start()
            threading.Thread(target=self.update_duration).start()
        else:
            self.is_recording = False
            self.recording_status.set("Recording stopped")

    def update_duration(self):
        while self.is_recording:
            duration = int(time.time() - self.recording_start_time)
            minutes, seconds = divmod(duration, 60)
            self.recording_duration.set(f"Duration: {minutes:02d}:{seconds:02d}")
            time.sleep(1)

    def record_audio(self):
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 1
        fs = 44100

        p = pyaudio.PyAudio()

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        while self.is_recording:
            data = stream.read(chunk)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            wf = wave.open(temp_file.name, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(self.frames))
            wf.close()

        self.audio_file = temp_file.name

    def select_file(self):
        self.audio_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav;*.m4a")])

    def transcribe(self):
        if not self.audio_file:
            messagebox.showerror("Error", "Please record or select an audio file first.")
            return

        if not self.client:
            messagebox.showerror("Error", "Please submit a valid OpenAI API key first.")
            return

        try:
            with open(self.audio_file, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )

            self.transcription = transcript.text
            self.transcription_text.delete(1.0, tk.END)
            self.transcription_text.insert(tk.END, self.transcription)
        except Exception as e:
            messagebox.showerror("Error", f"Transcription failed: {str(e)}")

    def play_audio(self):
        if not self.audio_file:
            messagebox.showerror("Error", "No audio file selected.")
            return

        pygame.mixer.init()
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play()

    def copy_text(self):
        if not self.transcription:
            messagebox.showerror("Error", "No transcription available.")
            return

        self.master.clipboard_clear()
        self.master.clipboard_append(self.transcription)
        messagebox.showinfo("Success", "Transcription copied to clipboard.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceTranscriptionApp(root)
    root.mainloop()
