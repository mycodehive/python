import time
import pyautogui
from pywinauto import Desktop

# URL 및 좌표 설정
TARGET_URL = "iacf.sejong.ac.kr"
CLICK_POSITION = (500, 20)
INTERVAL = 20  # 20초

def find_chrome_with_url():
    windows = Desktop(backend="uia").windows()
    for window in windows:
        if window.class_name() == "Chrome_WidgetWin_1":
            try:
                address_bar = window.child_window(title="주소 및 검색창", control_type="Edit")
                url = address_bar.get_value()
                if TARGET_URL in url:
                    return window
            except:
                continue
    return None

def is_window_active(window):
    active_window = Desktop(backend="uia").get_active()
    return active_window == window

def click_background():
    pyautogui.click(*CLICK_POSITION)

if __name__ == "__main__":
    print("Monitoring started...")
    try:
        while True:
            target_window = find_chrome_with_url()
            if target_window:
                if not is_window_active(target_window):
                    click_background()
                    print(f"Clicked at {CLICK_POSITION} on window '{target_window.window_text()}'")
                else:
                    print("Target window is active. Skipping click.")
            else:
                print("Target window not found.")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
