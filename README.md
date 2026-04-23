# 🌸 MiniGame-Flower-Helper for “花札物语”

> **中文** | [English](#-英文介绍)

**MiniGame-Flower-Helper** 是一个专为微信小游戏“花札物语”设计的轻量级自动化脚本。

本项目摒弃了缓慢的 OCR 文字识别方案，转而采用 **OpenCV 计算机视觉** 技术，配合**多尺度模版匹配**算法，实现了毫秒级的响应速度和极高的识别准确率。支持自动接取任务、自动翻页、以及抢到任务后的邮件远程通知。

## ✨ 核心亮点

* **⚡ 极速响应**: 纯视觉识别方案，单次扫描仅需 0.05秒，不仅快，而且资源占用极低。
* **🔍 多尺度自适应**: 内置多尺度缩放算法（默认 1.0x ~ 0.9x），完美解决截图与游戏内图标大小不一致的问题。
* **📧 实时通知**: 支持 SMTP 协议（QQ邮箱/163邮箱），抢到稀有花朵后立即发送邮件提醒（微信可直接弹窗）。
* **🛡️ 安全配置**: 采用 JSON 配置文件，敏感信息（如邮箱密码）与代码彻底分离，防止开源时泄露。
* **🇨🇳 中文支持**: 解决了 OpenCV 在 Windows 下无法读取中文路径图片的痛点，素材命名随意写。

## 🚀 快速开始（无需安装python）

1.  **下载以下文件**
    * targets 文件夹
    * ui 文件夹
    * config.json
    * FlowerBot.exe

2.  **配置参数**
    * 将项目根目录下的 `config.sample.json` 重命名为 `config.json`。
    * 用记事本或 IDE 打开 `config.json`，填入你的邮箱授权码和想要调整的参数。

3.  **准备素材**
    * 在游戏的百花册中截图你想要抢的花朵图标（参考我的例子，尽量只截图标最中间的一小块，不要包含任何背景。或者等小鸭赛刷出你要的花后在小鸭赛界面截图）。
    * 将图片放入 `targets` 文件夹中（例如 `春英郁金香.png`）。

4.  **运行脚本**
    双击打开 FlowerBot.exe


## 🛠️ 虚拟机运行方法

1. 在windows搜索栏中搜索 “启用或关闭 Windows 功能” 并打开
2. 找到“Windows沙盒”，勾选，点击确定 (可能需要重启电脑）
3. 在D盘根目录新建文件夹 Guaji_box (D:\Guaji_box)
4. 将以下文件和文件夹拷贝到Guaji_box

   a) targets 文件夹

   b) ui 文件夹

   c) config.json

   d) FlowerBot.exe

   e) Start_Farm.wsb

   f) Weixin文件夹      *从C:\Program Files\Tencent拷贝
7. 双击Start_Farm.wsb, 等待虚拟机启动
8. 在虚拟机内扫码登陆微信，打开花札小程序
9. 重新截图targets和ui      *有的机器不需要重新截图，启动后如果无反应，说明图片匹配不上，就需要重新截图
10. 双击FlowerBot.exe, 启动脚本

*一定一定不能最小化，会导致脚本报错执行失败。可以拖到最边上或者用其他窗口挡住虚拟机窗口


## 🛠️ 完整部署方法

1.  **下载项目**
    ```bash
    git clone [https://github.com/你的用户名/MiniGame-Flower-Helper.git](https://github.com/你的用户名/MiniGame-Flower-Helper.git)
    cd MiniGame-Flower-Helper
    ```

2.  **安装依赖**
    建议使用 Python 3.8+ 环境：
    ```bash
    pip install -r requirements.txt
    ```

3.  **配置参数**
    * 将项目根目录下的 `config.sample.json` 复制一份，重命名为 `config.json`。
    * 用记事本或 IDE 打开 `config.json`，填入你的邮箱授权码和想要调整的参数。

4.  **准备素材**
    * 在游戏的百花册中截图你想要抢的花朵图标（参考我的例子，尽量只截图标最中间的一小块，不要包含任何背景。或者等小鸭赛刷出你要的花后在小鸭赛界面截图）。
    * 将图片放入 `targets` 文件夹中（例如 `春英郁金香.png`）。

5.  **运行脚本**
    * 在终端运行以下命令：

```bash
python main.py
```


## ⚙️ 进阶配置说明

如果你发现识别不准，可以在 `config.json` 中微调 `search` 部分：

| 参数 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `max_scale` | 1.0 | 搜索时的最大缩放比例 (1.0 = 原图大小) |
| `min_scale` | 0.9 | 搜索时的最小缩放比例 |
| `match_threshold` | 0.9 | 匹配相似度阈值 (建议 0.85 - 0.95) |

* **max_scale / min_scale**: 如果你截的图是原图大小，设为 `1.0` 到 `0.9` 即可覆盖大部分情况。
* **match_threshold**: 设为 `0.9` 表示相似度必须达到 90% 才点击，能有效防止误触。

## ⚠️ 免责声明 (Disclaimer)

本项目仅供 Python 编程学习与技术交流使用。请勿用于商业用途或违反游戏官方的服务条款。使用者需自行承担运行脚本可能带来的风险。



<h2 id="-英文介绍">📖 English Description</h2>

**MiniGame-Flower-Helper** is a lightweight, high-performance automation script designed for WeChat flower planting mini-game “花札物语”. 

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
    git clone [https://github.com/Mougaku/MiniGame-Flower-Helper.git](https://github.com/Mougaku/MiniGame-Flower-Helper.git)
    cd MiniGame-Flower-Helper
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

---

*Made with ❤️ and Python.*
