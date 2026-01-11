import tkinter as tk
from tkinter import ttk
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = None
running = False
ads_skipped = 0


def start_bot():
    global driver, running, ads_skipped

    if running:
        return

    running = True
    status_label.config(text="Status: Running")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--mute-audio")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.youtube.com")

    while running:
        try:
            skip = driver.find_element(By.CLASS_NAME, "ytp-skip-ad-button")
            skip.click()
            increment_counter()
        except:
            pass

        try:
            driver.find_element(By.CLASS_NAME, "ad-showing")
            video = driver.find_element(By.TAG_NAME, "video")
            driver.execute_script(
                "arguments[0].currentTime = arguments[0].duration;", video
            )
            increment_counter()
        except:
            pass

        time.sleep(1)


def increment_counter():
    global ads_skipped
    ads_skipped += 1
    counter_label.config(text=f"Ads skipped today: {ads_skipped}")


def stop_bot():
    global running, driver
    running = False
    status_label.config(text="Status: Stopped")

    try:
        driver.quit()
    except:
        pass


def start_thread():
    threading.Thread(target=start_bot, daemon=True).start()


# ---------- GUI ----------
root = tk.Tk()
root.title("YouTube Ad Skipper")
root.geometry("340x220")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

title = ttk.Label(
    root,
    text="YouTube Ad Skipper",
    font=("Segoe UI", 14, "bold")
)
title.pack(pady=10)

status_label = ttk.Label(
    root,
    text="Status: Stopped",
    font=("Segoe UI", 10)
)
status_label.pack(pady=5)

counter_label = ttk.Label(
    root,
    text="Ads skipped today: 0",
    font=("Segoe UI", 10)
)
counter_label.pack(pady=5)

start_btn = ttk.Button(
    root,
    text="▶ Start Skipping Ads",
    command=start_thread
)
start_btn.pack(pady=8)

stop_btn = ttk.Button(
    root,
    text="⏹ Stop",
    command=stop_bot
)
stop_btn.pack(pady=5)

root.mainloop()
