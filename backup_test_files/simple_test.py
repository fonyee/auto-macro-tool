#!/usr/bin/env python3
"""
简单测试脚本
"""

import sys

print("开始简单测试...")

# 测试基本导入
try:
    import os
    import threading
    print("✓ 成功导入基本模块")
except Exception as e:
    print(f"✗ 导入基本模块失败: {e}")

# 测试PySide6导入
try:
    from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
    from PySide6.QtCore import Qt, Signal
    print("✓ 成功导入PySide6模块")
except Exception as e:
    print(f"✗ 导入PySide6模块失败: {e}")

# 测试pynput导入
try:
    from pynput import mouse, keyboard
    print("✓ 成功导入pynput模块")
except Exception as e:
    print(f"✗ 导入pynput模块失败: {e}")

print("测试完成")
