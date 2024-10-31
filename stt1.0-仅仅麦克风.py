'''
从麦克风读取音源
'''
import os
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# 设置模型路径
model_path = "./vosk-model-small-cn-0.22"  # 替换为您的模型路径
if not os.path.exists(model_path):
    print("请下载并解压 Vosk 中文模型到指定路径")
    exit(1)

# 初始化 Vosk 模型
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# 设置录音参数
samplerate = 16000  # 采样率
channels = 1        # 单声道

# 实时音频识别
def callback(indata, frames, time, status):
    if status:
        print(status)
    
    # 直接将 indata 转换为字节格式
    byte_data = bytes(indata)
    if recognizer.AcceptWaveform(byte_data):
        result = recognizer.Result()
        print(result)

# 开始录音
with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                       channels=channels, callback=callback):
    print("开始录音，按 Ctrl+C 停止...")
    while True:
        sd.sleep(1000)
