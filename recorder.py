import sounddevice as sd
from scipy.io.wavfile import write


def record_audio():
    print("STO REGISTRANDO...")
    fs = 44100  # Sample rate
    seconds = 10  # Duration of recording
    
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write("output.ogg", fs, myrecording)  # Save as WAV file
    return "output.ogg"
