#!/usr/bin/env python3
"""
测试快捷键系统
"""

import sys
import os

# 添加项目路径到Python路径
sys.path.append(os.path.abspath('.'))

print("开始测试快捷键系统...")

# 测试导入PySide6的QShortcut
try:
    from PySide6.QtWidgets import QShortcut
    from PySide6.QtCore import QKeySequence
    print("✓ 成功导入QShortcut和QKeySequence")
except Exception as e:
    print(f"✗ 导入QShortcut和QKeySequence失败: {e}")
    import traceback
    traceback.print_exc()

print("测试完成")
