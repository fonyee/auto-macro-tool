#!/usr/bin/env python3
"""
简化版主窗口类
"""

import os
import threading
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QSpinBox, QFileDialog, QMessageBox, QGroupBox
)
from PySide6.QtCore import Qt, Signal
from app.recorder import Recorder
from app.player import Player


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
    
    def _create_ui(self):
        """
        创建用户界面
        """
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
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
        
        self.stop_play_button = QPushButton("停止回放")
        self.stop_play_button.clicked.connect(self._on_stop_play_clicked)
        self.stop_play_button.setEnabled(False)
        play_buttons_layout.addWidget(self.stop_play_button)
        play_layout.addLayout(play_buttons_layout)
        
        play_group.setLayout(play_layout)
        main_layout.addWidget(play_group)
        
        # 创建状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
    
    def _on_record_clicked(self):
        """
        开始录制按钮点击事件
        """
        self.is_recording = True
        self.record_button.setEnabled(False)
        self.stop_record_button.setEnabled(True)
        self.play_button.setEnabled(False)
        
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
        
        self.is_playing = True
        self.play_button.setEnabled(False)
        self.stop_play_button.setEnabled(True)
        self.record_button.setEnabled(False)
        
        # 开始回放（在新线程中）
        self.update_status.emit("正在回放...")
        playback_thread = threading.Thread(target=self._playback_thread)
        playback_thread.daemon = True
        playback_thread.start()
    
    def _on_stop_play_clicked(self):
        """
        停止回放按钮点击事件
        """
        self.player.stop_playing()
        self.is_playing = False
        
        self.play_button.setEnabled(True)
        self.stop_play_button.setEnabled(False)
        self.record_button.setEnabled(True)
        
        self.update_status.emit("回放已停止")
    
    def _playback_thread(self):
        """
        回放线程
        """
        self.player.start_playing()
        self.is_playing = False
        
        # 更新UI状态
        self.play_button.setEnabled(True)
        self.stop_play_button.setEnabled(False)
        self.record_button.setEnabled(True)
        
        self.update_status.emit("回放完成")
    
    def _update_status_label(self, text):
        """
        更新状态标签
        """
        self.status_label.setText(text)
    
    def closeEvent(self, event):
        """
        窗口关闭事件
        """
        # 停止录制和回放
        if self.is_recording:
            self.recorder.stop_recording()
        if self.is_playing:
            self.player.stop_playing()
        
        event.accept()
