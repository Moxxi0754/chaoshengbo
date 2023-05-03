import wave

import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft
import numpy as np
import scipy.io.wavfile as wav1
import matplotlib.pyplot as plt
import hfmbm
import power

# 打开wav文件
file_path = "result.wav"
with wave.open(file_path, "rb") as wav:
    # 读取wav文件的采样率和采样数据
    framerate = wav.getframerate()
    data = np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16)
# Load the audio file
sample_rate, samples = wav1.read("result.wav")

# Calculate the spectrogram
# Calculate spectrogram for decoding
decoding_spectrogram, _, times, _ = plt.specgram(samples, Fs=sample_rate, NFFT=2048, noverlap=1024)
spectrogram, frequencies, times, _ = plt.specgram(samples, Fs=sample_rate, NFFT=1024, noverlap=512)

wantnum = 0
# Find the index of the desired time point
time_index = np.where(times >= wantnum)[0][0]

# Get the frequencies and corresponding amplitude values at the desired time point
frequencies_at_time = frequencies

# Find the frequency with the highest amplitude
# max_frequency_index = np.argmax(amplitude_at_time)
# max_frequency = frequencies_at_time[max_frequency_index]

# print("The frequency at time point", wantnum, "is", max_frequency, "Hz")
# 计算每个FFT数据块的长度和重叠量
fft_len = 1024
hop_len = fft_len // 2
spectrogram, frequencies, times, _ = plt.specgram(samples, Fs=sample_rate, NFFT=2048, noverlap=1024)

# Load the audio file
# 计算频率随时间变化的FFT谱图
spectrogram = np.abs(np.array([fft(data[i:i + fft_len]) for i in range(0, len(data) - fft_len, hop_len)]))
spectrogram_resized = np.resize(spectrogram, (len(frequencies), len(times)))

# 判断连续的0.06秒的低于15000Hz的时间段数量
num_zero_periods = 0
is_zero_period = False
for i in range(spectrogram.shape[0]):
    # 修改判断条件，判断是否有0.06秒连续低于15000Hz的时间段
    if np.all(spectrogram[i][:fft_len // 2] < 15000) and np.all(spectrogram[i + 1][:fft_len // 2] < 15000):
        if not is_zero_period:
            is_zero_period = True
            num_zero_periods += 1
    else:
        is_zero_period = False
# num_zero_periods = 0
# is_zero_period = False
# for i in range(spectrogram.shape[1]):
#     # 判断是否有0.06秒连续低于15000Hz的时间段
#     if np.all(spectrogram[:fft_len//2, i:i+int(0.06*sample_rate/hop_len)] < 15000):
#         if not is_zero_period:
#             is_zero_period = True
#             num_zero_periods += 1
#     else:
#         is_zero_period = False
print("The number of continuous 1s periods with frequency below 15000Hz is:", num_zero_periods)

# 找到第一个频率大于15500且分贝大于30的时间节点，作为需要译码的声波段的起点
# start_time = 0
# for i in range(spectrogram.shape[0]):
#     if np.any(spectrogram[i][:fft_len // 2] > 15500 and (power.calculate_energy(file_path, i * hop_len / framerate, 0).any() > 30):
#         start_time = i * hop_len / framerate
#         break
# print(start_time)
start_time_index = 0
for i in range(len(frequencies)):
    for j in range(len(times)):
        if frequencies[i] > 15500 and power.calculate_energy(file_path, times[j], 0.1) > 30:
            start_time_index = j
            break
    if start_time_index > 0:
        break

# Calculate the start time in seconds
start_time = times[start_time_index]
# 计算每一段需要译码的声波的持续时间
lasttime = (5 - num_zero_periods * 0.1) / (num_zero_periods + 1)
# print(num_zero_periods)
print("空白时间：", lasttime)
# 进行译码
result = ""
cur_time = start_time

while cur_time < 5:

    wantnum = cur_time
    time_index = np.where(times >= wantnum)[0][0]

    # Define the new set of frequencies to interpolate at

    # Interpolate the spectrogram to obtain the amplitude values at the new set of frequencies
    new_frequencies = np.linspace(frequencies[0], frequencies[-1], num=10000)
    amplitude_at_time = np.interp(new_frequencies, frequencies, decoding_spectrogram[:, time_index], left=0, right=0)

    # Interpolate the spectrogram to obtain the amplitude values at the new set of frequencies
    # amplitude_at_time = np.interp(new_frequencies, frequencies, spectrogram[:, time_index], left=0, right=0)

    # Find the frequency with the highest amplitude
    max_frequency_index = np.argmax(amplitude_at_time)
    max_frequency = new_frequencies[max_frequency_index]
    if 18800 <= max_frequency <= 19200:
        result += "0"
    elif 20800 <= max_frequency <= 21200:
        result += "1"
    else:
        print("Cannot decode at time {}".format(cur_time))
        cur_time += lasttime + 0.1
        continue
    # print(cur_time)
    cur_time += lasttime + 0.1

print("哈夫曼编码：", result)
print("译码结果：", hfmbm.huffman_decode(result, hfmbm.huffman_encode(hfmbm.letter_freq)))
