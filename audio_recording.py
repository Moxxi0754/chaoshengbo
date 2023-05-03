import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

# 录音参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

# 初始化PyAudio
audio = pyaudio.PyAudio()

# 打开流
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("开始录音...")

# 读取音频数据
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("录音结束...")

# 停止数据流
stream.stop_stream()
stream.close()
audio.terminate()

# 写入WAV文件
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

# 读取WAV文件并生成频率随时间变化的图
wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
signal = wf.readframes(-1)
signal = np.frombuffer(signal, dtype='int16')

# 将录音数据转换为数组
audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

# 生成频谱图
plt.figure()
plt.specgram(audio_data, Fs=RATE * 1.25, cmap='gray')
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.title("Spectrogram of output.wav")
plt.show()
