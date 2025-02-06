import tkinter as tk
import requests
import time
from datetime import datetime
import pytz
import pygetwindow as gw
import psutil
import os
import sys
import json

prayer_mapping = {
    "Fajr": "الفجر",
    "Dhuhr": "الظهر",
    "Asr": "العصر",
    "Maghrib": "المغرب",
    "Isha": "العشاء"
}

appdata_dir = os.path.join(os.environ["APPDATA"], "PrayerReminder")
if not os.path.exists(appdata_dir):
    os.makedirs(appdata_dir)
data_file = os.path.join(appdata_dir, "prayer_status.json")

response = requests.get("http://api.aladhan.com/v1/timingsByCity", 
                        params={"city": "Gaza", "country": "Palestine", "method": "2"})
print(response.json()["data"]["timings"])

def load_prayer_data():
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception:
                data = []
    else:
        data = []
    return data

def save_prayer_data(data):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def update_prayer_status(prayer_ar, status):
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")
    data = load_prayer_data()
    updated = False
    for entry in data:
        if entry["date"] == current_date and entry["prayer"] == prayer_ar:
            entry["status"] = status
            entry["time"] = current_time
            updated = True
            break
    if not updated:
        data.append({"date": current_date, "prayer": prayer_ar, "status": status, "time": current_time})
    save_prayer_data(data)

def reset_database_for_new_day():
    today = datetime.now().strftime("%Y-%m-%d")
    data = load_prayer_data()
    new_data = [entry for entry in data if entry["date"] == today]
    save_prayer_data(new_data)

def get_prayer_times():
    url = "http://api.aladhan.com/v1/timingsByCity"
    params = {
        "city": "Gaza",
        "country": "Palestine",
        "method": "2"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'data' in data:
            return data['data']['timings']
    except Exception:
        pass
    return None

def is_prayer_time(prayer_times):
    palestine_tz = pytz.timezone('Asia/Gaza')
    current_time = datetime.now(palestine_tz).strftime("%H:%M")
    for prayer in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
        if prayer_times.get(prayer) == current_time:
            return prayer
    return None

def minimize_all_windows():
    minimized_windows = []
    for window in gw.getWindowsWithTitle(""):
        if window.title != "Prayer Reminder":
            window.minimize()
            minimized_windows.append(window)
    return minimized_windows

def restore_minimized_windows(minimized_windows):
    for window in minimized_windows:
        if window.isMinimized:
            window.restore()

def terminate_task_manager():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'Taskmgr.exe':
            try:
                proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

def show_missed_prayer_popup(prayer_ar):
    window = tk.Tk()
    window.title("تنبيه الصلاة الفائتة")
    window.attributes('-fullscreen', True)
    window.configure(bg='black')
    window.attributes('-topmost', True)
    window.protocol("WM_DELETE_WINDOW", lambda: None)

    frame = tk.Frame(window, bg='black')
    frame.pack(expand=True)

    label_text = f"لقد فاتتك صلاة {prayer_ar}.\nاضغط على الزر لتأكيد أنك صليت."
    label = tk.Label(frame, text=label_text, font=("Arial", 28, "bold"), fg="white", bg="black",
                     wraplength=800, justify="center")
    label.pack(pady=20)

    def on_ack():
        update_prayer_status(prayer_ar, "prayed")
        window.destroy()

    button_text = f"أنا صليت {prayer_ar}"
    tk.Button(frame, text=button_text, font=("Arial", 24, "bold"), command=on_ack, padx=20, pady=10).pack(pady=40)
    window.mainloop()

def show_black_screen(prayer):
    prayer_ar = prayer_mapping.get(prayer, prayer)
    
    window = tk.Tk()
    window.title("تنبيه الصلاة")
    window.attributes('-fullscreen', True)
    window.configure(bg='black')
    window.attributes('-topmost', True)
    window.protocol("WM_DELETE_WINDOW", lambda: None)

    frame = tk.Frame(window, bg='black')
    frame.pack(expand=True)

    label_text = f"حان وقت صلاة {prayer_ar} اذا صليت اضغط علا الكبسة الي تحت"
    label = tk.Label(frame, text=label_text, font=("Arial", 28, "bold"), fg="white", bg="black",
                     wraplength=800, justify="center")
    label.pack(pady=20)

    button_text = f"والله صليت {prayer_ar}"
    
    def log_and_close():
        update_prayer_status(prayer_ar, "missed")
        window.destroy()
    
    timer_id = window.after(300000, log_and_close)

    def on_button_click():
        window.after_cancel(timer_id)
        update_prayer_status(prayer_ar, "prayed")
        window.destroy()

    tk.Button(frame, text=button_text, font=("Arial", 24, "bold"),
              command=on_button_click, padx=20, pady=10).pack(pady=40)
    
    minimized_windows = minimize_all_windows()
    window.mainloop()
    restore_minimized_windows(minimized_windows)

def main():
    reset_database_for_new_day()
    prayer_times = get_prayer_times()
    if prayer_times is None:
        return
    while True:
        prayer = is_prayer_time(prayer_times)
        if prayer:
            show_black_screen(prayer)
            if prayer == "Isha":
                reset_database_for_new_day()
        time.sleep(60)

if __name__ == "__main__":
    main()
