import cv2
import numpy as np
import pyautogui
import time
import random
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# ================= 配置区 =================
try:
    from config import *
except Exception as e:
    print(f"❌ 配置加载失败: {e}")
    exit()


# ================= 工具函数区 =================

def is_color_similar(image_crop, template_img, threshold=5.0):
    """
    【新增】对比两张图片的平均颜色差异
    threshold: 允许的色差阈值 (建议 50-80)。
               如果发现颜色不一样也点了，就把这个数改小（例如 40）。
               如果发现颜色一样但不点，就把这个数改大（例如 80）。
    """
    try:
        # 1. 计算切片区域的平均颜色 (B, G, R)
        # axis=(0, 1) 表示计算整个长宽面的平均值
        avg_crop = np.mean(image_crop, axis=(0, 1))

        # 2. 计算模板的平均颜色
        avg_template = np.mean(template_img, axis=(0, 1))

        # 3. 计算两者颜色的欧式距离 (色差)
        color_diff = np.linalg.norm(avg_crop - avg_template)

        # 4. 如果色差小于阈值，说明颜色也对上了
        return color_diff < threshold, color_diff
    except Exception as e:
        print(f"⚠️ 颜色校验出错: {e}")
        return False, 999.0


def cv_imread(file_path):
    """
    【中文路径修复版】读取图片
    使用 numpy 读取二进制流，再解码。
    强制转换为 3 通道 BGR。
    """
    try:
        img_array = np.fromfile(file_path, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            print(f"❌ 无法解码图片 (可能已损坏): {file_path}")
            return None
        return img
    except Exception as exception:
        print(f"❌ 读取图片出错: {file_path} \n错误信息: {exception}")
        return None


def send_email_notify(task_name):
    """
    使用 SMTP 发送邮件通知
    """
    if not MAIL_SENDER or not MAIL_LICENSE:
        # print("⚠️ 邮箱配置未填写，跳过发送") # 避免刷屏，可以注释掉
        return

    print(f"📧 正在发送邮件通知: {task_name}")
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
        server = smtplib.SMTP_SSL(MAIL_HOST, 465)
        server.login(MAIL_SENDER, MAIL_LICENSE)
        server.sendmail(MAIL_SENDER, [MAIL_RECEIVER], message.as_string())
        server.quit()
        print("✅ 邮件发送成功！")
    except Exception as exception:
        print(f"❌ 邮件发送失败: {exception}")


def get_screenshot_cv():
    screen = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)


# ================= 核心逻辑区 =================

