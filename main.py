#!/usr/bin/env python3
"""
自动化工具主入口文件
"""

import sys
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow


def main():
    """
    主函数
    """
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 设置应用程序风格为Fusion，确保跨平台一致性
    app.setStyle('Fusion')
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
