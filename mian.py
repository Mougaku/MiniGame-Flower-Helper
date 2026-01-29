import cv2
import numpy as np
import pyautogui
import time
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# ================= 配置区 =================
try:
    from config import *
except Exception as e:
    print(f"❌ 配置加载失败: {e}")
    exit()


# ========================================

def cv_imread(file_path):
    """
    【中文路径修复版】读取图片
    使用 numpy 读取二进制流，再解码。
    关键修正：使用 cv2.IMREAD_COLOR 强制转换为 3 通道 BGR，防止因透明通道导致匹配报错。
    """
    try:
        # np.fromfile 支持中文路径，读取为 uint8 数组
        img_array = np.fromfile(file_path, dtype=np.uint8)

        # 【修改点】使用 cv2.IMREAD_COLOR (数值为1)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            print(f"❌ 无法解码图片 (可能已损坏): {file_path}")
            return None

        return img
    except Exception as e:
        print(f"❌ 读取图片出错: {file_path} \n错误信息: {e}")
        return None

def send_email_notify(task_name):
    """
    使用 SMTP 发送邮件通知 (永久免费稳定版)
    """
    if not MAIL_SENDER or not MAIL_LICENSE:
        print("⚠️ 邮箱配置未填写，跳过发送")
        return

    print(f"📧 正在发送邮件通知: {task_name}")

    # 1. 构造邮件内容
    subject = f"🎉 抢到任务：{task_name}"
    content = f"""
    <h3>恭喜！自动脚本已成功接取任务</h3>
    <p>任务名称：<b style="color:red; font-size:20px;">{task_name}</b></p>
    <p>请及时上线查看或保持挂机。</p>
    """

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = Header("自动抢花脚本", 'utf-8')
    message['To'] = Header("主人", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        # 2. 连接服务器并发送
        server = smtplib.SMTP_SSL(MAIL_HOST, 465)  # QQ邮箱使用 SSL 端口 465
        server.login(MAIL_SENDER, MAIL_LICENSE)
        server.sendmail(MAIL_SENDER, [MAIL_RECEIVER], message.as_string())
        server.quit()
        print("✅ 邮件发送成功！")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")


def get_screenshot_cv():
    screen = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)


def multi_scale_search(target_path, screen_img):
    """
    多尺度匹配核心逻辑
    自动缩放模版图，尝试匹配屏幕
    """
    template = cv_imread(target_path)
    if template is None: return None

    t_h, t_w = template.shape[:2]

    # === 核心循环：从大到小尝试缩放 ===
    found = None

    # np.arange 生成从 MAX 到 MIN 的序列，比如 [1.0, 0.95, 0.90 ... 0.5]
    for scale in np.arange(MAX_SCALE, MIN_SCALE, -SCALE_STEP):
        # 1. 计算缩放后的尺寸
        resize_w = int(t_w * scale)
        resize_h = int(t_h * scale)

        # 如果缩放后比屏幕还大，或者太小(小于10像素)，就跳过
        if resize_w > screen_img.shape[1] or resize_h > screen_img.shape[0] or resize_w < 10:
            continue

        # 2. 缩放模版图
        resized_template = cv2.resize(template, (resize_w, resize_h))

        # 3. 匹配
        res = cv2.matchTemplate(screen_img, resized_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # 4. 如果匹配度达标
        if max_val >= MATCH_THRESHOLD:
            # 记录最佳匹配结果
            if found is None or max_val > found[0]:
                center_x = max_loc[0] + resize_w // 2
                center_y = max_loc[1] + resize_h // 2
                found = (max_val, center_x, center_y, scale)

    if found:
        print(f"   ⚡️ 缩放匹配成功! 图片:{os.path.basename(target_path)} 缩放:{found[3]:.2f} 相似度:{found[0]:.2f}")
        return (found[1], found[2])

    return None


def smart_click_image(img_name, folder, timeout=1.0):
    path = os.path.join(folder, img_name)
    if not os.path.exists(path): return False

    start_time = time.time()
    while time.time() - start_time < timeout:
        screen = get_screenshot_cv()
        # UI 按钮通常是固定的，不需要缩放，直接用普通匹配
        template = template = cv_imread(path)
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val >= 0.8:
            h, w = template.shape[:2]
            pyautogui.click(max_loc[0] + w // 2, max_loc[1] + h // 2)
            return True
        time.sleep(0.1)
    return False


def confirm_task_logic():
    print("   👀 等待弹窗...")
    time.sleep(0.5)

    if smart_click_image('confirm_button.png', UI_FOLDER):
        print("✅✅✅ 成功接取！")
        return True

    print("   ⚠️ 未能接取，关闭")
    if not smart_click_image('close_button.png', UI_FOLDER):
        pyautogui.click(960, 300)

    time.sleep(0.3)
    return False


def step_hunt_loop(targets):
    print(f"🔎 正在扫描 {len(targets)} 个目标 (多尺度)...")

    screen = get_screenshot_cv()

    for target_file in targets:
        target_path = os.path.join(TARGET_FOLDER, target_file)

        # 调用多尺度搜索
        loc = multi_scale_search(target_path, screen)

        if loc:
            print(f"   🎯 点击目标: {target_file}")
            pyautogui.click(loc[0], loc[1])

            if confirm_task_logic():
                return target_file

            # 没抢到，重新截图继续
            time.sleep(0.1)
            screen = get_screenshot_cv()

    return None


def main():
    print("🚀 极速抢任务脚本 (多尺度缩放版) 已启动")

    targets = [f for f in os.listdir(TARGET_FOLDER) if f.endswith('.png') or f.endswith('.jpg')]
    if not targets:
        print("❌ targets 文件夹为空！")
        return

    while True:
        try:
            print("\n--- 新一轮 ---")

            if not smart_click_image('enter_button.png', UI_FOLDER):
                smart_click_image('back_button.png', UI_FOLDER)
                continue

            time.sleep(1)

            task_taken_name = None
            for i in range(SCROLL_LOOP_COUNT):
                print(f"📄 第 {i + 1} 页")

                task_taken_name = step_hunt_loop(targets)
                if task_taken_name:
                    break

                if i < SCROLL_LOOP_COUNT - 1:
                    print("⬇️ 滚动...")
                    pyautogui.scroll(SCROLL_AMOUNT)
                    time.sleep(SCROLL_WAIT)

            if task_taken_name:
                print(f"🎉 任务完成: {task_taken_name}")
                send_email_notify(task_taken_name)
                break

            print("⬅️ 返回刷新...")
            smart_click_image('back_button.png', UI_FOLDER)
            time.sleep(random.uniform(1.0, 2.0))

        except KeyboardInterrupt:
            print("🛑 用户停止")
            break
        except Exception as e:
            print(f"❌ 运行错误: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()