def multi_scale_search(target_path, screen_img, task_name):
    """
    【修改版】多尺度匹配 + 颜色强校验
    """
    template = cv_imread(target_path)
    if template is None: return None

    t_h, t_w = template.shape[:2]

    found = None  # 存储最佳匹配结果

    # 从大到小尝试缩放
    for scale in np.arange(MAX_SCALE, MIN_SCALE, -SCALE_STEP):
        # 1. 计算缩放后的尺寸
        resize_w = int(t_w * scale)
        resize_h = int(t_h * scale)

        # 边界检查
        if resize_w > screen_img.shape[1] or resize_h > screen_img.shape[0] or resize_w < 10:
            continue

        # 2. 缩放模版图
        resized_template = cv2.resize(template, (resize_w, resize_h))

        # 3. 形状匹配
        res = cv2.matchTemplate(screen_img, resized_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # 4. 如果形状相似度达标 (MATCH_THRESHOLD 在 config 里)
        if max_val >= MATCH_THRESHOLD:

            # ===【新增步骤】颜色校验 ===
            top_left_x = max_loc[0]
            top_left_y = max_loc[1]

            # 从屏幕上把这一块切下来
            screen_crop = screen_img[top_left_y: top_left_y + resize_h,
            top_left_x: top_left_x + resize_w]

            # 对比颜色
            color_ok, color_diff = is_color_similar(screen_crop, resized_template, threshold=5.0)

            if color_ok:
                # 只有颜色也对上了，才算找到
                # 记录最佳匹配 (相似度最高的一个)
                if found is None or max_val > found[0]:
                    center_x = top_left_x + resize_w // 2
                    center_y = top_left_y + resize_h // 2
                    found = (max_val, center_x, center_y, scale, color_diff)
            else:
                # 可选：打印一下为什么跳过，方便调试
                print(f"   ⚠️ 跳过干扰项{task_name}: 缩放:{scale:.2f} | 形状分={max_val:.2f} 但色差={color_diff:.1f}")
                pass

    if found:
        print(
            f"   ⚡️ 匹配成功! 目标:{os.path.basename(target_path)} | 缩放:{found[3]:.2f} | 相似度:{found[0]:.2f} | 色差:{found[4]:.1f}")
        return found[1], found[2]

    return None


def smart_click_image(img_name, folder, timeout=1.0):
    path = os.path.join(folder, img_name)
    if not os.path.exists(path): return False

    start_time = time.time()
    while time.time() - start_time < timeout:
        screen = get_screenshot_cv()
        template = cv_imread(path)
        if template is None: return False

        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val >= 0.8:
            h, w = template.shape[:2]
            pyautogui.click(max_loc[0] + w // 2, max_loc[1] + h // 2)
            return True
        time.sleep(0.3)
    return False


def confirm_task_logic():
    print("   👀 等待弹窗...")
    time.sleep(1.5)
    if smart_click_image('confirm_button.png', UI_FOLDER):
        print("✅✅✅ 成功接取！")
        return True

    print("   ⚠️ 未能接取，关闭")
    if not smart_click_image('close_button.png', UI_FOLDER):
        pyautogui.click(960, 300)  # 防止找不到关闭按钮时的兜底点击

    time.sleep(0.3)
    return False


def step_hunt_loop(targets):
    print(f"🔎 正在扫描 {len(targets)} 个目标...")

    screen = get_screenshot_cv()
    if screen is None:  # 【新增】防止屏幕截图失败
        print("❌ 截图失败，跳过本次扫描")
        return None

    for target_file in targets:
        target_path = os.path.join(TARGET_FOLDER, target_file)

        # 调用修改后的多尺度搜索
        loc = multi_scale_search(target_path, screen, target_file)

        if loc:
            print(f"   🎯 点击坐标: {loc}")
            pyautogui.click(loc[0], loc[1])

            if confirm_task_logic():
                return target_file

            # 没抢到，重新截图继续 (防止画面变化)
            time.sleep(0.1)
            screen = get_screenshot_cv()
        else:
            pass

    return None


def main():
    print("🚀 极速抢任务脚本 (颜色增强版) 已启动")

    if not os.path.exists(TARGET_FOLDER):
        print(f"❌ 错误: 找不到 {TARGET_FOLDER} 文件夹")
        return

    targets = [f for f in os.listdir(TARGET_FOLDER) if f.endswith('.png') or f.endswith('.jpg')]
    if not targets:
        print("❌ targets 文件夹为空！")
        return

    while True:
        try:
            print("\n--- 新一轮扫描 ---")

            # 检查是否在任务界面，不在就点进去
            if not smart_click_image('enter_button.png', UI_FOLDER):
                # 如果没找到入口，也没在列表页，可能是卡在二级菜单，点返回试试
                smart_click_image('back_button.png', UI_FOLDER)
                # (上面这行视情况开启，有时候会误触)
                time.sleep(0.5)
                smart_click_image('enter_button.png', UI_FOLDER)
                pass

            time.sleep(0.5)

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
                # 抢到一个后退出还是继续？如果继续就把下面这行 break 注释掉
                break

            print("⬅️ 返回刷新列表...")
            smart_click_image('back_button.png', UI_FOLDER)
            # 随机等待，模拟人类，防止被检测
            time.sleep(random.uniform(0.5, 1.0))

        except KeyboardInterrupt:
            print("🛑 用户主动停止")
            break
        except Exception as exception:
            print(f"❌ 主循环运行错误: {exception}")
            time.sleep(1)


if __name__ == "__main__":
    main()