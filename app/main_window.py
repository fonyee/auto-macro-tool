#!/usr/bin/env python3
"""
主窗口类
"""

import os
import threading
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QSpinBox, QFileDialog, QMessageBox, QGroupBox, QSlider,
    QTextEdit, QApplication
)
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QKeySequence
from app.recorder import Recorder
from app.player import Player
from pynput import keyboard


class KeyboardListener(QThread):
    """
    全局键盘监听器线程
    """
    
    # 信号定义
    start_record = Signal()
    stop_record = Signal()
    start_play = Signal()
    stop_play = Signal()
    toggle_pause = Signal()
    
    def __init__(self):
        super().__init__()
        self.listener = None
        self.is_running = True
    
    def run(self):
        """
        启动全局键盘监听器
        """
        # 定义全局热键
        hotkeys = {
            '<ctrl>+r': self.on_start_record,
            '<ctrl>+s': self.on_stop_record,
            '<ctrl>+p': self.on_start_play,
            '<ctrl>+t': self.on_stop_play,
            '<space>': self.on_toggle_pause
        }
        
        try:
            # 创建全局热键监听器
            with keyboard.GlobalHotKeys(hotkeys) as self.listener:
                while self.is_running:
                    self.listener.join(0.1)
        except Exception:
            pass
    
    def stop(self):
        """
        停止键盘监听器
        """
        self.is_running = False
        if self.listener:
            self.listener.stop()
    
    def on_start_record(self):
        """
        开始录制热键触发
        """
        self.start_record.emit()
    
    def on_stop_record(self):
        """
        停止录制热键触发
        """
        self.stop_record.emit()
    
    def on_start_play(self):
        """
        开始回放热键触发
        """
        self.start_play.emit()
    
    def on_stop_play(self):
        """
        停止回放热键触发
        """
        self.stop_play.emit()
    
    def on_toggle_pause(self):
        """
        暂停/继续热键触发
        """
        self.toggle_pause.emit()


