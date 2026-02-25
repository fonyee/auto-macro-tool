#!/usr/bin/env python3
"""
动作回放模块
"""

import time
from PySide6.QtCore import QObject, Signal
from pynput import mouse, keyboard


class Player(QObject):
    """
    回放鼠标和键盘动作的类
    """
    
    # 信号定义
    repeat_started = Signal(int)  # 重复开始信号，参数为重复次数
    
    def __init__(self):
        """
        初始化播放器
        """
        super().__init__()
        self.is_playing = False
        self.is_paused = False
        self.actions = []
        self.repeat_count = 1
        self.current_repeat = 0
        self.current_action_index = 0
        self.speed = 1.0  # 播放速度，默认1.0倍
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
    
    def set_actions(self, actions):
        """
        设置要回放的动作
        """
        self.actions = actions
        return True
    
    def set_repeat_count(self, count):
        """
        设置重复次数
        """
        self.repeat_count = max(1, count)
        return True
    
    def set_speed(self, speed):
        """
        设置播放速度
        """
        # 确保速度在合理范围内
        self.speed = max(0.25, min(4.0, speed))
        return True
    
    def get_speed(self):
        """
        获取当前播放速度
        """
        return self.speed
    
    def start_playing(self):
        """
        开始回放
        """
        self.is_playing = True
        self.is_paused = False
        self.current_repeat = 0
        self.current_action_index = 0
        
        try:
            while self.is_playing and self.current_repeat < self.repeat_count:
                # 发射重复开始信号
                self.current_repeat += 1
                self.repeat_started.emit(self.current_repeat)
                
                self._play_actions()
                if not self.is_playing:
                    break
                self.current_action_index = 0
        except Exception:
            self.stop_playing()
        
        return True
    
    def stop_playing(self):
        """
        停止回放
        """
        self.is_playing = False
        self.is_paused = False
        return True
    
    def pause_playing(self):
        """
        暂停回放
        """
        self.is_paused = True
        return True
    
    def resume_playing(self):
        """
        恢复回放
        """
        self.is_paused = False
        return True
    
    def get_is_paused(self):
        """
        获取暂停状态
        """
        return self.is_paused
    
    def _play_actions(self):
        """
        回放一组动作
        """
        if not self.actions:
            return
        
        start_time = time.time()
        
        # 从当前动作索引开始播放
        for i in range(self.current_action_index, len(self.actions)):
            if not self.is_playing:
                break
            
            # 检查是否暂停
            while self.is_paused:
                time.sleep(0.01)  # Reduced sleep time from 0.1s to 0.01s for faster response
                if not self.is_playing:
                    break
            
            if not self.is_playing:
                break
            
            action = self.actions[i]
            self.current_action_index = i
            
            # 等待到动作应该执行的时间，考虑播放速度
            expected_time = action['timestamp'] / self.speed
            actual_time = time.time() - start_time
            if expected_time > actual_time:
                time.sleep(expected_time - actual_time)
            
            # 执行动作
            self._execute_action(action)
        
        # 重置当前动作索引
        self.current_action_index = 0
    
    def _execute_action(self, action):
        """
        执行单个动作
        """
        action_type = action['type']
        
        if action_type == 'mouse_move':
            self._execute_mouse_move(action)
        elif action_type == 'mouse_click':
            self._execute_mouse_click(action)
        elif action_type == 'mouse_scroll':
            self._execute_mouse_scroll(action)
        elif action_type == 'key_press':
            self._execute_key_press(action)
        elif action_type == 'key_release':
            self._execute_key_release(action)
    
    def _execute_mouse_move(self, action):
        """
        执行鼠标移动
        """
        x = action['x']
        y = action['y']
        self.mouse_controller.position = (x, y)
    
    def _execute_mouse_click(self, action):
        """
        执行鼠标点击
        """
        x = action['x']
        y = action['y']
        button = action['button']
        pressed = action['pressed']
        
        # 移动到点击位置
        self.mouse_controller.position = (x, y)
        
        # 确定按钮类型
        if 'left' in button:
            mouse_button = mouse.Button.left
        elif 'right' in button:
            mouse_button = mouse.Button.right
        elif 'middle' in button:
            mouse_button = mouse.Button.middle
        else:
            return
        
        # 执行点击
        if pressed:
            self.mouse_controller.press(mouse_button)
        else:
            self.mouse_controller.release(mouse_button)
    
    def _execute_mouse_scroll(self, action):
        """
        执行鼠标滚轮
        """
        dx = action['dx']
        dy = action['dy']
        self.mouse_controller.scroll(dx, dy)
    
    def _execute_key_press(self, action):
        """
        执行键盘按下
        """
        key = action['key']
        self._press_key(key)
    
    def _execute_key_release(self, action):
        """
        执行键盘释放
        """
        key = action['key']
        self._release_key(key)
    
    def _press_key(self, key):
        """
        按下键盘按键
        """
        try:
            # 尝试直接按下字符键
            if len(key) == 1 and key.isprintable():
                self.keyboard_controller.press(key)
            else:
                # 处理特殊按键
                special_key = self._get_special_key(key)
                if special_key:
                    self.keyboard_controller.press(special_key)
        except Exception:
            pass
    
    def _release_key(self, key):
        """
        释放键盘按键
        """
        try:
            # 尝试直接释放字符键
            if len(key) == 1 and key.isprintable():
                self.keyboard_controller.release(key)
            else:
                # 处理特殊按键
                special_key = self._get_special_key(key)
                if special_key:
                    self.keyboard_controller.release(special_key)
        except Exception:
            pass
    
    def _get_special_key(self, key_str):
        """
        获取特殊按键对象
        """
        key_map = {
            'Key.esc': keyboard.Key.esc,
            'Key.tab': keyboard.Key.tab,
            'Key.caps_lock': keyboard.Key.caps_lock,
            'Key.shift': keyboard.Key.shift,
            'Key.ctrl_l': keyboard.Key.ctrl_l,
            'Key.alt_l': keyboard.Key.alt_l,
            'Key.space': keyboard.Key.space,
            'Key.enter': keyboard.Key.enter,
            'Key.backspace': keyboard.Key.backspace,
            'Key.right': keyboard.Key.right,
            'Key.left': keyboard.Key.left,
            'Key.down': keyboard.Key.down,
            'Key.up': keyboard.Key.up,
            'Key.ctrl_r': keyboard.Key.ctrl_r,
            'Key.alt_r': keyboard.Key.alt_r,
            'Key.print_screen': keyboard.Key.print_screen,
            'Key.scroll_lock': keyboard.Key.scroll_lock,
            'Key.pause': keyboard.Key.pause,
            'Key.insert': keyboard.Key.insert,
            'Key.home': keyboard.Key.home,
            'Key.page_up': keyboard.Key.page_up,
            'Key.delete': keyboard.Key.delete,
            'Key.end': keyboard.Key.end,
            'Key.page_down': keyboard.Key.page_down,
            'Key.num_lock': keyboard.Key.num_lock,
            'Key.cmd': keyboard.Key.cmd,
            'Key.cmd_r': keyboard.Key.cmd_r,
        }
        
        return key_map.get(key_str)
    
    def get_is_playing(self):
        """
        获取当前播放状态
        """
        return self.is_playing
