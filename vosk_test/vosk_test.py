from vosk import Model, KaldiRecognizer
import pyaudio


model = Model(r"C:\Users\tomek\Desktop\Projekt audio\PTI-speech-recongition\vosk_test\vosk-model-small-pl-0.22")  # noqa: E501
recognizer = KaldiRecognizer(model, 48000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=48000,
                  input=True, frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4800)

    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        print(f"'{text}'")
