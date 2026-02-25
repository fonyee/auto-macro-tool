# Auto Macro Tool - 录制和回放用户的鼠标和键盘操作的小工具

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/PySide6-6.0+-green.svg" alt="PySide6">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
</p>

## 📋 项目概述

Auto Macro Tool 是一款能够录制和回放用户的鼠标和键盘操作的小工具，适用于重复性任务处理。

### 核心特性

- 🎬 **智能录制**：精确记录鼠标移动、点击、滚轮和键盘输入
- ▶️ **灵活回放**：支持多次重复执行录制内容
- 🎛️ **速度控制**：0.5x - 2.0x 多档速度调节
- 🔄 **重复执行**：支持设置重复次数，自动循环执行
- ⌨️ **快捷键支持**：全局快捷键，操作更便捷
- 💾 **动作保存**：录制内容可保存为文件，随时加载使用

---

## 🚀 快速开始

### 环境要求

- **操作系统**: Windows 10/11
- **Python**: 3.8 或更高版本
- **依赖库**: PySide6, pynput

### 安装步骤

#### 方法一：使用批处理文件启动（推荐）

1. 双击 `start.bat` 文件即可自动检查环境并启动

#### 方法二：手动安装

1. **克隆仓库**
   ```bash
   git clone https://github.com/yourusername/auto-macro-tool.git
   cd auto-macro-tool
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动应用**
   ```bash
   python main.py
   ```

---

## 📖 使用指南

### 界面说明
<img width="238" height="271" alt="screenshot" src="https://github.com/user-attachments/assets/d7bc727b-1166-47df-8234-6ff6b2268e86" />


### 基本操作流程

#### 1. 录制操作

1. 点击 **"开始录制"** 按钮或按 `Ctrl+R`
2. 执行需要录制的鼠标和键盘操作
3. 点击 **"停止录制"** 按钮或按 `Ctrl+S`

#### 2. 回放操作

1. 设置 **重复次数**（默认 1 次）
2. 选择 **播放速度**（默认 1.0x）
3. 点击 **"开始回放"** 按钮或按 `Ctrl+P`
4. 观察状态提示和重复计数器

#### 3. 保存和加载

- **保存动作**：点击 "保存动作" 按钮，选择保存位置
- **加载动作**：点击 "加载动作" 按钮，选择动作文件

### 快捷键说明

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + R` | 开始录制 |
| `Ctrl + S` | 停止录制 |
| `Ctrl + P` | 开始回放 |
| `Ctrl + T` | 停止回放 |
| `Space` | 暂停/继续回放 |

---

## 🏗️ 技术架构

### 项目结构

```
auto-macro-tool/
├── app/
│   ├── __init__.py          # 应用包初始化
│   ├── main_window.py       # 主窗口界面
│   ├── recorder.py          # 录制功能模块
│   ├── player.py            # 回放功能模块
│   └── utils.py             # 工具函数
├── main.py                  # 程序入口
├── start.bat               # Windows 启动脚本
├── requirements.txt        # 依赖列表
└── README.md              # 项目文档
```

### 核心模块

#### Recorder（录制器）
- 监听鼠标事件：移动、点击、滚轮
- 监听键盘事件：按键按下和释放
- 记录时间戳，确保回放时序准确

#### Player（播放器）
- 解析录制数据
- 控制播放速度
- 支持重复执行
- 实时状态反馈

#### MainWindow（主窗口）
- PySide6 构建的图形界面
- 状态显示和更新
- 用户交互处理

---

## 🔧 配置说明

### 重复次数设置

在回放控制区域的 "重复次数" 输入框中设置：
- 最小值：1
- 最大值：999
- 步进值：1

### 播放速度调节

提供多种方式调节速度：
- **滑块调节**：25% - 400%
- **预设按钮**：0.5x, 1.0x, 1.5x, 2.0x

---

## 📝 API 文档

### Recorder 类

```python
from app.recorder import Recorder

recorder = Recorder()
recorder.start_recording()  # 开始录制
recorder.stop_recording()   # 停止录制
actions = recorder.get_actions()  # 获取录制的动作
```

### Player 类

```python
from app.player import Player

player = Player()
player.set_actions(actions)       # 设置动作
player.set_repeat_count(3)        # 设置重复次数
player.set_speed(1.5)             # 设置播放速度
player.start_playing()            # 开始回放
player.stop_playing()             # 停止回放
```

---

## 🤝 贡献规范

### 提交代码

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范

- 遵循 PEP 8 编码规范
- 添加必要的注释和文档字符串
- 确保代码通过基本测试

---

## ❓ 常见问题解答

### Q1: 录制时无法捕获某些应用程序的操作？

**A**: 某些安全软件或游戏可能会阻止输入监听。尝试：
- 以管理员身份运行程序
- 暂时关闭相关安全软件
- 检查应用程序的权限设置

### Q2: 回放时鼠标位置不准确？

**A**: 确保：
- 屏幕分辨率与录制时一致
- 目标应用程序窗口位置与录制时一致
- 使用相同的显示缩放比例

### Q3: 如何停止正在进行的回放？

**A**: 可以使用以下方式：
- 点击 "停止回放" 按钮
- 按快捷键 `Ctrl + T`
- 点击窗口关闭按钮

### Q4: 支持哪些操作系统？

**A**: 目前仅支持 Windows 10/11

### Q5: 录制的动作文件可以在其他电脑上使用吗？

**A**: 可以，但需要注意：
- 屏幕分辨率应保持一致
- 目标应用程序的界面布局应相同
- 文件路径使用相对路径

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE) 开源。

```
MIT License

Copyright (c) 2026 fonyee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 📞 联系方式

- **作者**: fonyee
- **邮箱**: fonyee@outlook.com
- **GitHub**: [github.com/fonyee](https://github.com/fonyee)

---

## 🙏 致谢

感谢以下开源项目：
- [PySide6](https://doc.qt.io/qtforpython/) - 跨平台 GUI 框架
- [pynput](https://github.com/moses-palmer/pynput) - 输入监听库

---

<p align="center">
  <b>如果这个项目对您有帮助，请给个 ⭐ Star 支持一下！</b>
</p>
