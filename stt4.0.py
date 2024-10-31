'''
- 新增输入设备的选择功能。
- 在3.0基础上优化了音频回调函数,提前显示部分，视觉上加快速度。
- 结构上使用了多线程。
'''
import os
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import threading

select_input_device = 2 # 1为麦克风音频 2为电脑音频

# 自动获取所选设备索引
def get_input_device_index():
    if select_input_device == 2:
        dev_status = "BlackHole"
    else:
        dev_status = "麦克风"
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        if dev_status in device['name']:
            return idx
    raise RuntimeError(f"未找到 {dev_status} 设备")

# 设置参数  
samplerate = 16000  # 采样率  
channels = 1        # 通道数（立体声）  
dtype = 'int16'     # 数据类型（16位整数）  
blocksize = 4096    # 每个回调的块大小（帧数
device_index = get_input_device_index() # 获取所选设备索引


# 初始化vosk模型
def initialize_recognizer(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError("模型路径无效")
    model = Model(model_path)
    return KaldiRecognizer(model, 16000)

# 音频回调处理函数
def callback(indata, frames, time, status):
    if status:
        print(status)
    byte_data = bytes(indata)
    if recognizer.AcceptWaveform(byte_data):
        result = recognizer.Result()
        print(result)
    else:
        partial_result = recognizer.PartialResult()
        print(partial_result)  # 输出部分结果，提高反馈速度

# 捕获并指定回调函数处理音频数据
def audio_thread():
    with sd.RawInputStream(samplerate=samplerate, blocksize=blocksize, dtype=dtype,
                           channels=channels, device=device_index, callback=callback):
        print("开始录音，按 Ctrl+C 停止...")
        while True:
            sd.sleep(1000)

def main():
    model_path = "./vosk-model-cn-0.22"
    global recognizer  # 声明全局变量以便在回调中访问
    global device_index 
    
    recognizer = initialize_recognizer(model_path)

    # 启动音频处理线程
    threading.Thread(target=audio_thread, daemon=True).start()

    # 主线程可以用于其他任务
    try:
        while True:
            sd.sleep(1000)
    except KeyboardInterrupt:
        print("停止录音。")

if __name__ == "__main__":
    main()
