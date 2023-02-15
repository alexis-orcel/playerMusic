import librosa
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("Music Player")

def choose_file():
    global filename
    filename = filedialog.askopenfilename()

def play():
    global filename
    librosa.load(filename)

play_button = tk.Button(root, text="Play", command=play)
play_button.pack()

file_button = tk.Button(root, text="Choose File", command=choose_file)
file_button.pack()

root.mainloop()
