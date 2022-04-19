# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serial_client_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1522, 510)
        self.formGroupBox = QtWidgets.QGroupBox(Form)
        self.formGroupBox.setGeometry(QtCore.QRect(20, 20, 221, 321))
        self.formGroupBox.setObjectName("formGroupBox")
        self.formLayout = QtWidgets.QFormLayout(self.formGroupBox)
        self.formLayout.setContentsMargins(10, 10, 10, 10)
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.uart_detect_label = QtWidgets.QLabel(self.formGroupBox)
        self.uart_detect_label.setObjectName("uart_detect_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.uart_detect_label)
        self.uart_check_box = QtWidgets.QPushButton(self.formGroupBox)
        self.uart_check_box.setAutoRepeatInterval(100)
        self.uart_check_box.setDefault(True)
        self.uart_check_box.setObjectName("uart_check_box")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.uart_check_box)
        self.uart_select_label = QtWidgets.QLabel(self.formGroupBox)
        self.uart_select_label.setObjectName("uart_select_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.uart_select_label)
        self.uart_port_combo_box = QtWidgets.QComboBox(self.formGroupBox)
        self.uart_port_combo_box.setMaximumSize(QtCore.QSize(104, 16777215))
        self.uart_port_combo_box.setObjectName("uart_port_combo_box")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.uart_port_combo_box)
        self.uart_baudrate_label = QtWidgets.QLabel(self.formGroupBox)
        self.uart_baudrate_label.setObjectName("uart_baudrate_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.uart_baudrate_label)
        self.uart_baudrate_combo_box = QtWidgets.QComboBox(self.formGroupBox)
        self.uart_baudrate_combo_box.setMaxVisibleItems(10)
        self.uart_baudrate_combo_box.setObjectName("uart_baudrate_combo_box")
        self.uart_baudrate_combo_box.addItem("")
        self.uart_baudrate_combo_box.addItem("")
        self.uart_baudrate_combo_box.addItem("")
        self.uart_baudrate_combo_box.addItem("")
        self.uart_baudrate_combo_box.addItem("")
        self.uart_baudrate_combo_box.addItem("")
        self.uart_baudrate_combo_box.addItem("")
        self.uart_baudrate_combo_box.addItem("")
        self.uart_baudrate_combo_box.addItem("")
        self.uart_baudrate_combo_box.addItem("")
        self.uart_baudrate_combo_box.addItem("")
        self.uart_baudrate_combo_box.addItem("")
        self.uart_baudrate_combo_box.addItem("")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.uart_baudrate_combo_box)
        self.uart_data_bit_label = QtWidgets.QLabel(self.formGroupBox)
        self.uart_data_bit_label.setObjectName("uart_data_bit_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.uart_data_bit_label)
        self.uart_data_bit_combo_box = QtWidgets.QComboBox(self.formGroupBox)
        self.uart_data_bit_combo_box.setObjectName("uart_data_bit_combo_box")
        self.uart_data_bit_combo_box.addItem("")
        self.uart_data_bit_combo_box.addItem("")
        self.uart_data_bit_combo_box.addItem("")
        self.uart_data_bit_combo_box.addItem("")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.uart_data_bit_combo_box)
        self.uart_parity_bit_label = QtWidgets.QLabel(self.formGroupBox)
        self.uart_parity_bit_label.setObjectName("uart_parity_bit_label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.uart_parity_bit_label)
        self.uart_parity_bit_combo_box = QtWidgets.QComboBox(self.formGroupBox)
        self.uart_parity_bit_combo_box.setObjectName("uart_parity_bit_combo_box")
        self.uart_parity_bit_combo_box.addItem("")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.uart_parity_bit_combo_box)
        self.open_button = QtWidgets.QPushButton(self.formGroupBox)
        self.open_button.setObjectName("open_button")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.open_button)
        self.close_button = QtWidgets.QPushButton(self.formGroupBox)
        self.close_button.setObjectName("close_button")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.close_button)
        self.uart_stop_bit_label = QtWidgets.QLabel(self.formGroupBox)
        self.uart_stop_bit_label.setObjectName("uart_stop_bit_label")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.uart_stop_bit_label)
        self.uart_stop_bit_combo_box = QtWidgets.QComboBox(self.formGroupBox)
        self.uart_stop_bit_combo_box.setObjectName("uart_stop_bit_combo_box")
        self.uart_stop_bit_combo_box.addItem("")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.uart_stop_bit_combo_box)
        self.state_label = QtWidgets.QLabel(self.formGroupBox)
        self.state_label.setText("")
        self.state_label.setTextFormat(QtCore.Qt.AutoText)
        self.state_label.setScaledContents(True)
        self.state_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.state_label.setObjectName("state_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.state_label)
        self.verticalGroupBox = QtWidgets.QGroupBox(Form)
        self.verticalGroupBox.setGeometry(QtCore.QRect(240, 20, 401, 321))
        self.verticalGroupBox.setObjectName("verticalGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.receive_text_text_browser = QtWidgets.QTextBrowser(self.verticalGroupBox)
        self.receive_text_text_browser.setObjectName("receive_text_text_browser")
        self.verticalLayout.addWidget(self.receive_text_text_browser)
        self.verticalGroupBox_2 = QtWidgets.QGroupBox(Form)
        self.verticalGroupBox_2.setGeometry(QtCore.QRect(240, 340, 401, 101))
        self.verticalGroupBox_2.setObjectName("verticalGroupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalGroupBox_2)
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.send_text_text_browser = QtWidgets.QTextEdit(self.verticalGroupBox_2)
        self.send_text_text_browser.setObjectName("send_text_text_browser")
        self.verticalLayout_2.addWidget(self.send_text_text_browser)
        self.send_button = QtWidgets.QPushButton(Form)
        self.send_button.setGeometry(QtCore.QRect(650, 380, 61, 31))
        self.send_button.setObjectName("send_button")
        self.clear_send_text_button = QtWidgets.QPushButton(Form)
        self.clear_send_text_button.setGeometry(QtCore.QRect(650, 410, 61, 31))
        self.clear_send_text_button.setObjectName("clear_send_text_button")
        self.formGroupBox1 = QtWidgets.QGroupBox(Form)
        self.formGroupBox1.setGeometry(QtCore.QRect(20, 340, 221, 101))
        self.formGroupBox1.setObjectName("formGroupBox1")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formGroupBox1)
        self.formLayout_2.setContentsMargins(10, 10, 10, 10)
        self.formLayout_2.setSpacing(10)
        self.formLayout_2.setObjectName("formLayout_2")
        self.receive_size_label = QtWidgets.QLabel(self.formGroupBox1)
        self.receive_size_label.setObjectName("receive_size_label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.receive_size_label)
        self.send_size_label = QtWidgets.QLabel(self.formGroupBox1)
        self.send_size_label.setObjectName("send_size_label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.send_size_label)
        self.receive_data_num_line_edit = QtWidgets.QLineEdit(self.formGroupBox1)
        self.receive_data_num_line_edit.setObjectName("receive_data_num_line_edit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.receive_data_num_line_edit)
        self.send_data_num_line_edit = QtWidgets.QLineEdit(self.formGroupBox1)
        self.send_data_num_line_edit.setObjectName("send_data_num_line_edit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.send_data_num_line_edit)
        self.hex_send = QtWidgets.QCheckBox(Form)
        self.hex_send.setGeometry(QtCore.QRect(650, 360, 71, 16))
        self.hex_send.setObjectName("hex_send")
        self.hex_receive = QtWidgets.QCheckBox(Form)
        self.hex_receive.setGeometry(QtCore.QRect(650, 40, 71, 16))
        self.hex_receive.setObjectName("hex_receive")
        self.clear_receive_text_button = QtWidgets.QPushButton(Form)
        self.clear_receive_text_button.setGeometry(QtCore.QRect(650, 60, 61, 31))
        self.clear_receive_text_button.setObjectName("clear_receive_text_button")
        self.timer_send_cb = QtWidgets.QCheckBox(Form)
        self.timer_send_cb.setGeometry(QtCore.QRect(250, 440, 71, 16))
        self.timer_send_cb.setObjectName("timer_send_cb")
        self.timer_lineEdit = QtWidgets.QLineEdit(Form)
        self.timer_lineEdit.setGeometry(QtCore.QRect(340, 440, 61, 20))
        self.timer_lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.timer_lineEdit.setObjectName("timer_lineEdit")
        self.timer_unit_label = QtWidgets.QLabel(Form)
        self.timer_unit_label.setGeometry(QtCore.QRect(410, 440, 54, 20))
        self.timer_unit_label.setObjectName("timer_unit_label")

        

        self.uartFormGroupBox = QtWidgets.QGroupBox(Form)
        self.uartFormGroupBox.setGeometry(QtCore.QRect(750, 20, 321, 400))
        self.uartFormGroupBox.setObjectName("uartFormGroupBox")

        self.uartFormLayout = QtWidgets.QFormLayout(self.uartFormGroupBox)
        self.uartFormLayout.setContentsMargins(10, 10, 10, 10)
        self.uartFormLayout.setSpacing(10)
        self.uartFormLayout.setObjectName("uartFormLayout")

        # self.uartFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.uart_check_box)

        self.label_calibration = QtWidgets.QLabel(Form)
        # self.label_calibration.setGeometry(QtCore.QRect(800, 40, 128, 180))
        self.label_calibration.setScaledContents(True)
        self.label_calibration.setObjectName("label_calibration")


        self.set_uart_mode_box = QtWidgets.QComboBox(self.uartFormGroupBox)
        self.set_uart_mode_box.setMaxVisibleItems(12)
        self.set_uart_mode_box.setObjectName("set_uart_mode_box")
        for i in range(12):
            self.set_uart_mode_box.addItem("")
       
        self.set_uart_bauderate_box = QtWidgets.QComboBox(self.uartFormGroupBox)
        self.set_uart_bauderate_box.setMaxVisibleItems(10)
        self.set_uart_bauderate_box.setObjectName("set_uart_bauderate_box")
        for i in range(4):
            self.set_uart_bauderate_box.addItem("")

        self.get_uart_software_version_box = QtWidgets.QComboBox(self.uartFormGroupBox)
        self.get_uart_software_version_box.setMaxVisibleItems(10)
        self.get_uart_software_version_box.setObjectName("get_uart_software_version_box")
        for i in range(9):
            self.get_uart_software_version_box.addItem("")
        
       
  
        self.detect_uart_bauderate_button =  QtWidgets.QPushButton(self.uartFormGroupBox)
        self.detect_uart_bauderate_button.setObjectName("detect_uart_bauderate_button")


        self.detect_uart_bauderate_result_label = QtWidgets.QLabel(self.uartFormGroupBox)
        self.detect_uart_bauderate_result_label.setObjectName("detect_uart_bauderate_result_label")

        self.uart_image_position_result_label = QtWidgets.QLabel(self.uartFormGroupBox)
        self.uart_image_position_result_label.setObjectName("uart_image_position_result_label")


        self.uartFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('校准图片:', self.uartFormGroupBox))
        self.uartFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_calibration)

        
        self.uartFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('图片坐标: ', self.uartFormGroupBox))
        self.uartFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.uart_image_position_result_label)
        

        self.uartFormLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('自动检测协议串口波特率', self.uartFormGroupBox))
        self.uartFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.detect_uart_bauderate_button)

        self.uartFormLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('检测结果: ', self.uartFormGroupBox))
        self.uartFormLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.detect_uart_bauderate_result_label)

        self.uartFormLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('设置协议串口波特率:', self.uartFormGroupBox))
        self.uartFormLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.set_uart_bauderate_box)

        self.uartFormLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('模式:', self.uartFormGroupBox))
        self.uartFormLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.set_uart_mode_box)

        self.uartFormLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('查询版本:', self.uartFormGroupBox))
        self.uartFormLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.get_uart_software_version_box)
        

        self.uartStateFormGroupBox = QtWidgets.QGroupBox(Form)
        self.uartStateFormGroupBox.setGeometry(QtCore.QRect(1090, 240, 301, 201))
        self.uartStateFormGroupBox.setObjectName("uartStateFormGroupBox")
        self.uartStateFormLayout = QtWidgets.QVBoxLayout(self.uartStateFormGroupBox)
        self.uartStateFormLayout.setContentsMargins(10, 10, 10, 10)
        self.uartStateFormLayout.setObjectName("uartStateFormLayout")
        self.uart_state_text_browser = QtWidgets.QTextEdit(self.uartStateFormGroupBox)
        self.uart_state_text_browser.setObjectName("uart_state_text_browser")
        self.uartStateFormLayout.addWidget(self.uart_state_text_browser)

        self.uart_state_ocr_tts_play_check_box = QtWidgets.QCheckBox(Form)
        self.uart_state_ocr_tts_play_check_box.setGeometry(QtCore.QRect(1400, 240, 71, 16))
        self.uart_state_ocr_tts_play_check_box.setObjectName("uart_state_ocr_tts_play_check_box")

        self.uart_state_ocr_translate_show_check_box = QtWidgets.QCheckBox(Form)
        self.uart_state_ocr_translate_show_check_box.setGeometry(QtCore.QRect(1400, 260, 71, 16))
        self.uart_state_ocr_translate_show_check_box.setObjectName("uart_state_ocr_translate_show_check_box")

        self.uart_state_ocr_dict_show_check_box = QtWidgets.QCheckBox(Form)
        self.uart_state_ocr_dict_show_check_box.setGeometry(QtCore.QRect(1400, 280, 71, 16))
        self.uart_state_ocr_dict_show_check_box.setObjectName("uart_state_ocr_dict_show_check_box")


        self.set_calibration_up_position = QtWidgets.QPushButton(Form)
        self.set_calibration_up_position.setGeometry(QtCore.QRect(1140, 40, 50, 50))
        self.set_calibration_up_position.setObjectName("set_calibration_up_position")
        self.set_calibration_down_position = QtWidgets.QPushButton(Form)
        self.set_calibration_down_position.setGeometry(QtCore.QRect(1140, 140, 50, 50))
        self.set_calibration_down_position.setObjectName("set_calibration_down_position")
        self.set_calibration_left_position = QtWidgets.QPushButton(Form)
        self.set_calibration_left_position.setGeometry(QtCore.QRect(1090, 90, 50, 50))
        self.set_calibration_left_position.setObjectName("set_calibration_left_position")
        self.set_calibration_right_position = QtWidgets.QPushButton(Form)
        self.set_calibration_right_position.setGeometry(QtCore.QRect(1190, 90, 50, 50))
        self.set_calibration_right_position.setObjectName("set_calibration_right_position")


        self.calibrationformGroupBox = QtWidgets.QGroupBox(Form)
        self.calibrationformGroupBox.setGeometry(QtCore.QRect(1300, 40, 150, 150))
        self.calibrationformGroupBox.setObjectName("calibrationformGroupBox")
        self.calibrationformLayout = QtWidgets.QFormLayout(self.calibrationformGroupBox)
        self.calibrationformLayout.setContentsMargins(10, 10, 10, 10)
        self.calibrationformLayout.setSpacing(10)
        self.calibrationformLayout.setObjectName("calibrationformLayout")

        self.calibrationformLayout_x_pos_line_edit = QtWidgets.QLineEdit(self.calibrationformGroupBox)
        self.calibrationformLayout_x_pos_line_edit.setObjectName("calibrationformLayout_x_pos_line_edit")

        self.calibrationformLayout_y_pos_line_edit = QtWidgets.QLineEdit(self.calibrationformGroupBox)
        self.calibrationformLayout_y_pos_line_edit.setObjectName("calibrationformLayout_y_pos_line_edit")

        self.set_calibration_button = QtWidgets.QPushButton(Form)
        self.set_calibration_button.setObjectName("set_calibration_button")

        self.calibrationformLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('x坐标:', self.calibrationformGroupBox))
        self.calibrationformLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.calibrationformLayout_x_pos_line_edit)
        
        self.calibrationformLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('y坐标:', self.calibrationformGroupBox))
        self.calibrationformLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.calibrationformLayout_y_pos_line_edit)
        
        self.calibrationformLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('串口设置:', self.calibrationformGroupBox))
        self.calibrationformLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.set_calibration_button)

        self.verticalGroupBox.raise_()
        self.verticalGroupBox_2.raise_()
        self.uartStateFormGroupBox.raise_()

        self.formGroupBox.raise_()
        self.send_button.raise_()
        self.clear_send_text_button.raise_()
        self.formGroupBox.raise_()
        self.hex_send.raise_()
        self.hex_receive.raise_()
        self.clear_receive_text_button.raise_()
        self.timer_send_cb.raise_()
        self.timer_lineEdit.raise_()
        self.timer_unit_label.raise_()
        self.label_calibration.raise_()
        self.uart_state_ocr_tts_play_check_box.raise_()
        self.uart_state_ocr_translate_show_check_box.raise_()
        self.uart_state_ocr_dict_show_check_box.raise_()
        self.set_calibration_up_position.raise_()
        self.set_calibration_down_position.raise_()
        self.set_calibration_left_position.raise_()
        self.set_calibration_right_position.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.formGroupBox.setTitle(_translate("Form", "串口设置"))
        self.uart_detect_label.setText(_translate("Form", "串口检测："))
        self.uart_check_box.setText(_translate("Form", "检测串口"))
        self.uart_select_label.setText(_translate("Form", "串口选择："))
        self.uart_baudrate_label.setText(_translate("Form", "波特率："))
        self.uart_baudrate_combo_box.setItemText(0, _translate("Form", "115200"))
        self.uart_baudrate_combo_box.setItemText(1, _translate("Form", "1500000"))
        self.uart_baudrate_combo_box.setItemText(2, _translate("Form", "1000000"))
        self.uart_baudrate_combo_box.setItemText(3, _translate("Form", "3000000"))
        self.uart_baudrate_combo_box.setItemText(4, _translate("Form", "14400"))
        self.uart_baudrate_combo_box.setItemText(5, _translate("Form", "19200"))
        self.uart_baudrate_combo_box.setItemText(6, _translate("Form", "38400"))
        self.uart_baudrate_combo_box.setItemText(7, _translate("Form", "57600"))
        self.uart_baudrate_combo_box.setItemText(8, _translate("Form", "76800"))
        self.uart_baudrate_combo_box.setItemText(9, _translate("Form", "12800"))
        self.uart_baudrate_combo_box.setItemText(10, _translate("Form", "230400"))
        self.uart_baudrate_combo_box.setItemText(11, _translate("Form", "460800"))
        self.uart_baudrate_combo_box.setItemText(12, _translate("Form", "9600"))

        self.uartFormGroupBox.setTitle(_translate("Form", "串口解析"))
        self.uartStateFormGroupBox.setTitle(_translate("Form", "串口解析状态"))

        mode_dict = {"单行扫描模式":0x00, "多行扫描模式": 0x01, "产测模式": 0x03, "调试模式": 0x04, \
                    "老化模式": 0x05, "标定模式": 0x06, "离线单行扫描模式": 0x07, \
                    "最大图模式": 0x09, "重启": 0x0a, "离线uart传图模式": 0x0b, "在线uart传图模式": 0x0c, \
        }
        for index, key in enumerate(mode_dict.keys()):
            self.set_uart_mode_box.setItemText(index, _translate("Form", key))
        
        baudrate_dict = {"115200":0x03, "1000000": 0x05, "1500000": 0x06, "3000000": 0x07}
        for index, key in enumerate(baudrate_dict.keys()):
            self.set_uart_bauderate_box.setItemText(index, _translate("Form", key))

  
        res_software_version_dict = {"固件和拼接算法版本": 0x00, "固件版本":0x01, "拼接算法版本": 0x02, "CHIPID": 0x03, "切行算法版本": 0x04, \
                    "OCR算法版本": 0x05, "TTS引擎版本": 0x06, "TTS发音人ID": 0x07, "所有信息": 0x10
        }
        for index, key in enumerate(res_software_version_dict.keys()):
            self.get_uart_software_version_box.setItemText(index, _translate("Form", key))

        # self.detect_uart_bauderate_box.setItemText(0, _translate("Form", "0"))
        # self.detect_uart_bauderate_box.setItemText(1, _translate("Form", "1"))


        self.uart_data_bit_label.setText(_translate("Form", "数据位："))
        self.uart_data_bit_combo_box.setItemText(0, _translate("Form", "8"))
        self.uart_data_bit_combo_box.setItemText(1, _translate("Form", "7"))
        self.uart_data_bit_combo_box.setItemText(2, _translate("Form", "6"))
        self.uart_data_bit_combo_box.setItemText(3, _translate("Form", "5"))
        self.uart_parity_bit_label.setText(_translate("Form", "校验位："))
        self.uart_parity_bit_combo_box.setItemText(0, _translate("Form", "N"))
        self.open_button.setText(_translate("Form", "打开串口"))
        self.close_button.setText(_translate("Form", "关闭串口"))
        self.uart_stop_bit_label.setText(_translate("Form", "停止位："))
        self.uart_stop_bit_combo_box.setItemText(0, _translate("Form", "1"))
        self.verticalGroupBox.setTitle(_translate("Form", "接受区"))
        self.verticalGroupBox_2.setTitle(_translate("Form", "发送区"))
        self.send_text_text_browser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\'; font-size:9pt;\">123456</span></p></body></html>"))
        self.send_button.setText(_translate("Form", "发送"))
        self.clear_send_text_button.setText(_translate("Form", "清除"))
        self.formGroupBox1.setTitle(_translate("Form", "串口状态"))
        self.calibrationformGroupBox.setTitle(_translate("Form", "串口坐标设置"))
        self.receive_size_label.setText(_translate("Form", "已接收："))
        self.send_size_label.setText(_translate("Form", "已发送："))
        self.hex_send.setText(_translate("Form", "Hex发送"))
        self.hex_receive.setText(_translate("Form", "Hex接收"))
        self.uart_state_ocr_tts_play_check_box.setText(_translate("Form", "TTS播报"))
        self.uart_state_ocr_translate_show_check_box.setText(_translate("Form", "翻译"))
        self.uart_state_ocr_dict_show_check_box.setText(_translate("Form", "词典"))
        self.clear_receive_text_button.setText(_translate("Form", "清除"))
        self.timer_send_cb.setText(_translate("Form", "定时发送"))
        self.timer_lineEdit.setText(_translate("Form", "1000"))
        self.timer_unit_label.setText(_translate("Form", "ms/次"))
        self.label_calibration.setText(_translate("Form", "校准图片显示"))
        self.detect_uart_bauderate_button.setText(_translate("Form", "开始自动检测"))
        self.set_calibration_up_position.setText(_translate("Form", "上"))
        self.set_calibration_down_position.setText(_translate("Form", "下"))
        self.set_calibration_left_position.setText(_translate("Form", "左"))
        self.set_calibration_right_position.setText(_translate("Form", "右"))
        self.set_calibration_button.setText(_translate("Form", "设置"))

        

