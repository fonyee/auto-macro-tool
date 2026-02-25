#!/usr/bin/env python3
"""
测试主文件
"""

import sys

print("开始测试...")
print(f"Python版本: {sys.version}")

# 测试导入PySide6
try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
    print("✓ 成功导入PySide6")
except Exception as e:
    print(f"✗ 导入PySide6失败: {e}")
    import traceback
    traceback.print_exc()

# 测试导入app模块
try:
    from app import recorder
    print("✓ 成功导入app.recorder")
except Exception as e:
    print(f"✗ 导入app.recorder失败: {e}")
    import traceback
    traceback.print_exc()

try:
    from app import player
    print("✓ 成功导入app.player")
except Exception as e:
    print(f"✗ 导入app.player失败: {e}")
    import traceback
    traceback.print_exc()

# 测试导入main_window
try:
    from app.main_window import MainWindow
    print("✓ 成功导入app.main_window")
except Exception as e:
    print(f"✗ 导入app.main_window失败: {e}")
    import traceback
    traceback.print_exc()

print("测试完成")
