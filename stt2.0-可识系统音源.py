'''
从系统读取音源。利用了BlackHole 2ch 把输出的音频路由到输入（麦克风）中
'''
import os
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# 设置模型路径
model_path = "./vosk-model-small-cn-0.22"  
if not os.path.exists(model_path):
    print("模型null")
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
    byte_data = bytes(indata)
    if recognizer.AcceptWaveform(byte_data):
        result = recognizer.Result()
        print(result)
        
# 自动获取 BlackHole 设备索引
def get_blackhole_device_index():
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        if "BlackHole" in device['name']:
            return idx
    raise RuntimeError("未找到 BlackHole 设备")

# BlackHole 的设备索引
device_index = get_blackhole_device_index()

# 开始录音
with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                       channels=channels, device=device_index, callback=callback):
    print("开始录音，按 Ctrl+C 停止...")
    while True:
        sd.sleep(1000)

