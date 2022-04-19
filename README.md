# scanpen-serial-client
基于Pyqt5.0的串口工具

# 主体功能
支持串口设备设置打开/关闭，串口数据收/发，定时发送等

# 协议解析
适配了扫描笔的协议，可以在协议支持的范围内显示OCR文本、校准图片、切行图片等，并且可以支持手动校准等，并且集成了EVS协议，可以二次开发扩展

# released version:v1.0.1
增加协议解析支持 CSK4 扫描笔


# 系统要求
版本要求：python3.7及以上

# 使用步骤

**环境安装**
如果系统中有venv或者conda虚拟化环境，建议使用该类虚拟化环境进行环境创建

本工具依赖如下python软件包，请确保python环境已经安装如下软件包。
requirements:
```shell
colorama==0.4.4
eventlet==0.31.1
numpy==1.21.1
opencv_python==4.5.4.58
Pillow==9.1.0
playsound==1.3.0
prettytable==2.2.0
psutil==5.8.0
PyAudio==0.2.11
pynput==1.7.3
PyQt5==5.15.6
pyserial==3.5
pyusb==1.2.1
requests==2.26.0
websocket_client==1.3.2

```

此处以`anaconda`为例：
```shell
conda create -n py37 python=3.7
pip install -r requirements.txt
```
目前在macOS Big Sur 11.6.5 上测试可以正常运行


# 关于软件包分发
如果需要在特定平台(windows、Linux发行版本)进行软件包分发，可以使用`pyinstaller` 进行软件包打包分发。

如果基于本工程进行二次开发后，软件包如有更新，需要更新`requirements.txt`


# 如何生成requirements?

**pipreqs**

好处：可以通过对项目目录的扫描，自动发现使用了那些类库，自动生成依赖清单。

缺点：可能会有些偏差，需要检查并自己调整下。

使用方法:
```shell
pip install pipreqs
pipreqs ./
```

**pip freeze**

使用`pip freeze > requirements.txt`，这种方式需要配合virtualenv，否则把整个环境中的包都列出来了。

# 运行程序

**Linux**
```shell
conda activate py37
python src/serial_client.py
```

**windows下这样运行脚本**
```shell
set root=D:\tools\dev\Anaconda3
call %root%\Scripts\activate.bat py37

python src/serial_client.py

pause
```
