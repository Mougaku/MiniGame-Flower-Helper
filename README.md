# 🌸 MiniGame-Flower-Helper (花札物语)

> **English** | [中文](#-中文介绍)

**MiniGame-Flower-Helper** is a lightweight, high-performance automation script designed for WeChat flower planting mini-games. 

Unlike traditional OCR-based bots, this project utilizes **OpenCV** with **Multi-Scale Template Matching**, achieving extreme speed (avg. 0.05s) and high accuracy even with resolution differences. It also supports real-time email notifications via SMTP.

## ✨ Key Features

* **⚡ Blazing Fast**: Abandoned slow OCR; uses pure Computer Vision (OpenCV) for millisecond-level reaction.
* **🔍 Multi-Scale Search**: Automatically scales target templates (1.0x - 0.9x) to match game icons perfectly, resolving resolution mismatch issues.
* **📧 Remote Notification**: Sends real-time emails (via SMTP) to your phone when a high-value flower task is claimed.
* **🛡️ Secure Design**: Configuration data (`config.json`) is strictly separated from code to prevent credential leaks.
* **🇨🇳 Robust**: Solves Windows path encoding issues, fully supporting Chinese filenames for image targets.

## 🛠️ Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YourUsername/Cyber-Gardener.git](https://github.com/YourUsername/Cyber-Gardener.git)
    cd Cyber-Gardener
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Configuration**
    * Copy `config.sample.json` and rename it to `config.json`.
    * Fill in your SMTP email credentials and game settings in `config.json`.
    * *Note: `config.json` is git-ignored to keep your secrets safe.*

4.  **Prepare Targets**
    * Take screenshots of the flowers you want to collect.
    * Crop them to the icon only (save as `.png`).
    * Place them in the `targets/` folder.

## 🚀 Usage

Run the main script:

```bash
python main.py
 ```


<h2 id="-中文介绍">📖 中文介绍</h2>

花札物语小鸭赛脚本 是一个专为微信小游戏花札物语设计的轻量级自动化脚本。

本项目摒弃了缓慢的 OCR 文字识别方案，转而采用 OpenCV 计算机视觉 技术，配合多尺度模版匹配算法，实现了毫秒级的响应速度和极高的识别准确率。支持自动接取任务、自动翻页、以及抢到任务后的邮件远程通知。

✨ 核心亮点
⚡ 极速响应: 纯视觉识别方案，单次扫描仅需 0.05秒，不仅快，而且资源占用极低。

🔍 多尺度自适应: 内置多尺度缩放算法（默认 1.0x ~ 0.9x），完美解决截图与游戏内图标大小不一致的问题。

📧 实时通知: 支持 SMTP 协议（QQ邮箱/163邮箱），抢到稀有花朵后立即发送邮件提醒（微信可直接弹窗）。

🛡️ 安全配置: 采用 JSON 配置文件，敏感信息（如邮箱密码）与代码彻底分离，防止开源时泄露。

🇨🇳 中文支持: 解决了 OpenCV 在 Windows 下无法读取中文路径图片的痛点，素材命名随意写。

🛠️ 快速开始
下载项目

Bash
git clone [https://github.com/你的用户名/Cyber-Gardener.git](https://github.com/你的用户名/Cyber-Gardener.git)
cd Cyber-Gardener
安装依赖 建议使用 Python 3.8+ 环境：

Bash
pip install -r requirements.txt
配置参数

将项目根目录下的 config.sample.json 复制一份，重命名为 config.json。

用记事本或 IDE 打开 config.json，填入你的邮箱授权码和想要调整的参数。

准备素材

在游戏任务列表中截图你想要抢的花朵图标（尽量只截图标，不要包含过多背景）。

将图片放入 targets 文件夹中（例如 春英郁金香.png）。

🚀 运行脚本
在终端运行以下命令：

Bash
python main.py
⚙️ 进阶配置说明
如果你发现识别不准，可以在 config.json 中微调 search 部分：

max_scale / min_scale: 缩放范围。如果你截的图是原图大小，设为 1.0 到 0.9 即可。

match_threshold: 匹配阈值。设为 0.9 表示相似度必须达到 90% 才点击，防止误触。

⚠️ 免责声明 (Disclaimer)
本项目仅供 Python 编程学习与技术交流使用。请勿用于商业用途或违反游戏官方的服务条款。使用者需自行承担运行脚本可能带来的风险。

Made with ❤️ and Python.
