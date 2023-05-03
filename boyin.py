import wave
import pyaudio

# 打开WAV文件
wav_file = wave.open('mixoutput.wav', 'rb')

# 获取WAV文件的音频参数
channels = wav_file.getnchannels()
sample_width = wav_file.getsampwidth()
frame_rate = wav_file.getframerate()
frames = wav_file.getnframes()

# 创建PyAudio对象
audio = pyaudio.PyAudio()

# 打开音频流
stream = audio.open(
    format=audio.get_format_from_width(sample_width),
    channels=channels,
    rate=frame_rate,
    output=True
)

# 从WAV文件中读取并播放数据
data = wav_file.readframes(frames)
stream.write(data)

# 关闭流和PyAudio对象
stream.close()
audio.terminate()
