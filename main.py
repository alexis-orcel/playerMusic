import librosa
import tkinter as tk
from tkinter import filedialog, messagebox
import pyaudio
import wave
import numpy as np
from tkinter import ttk

root = tk.Tk()
root.title("Music Player")

chunk = 1024
rate=44100

def choose_file():
    global paused
    global volume
    global y
    global sr
    global filename
    global file_list
    global wf
    global p
    global stream
    filename = filedialog.askopenfilename()
    file_list.append(filename)
    update_file_list()
    y, sr = librosa.load(filename)
    wf = wave.open(filename, 'rb')
    play()

def update_file_list():
    file_list_box.delete(0, tk.END)
    for file in file_list:
        file_list_box.insert(tk.END, file)

def play():
    global paused
    global volume
    global y
    global sr
    global wf
    global p
    global stream
    if paused:
        paused = False
    else:
        y = librosa.effects.time_stretch(y, rate=volume) # A voir !!!!!!!!!!!!!!!
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(chunk)
        while data != b'':
            stream.write(data)
            data = wf.readframes(chunk)
        progress_bar.start()

def pause():
    global paused
    global volume
    global y
    global sr
    global wf
    global p
    global stream
    paused = True
    progress_bar.stop()
    stream.stop_stream()
    stream.close()
    p.terminate()

def stop():
    global paused
    global volume
    global y
    global sr
    global wf
    global p
    global stream
    paused = True
    progress_bar.stop()
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

def volume_up():
    global volume
    global y
    global sr
    global stream
    volume += 0.1
    y = librosa.effects.time_stretch(y, sr, rate=volume)
    stream.set_volume(volume)


def volume_down():
    global volume
    global y
    global sr
    global stream
    volume -= 0.1
    y = librosa.effects.time_stretch(y, sr, rate=volume)
    stream.set_volume(volume)


def remove_file():
    global file_list
    if file_list_box.curselection():
        file_list.pop(file_list_box.curselection()[0])
        update_file_list()
    else:
        messagebox.showerror("Error")



paused = False
volume = 1.0
y = None
sr = None
filename = ""
file_list = []
root.title("Music Player")

file_button = tk.Button(root, text="Choose File", command=choose_file)
file_button.pack()

play_button = tk.Button(root, text="Play", command=play)
play_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop)
stop_button.pack()

volume_up_button = tk.Button(root, text="Volume Up", command=volume_up)
volume_up_button.pack()

volume_down_button = tk.Button(root, text="Volume Down", command=volume_down)
volume_down_button.pack()

loop_var = tk.IntVar()
loop_checkbox = tk.Checkbutton(root, text="Loop", variable=loop_var)
loop_checkbox.pack()

add_file_button = tk.Button(root, text="Add File", command=choose_file)
add_file_button.pack()

remove_file_button = tk.Button(root, text="Remove File", command=remove_file)
remove_file_button.pack()

file_list_box = tk.Listbox(root)
file_list_box.pack()

progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='indeterminate')
progress_bar.pack()

root.mainloop()

