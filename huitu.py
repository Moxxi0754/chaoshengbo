import pyaudio
import numpy as np
import wave
import matplotlib.pyplot as plt
import time
import hfmbm


def encode_to_signal(code):
    signal = []
    bit_time = (5.0 - 0.1 * (len(code) - 1)) / len(code) # 计算每一位信号分配的时间
    blank_time = int(0.1 * 44100) # 计算空白时间所占采样点个数
    for i, bit in enumerate(code):
        if bit == '0':
            signal += [np.sin(2 * np.pi * 16000 * t) for t in np.arange(0, bit_time, 1 / 44100)]
            signal += [0] * blank_time # 添加空白时间
        elif bit == '1':
            signal += [np.sin(2 * np.pi * 17600 * t) for t in np.arange(0, bit_time, 1 / 44100)]
            signal += [0] * blank_time # 添加空白时间
    return np.array(signal)


# 开启录音
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

# 获取录音数据
frames = []
print("开始录音...")
for i in range(0, int(44100 / 1024 * 5)):
    data = stream.read(1024)
    frames.append(data)
print("录音结束。")

# 关闭录音
stream.stop_stream()
stream.close()
p.terminate()

# 将录音数据转换为数组
audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
code=hfmbm.encode_sentence()
# 将编码转换为超声波信号
# code = input("请输入编码：")
signal = encode_to_signal(code)

# 将超声波信号混入录音数据
mixed_data = (audio_data + signal[:len(audio_data)] * 10000).astype(np.int16)

# 将混合数据保存为WAV文件
with wave.open('mixoutput.wav', 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(44100)
    wf.writeframes(mixed_data)

# # 绘制波形图
# plt.figure()
# plt.plot(np.arange(len(mixed_data)) / 44100, mixed_data)
# plt.xlabel("Time (s)")
# plt.ylabel("Amplitude")
# plt.title("Waveform of output.wav")
# plt.show()

# 绘制频率随时间变化的频谱图
plt.figure()
plt.specgram(mixed_data, Fs=44100, cmap='gray')
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.title("Spectrogram of mixoutput.wav")
plt.show()
