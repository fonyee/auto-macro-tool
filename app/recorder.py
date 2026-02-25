#!/usr/bin/env python3
"""
鼠标和键盘动作录制模块
"""

import time
from datetime import datetime
from pynput import mouse, keyboard


class Recorder:
    """
    录制鼠标和键盘动作的类
    """
    
    def __init__(self):
        """
        初始化录制器
        """
        self.is_recording = False
        self.actions = []
        self.start_time = None
        self.mouse_listener = None
        self.keyboard_listener = None
    
    def start_recording(self):
        """
        开始录制
        """
        self.is_recording = True
        self.actions = []
        self.start_time = time.time()
        
        # 开始监听鼠标事件
        self.mouse_listener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )
        self.mouse_listener.start()
        
        # 开始监听键盘事件
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        self.keyboard_listener.start()
        
        return True
    
    def stop_recording(self):
        """
        停止录制
        """
        if not self.is_recording:
            return False
        
        self.is_recording = False
        
        # 停止监听
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        return True
    
    def on_mouse_move(self, x, y):
        """
        鼠标移动事件处理
        """
        if not self.is_recording:
            return
        
        timestamp = time.time() - self.start_time
        self.actions.append({
            'type': 'mouse_move',
            'x': x,
            'y': y,
            'timestamp': timestamp
        })
    
    def on_mouse_click(self, x, y, button, pressed):
        """
        鼠标点击事件处理
        """
        if not self.is_recording:
            return
        
        timestamp = time.time() - self.start_time
        self.actions.append({
            'type': 'mouse_click',
            'x': x,
            'y': y,
            'button': str(button),
            'pressed': pressed,
            'timestamp': timestamp
        })
    
    def on_mouse_scroll(self, x, y, dx, dy):
        """
        鼠标滚轮事件处理
        """
        if not self.is_recording:
            return
        
        timestamp = time.time() - self.start_time
        self.actions.append({
            'type': 'mouse_scroll',
            'x': x,
            'y': y,
            'dx': dx,
            'dy': dy,
            'timestamp': timestamp
        })
    
    def on_key_press(self, key):
        """
        键盘按下事件处理
        """
        if not self.is_recording:
            return
        
        timestamp = time.time() - self.start_time
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)
        
        self.actions.append({
            'type': 'key_press',
            'key': key_str,
            'timestamp': timestamp
        })
    
    def on_key_release(self, key):
        """
        键盘释放事件处理
        """
        if not self.is_recording:
            return
        
        timestamp = time.time() - self.start_time
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)
        
        self.actions.append({
            'type': 'key_release',
            'key': key_str,
            'timestamp': timestamp
        })
    
    def get_actions(self):
        """
        获取录制的动作
        """
        return self.actions
    
    def save_actions(self, filename):
        """
        保存录制的动作到文件
        """
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.actions, f, indent=2, ensure_ascii=False)
        return True
    
    def load_actions(self, filename):
        """
        从文件加载录制的动作
        """
        import json
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.actions = json.load(f)
            return True
        except Exception:
            return False
