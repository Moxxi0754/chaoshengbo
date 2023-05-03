import scipy.io.wavfile as wavfile
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt

# 读取wav文件
rate, data = wavfile.read('mixoutput.wav')

# 计算截止频率
nyquist_rate = rate / 2
cutoff_frequency = 15000 / nyquist_rate

# 创建滤波器
coefficients = signal.butter(4, cutoff_frequency, btype='highpass')
b = coefficients[0]
a = coefficients[1]

# 应用滤波器
filtered_data = signal.filtfilt(b, a, data)

# 计算噪声门限
noise_threshold = np.mean(np.abs(filtered_data)) * 0.1

# 去除背景噪声
for i in range(len(filtered_data)):
    if np.abs(filtered_data[i]) < noise_threshold:
        filtered_data[i] = 0

# 保存新的wav文件
wavfile.write('result.wav', rate, np.int16(filtered_data))

# 绘制频谱图
nfft = 1024
window = np.hamming(nfft)
f, t, Sxx = signal.spectrogram(data, rate, window=window, nfft=nfft)

f_filtered, t_filtered, Sxx_filtered = signal.spectrogram(filtered_data, rate, window=window, nfft=nfft)
eps = 1e-10
Sxx_filtered[Sxx_filtered <= 0] = eps


plt.subplot(2, 1, 1)
plt.pcolormesh(t, f, 20 * np.log10(Sxx), cmap='viridis')
plt.title('Original Spectrogram')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar()
plt.show()
plt.subplot(2, 1, 2)
plt.pcolormesh(t_filtered, f_filtered, 20 * np.log10(Sxx_filtered + eps), cmap='viridis')
plt.title('Filtered Spectrogram')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar()
plt.show()