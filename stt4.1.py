import os
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import threading
import time
import re

select_input_device = 2  # 1为麦克风音频 2为电脑音频

# 自动获取所选设备索引
def get_input_device_index():
    if select_input_device == 2:
        dev_status = "BlackHole"
    else:
        dev_status = "Air麦克风"
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        if dev_status in device['name']:
            return idx
    raise RuntimeError(f"未找到 {dev_status} 设备")

# 设置参数  
samplerate = 16000  # 采样率  
channels = 1        # 通道数（立体声）  
dtype = 'int16'     # 数据类型（16位整数）  
blocksize = 4096    # 每个回调的块大小（帧数）
device_index = get_input_device_index()  # 获取所选设备索引

# 初始化vosk模型
def initialize_recognizer(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError("模型路径无效")
    model = Model(model_path)
    return KaldiRecognizer(model, 16000)

# 输出文件路径
output_file_path = f"./text/{int(time.time())}.txt"

# 提取双引号中的内容并去掉空格
def extract_text_from_result(result):
    match = re.search(r':\s*"([^"]*)"', result)
    return match.group(1).replace(" ", "") if match else ""

# 音频回调处理函数
def callback(indata, frames, time, status):
    if status:
        print(status)
    byte_data = bytes(indata)
    if recognizer.AcceptWaveform(byte_data):
        result = recognizer.Result()
        # 提取结果文本
        result_text = extract_text_from_result(result) + "。"
        # print(result_text)
        with open(output_file_path, "a", encoding='utf-8') as f:
            f.write(result_text + "\n")
    else:
        partial_result = recognizer.PartialResult()
        # 提取部分结果文本
        partial_text = extract_text_from_result(partial_result)
        # print(partial_text)  # 输出部分结果，提高反馈速度
        print("\033[2J\033[H", end='')  # 清空屏幕并回到顶部
        print("\033[1;33m" +partial_text + "\033[0m", end='', flush=True)  # 输出新文本

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
