# -*- coding: utf-8 -*-

from ctypes import util
from subprocess import call
import sys
import os
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QComboBox, QLabel, QWidget, QPushButton, QApplication
from PyQt5.QtGui import QPalette, QBrush, QPixmap

from PyQt5.QtCore import QTimer
from serial_client_ui import Ui_Form

# sys.path.append("..")
sys.path.append(".")
from plugins import utils as utils
from plugins import logger as logger
# audio play
import sys
import ctypes
# from sdl2 import *

import threading
import time

from pyevs import evs_linux

#from play_once import MyThread


class Pyqt5_Serial(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(Pyqt5_Serial, self).__init__()
        self.setupUi(self)
        self.init()
        self.setWindowTitle("串口小助手")
        self.ser = serial.Serial()
        self.port_check()


        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.receive_data_num_line_edit.setText(str(self.data_num_received))
        self.data_num_sended = 0
        self.send_data_num_line_edit.setText(str(self.data_num_sended))

        # audio play
        
        self.targetWavFile = ''
        self.targetWavDir = 'wav_kt'
        #self.targetWavDir = 'wav_light'
        self.isPlayEnd = 1
        self.playLock = threading.Lock()

        self.uart_data_init()
        self.evs_app_init()


    def init(self):

        self.com_dict = {}

        # 串口检测按钮
        self.uart_check_box.clicked.connect(self.port_check)

        # 串口信息显示
        self.uart_port_combo_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)  # 参照内容调整位置
        self.uart_port_combo_box.currentTextChanged.connect(self.port_imf)

        # 打开串口按钮
        self.open_button.clicked.connect(self.port_open)

        # 关闭串口按钮
        self.close_button.clicked.connect(self.port_close)

        # 发送数据按钮
        self.send_button.clicked.connect(self.data_send)

        # 定时发送数据
        self.timer_send = QTimer()
        self.timer_send.timeout.connect(self.data_send)
        self.timer_send_cb.stateChanged.connect(self.data_send_timer)

        self.timer_receive_period = 2

        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)

        # EVS WS接受定时器
        self.evs_timer = QTimer()
        self.evs_timer.timeout.connect(self.evs_receive)

        # 清除发送窗口
        self.clear_send_text_button.clicked.connect(self.send_data_clear)

        # 清除接收窗口
        self.clear_receive_text_button.clicked.connect(self.receive_data_clear)


        self.set_calibration_up_position.clicked.connect(self.set_calibration_position_up)
        self.set_calibration_down_position.clicked.connect(self.set_calibration_position_down)
        self.set_calibration_left_position.clicked.connect(self.set_calibration_position_left)
        self.set_calibration_right_position.clicked.connect(self.set_calibration_position_right)


        # 检测串口波特率button
        self.detect_uart_bauderate_button.clicked.connect(self.detect_uart_bauderate_start)

         # 协议串口波特率combo box
        self.set_uart_bauderate_box.activated[str].connect(self.set_uart_bauderate)

          # 协议模式切换combo box
        self.set_uart_mode_box.activated[str].connect(self.set_work_mode)

        self.get_uart_software_version_box.activated[str].connect(self.get_uart_software_version)

        # 串口绝对坐标设置
        self.set_calibration_button.clicked.connect(self.set_calibration_position)

        # hex_send
        self.hex_send.setChecked(True)
        self.hex_receive.setChecked(True)
        self.uart_state_ocr_tts_play_check_box.setChecked(True)
        self.uart_state_ocr_translate_show_check_box.setChecked(True)
        self.uart_state_ocr_dict_show_check_box.setChecked(True)

        # 设置x y默认坐标
        self.calibrationformLayout_x_pos_line_edit.setText("0")
        self.calibrationformLayout_y_pos_line_edit.setText("90")

        if False:
            self.send_text_text_browser.setText("""58 46 7B 1B 01 CB FF 00 53 00 01 00 00 00 30 00 B0 00 46 00 FA 00 50 1B 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF D8 FF E0 00 10 4A 46 49 46 00 01 01 00 00 01 00 01 00 00 FF DB 00 43 00 02 01 01 01 01 01 02 01 01 01 02 02 02 02 02 04 03 02 02 02 02 05 04 04 03 04 06 05 06 06 06 \
                                      05 06 06 06 07 09 08 06 07 09 07 06 06 08 0B 08 09 0A 0A 0A 0A 0A 06 08 0B 0C 0B 0A 0C 09 0A 0A 0A FF C0 00 0B 08 00 B4 00 80 01 01 11 00 FF C4 00 1F 00 00 01 05 01 01 01 01 01 01 00 00 00 00 00 00 00 00 01 02 03 04 05 06 07 08 09 0A 0B FF C4 00 B5 10 00 02 01 03 03 02 04 03 05 05 04 04 00 00 \
                                      01 7D 01 02 03 00 04 11 05 12 21 31 41 06 13 51 61 07 22 71 14 32 81 91 A1 08 23 42 B1 C1 15 52 D1 F0 24 33 62 72 82 09 0A 16 17 18 19 1A 25 26 27 28 29 2A 34 35 36 37 38 39 3A 43 44 45 46 47 48 49 4A 53 54 55 56 57 58 59 5A 63 64 65 66 67 68 69 6A 73 74 75 76 77 78 79 7A 83 84 85 86 87 88 89 \
                                      8A 92 93 94 95 96 97 98 99 9A A2 A3 A4 A5 A6 A7 A8 A9 AA B2 B3 B4 B5 B6 B7 B8 B9 BA C2 C3 C4 C5 C6 C7 C8 C9 CA D2 D3 D4 D5 D6 D7 D8 D9 DA E1 E2 E3 E4 E5 E6 E7 E8 E9 EA F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FF DA 00 08 01 01 00 00 3F 00 FC A6 86 EC C5 93 38 52 71 F5 AB 96 3A C2 2D C2 FC 9F 78 7D EC D6 \
                                      AD A6 B1 08 6C 80 A5 C8 CA B3 37 1F 8D 76 5E 0E F1 62 41 7F E6 B9 23 0F D7 66 7B 57 BD FC 2F F8 A3 75 60 D1 DF DB DD FD D1 81 9E 73 5F 49 FC 2E FD A2 0E 92 12 47 BB E4 70 4E 7A 75 F6 AF A1 7E 1E 7E D4 CC 85 3C A9 F2 0F 71 FF 00 EC D7 B2 78 63 F6 B0 B8 48 02 FF 00 6A 4A 83 FB BB F1 FD 2B A7 83 \
                                      F6 BD B8 89 3F E4 24 BE CF 23 67 F9 AD 41 AB 7E D8 37 66 3C 1D 4C E7 FE 99 29 AE 03 C5 9F B5 95 D5 DA B4 13 DD 13 E8 58 F4 AF 1C F8 83 FB 45 0B D8 E5 8E 3B 92 FF 00 DD ED CD 78 7F 8E BE 2F C9 7D 2B 47 71 73 F3 73 B2 BC 77 C7 BE 3A 92 E3 E7 37 3C 73 B7 9E 05 79 77 89 B5 59 E5 26 58 88 93 1F C3 \
                                      9A E6 AF DA 39 65 C3 C7 BF F7 7D 58 D7 CC A9 7E D2 C8 63 8F 39 29 82 73 C5 3E 1B CD 48 65 2D 6C B3 8C 05 AD 4B 4B 7D 66 6D A6 2B 69 17 27 EE EC C9 15 D4 F8 63 C3 FA F9 65 7B 8B B1 1A EE FB A6 33 E9 D6 BD 17 C1 7A 7D DF 98 A6 4B F2 4A B7 F0 1D B9 AF 5E F0 87 8B 22 D3 9B 72 5D 97 D8 C4 31 DB DB \
                                      B5 7A 7F 87 FE 2E 4D 0A 47 F6 77 3B 87 5C 7F FA AB B1 D2 7E 39 4E B1 64 6A 3B 4F F1 7C C3 FC 2B 49 7E 3E 5E AA E3 ED C7 3D B7 74 FE 55 5E EF E3 75 D1 CB 25 F7 E6 FD 2B 9F D6 BE 33 C9 E5 13 25 F9 66 3D 93 83 5C 9E AF F1 35 AE 77 24 92 7C E4 7F CB 43 9F E9 5C 76 BB E3 09 DD FC A8 F7 37 FB 44 FF \
                                      00 2A E4 75 7D 62 FA F4 B4 5D 88 E5 FA 8F C2 B9 9B A6 9E E6 EC C7 2C BB 50 FE 67 FC 2A 95 D5 94 A9 2A 25 BC 5B F9 FE 13 C5 70 51 FC 39 D2 A1 6D D3 68 D0 4D C7 53 08 6C FE 95 6A 2F 08 58 5B A2 CB 6B A2 DA 22 93 D2 38 00 AB 76 DE 15 81 25 65 8A 2D 9B B1 F7 3D 6A F6 9F E1 FB 82 C1 16 EB 6E 0F CF \
                                      BB A9 AD EB 3D 12 E6 D5 F6 C3 78 15 77 F3 BB BD 6E E9 D6 FE 43 EC 92 56 5F F6 47 7A DF D3 DE F9 9C 20 52 42 8E E6 B7 AC EE 67 79 05 B4 F2 1C E3 2F C7 6A D0 12 AA B0 FD FB 7C EA 70 3D EA 50 CC F8 1E 60 E9 9F 9B BD 2B C7 13 FF 00 AA 51 C1 CF 26 AB BD 8D BA 66 58 94 AB 95 FE 3F 4A CC 9F C3 8B 32 \
                                      79 F2 DC 9F F6 48 AA 77 3A 1C 68 EE 76 1D AC 98 70 C7 BD 67 4D E1 8C C7 B5 2D 03 9F 43 CD 33 FE 11 07 12 45 F2 85 24 F6 15 C3 0D 26 4F 3B 74 72 00 7A 8C 1E 31 E9 4D B4 D2 B6 62 09 64 6C 9F 6A BB 6F A7 4B 14 58 80 6E C8 F9 B8 E4 D5 BB 5D 3D 19 63 57 45 4C F7 0B 93 C5 5B B6 D2 5E E6 42 24 5D DC \
                                      9C B2 A9 1C 56 8D 9E 90 02 AD C4 B9 6E F1 7F 85 6B D8 AC 72 FC A5 9A 12 CD 9C FA 56 D5 8D A3 F9 2C 14 7F C0 FB D5 A8 AC ED 63 B7 06 E6 13 FD D2 E3 BD 58 B5 B4 96 D6 14 24 E4 27 72 79 35 68 42 B7 A1 76 A8 53 FC 44 8E 6A D4 1A 1C 89 13 B2 8F BC BD CF 4F F0 A8 7F B2 1A 39 51 A5 42 C8 38 45 5A 4F \
                                      EC 26 E8 E4 F0 DC C6 47 6A 2D BC 3F 19 86 5B 88 B2 84 9C 28 6F E7 50 37 83 5E 36 DF 34 ED F8 57 95 A6 9B 07 9D 85 DB EE DB 31 4C 9B 4D 91 EE 55 7C AD B9 ED 8A B1 06 99 23 DB 99 23 FE 1C F9 B9 EF 53 9B 3F 30 C3 34 36 BB 42 75 03 B5 5C B1 B4 C6 62 8A 30 49 43 D7 F9 D5 DB 3B 29 48 2F 2C 80 15 FB \
                                      80 71 5B 56 56 91 AE D9 E5 93 FE 59 72 3D 0D 68 DB 5B A6 CF 3D DA 1D 91 0D DE E7 35 71 6D 99 63 41 94 7F 54 AD 0B 4D 3E 17 F9 E3 8B 81 D8 FD 3A 55 9B 5D 36 0F 37 CC 85 78 EA 5B FB 9F 85 5C B7 D2 A3 76 26 16 F3 3E 42 55 08 A9 2D F4 F9 A3 83 CC 95 38 0B C3 1A 74 76 4D E6 AC D2 30 25 0F CB 81 53 \
                                      DC E9 F6 EF 3A C3 71 65 8D C7 20 8E B5 04 F6 92 EE F9 21 F9 7A 1C B7 41 5E 17 15 A9 4B A6 F3 63 F9 55 70 48 E9 9F 4A B1 FD 9D 8C 3F 99 8C 8E 32 3B FA D4 F0 5A 16 8C 70 AD BF 9A B5 6D 63 34 32 66 48 D7 FD 9F A5 58 9B 47 90 CF FE 8E 76 92 72 78 E2 A5 4B 05 7F F4 69 F0 B8 39 38 5F D6 B4 2D AD 51 \
                                      E1 4B 7F 25 98 73 8C 75 FA D6 C5 B6 9C 1A 08 DE 41 90 FF 00 26 E5 5F 4E D5 73 EC D6 DE 48 70 82 4D AC 01 E3 B5 69 E9 F6 B1 47 BE 4D 80 F2 36 E2 B4 AC F4 E8 09 FD EC 5B 64 53 D8 F5 AD CB 1D 22 DF 3E 45 B8 68 91 93 76 E4 EB 4E B7 D1 63 BF 22 3F B4 7C A1 4F 1D E9 ED A2 44 2D FE 5D 2F 2E DC 6E 4E \
                                      68 93 41 94 E5 E5 87 69 11 9D 9E 62 60 E2 AB A6 8E DE 58 F3 1F 1E 60 F9 9C F0 4F D2 BE 7E 7B 76 78 04 6B 22 FD CE 76 F5 A7 41 0A 82 92 E4 E4 FA D4 F6 DA 5D BB 2F DA 3E 71 93 C7 3D 2A D4 16 37 0F 7A B7 71 DB 6D 00 75 67 ED 5A 10 E9 D7 7B 9A E0 C8 18 67 77 FB 58 C7 4A B1 6D A5 C7 24 7E 63 9E 08 \
                                      E3 22 AC 59 E9 92 DB 94 45 87 AF 5E D5 A7 A7 69 D2 DC 1C 4A E5 17 77 1F 3F 4F 7A D3 B7 D2 E3 4C C7 1A C6 3D 0B BE 4B 7E 35 B5 A4 D9 3D BB 6F 92 DD 76 8C 61 47 35 A9 6B 63 18 3E 71 B2 E0 FC D8 EB BB DE B4 20 82 E2 D6 4C A8 C8 3D AB 5B 4D D1 FE D1 75 BD 61 3B BC 9C A6 3A 7E 35 3A E9 97 00 96 66 \
                                      61 E5 E1 7E 51 9D C3 DA AC C1 A1 BC 6E F7 77 6C 25 89 0F 1B EA 2D 47 4A B0 76 F9 34 DD E3 27 07 D2 BC 1F E1 4F EC F9 F1 3B E3 8D E5 F5 97 C2 0F 0C 1D 4E 5D 31 55 EF 17 76 36 E7 A2 E7 FB DE D5 6B C5 7F B3 6F ED 07 E0 29 5E 1F 16 FC 09 F1 04 31 C3 F3 6E B4 B0 F3 D5 C7 AF CB CD 72 B1 E9 97 31 49 \
                                      F6 47 87 B9 FB FD 46 2B EA FF 00 D9 03 FE 09 6B 69 FB 57 FC 1E D2 FE 30 DD FC 68 BC F0 FD B6 A7 24 D1 A5 85 9E 9F 1C A5 0C 72 32 75 73 EA 2B D7 AE BF E0 86 7E 04 D1 34 EB 8B E3 FB 49 78 B6 E6 78 2D 64 75 FF 00 89 55 A2 C7 95 52 7A 73 D7 A5 7C 1A 2C 65 7B F9 E1 5C 85 8A E6 58 C2 64 7F 0B 91 9A \
                                      B9 A6 E9 53 34 E5 A7 97 28 E9 91 CF 15 F4 17 FC 13 5F F6 61 F0 27 ED 3D F1 7B 59 D1 FE 29 68 66 FB C3 7A 16 9C 5A 5B 55 91 95 A4 9D F6 EC E4 11 D3 E6 FF 00 BE AB EC BD 7F FE 09 0D FB 27 6A 09 B7 C3 D1 EB BA 2F A1 B1 D5 1B 91 FD DC 3E 57 F4 CD 7C 77 FB 58 FE CF 5E 1A FD 9B BE 31 7F C2 A8 F0 56 \
                                      BB A8 6A B0 8B 35 B8 33 EA 7B 7C D4 DC 4E 13 E5 EB D3 AD 72 49 6A 4B DB D9 49 69 E5 5C A3 94 7F 9B 93 ED 5A 96 B6 92 C2 E6 C4 5B BB ED 5C 26 07 53 5A 7A 1E 95 76 DB 1D 6D 64 26 3F 94 05 19 AD C8 3C 37 74 CA C9 E4 B1 F3 79 DB 1F 51 EF 56 7F B2 AD E7 F9 7E C5 E5 85 1C 99 A3 E0 D5 3B CD 26 50 99 \
                                      F2 60 50 A7 E4 68 9F 83 5E A7 FF 00 04 44 F8 65 71 65 F0 CB C6 1F 12 2F 2D 9D 24 D5 FC 4A 62 B3 6F E1 7B 74 89 17 3F F7 D0 6A FB 63 C7 17 83 C3 FE 14 BD BE BA BF 92 18 A0 B2 95 E4 94 C9 F7 70 84 E6 BF 0C B5 2D 5A 4F 18 F8 BB 55 F1 4B 5B 08 86 A5 7F 73 75 1A 8E CA D2 31 FE B5 FA A1 FF 00 04 79 \
                                      B5 8F FE 18 33 C2 A3 EF 08 F5 0D 48 46 FE BF E9 72 57 D2 FA A5 9F DA B4 EB 98 F3 8D F0 32 8F CA BF 0B B5 5B 44 B3 F1 6E BB 60 53 CA 30 EB D7 FB 7E 5E DE 69 CD 4B 67 65 02 69 C2 EE 49 24 51 91 BC 7A 0A FD 25 FF 00 82 37 FC 28 FF 00 84 4B F6 71 D4 3E 25 DF 5A 6D BA F1 9E B7 25 C2 C8 E3 E6 F2 21 \
                                      67 82 3C 7A 2E D4 53 F8 D7 D7 9B 17 6E D1 5F 94 7F B5 0F 8D 1F E2 AF ED 45 E3 AF 15 3C DF BA 87 5A 7D 37 4E 65 E9 E5 DA 33 40 71 F5 60 C6 B9 6D 27 4B CA A4 72 6D 92 71 26 62 93 FB 83 FA 57 45 0E 9B 2F CA 61 91 B2 89 95 F2 8F 3F FE AA D6 D1 20 91 6D 2D 19 6E 33 BC 6F B8 00 F2 A7 D2 B7 34 AB 03 \
                                      AB 4E 37 AC 87 CD C8 49 55 31 B3 DE AD 08 5A C4 4E 27 FF 00 4A 48 59 E2 22 E3 E6 07 1F C5 59 1F F0 8E B2 43 17 D9 F4 CC 02 BF BC 12 13 81 5F 64 FF 00 C1 3B 7E 15 FF 00 C2 A8 FD 8D FC 0D A3 4F 19 4B BB ED 16 2D 46 F9 59 7E E4 B3 8D EC BF 99 AA 9F F0 51 7F 1F C5 E0 7F D9 5F C4 96 D9 63 7B AF D9 \
                                      CB A4 69 B1 C5 F7 9E 69 A0 93 EE FE 0A 4D 7E 4C 59 78 2F C7 EF E5 C1 A2 FC 38 F1 24 C6 28 B6 09 A0 D0 E6 31 83 F5 DB 8A FD 52 FF 00 82 4E F8 3F C4 DE 03 FD 88 BC 3F E1 5F 19 E8 37 5A 6E A3 06 AF AA 33 DA 5E C0 63 90 2B DD C8 EA 76 B7 A8 35 F4 71 88 38 F2 E4 5F 95 BA E6 BF 27 FC 5D FF 00 04 F6 \
                                      FD B2 2E 3E 24 EB ED A2 7C 10 37 56 D7 9A F5 E5 CC 17 93 EA 50 C6 AD 13 CC CC 9D FF 00 BA 40 AF 33 F8 ED F0 43 E2 9F C0 8D 4F 4E F0 67 C4 BD 02 1D 37 5B D7 A2 8D 74 EB 15 BA 12 FF 00 AC B8 5B 71 92 3A FC EC 3A 57 EC 67 C1 2F 86 16 7F 07 3E 10 F8 6B E1 75 9F DD D0 F4 58 2D 26 7C 7D F9 15 7E 76 \
                                      FF 00 BE B2 6B A9 B8 B5 5B BB 67 B7 3D 24 8D 90 FE 23 15 F3 5D A7 FC 12 8B F6 70 6B E9 75 1D 73 5B F1 2E A3 24 AE CE C2 4D 49 A3 5C B1 C9 27 61 CB 1F 7A E8 34 DF F8 26 7F EC A7 60 F9 FF 00 84 6F 53 94 E0 64 36 AD 28 CF E4 73 5E 45 FB 65 FE CD DF 0F 3E 04 AF 87 6F FE 19 E8 B2 59 5A 6A B7 13 DB \
                                      EA 10 1B 96 93 69 0B B9 59 77 1F C0 FF 00 FA EB C7 B4 9D 26 34 B4 86 78 ED 70 25 7D B3 9F 6C F7 35 D1 2D D6 8C EB 15 A5 8B 4E 23 8F EE 30 6E 83 EB E9 51 4B 79 1E 24 86 3D 2E 19 E3 69 B7 17 43 83 D3 A6 6A 1B FD 5A E9 65 12 3D 89 44 DA 7E 5D BB B1 EC 48 EF 5F A1 B6 D6 36 BA 5D AC 7A 5E 9D 08 8E \
                                      DE D6 31 15 BC 6A 38 54 5E 14 57 C4 9F F0 56 3F 12 EA B7 1F 18 3E 0B 7C 3C B7 BA F2 6D 7F E1 2E B2 D5 25 75 62 18 BF DB 16 CF 1F F7 C5 CB D7 DB 1A 5E 8B A5 68 B0 FD 9B 4B B0 8A 14 4F E0 85 00 15 75 4E FF 00 53 4E 3F DE C6 45 3B 3B B8 06 BE 4C FD A3 7E 03 C7 F1 BB FE 0A 6D F0 AB 50 D6 BC 3B 2D \
                                      F6 93 E1 3F 08 3E A7 A8 EF 88 9B 77 FD FD DF 94 AF FE D2 CE 20 75 FA 13 5F 5D 29 76 CB 48 7E 63 C9 A6 49 73 6D 07 CF 3D CC 68 BE AE E0 7F 3A B1 6F 2C 53 47 BE 17 56 1D 99 4E 6A 6E D9 AF 97 7F E0 A1 9A BE 8F E2 4D 3B 42 F0 DF 87 F5 4B 5B BD 47 4E D6 24 1A 8D 9C 37 2A D2 5B 03 07 F1 AE 72 9D AB \
                                      E7 3B 88 DE C2 25 D2 AC BF D2 63 25 7E D2 F9 DB 8F C2 AC 5B 3D 92 C0 CA 2D C3 4B E6 61 77 8E D5 1C 02 78 A6 2D 3C 01 14 86 DF 12 8E 01 E2 A4 D5 E7 FB 54 69 04 36 8A 86 1E 8D 0A 72 DE E7 DE BF 43 4A B3 0D EA 3E B5 F0 2F FC 16 27 57 7F 0A FC 61 F8 51 E2 A8 E3 F9 E0 DF 20 C2 67 3E 45 D4 57 18 FF \
                                      00 C8 78 FC 6B A0 B5 FF 00 82 D1 F8 06 58 D2 08 3E 01 F8 A2 47 F2 97 71 2D 07 CA F8 E4 73 30 24 7A 37 E9 5F 46 7E C7 9F B4 B4 1F B5 77 C2 BB 9F 8A 96 BE 14 6D 1E 18 B5 FB AD 35 2D 1E 6F 31 BF 73 B7 2C 48 E3 A9 35 EA D8 F9 37 6F AF 83 3E 3D 7F C1 50 BE 3A FC 35 F8 97 E2 9F 08 F8 6F C1 7E 13 5B \
                                      0F 0E 6B B7 B6 42 EB 50 5B 92 F2 A4 12 B2 65 B6 B6 3B 67 8C 57 D7 BF B3 47 8A 3E 2D 78 EB E0 B6 83 E3 6F 8D 7E 19 B2 D1 FC 45 AA DA 9B 8B BD 2F 4E 47 54 B6 46 63 E5 AE 24 24 EE D9 B4 9E 7A 9A EF BF 87 8A FC E7 FD BD FC 55 E3 EB 6F DA EF 56 D0 07 C4 1D 6E D6 C6 3B 4B 79 6D 2D EC B5 69 61 44 57 \
                                      1D 82 9E B9 5E BE F5 F4 9F FC 12 DE E3 50 D4 3F 66 59 2E 35 2D 6E FA FE 4F F8 4B 75 24 33 6A 17 8F 33 E4 49 86 19 72 70 33 FD 6B E8 FB AF 31 21 26 3E BB 4E 2B F3 67 5A D4 CD CE B3 AD CF A3 22 99 AE 35 CB F9 E5 B9 27 1E 6B 35 CC 87 39 1E BD 7F 1A A4 D2 EA A6 EE 1B 49 22 40 4C 7B 9A 40 F9 07 35 \
                                      AA 97 D7 7E 72 25 CC 22 64 80 6C 5F DD F4 FA 9F 4A 86 DE D6 3B CD 62 58 1C 6D 66 CE D6 07 EF FD 69 F1 45 7A AE 21 B9 68 52 25 0C AD B5 B7 13 5F A1 BF C2 4E 2B E0 6F F8 2D DD A2 7F C5 AD D5 0A FF 00 AB D5 6F 63 C8 EF BA 06 E3 F4 AF 89 AC 72 A3 6A C7 D7 98 DF A1 AF D1 CF F8 22 D5 C1 9B F6 4D D7 \
                                      2D 87 FC B0 F8 8D A8 A9 5F 42 63 85 CF FE 85 5F 5C 3A F7 02 BF 20 7F 6B 61 75 1F ED 33 F1 2E C5 2D 83 C5 1F 8F 2E AE 7E CD 20 F9 6E 3F D2 CC 8F 1F D1 86 47 E3 5F AC 5F 05 FC 79 A0 7C 53 F8 5D A0 FC 42 F0 C5 C7 99 63 AA 69 B1 CB 01 C8 E3 F8 4A F1 E8 CA 45 75 3B 72 30 06 2B E0 9F F8 2A 1F 87 D7 \
                                      45 F8 FB A0 EB FF 00 74 6A DE 13 DB 27 CB C6 E8 AE 64 FD 70 C3 F2 AF 77 FF 00 82 61 69 53 E9 BF B2 BD 85 DD CC 5B 17 53 D6 AF AF E0 3F DF 49 25 E0 FF 00 3A FA 12 E9 D2 1B 69 24 67 00 2C 6C C5 98 F0 38 AF CB 2D 0E F1 2F 22 5D 5A 3F 34 8B E9 64 93 62 9F 95 51 FA 56 BA CA 26 D4 3E CD 04 AC C8 36 \
                                      8C 63 EE F1 5B 11 2D BA A8 28 B9 8B 1F 38 F3 33 54 2D EF 65 B7 F1 00 F2 20 07 30 F2 CF 9E 2A DC B7 B1 47 17 94 B1 2A 3E EC 0C 7F 19 AF D0 EE 0F F8 57 C3 FF 00 F0 5A CD 30 5C 78 53 E1 8D F2 B6 0A F8 C2 48 B8 F4 36 77 07 FA 57 17 FB 21 FF 00 C1 33 7E 19 FE D3 7F 02 F4 4F 8D BE 31 F8 A1 E2 7D 3F \
                                      FB 63 CE 31 E9 DA 3D C2 22 85 49 9D 3E 62 72 7B 57 DA FF 00 B3 37 EC C9 F0 EB F6 53 F8 7D 37 C3 3F 86 4D 7A F6 37 5A 9B DF DD CF A8 4E 5E 59 67 65 54 2D 9E DF 2A 28 C0 F4 AF 46 DB F2 ED AF 1B F8 85 FB 01 7E C8 DF 14 BC 69 7D F1 1B C7 BF 06 AD B5 1D 6B 51 6D D7 D7 CD A9 DD C6 65 3E A5 52 50 BF \
                                      A5 61 6B 7E 25 F8 33 FF 00 04 F7 D1 74 EF 05 78 47 44 97 4D F0 EE B1 24 F2 DA 58 CB 7D 73 73 15 BC E1 46 76 79 8E DE 52 61 73 B1 70 B9 DD D0 9E 7D AF E1 77 8D 2D BE 25 7C 36 D0 FE 22 59 A8 F2 35 BD 2E 2B D8 76 7F 72 41 91 DC FF 00 3A F9 D3 FE 0A C1 E0 FB 79 BE 0B 68 9F 16 98 EC 93 C3 1E 23 82 \
                                      29 5B 66 73 6F 75 98 5B 77 B0 62 87 EB 5E B3 FB 0E E8 37 BE 1A FD 93 3C 03 A4 EA B6 6D 0D CA E8 5E 6C F1 48 98 60 64 9A 49 3A 76 FB D5 D7 FC 72 D6 26 F0 E7 C1 7F 18 78 8A DF 1E 65 97 84 F5 29 A2 CF 4D CB 6B 21 15 F9 B1 E1 F1 34 B1 C1 6E F6 C1 56 68 77 E4 0C 7E 03 DA B6 52 CD 22 68 9C DD AF 9C \
                                      1B 6A E1 BA 7B D6 84 56 D1 DB C7 F3 5C 46 C0 13 E6 03 D2 A3 DB 0C D1 C8 27 71 92 DC 7A 54 72 CF 62 AB 1F DB 24 5D D0 E7 CB 01 0F E7 5F A2 1A 2E A7 67 AD 69 16 DA D5 91 CC 17 76 E9 3C 2C 7B A3 0C 8F E7 5F 1B FF 00 C1 69 6C BE D5 F0 8F E1 FD C2 8F F5 5F 10 63 1B C1 E9 9B 3B 9A F4 DF F8 25 54 C2 \
                                      4F D8 6F C1 E3 CB FF 00 57 25 F2 FD 7F D2 E4 E6 BE 85 BA BB 8A D2 13 3D D4 CB 1C 48 A5 9E 47 6C 05 03 A9 27 B0 AE 7A C3 E3 3F C1 CD 4B 53 4D 0B 4C F8 C1 E1 3B 9B D9 5F 64 56 70 78 96 D5 E5 76 3D 00 41 26 49 AE 9C 2B 1A F8 F3 FE 0A D9 0F 93 E1 9F 04 EA 3C 82 DA F1 B7 F9 78 DE 3C 99 DF 1F 86 DC \
                                      FE 35 E9 BF F0 4C 8F 1A 1F 17 7E C7 1E 18 B1 98 8F B4 E8 32 DE E9 97 0B 9E 7E 4B B9 BC B6 3F EF 26 0F BD 7A D7 C6 2F 85 9A 07 C6 7F 87 7A 97 C3 7F 11 CF 73 0D B6 A5 08 C5 D5 91 02 6B 69 54 EE 8E 64 DC 0A EE 56 01 BE 60 47 1C 8A DB F0 A7 87 EC FC 2B E1 AB 0F 0C 69 CB 88 34 EB 28 AD 60 19 3C 24 \
                                      68 14 75 CF 61 5E 53 FB 79 F8 D5 FC 25 FB 3A EA 36 96 CE 04 DA E5 DC 5A 4A EE F4 99 5F 77 D7 E5 0D 5F 0C D9 C5 24 10 7D 9A 1B A9 37 6D 50 46 CC 67 1D 6B 6A D2 08 9D BC DB 4B 6D C9 B7 E7 62 38 53 D6 96 09 A0 78 E4 65 88 75 C2 0D B5 31 B5 75 9C 79 43 F7 7B BE 4D E3 DB 9F C2 9B F6 3F 36 CC 79 91 \
                                      12 E0 65 DD 47 CB 5F 7B 7C 22 81 63 F8 45 E1 58 C7 6F 0D 58 FF 00 E8 84 AF 98 3F E0 B2 70 B4 9F 01 FC 1F 70 0F FA 9F 88 56 C4 E3 DE D2 E8 57 61 FF 00 04 99 96 49 3F 62 2D 05 25 93 FD 4E B1 A9 C6 BF EC 01 76 FF 00 2D 7B 2F ED 04 17 FE 14 27 8E 55 BB 78 2B 56 FF 00 D2 39 6B F2 2F E0 54 29 A7 FC \
                                      51 F0 37 88 2D 52 14 BF 8B C4 36 A1 0E D5 CB EE F9 4F 3D BE 53 5F B4 F3 E3 ED 12 28 FE F1 C7 E7 5F 23 FF 00 C1 5B 6D 43 FC 38 F0 75 F4 8D B9 62 F1 6A 2F 96 D8 F9 37 5A DD 8D C3 BE 4F F2 15 C7 FF 00 C1 27 FE 28 D8 78 7F E2 97 8A FE 08 5D 49 E6 36 B9 A7 DB EA 9A 4C C0 FD D1 6A AE B2 C5 8F FB 68 \
                                      1B F3 AF BD 63 E5 37 1E 69 E3 91 D3 15 F1 CF FC 14 B3 C5 50 6B 1E 33 F0 7F C3 B8 EF 1B 1A 4F 9B AB DE 20 FB A1 D8 18 62 FC 71 E6 FD 2B C0 2D B7 DD C8 E9 B7 6E DE 32 3F 87 DA B4 3C D8 CC 42 33 95 54 09 87 5F EF 52 C9 A9 F9 3B CC 71 22 73 80 DD 73 8A 7C 57 F7 3F 2D CC 73 FD DF EE 7A 8E D5 12 6B \
                                      57 8E 87 3F BB F3 64 C6 7A E2 BE F5 F8 25 78 D7 FF 00 04 BC 17 7E 4F FA DF 09 E9 EF FF 00 90 12 BE 73 FF 00 82 C6 2E 3F 66 5D 0A E9 F0 04 7F 10 6C 32 FE 9F E8 D7 75 AF FF 00 04 87 D4 0D FF 00 EC 6F 04 5B 3F E3 D3 C5 3A 8C 01 87 49 30 CA 77 57 D0 5F 15 AD 53 52 F8 57 E2 9B 29 09 DB 37 86 75 08 \
                                      D8 2F 5E 6D A4 15 F8 CF F0 76 E2 69 7C 59 E0 BB 9B 94 FF 00 51 E2 6B 12 FB 3D A7 5F E9 5F B7 AD B1 A6 63 BB F8 BA 8E F5 F2 97 FC 15 9E D9 64 F8 3B E1 29 B2 47 97 E3 88 37 63 BA 9B 5B B1 8F E5 5F 24 7C 11 F1 1F 89 BC 11 F1 D3 C2 3E 2D F0 35 A6 75 38 35 D4 86 04 B7 8C B3 CB 6F 37 EE A5 5C 0F FA \
                                      66 EC 7F 0A FD 71 FF 00 55 3C 91 AF 4D E7 6D 07 3B 76 81 9A FC DF FD A5 35 AF 12 F8 87 E3 D7 89 6F FC 5B 67 73 6C EB AB CF 6F 6B 6D 2C 45 0C 76 C9 2B 34 2A 7F 07 DD 9F F6 AB 9E D1 6E A3 8E D0 42 D0 C5 B8 87 67 03 FB C6 A2 85 ED 20 B8 49 61 8F E4 45 D8 57 3C 6E A9 A2 78 A2 BB 1F 69 99 64 45 6F \
                                      95 01 E9 EB 56 05 CF D9 DB 6C 56 C0 9D D9 DB EF 4C BA DC 98 DA B8 5D F9 39 FE 75 F7 3F EC B7 74 2E FF 00 66 8F 87 B3 A4 78 53 E0 DB 00 A3 D8 44 00 AF 12 FF 00 82 C1 42 F3 FE C8 F0 B2 AF 11 F8 D7 4F 2F CF 45 F2 EE 05 33 FE 08 DD 2B AF EC AD A9 D8 C9 26 45 B7 8D 2E 84 6B FD D0 63 8C E3 F3 CF E7 \
                                      5F 50 F8 A3 4B 7D 6F C3 1A 96 87 0C BE 5B DF E9 D7 16 CB 21 FE 13 24 65 73 FA D7 C6 DE 11 FF 00 82 43 CD A3 F8 87 4D D4 EE FE 35 AA 41 A7 EA 10 DC AC 76 7A 1F F7 24 57 28 37 49 C7 4C 64 93 F8 D7 DB 89 1E 17 E4 8B 03 1C 28 AF 98 BF E0 AB 1B 17 E0 06 89 34 87 E4 5F 1C 58 E5 47 5E 61 B8 03 F9 D6 \
                                      1F FC 13 6B F6 67 D5 F4 8B 86 FD A1 BC 7B A5 1B 69 EE AD CC 5E 1B B6 66 39 4B 66 5C 34 B8 EC 5B FB DF EC F1 D4 E7 EC 64 1C 61 8F 35 2F 1D EB CB 3F 69 7F D9 83 C2 BF 1F F4 1F B5 A9 FE CF F1 1D A2 7F C4 BB 56 8F A9 DB 9C 47 2F F7 97 E6 3F 4C D7 C3 1E 36 F8 73 AF FC 3D F1 1C 9E 0F F1 8C 12 5A 6A \
                                      71 A1 31 C6 40 02 7C 75 65 F5 EA 32 3B 7D 30 4D 28 6E 6D E5 87 CA 96 2C FC D9 0A 3F BD E9 57 5B EC 81 D6 28 6D 30 C7 AE 6A 5B 91 A7 79 87 7C 05 8F 18 6D DD 6A 2B F8 EE 89 FD C3 0F 21 C0 DF FB C0 70 6B EC CF D8 A2 EA EA E3 F6 43 F8 6B F6 CB 8F 36 7F F8 44 2D 04 B2 8E 8C D8 E4 D7 99 FF 00 C1 5D \
                                      00 3F B1 8E A1 37 FC F2 F1 0D 8B AB E3 EE 1F DE 7C D5 CD FF 00 C1 14 B5 03 71 FB 3D 78 BA DC B0 7F 27 C7 4D B4 FF 00 7B 36 90 D7 D8 FB C7 DE CD 38 02 C3 20 FD 79 A7 87 C7 4C 74 FE F0 AC AF 11 F8 27 C2 9E 31 7B 43 E2 6D 16 2B DF B1 5C 79 F6 9E 6B 1F DD C9 8C 6E 18 3D 7A D6 DC 31 24 28 23 89 40 \
                                      00 70 00 AC 9F 88 1F 11 BC 21 F0 AB C1 D7 DE 3C F1 DE B5 1E 9F A5 69 F1 EE B9 B8 93 D7 F8 51 47 57 76 3C 2A 0E 49 35 87 F0 07 F6 88 F8 71 FB 47 F8 3D FC 65 F0 E7 53 F3 22 86 E7 C8 BC B4 9F 68 B8 B3 93 1B 82 4C 80 9D 84 A9 07 DC 1E 33 5D F6 EE 3A 57 8D FE DC 1E 13 F0 0E AB F0 1B 58 F1 27 8A F4 \
                                      F8 9A F7 4B B7 69 74 3B 8F BA F1 DE EC 61 16 1B AF 53 C8 EE B9 07 8A F8 5E DA 26 FE CF 17 D6 93 05 DF B4 4C 57 BD 68 CB A9 24 71 C7 1F D9 FE EA 63 2D D4 52 5C 6A 56 82 EB E5 B6 2B 80 07 9B 8C D4 77 39 79 95 63 9F 0E EC 7F 83 AF 15 F5 EF FC 13 EB 52 1A 97 EC 53 F0 E6 54 1C 45 E1 E1 0F 5C F0 92 \
                                      BA FF 00 4A E7 3F E0 A9 BA 7C 5A 9F EC 43 E3 04 74 E2 18 E3 93 3E 9D 79 FC AB E5 1F F8 27 3F ED B1 F0 AB F6 4D F0 FF 00 8A 7C 29 F1 2E DB 59 36 3E 20 D6 61 BD D3 6E 34 EB 0F 34 44 EB 08 89 91 86 EE FB 41 DD 5F 46 EB 5F F0 57 EF D9 6A D6 C9 9F 4E D2 FC 65 23 91 FB A2 BA 12 02 7D C7 EF 6B E1 1D \
                                      7F F6 87 F8 EF E2 7B A9 AF AF FE 31 F8 9E DE DE 49 DC C3 66 BA A4 88 62 88 B1 28 85 91 F2 58 2E 01 3B 8F 23 AD 41 65 F1 33 E2 19 8D AF 1F E2 6F 89 B2 AD B8 6D F1 05 C6 77 7F DF 75 F7 4F FC 13 43 F6 BA D5 3C 74 93 7C 04 F8 AF E2 E9 2F 75 BB 78 16 5F 0E 5E DD EE 69 35 08 00 63 30 67 3D 59 30 3F \
                                      06 FA 13 F5 C6 AF AF E9 7E 1B D2 67 D6 F5 CD 42 3B 6B 4B 65 DD 3C D2 76 FF 00 EB D7 E7 47 ED 89 FB 5B 4B FB 47 F8 C6 DF 49 F0 D4 BE 4F 85 B4 59 58 E9 7B 88 22 EE 7E 50 DC 7D 36 E5 41 EF B8 E3 8E 5B 82 F8 43 F1 5B C7 9F 05 FC 7D 1F C4 9F 87 1A 96 CB F8 E3 10 5F C0 E4 AC 1A 95 BE EC FD 9E 70 3A \
                                      8F EE B7 DE 8D B9 1D 59 5B F4 A7 F6 74 FD A2 3C 21 FB 40 78 21 3C 47 A0 CB E5 5F 40 7C BD 57 4A 97 89 6D 25 FE E9 1E 9D C1 1C 11 C8 AF 14 FF 00 82 92 7C 50 65 FF 00 84 73 E0 ED 9B A3 AD EC 8D A9 EA 3E 5B 7C E9 E5 FC B1 29 1F DD 6D ED FF 00 7C D7 CC B6 12 40 F6 CB 04 23 FD 51 CF CA 2A 66 7B 3B \
                                      B8 9C 49 91 22 9F 97 E4 EF FD 2A C4 49 F6 38 D2 45 6C B4 83 9D DE B4 E8 ED 76 DC 4F FD 9F 65 8C 71 9D DD 2B 5B F6 23 FF 00 82 96 7C 0A F8 05 FB 36 F8 77 E1 27 C5 74 D6 7F B4 74 68 A5 1E 66 95 A5 99 D1 D1 A6 77 F5 1C F2 78 FF 00 1A 5F DB 47 FE 0A 61 FB 39 7E D0 7F B3 A7 89 FE 0E FC 34 9B 5C 1A \
                                      B6 B5 A7 34 36 CD A9 68 8F 0A 23 15 61 C9 CF 1D 6B E2 58 AF 88 01 25 F9 94 60 28 C7 A5 4B 11 45 9C DB C8 C0 31 C6 C6 DB D0 D5 F2 8A 90 E2 25 DC C0 E1 8F AD 5D B1 B8 8D 6D FC DB B9 C8 D8 46 D4 31 FD EF 53 9E D8 AD BF 0A 78 97 57 D0 3C 45 63 E2 5D 22 F4 D9 DE 69 57 8B 75 A7 5C C2 F8 78 E4 53 F2 \
                                      90 7E 99 1E E0 90 78 24 57 B1 7C 75 FD B4 FE 34 FE D2 5A 55 8F 85 BC 5F 25 B6 9B A7 E9 F0 62 7B 6D 21 99 23 D4 E5 FF 00 9E B2 0E DF EE 74 FC 32 0F 9B E9 F7 37 52 DC 46 65 B2 8B AF 5F 41 5B 96 13 46 8C 8A 77 03 F7 B7 2D 75 BE 01 F1 E7 8E BC 07 E2 44 D7 3C 01 E2 8B AD 22 FF 00 EE 8B AB 59 31 E6 \
                                      0E BB 64 1F C6 BE DF E2 6B 4B C5 3F 15 7C 63 F1 47 C5 77 1E 2D F1 EE AB F6 ED 56 58 D6 37 BB F2 95 46 07 40 02 E0 00 3D 2A BD 96 AF F6 29 BC C3 CB A7 0D 1F D6 B4 A3 9C 5E B8 8F 1B 26 C6 41 6E F5 25 96 B1 F2 24 0D B6 45 1B 8E F2 2A 71 A9 CB F6 65 DE E0 64 73 B4 57 C3 B1 DF DC 46 55 2D 11 7E FE \
                                      E4 52 D5 3A 6A 32 CD 73 E6 48 22 75 23 98 FB E6 AC C3 7C 96 C0 C3 3C F8 90 A7 DD AB B6 32 C6 AF 14 AE 88 C1 A3 F9 AA CA DD 49 70 EF B4 79 68 9C 9F 96 AC 41 77 64 61 D8 6E 64 F9 8F 19 5E 95 7E C2 E8 7D AB FD 21 BE E8 DA AA C3 B5 6A E9 F7 19 B9 F3 8C BC 01 D2 B4 AC 6E A6 FB 59 31 90 D8 E8 73 C1 \
                                      CD 6F 58 CD 78 9F BA 91 D7 6C 44 7D E9 32 7E 95 B3 06 B5 25 F9 91 36 20 11 9D A8 CB DE AD E9 86 44 97 C8 5B 65 E1 32 64 CF 4A D3 D2 ED D1 B7 5C AE 15 9B EF 67 D6 B6 91 8C B7 46 49 5C 24 67 0A AD 8C E2 A3 8F CA B7 CC 12 4E 77 26 7F D5 8A 75 C2 DC 34 4D 6D 05 C1 C0 5F DD BD 7C 43 62 7F 8B FD AF \
                                      F0 AB 16 F6 E8 7E 4F A9 A9 D2 63 E6 A9 D8 BF 36 33 C5 4D 77 79 71 0B 3C 88 FC 8E 95 A1 0C F3 4A 52 C9 A4 3B 24 87 7B 62 AD 69 D2 33 5A EF 7E 71 D0 1A BD 61 FB FB 2B AB B9 7E FC 7B 76 9F CF FC 2B 67 41 55 BC DC 2E 7E 7C DA 02 72 7B F3 56 63 F9 B4 DF 37 A1 E3 A7 6E B5 B3 A6 27 99 69 6F 72 CC 77 \
                                      B4 43 27 35 B3 A7 3C B6 B7 3B 2D E7 65 1E C6 B7 E1 B9 68 6F F2 8A 3E 44 FC EB 42 DB F7 D7 0D 93 8C 05 65 C7 63 CD 68 D8 5C DC FD AF 6B DC BB 2F 1F 2B 1E 29 16 53 24 DF 30 18 67 1B 96 9D 3D D4 F1 4D 2C 62 4F 95 65 DA 14 D7 FF D9 C2""")

        
        pix = QPixmap(128, 180)
        pix.fill()

        self.lb1 = self.label_calibration
        # self.lb1.setGeometry(900,100,300,200)
        # lb1.setStyleSheet("border: 2px solid red")
        self.lb1.setPixmap(pix)

        """ x_pos : 0 ~ 112"""
        """ y_pos : 0 ~ 140"""
        self.x_pos = 64
        self.x_pos_range = (0, 112)
        self.y_pos = 70
        self.y_pos_range = (0, 140)

    def evs_app_init(self):
        evs_linux.evs_app_init()
        self.evs_kwargs = {}
        # self.evs_timer.start(1000)

    def uart_data_init(self):      
        self.uartFrameHeaderTag = '5846'
        self.uartFrameHeaderLen = 6
        self.uartFrameDataLen = 5
        self.uartFrameLenByte = 11
        self.uartRecvList = list()
        self.image_counts = 0
        self.uartRecvHexStr = ''


        self.uart_frame_command_type_dict = {"设置CSK通讯串口波特率": 0x02, "查询软件版本": 0x19, "设置工作模式": 0x50, 
                                             "设置参数": 0x51, "下发合成文本": 0x53, "下发合成认证码": 0x54, 
                                             "下发手动校准信息":0x55, "下发校准绝对坐标": 0x56
        }
        self.uart_frame_response_type_dict = {"命令帧反馈": 0x01, "反馈工作状态": 0x50, "反馈标定状态": 0x51,
                                              "反馈软件版本": 0x04, "反馈合成加密码": 0x52, "上传通用数据": 0x53
        }

    def start_timer(self, slot, callback = None, expect_result= '', timeout=1000, interval=2):
        counter = 0
        count = int(timeout / interval)
        result = None
        def handler():
            nonlocal counter
            nonlocal result
            nonlocal expect_result
            nonlocal timer
            nonlocal callback

            counter += 1
            result = slot()
            # print('result:', result)
            if (result is not None and result != '' and result == expect_result) or counter >= count:
                # print('timer is going to close...')
                timer.stop()
                timer.deleteLater()

                callback(result, expect_result)


        timer = QTimer(self)
        timer.timeout.connect(handler)
        timer.start(interval)

        return result

    def uart_send_sync(self, cmd_hex_str, callback = None, expect_result = '收到正确的命令', timeout=1000, interval = 2):
        self.send_text_text_browser.setText(cmd_hex_str)

        # 停止定时器
        self.timer.stop()

        self.uartRecvHexStr = ""

        self.data_send()

        self.start_timer(self.data_receive, callback = callback,  expect_result = expect_result, timeout= timeout, interval = interval)

    def detect_uart_bauderate_start(self):
        if len(self.com_dict) == 0:
            logger.LOGE('未发现串口设备')
            return 
        def callback(result):
            self.detect_uart_bauderate_button.setEnabled(True)

            if result:
                self.detect_uart_bauderate_result_label.setText(f"检测成功: {result}")
            else:
                self.detect_uart_bauderate_result_label.setText(f"检测失败")

        self.detect_uart_bauderate_button.setEnabled(False)

        self.detect_uart_bauderate(baudrate_index=0, callback_function= callback)
    
    def detect_uart_bauderate(self, baudrate_index = 0, callback_function = None):

        def callback(result, expect_result):
            nonlocal baudrate_index
            nonlocal baudrate_dict
            nonlocal callback_function
            nonlocal baudrate

            print(f'set_uart_bauderate: [{result}]' )
            # 开启串口数据接受定时器
            self.timer.start(self.timer_receive_period)

            if result == expect_result:
                if callback_function:
                    callback_function(baudrate)
                return
            else:
                if baudrate_index >= ( len(baudrate_dict.keys()) -1 ):
                    logger.LOGE('detect_uart_bauderate:[未检测到CSK波特率]')
                    logger.LOGI('设置为默认波特率115200')

                    if callback_function:
                        callback_function(None)

                    self.port_switch_baudrate('115200')
                    return
                else:
                    baudrate_index += 1
                    self.detect_uart_bauderate(baudrate_index, callback_function)

            
        # if not self.ser.isOpen():
        #     logger.LOGE('串口未打开')
        #     self.port_switch_baudrate('115200')
        #     return
        

        baudrate_dict = {"115200":0x03, "1000000": 0x05, "1500000": 0x06, "3000000": 0x07}
        baudrate = list(baudrate_dict.keys())[baudrate_index]

        # 串口切到该波特率
        self.port_switch_baudrate(baudrate)

        cmd = [0x58, 0x46, 0x0e, 0x00, 0x04, 0x53, 0xf0, 0x00, self.uart_frame_command_type_dict.get('设置CSK通讯串口波特率'), 0, 0 ]
        if baudrate in baudrate_dict.keys():
            cmd[-2] = baudrate_dict.get(baudrate)
        else:
            print("协议串口使用默认波特率[115200]")
            cmd[-2] = baudrate_dict.get("115200")

        cmd[2], cmd[3] = self.int_to_list(len(cmd))
        cmd[5] = self.get_frame_lrc(cmd, 0, self.uartFrameHeaderLen -1 )
        cmd[-1] = self.get_frame_lrc(cmd, self.uartFrameHeaderLen, len(cmd) - self.uartFrameHeaderLen - 1)
        cmd_hex_str = self.list_to_hex_string_new(cmd)
        print(cmd_hex_str)
        
        # To-do 同步判断是否返回了正确的指令
        self.uart_send_sync(cmd_hex_str, callback=callback)

        
    def set_uart_bauderate(self, baudrate):
        def callback(result, expect_result):
            nonlocal baudrate
            print(f'set_uart_bauderate: [{result}]' )
            # 开启串口数据接受定时器
            self.timer.start(self.timer_receive_period)

            if result == expect_result:
                self.port_switch_baudrate(baudrate)

            

        if not self.ser.isOpen():
            logger.LOGE('串口未打开')
            return

        baudrate_dict = {"115200":0x03, "1000000": 0x05, "1500000": 0x06, "3000000": 0x07}
        cmd = [0x58, 0x46, 0x0e, 0x00, 0x04, 0x53, 0xf0, 0x00, self.uart_frame_command_type_dict.get('设置CSK通讯串口波特率'), 0, 0 ]
        if baudrate in baudrate_dict.keys():
            cmd[-2] = baudrate_dict.get(baudrate)
        else:
            print("协议串口使用默认波特率[115200]")
            cmd[-2] = baudrate_dict.get("115200")

        cmd[2], cmd[3] = self.int_to_list(len(cmd))
        cmd[5] = self.get_frame_lrc(cmd, 0, self.uartFrameHeaderLen -1 )
        cmd[-1] = self.get_frame_lrc(cmd, self.uartFrameHeaderLen, len(cmd) - self.uartFrameHeaderLen - 1)
        cmd_hex_str = self.list_to_hex_string_new(cmd)
        print(cmd_hex_str)
        
        # To-do 同步判断是否返回了正确的指令
        self.uart_send_sync(cmd_hex_str, callback=callback)
        
        

    def set_work_mode(self, mode_string):
        def callback(result, expect_result):
            self.timer.start(self.timer_receive_period)
            # nonlocal baudrate
            print(f'set_work_mode: [{result}]/[{expect_result}]' )

        if not self.ser.isOpen():
            logger.LOGE('串口未打开')
            return
        
        mode_dict = {"单行扫描模式":0x00, "多行扫描模式": 0x01, "产测模式": 0x03, "调试模式": 0x04, \
                    "老化模式": 0x05, "标定模式": 0x06, "离线单行扫描模式": 0x07, \
                    "最大图模式": 0x09, "重启": 0x0a, "离线uart传图模式": 0x0b, "在线uart传图模式": 0x0c, \
        }

        cmd = [0x58, 0x46, 0x0e, 0x00, 0x04, 0x53, 0xf0, 0x00, self.uart_frame_command_type_dict.get("设置工作模式"), 0, 0 ]
        if mode_string in mode_dict.keys():
            cmd[-2] = mode_dict.get(mode_string)
        else:
            print("协议串口使用默认模式[离线单行扫描模式]")
            cmd[-2] = mode_dict.get("离线单行扫描模式")

        cmd[2], cmd[3] = self.int_to_list(len(cmd))
        cmd[5] = self.get_frame_lrc(cmd, 0, self.uartFrameHeaderLen -1 )
        cmd[-1] = self.get_frame_lrc(cmd, self.uartFrameHeaderLen, len(cmd) - self.uartFrameHeaderLen - 1)
        cmd_hex_str = self.list_to_hex_string_new(cmd)
        print(cmd_hex_str)
        
        # To-do 同步判断是否返回了正确的指令
        self.uart_send_sync(cmd_hex_str, callback=callback)

    def get_uart_software_version(self, mode_string):
        def callback(result, expect_result):
            self.timer.start(self.timer_receive_period)
            # nonlocal baudrate
            print(f'get_uart_software_version: [{result}]/[{expect_result}]' )

        if not self.ser.isOpen():
            logger.LOGE('串口未打开')
            return
        

        res_software_version_dict = {"固件和拼接算法版本": 0x00, "固件版本":0x01, "拼接算法版本": 0x02, "CHIPID": 0x03, "切行算法版本": 0x04, \
                    "OCR算法版本": 0x05, "TTS引擎版本": 0x06, "TTS发音人ID": 0x07, "所有信息": 0x10
        }

        cmd = [0x58, 0x46, 0x0e, 0x00, 0x04, 0x53, 0xf0, 0x00, self.uart_frame_command_type_dict.get("查询软件版本"), 0, 0 ]
        if mode_string in res_software_version_dict.keys():
            cmd[-2] = res_software_version_dict.get(mode_string)
        else:
            print("协议串口使用默认模式[固件和拼接算法版本]")
            cmd[-2] = res_software_version_dict.get("固件和拼接算法版本")

        cmd[2], cmd[3] = self.int_to_list(len(cmd))
        cmd[5] = self.get_frame_lrc(cmd, 0, self.uartFrameHeaderLen -1 )
        cmd[-1] = self.get_frame_lrc(cmd, self.uartFrameHeaderLen, len(cmd) - self.uartFrameHeaderLen - 1)
        cmd_hex_str = self.list_to_hex_string_new(cmd)
        print(cmd_hex_str)
        
        # To-do 同步判断是否返回了正确的指令
        self.uart_send_sync(cmd_hex_str, callback=callback)


    def set_calibration_mode(self):
        self.send_text_text_browser.setText("""58 46 0b 00 04 53 f0 00 50 06 BA""")
        self.data_send()

    def set_ocr_mode(self):
        self.send_text_text_browser.setText("""58 46 0b 00 04 53 f0 00 50 07 b9""")
        self.data_send()

    def set_calibration_position_up(self):
        self.set_calibration_relative_position(0, -8)
        # if (self.y_pos + 2) <= self.y_pos_range[1]:
        #     self.y_pos += 2
        #     self.set_calibration_position(self.x_pos, self.y_pos)

    def set_calibration_position_down(self):
        self.set_calibration_relative_position(0, 8)
        # if (self.y_pos - 2) >= self.y_pos_range[0]:
        #     self.y_pos -= 2
        #     self.set_calibration_position(self.x_pos, self.y_pos)

    def set_calibration_position_left(self):
        self.set_calibration_relative_position(-16, 0)
        # if (self.x_pos - 16) >= self.x_pos_range[0]:
        #     self.x_pos -= 16
        #     self.set_calibration_position(self.x_pos, self.y_pos)

    def set_calibration_position_right(self):
        self.set_calibration_relative_position(16, 0)

        # if (self.x_pos + 16) <= self.x_pos_range[1]:
        #     self.x_pos += 16
        #     self.set_calibration_position(self.x_pos, self.y_pos)

    def int_to_list(self, data, bytes = 2, byteorder = 'little', signed = True):
        hex_str = data.to_bytes(bytes, byteorder=byteorder, signed=True).hex()
        return self.hex_string_to_list(hex_str)

    def set_calibration_relative_position(self, x_rela_pos, y_rela_pos):

        x_rela_low, x_rela_high = self.int_to_list(x_rela_pos) 
        y_rela_low, y_rela_high = self.int_to_list(y_rela_pos) 

        cmd = [0x58, 0x46, 0x0e, 0x00, 0x04, 0x53, 0xf0, 0x00, 0x55, x_rela_low,  x_rela_high, y_rela_low, y_rela_high, 0 ]
        cmd[5] = self.get_frame_lrc(cmd, 0, 5)
        cmd[-1] = self.get_frame_lrc(cmd, 6, 7)
        cmd_hex_str = self.list_to_hex_string_new(cmd)
        print(cmd_hex_str)
        self.send_text_text_browser.setText(cmd_hex_str)
        self.data_send()


    def set_calibration_position(self):
        def get_calibration_position():
            x_pos = self.calibrationformLayout_x_pos_line_edit.text()
            y_pos = self.calibrationformLayout_y_pos_line_edit.text()
            return int(x_pos), int(y_pos)

        x_pos, y_pos = get_calibration_position()

        x_end_pos = x_pos + 128
        y_end_pos = y_pos + 180
        cmd = [0x58, 0x46, 0x12, 0x00, 0x04, 0x53, 0xf0, 0x00, 0x56, x_pos % 256,  int( x_pos / 256 ), x_end_pos % 256 , int( x_end_pos / 256 ), y_pos % 256, int( y_pos / 256 ), y_end_pos % 256, int( y_end_pos / 256 ), 0 ]
        cmd[5] = self.get_frame_lrc(cmd, 0, 5)
        cmd[-1] = self.get_frame_lrc(cmd, 6, 11)
        cmd_hex_str = self.list_to_hex_string_new(cmd)
        print(cmd_hex_str)
        self.send_text_text_browser.setText(cmd_hex_str)
        self.data_send()
    

    def play_tts(self):
        def play_thread(self):
            '''
            tr = MyThread()
            #tr = MyMusic()
            tr.init(self.targetWavDir + '/' + self.targetWavFile)
            #tr.init("1.pcm")
            tr.start()
            tr.join()
            '''
            import os
            line = self.uartCommand
            
            notifyText = ""

            os.system('notify-send %s >/dev/null 2>&1' %
                    ("received: " + notifyText))

            # os.system('ffplay -nodisp -autoexit %s >/dev/null 2>&1'%("./wav_light/" + self.targetWavFile) )
            self.isPlayEnd = 1
            print("thread is playing end")
        # 获取播放锁
        self.playLock.acquire()
        t = threading.Thread(target=play_thread)
        self.isPlayEnd = 0
        t.start()
        t.join()
        # 释放播放锁
        self.playLock.release()

    def get_platform(self):
        import sys
        return sys.platform

    # 串口检测
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        com_dict = {}
        port_list = list(serial.tools.list_ports.comports())
        port_list = port_list[::-1]
        #port_list = ["/dev/ttyUSB0"]
        for port in port_list:
            if self.get_platform() == 'darwin':
                if '/dev/cu.usbserial' not in port[0]:
                    continue
            com_dict["%s" % port[0]] = "%s" % port[1]
            # self.uart_port_combo_box.addItem(port[0])
        if len(com_dict) == 0:
            self.state_label.setText(" 无串口")

        self.com_dict = com_dict

        self.uart_port_combo_box.clear()
        for item in self.com_dict.keys():
             self.uart_port_combo_box.addItem(item)



    # 串口信息
    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = self.uart_port_combo_box.currentText()
        if imf_s != "":
            self.state_label.setText(
                self.com_dict[imf_s])

    # 打开串口
    def port_open(self):
        self.ser.port = self.uart_port_combo_box.currentText()
        self.ser.baudrate = int(self.uart_baudrate_combo_box.currentText())
        self.ser.bytesize = int(self.uart_data_bit_combo_box.currentText())
        self.ser.stopbits = int(self.uart_stop_bit_combo_box.currentText())
        self.ser.parity = self.uart_parity_bit_combo_box.currentText()

        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None

        # 打开串口接收定时器，周期为2ms
        self.timer.start(self.timer_receive_period)

        if self.ser.isOpen():
            self.open_button.setEnabled(False)
            self.close_button.setEnabled(True)
            self.formGroupBox1.setTitle("串口状态（已开启）")

    # 关闭串口
    def port_close(self):
        self.timer.stop()
        self.timer_send.stop()
        try:
            self.ser.close()
        except:
            pass
        self.open_button.setEnabled(True)
        self.close_button.setEnabled(False)
        self.timer_lineEdit.setEnabled(True)

        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.receive_data_num_line_edit.setText(str(self.data_num_received))
        self.data_num_sended = 0
        self.send_data_num_line_edit.setText(str(self.data_num_sended))
        self.formGroupBox1.setTitle("串口状态（已关闭）")

    def port_switch_baudrate(self, baudrate):
        def get_baudrate_index(baudrate):
            baudrate_list = ["115200", "1000000", "1500000", "3000000"]
            if baudrate in baudrate_list:
                print( baudrate_list.index(baudrate) )
                return  baudrate_list.index(baudrate) 
            else:
                #默认返回115200
                return 0

        if self.ser.isOpen():
            self.port_close()
        
        index = self.uart_baudrate_combo_box.findText(baudrate)
        # index = get_baudrate_index(baudrate=baudrate)
        self.uart_baudrate_combo_box.setCurrentIndex(index)
        self.port_open()

    # 发送数据
    def data_send(self):
        if self.ser.isOpen():
            input_s = self.send_text_text_browser.toPlainText()
            if input_s != "":
                # 非空字符串
                if self.hex_send.isChecked():
                    # hex发送
                    input_s = input_s.strip()
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(
                                self, 'wrong data', '请输入十六进制数据，以空格分开!')
                            return None
                        input_s = input_s[2:].strip()
                        send_list.append(num)
                    input_s = bytes(send_list)
                else:
                    # ascii发送
                    input_s = (input_s + '\r\n').encode('utf-8')

                num = self.ser.write(input_s)
                self.data_num_sended += num
                self.send_data_num_line_edit.setText(str(self.data_num_sended))
        else:
            pass

    # 发送数据
    def single_send(self, text):
        if self.ser.isOpen():
            input_s = text
            if input_s != "":
                # 非空字符串
                if self.hex_send.isChecked():
                    # hex发送
                    input_s = input_s.strip()
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(
                                self, 'wrong data', '请输入十六进制数据，以空格分开!')
                            return None
                        input_s = input_s[2:].strip()
                        send_list.append(num)
                    print(send_list)
                    input_s = bytes(send_list)
                else:
                    # ascii发送
                    input_s = (input_s + '\r\n').encode('utf-8')

                num = self.ser.write(input_s)
                # self.data_num_sended += num
                # self.lineEdit_2.setText(str(self.data_num_sended))
        else:
            pass
   

   

    def readUartFromTxt(self, fileName='cmd.txt'):
        data = None
        result = dict()
        try:
            if os.path.isfile(fileName):
                with open(fileName) as f:
                    data = f.readlines()
                data = [i.strip().replace('\n', '')
                        for i in data if isinstance(i, str)]
        except Exception as err:
            # print(f'[readUartFromTxt]{err}') 
            print("")
        finally:
            if data and isinstance(data, list):
                for i in data:
                    result[i] = {'uart_send': i}
            return result

   
    def hex_string_to_list(self, x):
        return list(bytearray.fromhex(x))
    
    def list_to_hex_string(self, x):
        def ToBytes(data):
            if type(data) == type('12'):
                if len(data)%2 != 0:
                    data += '0'
                    print("add '0' at end,amended: ",end="")
                    print(data)
                return bytes().fromhex(data)
            elif type(data) == type([1,]):
                return bytes(data)
            else:
                print("only 'str' or 'list' is valid!")
                return None
        def ToHexStr(data):
            if type(data) == type([1,]):
                bytes_data = ToBytes(data)
                return bytes_data.hex()
            elif type(data) == type(b'\x00'):
                return data.hex()    
            else:
                print("only 'list' or 'bytes' is valid!")
                return None
        return ToHexStr(x)
        # import binascii
        # y = str(bytearray(x))
        # hex_string = binascii.b2a_hex(y)
        # return hex_string
    def list_to_hex_string_new(self, x):
        data  = ['{:02x}'.format(i) for i in x ]
        data = ' '.join(data)
        return data

    def get_hex_from_list(self, data):
         lens = len(data)
         out_data = 0
         for i in range(lens):
            out_data += data[i] << (8 * i)
         return out_data

    def get_frame_lrc(self, frame_list, pos, len):
        lrc_calc_result = 0
        for i in range(pos, pos + len):
            lrc_calc_result += frame_list[i]
        lrc_calc_result = 256 - (lrc_calc_result % 256)
        return lrc_calc_result

    def get_frame_lrc_check_result(self, frame_list, pos, len):
        # lrc = self.get_frame_lrc(frame_list)
        lrc_calc_result = 0
        for i in range(pos, pos + len):
            lrc_calc_result += frame_list[i] 

        if (lrc_calc_result % 256) == 0:
            return True
        else:
            return False
        
    
    def get_frame_len(self, frame_list):
        pos = 2
        len = 2
        return self.get_hex_from_list(frame_list[pos:pos+len])
        
    def get_frame_res_type(self, frame_list):
        res_type_dict = {0x01: {'name': '命令帧反馈', 'value': 0x01 }, \
                         0x50: {'name':'工作状态反馈', 'value': 0x50 } , \
                         0x51: {'name':'标定状态反馈', 'value': 0x51 }, \
                         0x04: {'name':'软件版本反馈', 'value': 0x04  }, \
                         0x52: {'name':'合成加密码反馈', 'value': 0x52  }, \
                         0x53: {'name':'通用数据上传反馈', 'value': 0x53  }
        }
        res_type = frame_list[self.uartFrameHeaderLen + 2 ]

        return res_type_dict.get(res_type)

    def get_frame_res_command_status(self, frame_list):
        res_command_dict = {0x00: {'name': '系统初始化成功', 'value': 0x00 }, \
                         0x10: {'name':'收到正确的命令', 'value': 0x10 } , \
                         0x11: {'name':'数据帧格式错误', 'value': 0x11 }, \
                         0x12: {'name':'数据帧参数错误', 'value': 0x12  }, \
                         0x13: {'name':'未在校准模式下的按压状态', 'value': 0x13  }
     
        }
        res_command_status = frame_list[self.uartFrameHeaderLen + 3 ]

        return res_command_dict.get(res_command_status)

    def get_frame_res_work_status(self, frame_list):
        res_work_dict = {0x00: {'name': '待机状态', 'value': 0x00 }, \
                         0x01: {'name':'扫描状态', 'value': 0x01 } , \
                         0x02: {'name':'等待状态', 'value': 0x02 }, \
                         0x03: {'name':'拒绝状态', 'value': 0x03  }, \
                         0x04: {'name':'标定状态', 'value': 0x04 } , \
                         0x05: {'name':'系统初始化完成', 'value': 0x05 }, \
                         0x06: {'name':'摄像头初始化异常', 'value': 0x06  }, \
                         0x07: {'name':'摄像头解析异常', 'value': 0x07 } , \
                         0x08: {'name':'算法初始化异常', 'value': 0x08 }, \
                         0x09: {'name':'OCR文本输出中', 'value': 0x09  }, \
                         0x0A: {'name':'OCR文本输出结束', 'value': 0x0A  }, \
                         0x0B: {'name':'TTS合成输出中', 'value': 0x0B } , \
                         0x0C: {'name':'TTS合成输出结束', 'value': 0x0C }
     
        }
        res_work_status = frame_list[self.uartFrameHeaderLen + 3 ]

        return res_work_dict.get(res_work_status)
    
    def get_frame_res_calibration_status(self, frame_list):
        res_calibration_dict = {0x00: {'name': '校准成功-ADJUST_OK', 'value': 0x00, 'x': 0x00, 'y': 0x00 }, \
                         0x02: {'name':'全黑-ERROR_FULL_BLACK', 'value': 0x02, 'x': 0x00, 'y': 0x00 } , \
                         0x04: {'name':'中心白-ERROR_CENTER_WHITE', 'value': 0x04, 'x': 0x00, 'y': 0x00 }, \
                         0x08: {'name':'灯光过亮-ERROR_UPON_LIGHT_OFF', 'value': 0x08, 'x': 0x00, 'y': 0x00  }, \
                         0x10: {'name':'灯光过暗-ERROR_DOWN_LIGHT_OFF', 'value': 0x10, 'x': 0x00, 'y': 0x00 } 
     
        }
        res_calibration_status = frame_list[self.uartFrameHeaderLen + 3 ]
        res_calibration_dict.get(res_calibration_status)['x'] = frame_list[self.uartFrameHeaderLen + 4 ]
        res_calibration_dict.get(res_calibration_status)['y'] = frame_list[self.uartFrameHeaderLen + 5 ]

        return res_calibration_dict.get(res_calibration_status)

    def get_frame_res_software_version(self, frame_list):
        
        res_software_version_dict = {   0x01: {'name':'固件版本', 'value': 0x01 , 'vesion': ''} , \
                                        0x02: {'name':'拼接算法版本', 'value': 0x02, 'vesion':'' }, \
                                        0x03: {'name':'CHIPID', 'value': 0x03, 'vesion':''  }, \
                                        0x04: {'name':'切行算法版本', 'value': 0x04, 'vesion':'' } , \
                                        0x05: {'name':'OCR算法版本', 'value': 0x05, 'vesion':'' }, \
                                        0x06: {'name':'TTS引擎版本', 'value': 0x06, 'vesion':''  }, \
                                        0x07: {'name':'TTS发音人ID', 'value': 0x07, 'vesion':'' } , \
                                        0x10: {'name':'所有信息', 'value': 0x10, 'vesion':'' }                 
     
        }
        res_software_type = frame_list[self.uartFrameHeaderLen + 3 ]

        if res_software_type in [0x01 , 0x02, 0x04, 0x05, 0x06 ]:
            res_software_version_dict.get(res_software_type)['version'] = hex(frame_list[self.uartFrameHeaderLen + 4 ] + frame_list[self.uartFrameHeaderLen + 5 ] * 2**8 )
        elif res_software_type == 0x03:
            chipid = self.get_hex_from_list(frame_list[self.uartFrameHeaderLen + 4: self.uartFrameHeaderLen + 4 + 8 ])
            res_software_version_dict.get(res_software_type)['version'] = hex(chipid)
        elif res_software_type == 0x07:
            tts_id = self.get_hex_from_list(frame_list[self.uartFrameHeaderLen + 4: self.uartFrameHeaderLen + 4 + 4 ])
            res_software_version_dict.get(res_software_type)['version'] = hex(tts_id)

        return res_software_version_dict.get(res_software_type)

    def get_frame_res_encode_data(self, frame_list):
        encode_data_len_bytes = 4
        encode_data_len = self.get_hex_from_list( frame_list[self.uartFrameHeaderLen + 3:  self.uartFrameHeaderLen + 3 + encode_data_len_bytes] )
        encode_data = frame_list[self.uartFrameHeaderLen + 3 + encode_data_len_bytes: self.uartFrameHeaderLen + 3 + encode_data_len_bytes + encode_data_len]

        return encode_data
    
    

    def get_frame_res_common_data(self, frame_list):
        def get_frame_data_member(frame_list, name, pos, len):
            if name in ['reserved', 'data']:
                return frame_list[pos:pos+len]
            else:
                return self.get_hex_from_list(frame_list[pos:pos+len])
        
        frame_command_bytes = 3
        common_data_type_bytes = 1
        common_data_id_bytes = 4
        common_data_x_start_bytes = 2
        common_data_x_end_bytes = 2
        common_data_y_start_bytes = 2
        common_data_y_end_bytes = 2
        common_data_len_bytes = 4
        common_data_reserved_bytes = 16



        res_common_data_dict = {       0x00: {'name':'校准图片jpg格式', 'value': 0x00 } , \
                                        0x01: {'name':'OCR文本', 'value': 0x01 }, \
                                        0x02: {'name':'离线切行图片raw', 'value': 0x02  }, \
                                        0x03: {'name':'离线拼接图片', 'value': 0x03 } , \
                                        0x04: {'name':'在线裁剪图片', 'value': 0x04 }
        }
        frame_res_common_data = {'type': { 'size': 1, 'pos': 0, 'data': 0 , 'data_info': res_common_data_dict}, \
                                 'id':{ 'size': 4, 'pos': 0, 'data': 0 }, \
                                  'x_start':{ 'size': 2, 'pos': 0, 'data': 0 }, \
                                  'x_end':{ 'size': 2, 'pos': 0, 'data': 0 }, \
                                  'y_start':{ 'size': 2, 'pos': 0, 'data': 0 }, \
                                  'y_end':{ 'size': 2, 'pos': 0, 'data': 0 }, \
                                  'data_len':{ 'size': 4, 'pos': 0, 'data': 0 }, \
                                  'reserved':{ 'size': 16, 'pos': 0, 'data': [] }, \
                                  'data':{ 'size': 0, 'pos': 0, 'data': [] }
        }
                            
        

        pos = self.uartFrameHeaderLen + frame_command_bytes
        for item in frame_res_common_data.keys():
            frame_res_common_data.get(item)['pos'] = pos
            frame_res_common_data.get(item)['data'] = get_frame_data_member(frame_list, item, \
                                                        frame_res_common_data.get(item)['pos'], \
                                                        frame_res_common_data.get(item)['size'])
            
            if item == 'data_len':
                frame_res_common_data.get('data')['size'] = frame_res_common_data.get(item)['data']

            pos += frame_res_common_data.get(item)['size']
        
        # print('frame_res_common_data:', frame_res_common_data)

        print('type:[{}],id:[{}],x_start:[{}],x_end:[{}],y_start:[{}],y_end:[{}],data_len:[{}],reserved:[{}]'.format(
            frame_res_common_data.get('type').get('data_info').get(frame_res_common_data.get('type').get('data')).get('name'),
            frame_res_common_data.get('id').get('data'),
            frame_res_common_data.get('x_start').get('data'),
            frame_res_common_data.get('x_end').get('data'),
            frame_res_common_data.get('y_start').get('data'),
            frame_res_common_data.get('y_end').get('data'),
            frame_res_common_data.get('data_len').get('data'),
            frame_res_common_data.get('reserved').get('data')
         ))

      
        return frame_res_common_data

    def show_image_result(self, *args, **kwargs):
        def iterm2_show_image(*args, **kwargs):
            # 显示拼接图
            util_name = 'imgcat'
            ret = utils.run_shell(f'command -v {util_name}')
            
            if ret.returncode == 0 and os.path.isfile(kwargs.get('image_file')):
                os.system('{} {}'.format( util_name, kwargs.get('image_file') ))
        
        # 显示图片信息：x,y 坐标
        if 'res_common_data' in kwargs.keys():
            res_common_data = kwargs.get('res_common_data')
            label_text = 'x:({},{}), y:({},{})'.format(res_common_data.get('x_start').get('data'), 
                                                res_common_data.get('x_end').get('data'),
                                                res_common_data.get('y_start').get('data'),
                                                res_common_data.get('y_end').get('data')
            )
            self.uart_image_position_result_label.setText(label_text)

        if 'image_file' in kwargs.keys():
            # MacOS 的iterm2才支持imgcat 终端显示图片
            if sys.platform == 'darwin':
                iterm2_show_image(**kwargs)

            pix = QPixmap(kwargs.get('image_file'))
            # lb1.setStyleSheet("border: 2px solid red")
            self.lb1.setPixmap(pix)

            return

        if 'image_data' in kwargs.keys():
            pix = QPixmap()
            pix.loadFromData(kwargs.get('image_data'))
            self.lb1.setPixmap(pix)

    def print_calibration_image(self, res_common_data):

        id = res_common_data.get('id').get('data')
        hex_list = res_common_data.get('data').get('data')
        image_file = f'../out/jpg/{id}_128_180.jpeg'

        # print('print_calibration_image', hex_list)

        if id == 1:
            self.image_counts = 0

        self.image_counts += 1
        image_counts = self.image_counts

        utils.dirs('../out/jpg')
        utils.write_bin_list_to_file(hex_list, image_file)

        logger.LOGB(f"图像结果: id[{id}], 已成功接受[{image_counts}]张")
        self.show_image_result(image_file= image_file, res_common_data = res_common_data)

    def print_offline_cut_line_image(self, res_common_data):
        id = res_common_data.get('id').get('data')
        width = res_common_data.get('x_end').get('data') - res_common_data.get('x_start').get('data')
        height = res_common_data.get('y_end').get('data') - res_common_data.get('y_start').get('data')

        hex_list = res_common_data.get('data').get('data')
        binary_images = utils.bin_list_to_bmp_bytes(hex_list, width , height)
        image_file = f'../out/jpg/{id}_{width}_{height}.jpeg'
        utils.dirs('../out/jpg')
        utils.write_bin_list_to_file(binary_images, image_file)

        self.show_image_result(image_data = binary_images, res_common_data = res_common_data)
        
    def scroll_text_browser_to_the_end(self, text_browser):
        # 获取到text光标
        textCursor = text_browser.textCursor()
        # 滚动到底部
        textCursor.movePosition(textCursor.End)
        # 设置光标到text中去
        text_browser.setTextCursor(textCursor)

    def evs_receive(self):
        print('232')
        kwargs = self.evs_kwargs
        kwargs['header_name'] = "audio_player.audio_out"
        evs_linux.client.get_ws_result(**kwargs)
        print('123')


    def print_ocr_text(self, res_common_data):
        import binascii, functools

        hex_list = res_common_data.get('data').get('data') 
        hex_str = self.list_to_hex_string(hex_list)
        hex_str = hex_str.replace(' ','')
        hex = hex_str.encode('utf-8')
        str_bin = binascii.unhexlify(hex)
        str = str_bin.decode('utf-8')

        logger.LOGI('OCR文本：', str)

        self.uart_state_text_browser.insertPlainText(f"OCR文本：[{str}]" + '\n')

        self.scroll_text_browser_to_the_end(self.uart_state_text_browser)
            
        kwargs = {}

        if self.uart_state_ocr_tts_play_check_box.checkState():
            # kwargs['condition'] = evs_linux.client.task_list
            kwargs['header_name'] = "audio_player.audio_out"
            # kwargs['timer'] = self.evs_timer
            self.evs_kwargs = kwargs
            # timer_callback = functools.partial(self.evs_receive, kwargs)
            # timer_callback = functools.partial(self.evs_receive, initParams=kwargs)
            # self.evs_timer.stop()
            
            

            result = evs_linux.get_tts(text = str, timer = self.evs_timer)
            # print(result)
            # self.evs_timer.stop()

        if self.uart_state_ocr_translate_show_check_box.checkState():
            print('\nget_traslate_text')
            # result = evs_linux.get_traslate_text(text = str, timer = self.evs_timer)
            # translate_text = result.get('translation')
            # print("\nget_traslate_text", result)

            # self.uart_state_text_browser.insertPlainText(f"译文：[{translate_text}]" + '\n')
            # self.scroll_text_browser_to_the_end(self.uart_state_text_browser)

        if self.uart_state_ocr_dict_show_check_box.checkState():
            # evs_linux.traslate(str)   
            print("uart_state_ocr_dict_show_check_box")


    def print_frame_info(self, frame_list):
        res_type = self.get_frame_res_type(frame_list)
        res_type_name = res_type.get('name')
        res_type_value = res_type.get('value')

        print('print_frame_info', res_type_name)

        if res_type_value == 0x01:
            res_status = self.get_frame_res_command_status(frame_list)
            ret = res_status.get('name')
            print(ret)
            return ret

        elif res_type_value == 0x50:
            res_status = self.get_frame_res_work_status(frame_list)
            ret = res_status.get('name')
            print(ret)
            return ret

        elif res_type_value == 0x51:
            res_status = self.get_frame_res_calibration_status(frame_list)
            ret = res_status.get('name')
            print(ret)
            return ret

        elif res_type_value == 0x04:
            res_status = self.get_frame_res_software_version(frame_list)   
            ret = res_status.get('name')
            print(ret)
            print(res_status)

            self.uart_state_text_browser.insertPlainText("{}: [{}]".format(res_status.get('name'), res_status.get('version')) + '\n')
            # 获取到text光标
            textCursor = self.uart_state_text_browser.textCursor()
            # 滚动到底部
            textCursor.movePosition(textCursor.End)
            # 设置光标到text中去
            self.uart_state_text_browser.setTextCursor(textCursor)

            return ret
        elif res_type_value == 0x52:
            res_encode_data = self.get_frame_res_encode_data(frame_list) 
            print(res_encode_data) 
            return "加密结果"

        elif res_type_value == 0x53:
            res_common_data = self.get_frame_res_common_data(frame_list) 

            # print(res_common_data.get('type').get('data_info').get(res_common_data['type']['data'] ) )
            
            # 校准图片
            if res_common_data.get('type').get('data') == 0x00:
                print('校准图片')
                self.print_calibration_image(res_common_data)
            # OCR文本
            elif res_common_data.get('type').get('data')== 0x01:
                print('OCR文本')
                self.print_ocr_text(res_common_data)
                
            # 离线切行图片raw
            elif res_common_data.get('type').get('data')== 0x02:
                print('离线切行图片raw')
                self.print_offline_cut_line_image(res_common_data)
            # 离线拼接图片 raw
            elif res_common_data.get('type').get('data')== 0x03:
                print('离线拼接图片 raw')
            # 在线裁剪图片 raw
            elif res_common_data.get('type').get('data')== 0x04:
                print('在线裁剪图片 raw')

            return res_common_data.get('type').get('data_info').get('name')
                
    # 解析数据 Castor liangyijia
    def data_hexStr_parse(self, dataInfo):
        import re

        uartFrameHeaderTag = self.uartFrameHeaderTag

        dataInfo = dataInfo.strip().replace(' ', '')
        dataInfo = self.uartRecvHexStr + dataInfo

        # print('dataInfo:', dataInfo)

        search_pos = 0

        result = None

        # 1.find Uart Header firstly
        while re.search(uartFrameHeaderTag, dataInfo[search_pos:]):
            
            (startPos, endPos) = re.search(uartFrameHeaderTag, dataInfo[search_pos:]).span()


            effectiveLen = int ( (len(dataInfo[startPos:])  ) / 2 )

            hex_list = self.hex_string_to_list(dataInfo[startPos: (startPos + 2 * effectiveLen )])


            # 帧长度最小值检查，不满足帧头长度直接缓冲
            if effectiveLen < self.uartFrameHeaderLen:
                self.uartRecvHexStr = dataInfo[startPos: (startPos + 2 * effectiveLen )]
                self.uartRecvList = self.hex_string_to_list(self.uartRecvHexStr)
                return 

            # 帧头检查
            if not self.get_frame_lrc_check_result(hex_list, 0, self.uartFrameHeaderLen):
                search_pos += endPos 
                logger.LOGE('帧头校验失败')
                logger.LOGE( (startPos, endPos)  )

                print(dataInfo[search_pos:])

                continue
            else:
                logger.LOGI( (startPos, endPos)  )

            search_pos += startPos + 2 * self.uartFrameHeaderLen

            # print('hex_list:', hex_list)

            # 获取帧长度
            uartFrameLenByte = self.get_frame_len(hex_list)
            logger.LOGI(f'effectiveLen:[{effectiveLen}]uartFrameLenByte:[{uartFrameLenByte}]')

            # 帧长度检查
            # if uartFrameLenByte > 10000:
            #     logger.LOGE('非法的帧')
            #     self.uartRecvList = list()
            #     self.uartRecvHexStr = ''
            #     return 

            self.uartFrameLenByte = uartFrameLenByte

            
            # 1.luck mode
            if effectiveLen == self.uartFrameLenByte:
                self.uartRecvList = list()
                self.uartRecvHexStr = ''

                # 帧数据检查
                if not self.get_frame_lrc_check_result(hex_list, self.uartFrameHeaderLen, self.uartFrameLenByte - self.uartFrameHeaderLen):
                    logger.LOGE('帧数据校验失败')
                    return
                

                # print('完整帧:', dataInfo[startPos:])
                print('完整帧')
                frame_list = self.hex_string_to_list(dataInfo[startPos: (startPos + 2 * effectiveLen)])
                result = self.print_frame_info(frame_list)

                return result
            
            # 2.pack mode TO-DO: pack Uart Frame
            elif effectiveLen < self.uartFrameLenByte:
                self.uartRecvList = list()
                
                self.uartRecvHexStr = dataInfo[startPos: (startPos + 2 * effectiveLen )]
                self.uartRecvList = self.hex_string_to_list(self.uartRecvHexStr)
                

            # 3.sticky mode TO-DO: unstick Uart Frame
            elif effectiveLen > self.uartFrameLenByte:
              
                # 帧数据检查
                if not self.get_frame_lrc_check_result(hex_list, self.uartFrameHeaderLen, self.uartFrameLenByte - self.uartFrameHeaderLen):
                    logger.LOGE('帧数据校验失败')
                    self.uartRecvList = list()
                    self.uartRecvHexStr = ''
                    return

                frame_list = self.hex_string_to_list(dataInfo[startPos: (startPos + 2 * effectiveLen)])
                result = self.print_frame_info(frame_list)
                
                self.uartRecvList = list()
                uart_len = effectiveLen - self.uartFrameLenByte
                self.uartRecvHexStr = dataInfo[ (2 * self.uartFrameLenByte) : (2* self.uartFrameLenByte + 2 * uart_len )]  
                self.uartRecvList = self.hex_string_to_list(self.uartRecvHexStr)

                return result

            return 
            
        # 2.pack Uart Frame

      
        logger.LOGE('该帧找不到header:', self.uartFrameHeaderTag)
        # print(dataInfo)

        return 



    # 接收数据

    def data_receive(self):
        num = 0

        result = None

        try:
            num = self.ser.inWaiting()
        except:
            self.port_close()
            return None
        if num > 0:
            data = self.ser.read(num)
            num = len(data)
            # hex显示
            if self.hex_receive.checkState():

                out_s = ''
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '
                # out_s += '\n'
                self.receive_text_text_browser.insertPlainText(out_s + '\n')

                # print("recv:{}".format(out_s.replace(' ', '')))

                # protocol
                result = self.data_hexStr_parse(out_s.replace(' ', ''))

                logger.LOGI(result)
                
            else:
                # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
                self.receive_text_text_browser.insertPlainText(
                    data.decode('iso-8859-1'))
                print(data.decode('iso-8859-1'))
                testString = data.decode('iso-8859-1')


            # 统计接收字符的数量
            self.data_num_received += num
            self.receive_data_num_line_edit.setText(str(self.data_num_received))

            if self.data_num_received > 1024 * 1024 * 10:
                print('清空发送')
                self.data_num_received = 0
                self.receive_data_num_line_edit.setText(str(self.data_num_received))
                self.receive_data_clear()

            if True:
                # 获取到text光标
                textCursor = self.receive_text_text_browser.textCursor()
                # 滚动到底部
                textCursor.movePosition(textCursor.End)
                # 设置光标到text中去
                self.receive_text_text_browser.setTextCursor(textCursor)
        else:
            pass
        
        

        return result

    # 定时发送数据
    def data_send_timer(self):
        if self.timer_send_cb.isChecked():
            self.timer_send.start(int(self.timer_lineEdit.text()))
            self.timer_lineEdit.setEnabled(False)
        else:
            self.timer_send.stop()
            self.timer_lineEdit.setEnabled(True)

    # 清除显示
    def send_data_clear(self):
        self.send_text_text_browser.setText("")

    def receive_data_clear(self):
        self.receive_text_text_browser.setText("")

    def closeEvent(self, event):
        evs_linux.exit_app()


if __name__ == '__main__':
    print("begin ...")

    app = QtWidgets.QApplication(sys.argv)
    myshow = Pyqt5_Serial()
    myshow.show()
    sys.exit(app.exec_())