class MainWindow(QMainWindow):
    """
    主窗口类
    """
    
    # 信号定义
    update_status = Signal(str)
    
    def __init__(self):
        """
        初始化主窗口
        """
        super().__init__()
        
        # 设置窗口属性
        self.setWindowTitle("自动化工具")
        self.setGeometry(100, 100, 500, 400)
        
        # 初始化组件
        self.recorder = Recorder()
        self.player = Player()
        self.is_recording = False
        self.is_playing = False
        
        # 创建UI
        self._create_ui()
        
        # 连接信号
        self.update_status.connect(self._update_status_label)
        
        # 初始化全局键盘监听器
        self.keyboard_listener = KeyboardListener()
        self.keyboard_listener.start_record.connect(self._on_record_clicked)
        self.keyboard_listener.stop_record.connect(self._on_stop_record_clicked)
        self.keyboard_listener.start_play.connect(self._on_play_clicked)
        self.keyboard_listener.stop_play.connect(self._on_stop_play_clicked)
        self.keyboard_listener.toggle_pause.connect(self._on_pause_clicked)
        
        # 启动键盘监听器线程
        self.keyboard_listener.start()
    
    def _create_ui(self):
        """
        创建用户界面
        """
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 设置整体样式
        self.setStyleSheet("""
            /* 主窗口样式 */
            QMainWindow {
                background-color: #f8f9fa;
            }
            
            /* 中央部件样式 */
            QWidget {
                background-color: #f8f9fa;
            }
            
            /* 分组框样式 */
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
                font-size: 14px;
                font-weight: 600;
                color: #495057;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                color: #343a40;
                font-weight: 600;
            }
            
            /* 按钮样式 */
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #0069d9;
            }
            
            QPushButton:pressed {
                background-color: #005cbf;
            }
            
            QPushButton:disabled {
                background-color: #6c757d;
                color: #ffffff;
            }
            
            /* 预设速度按钮样式 */
            QPushButton[text="0.5x"],
            QPushButton[text="1.0x"],
            QPushButton[text="1.5x"],
            QPushButton[text="2.0x"] {
                background-color: #e9ecef;
                color: #495057;
                border: 1px solid #dee2e6;
                min-width: 60px;
            }
            
            QPushButton[text="0.5x"]:hover,
            QPushButton[text="1.0x"]:hover,
            QPushButton[text="1.5x"]:hover,
            QPushButton[text="2.0x"]:hover {
                background-color: #dee2e6;
            }
            
            /* 标签样式 */
            QLabel {
                color: #495057;
                font-size: 14px;
            }
            
            /* 滑块样式 */
            QSlider {
                background: transparent;
            }
            
            QSlider::groove:horizontal {
                background: #dee2e6;
                height: 6px;
                border-radius: 3px;
            }
            
            QSlider::handle:horizontal {
                background: #007bff;
                width: 18px;
                height: 18px;
                border-radius: 9px;
                margin: -6px 0;
            }
            
            QSlider::handle:horizontal:hover {
                background: #0069d9;
            }
            
            /* 微调框样式 */
            QSpinBox {
                min-width: 120px;
                padding: 8px 40px 8px 10px;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                font-size: 14px;
                color: #495057;
                background-color: #ffffff;
            }
            
            QSpinBox:hover {
                border-color: #adb5bd;
            }
            
            QSpinBox:focus {
                border-color: #007bff;
                outline: none;
            }
            
            /* 微调框按钮样式 - 现代化设计 */ 
            QSpinBox::up-button, QSpinBox::down-button { 
                subcontrol-origin: padding; 
                subcontrol-position: right; 
                width: 28px; 
                height: 20px; 
                border: none; 
                background-color: transparent; 
                margin: 1px 2px; 
                border-radius: 3px; 
            } 
            
            QSpinBox::up-button { 
                subcontrol-position: top right; 
                margin-bottom: 0px; 
            } 
            
            QSpinBox::down-button { 
                subcontrol-position: bottom right; 
                margin-top: 0px; 
            } 
            
            QSpinBox::up-button:hover, QSpinBox::down-button:hover { 
                background-color: #f0f2f5; 
            } 
            
            QSpinBox::up-button:pressed, QSpinBox::down-button:pressed { 
                background-color: #e6e9ef; 
            } 
            
            QSpinBox::up-button:disabled, QSpinBox::down-button:disabled { 
                background-color: transparent; 
            } 
            
            /* 自定义加减符号 - 使用边框技巧创建三角形 */ 
            QSpinBox::up-arrow { 
                width: 0px; 
                height: 0px; 
                border-left: 4px solid transparent; 
                border-right: 4px solid transparent; 
                border-bottom: 6px solid #495057; 
                border-top: none; 
                margin: 5px auto; 
            } 
              
            QSpinBox::down-arrow { 
                width: 0px; 
                height: 0px; 
                border-left: 4px solid transparent; 
                border-right: 4px solid transparent; 
                border-top: 6px solid #495057; 
                border-bottom: none; 
                margin: 5px auto; 
            } 
            
            QSpinBox::up-arrow:hover { 
                border-bottom-color: #007bff; 
            } 
            
            QSpinBox::down-arrow:hover { 
                border-top-color: #007bff; 
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建录制控制组
        record_group = QGroupBox("录制控制")
        record_layout = QHBoxLayout()
        
        self.record_button = QPushButton("开始录制")
        self.record_button.clicked.connect(self._on_record_clicked)
        record_layout.addWidget(self.record_button)
        
        self.stop_record_button = QPushButton("停止录制")
        self.stop_record_button.clicked.connect(self._on_stop_record_clicked)
        self.stop_record_button.setEnabled(False)
        record_layout.addWidget(self.stop_record_button)
        
        record_group.setLayout(record_layout)
        main_layout.addWidget(record_group)
        
        # 创建回放控制组
        play_group = QGroupBox("回放控制")
        play_layout = QVBoxLayout()
        
        # 回放按钮
        play_buttons_layout = QHBoxLayout()
        self.play_button = QPushButton("开始回放")
        self.play_button.clicked.connect(self._on_play_clicked)
        play_buttons_layout.addWidget(self.play_button)
        
        self.pause_button = QPushButton("暂停")
        self.pause_button.clicked.connect(self._on_pause_clicked)
        self.pause_button.setEnabled(False)
        play_buttons_layout.addWidget(self.pause_button)
        
        self.stop_play_button = QPushButton("停止回放")
        self.stop_play_button.clicked.connect(self._on_stop_play_clicked)
        self.stop_play_button.setEnabled(False)
        play_buttons_layout.addWidget(self.stop_play_button)
        play_layout.addLayout(play_buttons_layout)
        
        # 重复次数设置
        repeat_layout = QHBoxLayout()
        repeat_label = QLabel("重复次数:")
        repeat_layout.addWidget(repeat_label)
        
        self.repeat_spinbox = QSpinBox()
        self.repeat_spinbox.setMinimum(1)
        self.repeat_spinbox.setMaximum(999)
        self.repeat_spinbox.setValue(1)
        self.repeat_spinbox.setSingleStep(1)  # 确保每次只增加/减少1
        repeat_layout.addWidget(self.repeat_spinbox)
        play_layout.addLayout(repeat_layout)
        
        # 速度调节设置
        speed_layout = QVBoxLayout()
        
        # 速度显示和滑块
        speed_control_layout = QHBoxLayout()
        speed_label = QLabel("播放速度:")
        speed_control_layout.addWidget(speed_label)
        
        self.speed_label = QLabel("1.0x")
        self.speed_label.setFixedWidth(50)
        speed_control_layout.addWidget(self.speed_label)
        
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(25)
        self.speed_slider.setMaximum(400)
        self.speed_slider.setValue(100)
        self.speed_slider.setTickInterval(25)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.valueChanged.connect(self._on_speed_changed)
        speed_control_layout.addWidget(self.speed_slider)
        speed_layout.addLayout(speed_control_layout)
        
        # 预设速度按钮
        preset_speed_layout = QHBoxLayout()
        preset_speeds = [0.5, 1.0, 1.5, 2.0]
        self.preset_buttons = []
        
        for speed in preset_speeds:
            button = QPushButton(f"{speed}x")
            button.clicked.connect(lambda checked, s=speed: self._on_preset_speed_clicked(s))
            self.preset_buttons.append(button)
            preset_speed_layout.addWidget(button)
        
        speed_layout.addLayout(preset_speed_layout)
        play_layout.addLayout(speed_layout)
        
        play_group.setLayout(play_layout)
        main_layout.addWidget(play_group)
        
        # 创建文件操作组
        file_group = QGroupBox("文件操作")
        file_layout = QHBoxLayout()
        
        self.save_button = QPushButton("保存动作")
        self.save_button.clicked.connect(self._on_save_clicked)
        file_layout.addWidget(self.save_button)
        
        self.load_button = QPushButton("加载动作")
        self.load_button.clicked.connect(self._on_load_clicked)
        file_layout.addWidget(self.load_button)
        
        self.shortcuts_button = QPushButton("快捷键")
        self.shortcuts_button.clicked.connect(self._on_shortcuts_clicked)
        file_layout.addWidget(self.shortcuts_button)
        
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)
        
        # 创建状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # 创建重复计数器显示（纯文字，无框）
        self.repeat_counter_label = QLabel("重复第 0 次")
        self.repeat_counter_label.setAlignment(Qt.AlignCenter)
        self.repeat_counter_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #6c757d;
                padding: 5px;
            }
        """)
        main_layout.addWidget(self.repeat_counter_label)
        
        # 连接重复计数信号
        self.player.repeat_started.connect(self._on_repeat_started)

    def _on_repeat_started(self, repeat_number):
        """重复开始处理"""
        self.repeat_counter_label.setText(f"重复第 {repeat_number} 次")

    def _on_record_clicked(self):
        """
        开始录制按钮点击事件
        """
        self.is_recording = True
        self.record_button.setEnabled(False)
        self.stop_record_button.setEnabled(True)
        self.play_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.load_button.setEnabled(False)
        
        # 开始录制
        self.recorder.start_recording()
        self.update_status.emit("正在录制...")
    
    def _on_stop_record_clicked(self):
        """
        停止录制按钮点击事件
        """
        self.is_recording = False
        self.record_button.setEnabled(True)
        self.stop_record_button.setEnabled(False)
        self.play_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.load_button.setEnabled(True)
        
        # 停止录制
        self.recorder.stop_recording()
        self.update_status.emit("录制完成")
        
        # 更新播放器的动作
        actions = self.recorder.get_actions()
        self.player.set_actions(actions)
    
    def _on_play_clicked(self):
        """
        开始回放按钮点击事件
        """
        # 检查是否有录制的动作
        actions = self.recorder.get_actions()
        if not actions:
            QMessageBox.warning(self, "警告", "没有录制的动作，请先录制")
            return
        
        # 如果正在播放，先停止当前回放（处理双击重新启动）
        if self.is_playing:
            self.player.stop_playing()
            # 等待当前回放线程结束
            time.sleep(0.1)
        
        self.is_playing = True
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_play_button.setEnabled(True)
        self.record_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.load_button.setEnabled(False)
        
        # 重置暂停按钮状态
        self.pause_button.setText("暂停")
        
        # 设置重复次数
        repeat_count = self.repeat_spinbox.value()
        self.player.set_repeat_count(repeat_count)
        
        # 设置播放速度
        current_speed = self.player.get_speed()
        self.player.set_speed(current_speed)
        
        # 开始回放（在新线程中）
        self.update_status.emit("正在回放...")
        playback_thread = threading.Thread(target=self._playback_thread)
        playback_thread.daemon = True
        playback_thread.start()
    
    def _playback_thread(self):
        """
        回放线程
        """
        self.player.start_playing()
        self.is_playing = False
        
        # 更新UI状态
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_play_button.setEnabled(False)
        self.record_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.load_button.setEnabled(True)
        
        self.update_status.emit("回放完成")
    
    def _on_stop_play_clicked(self):
        """
        停止回放按钮点击事件
        """
        self.player.stop_playing()
        self.is_playing = False
        
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_play_button.setEnabled(False)
        self.record_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.load_button.setEnabled(True)
        
        self.update_status.emit("回放已停止")
    
    def _on_save_clicked(self):
        """
        保存动作按钮点击事件
        """
        # 检查是否有录制的动作
        actions = self.recorder.get_actions()
        if not actions:
            QMessageBox.warning(self, "警告", "没有录制的动作，请先录制")
            return
        
        # 打开保存对话框
        filename, _ = QFileDialog.getSaveFileName(
            self, "保存动作", "", "JSON Files (*.json)"
        )
        
        if filename:
            # 确保文件扩展名正确
            if not filename.endswith('.json'):
                filename += '.json'
            
            # 保存动作
            if self.recorder.save_actions(filename):
                self.update_status.emit(f"动作已保存到 {filename}")
            else:
                QMessageBox.error(self, "错误", "保存失败")
    
    def _on_load_clicked(self):
        """
        加载动作按钮点击事件
        """
        # 打开加载对话框
        filename, _ = QFileDialog.getOpenFileName(
            self, "加载动作", "", "JSON Files (*.json)"
        )
        
        if filename:
            # 加载动作
            if self.recorder.load_actions(filename):
                # 更新播放器的动作
                actions = self.recorder.get_actions()
                self.player.set_actions(actions)
                self.update_status.emit(f"动作已从 {filename} 加载")
            else:
                QMessageBox.error(self, "错误", "加载失败")
    
    def _update_status_label(self, text):
        """
        更新状态标签
        """
        self.status_label.setText(text)
    
    def _on_speed_changed(self, value):
        """
        速度滑块变化事件处理
        """
        speed = value / 100.0
        self.player.set_speed(speed)
        self.speed_label.setText(f"{speed:.2f}x")
    
    def _on_preset_speed_clicked(self, speed):
        """
        预设速度按钮点击事件处理
        """
        self.player.set_speed(speed)
        self.speed_slider.setValue(int(speed * 100))
        self.speed_label.setText(f"{speed:.2f}x")
    
    def _on_pause_clicked(self):
        """
        暂停/继续按钮点击事件
        """
        if self.player.get_is_paused():
            # 恢复播放
            self.player.resume_playing()
            self.pause_button.setText("暂停")
            self.update_status.emit("恢复回放")
        else:
            # 暂停播放
            self.player.pause_playing()
            self.pause_button.setText("继续")
            self.update_status.emit("暂停回放")
    

    
    def _on_shortcuts_clicked(self):
        """
        显示快捷键使用说明
        """
        shortcuts_text = "快捷键使用说明:\n\n"
        shortcuts_text += "开始录制: Ctrl+R\n"
        shortcuts_text += "停止录制: Ctrl+S\n"
        shortcuts_text += "开始回放: Ctrl+P\n"
        shortcuts_text += "停止回放: Ctrl+T\n"
        shortcuts_text += "暂停/继续回放: Space\n"
        
        QMessageBox.information(self, "快捷键说明", shortcuts_text)
    
    def closeEvent(self, event):
        """
        窗口关闭事件
        """
        # 停止录制和回放
        if self.is_recording:
            self.recorder.stop_recording()
        if self.is_playing:
            self.player.stop_playing()
        
        # 停止键盘监听器线程
        if hasattr(self, 'keyboard_listener'):
            self.keyboard_listener.stop()
            self.keyboard_listener.wait(1.0)  # 等待线程停止
        
        event.accept()
