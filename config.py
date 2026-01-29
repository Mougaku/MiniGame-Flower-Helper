import json
import os
import sys

# 配置文件路径
CONFIG_FILE = 'config.json'
SAMPLE_FILE = 'config.sample.json'

def load_config():
    """读取配置文件的逻辑"""
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ 错误: 未找到配置文件 {CONFIG_FILE}")
        print(f"💡 提示: 请复制 {SAMPLE_FILE} 为 {CONFIG_FILE} 并填入你的配置信息。")
        # 暂停程序，防止闪退（如果是双击运行）
        input("按回车键退出...")
        sys.exit(1)

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        sys.exit(1)

# === 执行读取 ===
data = load_config()

# === 变量映射 (将 JSON 里的值赋给大写变量，供 main.py 调用) ===

# 1. 邮箱配置
MAIL_ENABLE = data['email'].get('enable', True) # 默认开启
MAIL_HOST = data['email']['host']
MAIL_SENDER = data['email']['sender']
MAIL_LICENSE = data['email']['license']
MAIL_RECEIVER = data['email']['receiver']

# 2. 游戏基础配置
TARGET_FOLDER = data['game']['target_folder']
UI_FOLDER = data['game']['ui_folder']
SCROLL_LOOP_COUNT = data['game']['scroll_loop_count']
SCROLL_AMOUNT = data['game']['scroll_amount']
SCROLL_WAIT = data['game']['scroll_wait']

# 3. 图像识别/搜索配置
MAX_SCALE = data['search']['max_scale']
MIN_SCALE = data['search']['min_scale']
SCALE_STEP = data['search']['scale_step']
MATCH_THRESHOLD = data['search']['match_threshold']

print("✅ 配置加载成功")