## 简单部署vosk 本地离线实时语音转文本
包括麦克风和设备系统内音源，可以实时转成文本形式。

应用举例：
- 看没有字幕视频，不习惯，想要字幕，但是平台不提供。
- 看异国他乡视频，听不懂，可以配合翻译接口，产生实时中文字幕。
- 线上开会，可以以文本记录。

tip：
- 模型选择可能导致转录或翻译不准确。

### 一、准备python环境
本例子使用Python 3.11.8版本。
python库：
- vosk
- sounddevice

### 二、安装虚拟音频设备软件

<blockquote>
如果只使用麦克风识别系统外部的声音，
可以省略此步骤。
</blockquote>
虚拟音频设备软件是为了把电脑系统内的声音路由到麦克风，可以识别正在播放的视频的音频。

我使用BlackHole 2ch。设备为mac ,所以我使用brew install BlackHole 2ch的命令安装，其他系统自行选择方法。

### 三、下载语言模型模型
[vosk语言模型列表](https://alphacephei.com/vosk/models)

我选择的是中文的大模型1.3G [《vosk-model-cn-0.22》](https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip) ,这个模型尚且准确度不尽人意，更别说40mb的小模型了，android等移动端本地离线stt长路漫漫。

### 四、实践
1. 解压模型
2. 查看音频输入索引
3. 修改代码中的参数
4. 运行

![正在实时stt电脑中播放的视频](https://s21.ax1x.com/2024/11/01/pADJHYt.png)

该截图使用的是github项目中的stt4.1版本.

释放时内存变化情况 -2G：
![内存占用](https://s21.ax1x.com/2024/11/01/pADJ7FI.png)

#### 查看电脑音频设备及其索引：
```
import sounddevice
print(sounddevice.query_devices())
```
举例：

```shell
(base) MacBook-Air ~ % python
Python 3.11.8 | packaged by conda-forge | (main, Feb 16 2024, 20:49:36) [Clang 16.0.6 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import sounddevice
>>> print(sounddevice.query_devices())
  0 “pointsun的iPhone”的麦克风, Core Audio (1 in, 0 out)
> 1 BlackHole 2ch, Core Audio (2 in, 2 out)
  2 外置耳机, Core Audio (0 in, 2 out)
  3 MacBook Air麦克风, Core Audio (1 in, 0 out)
  4 MacBook Air扬声器, Core Audio (0 in, 2 out)
< 5 多输出设备, Core Audio (0 in, 2 out)
>>>
```
