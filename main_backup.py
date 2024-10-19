import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import threading
import time
from datetime import datetime

# 預設值
default_account = "your_default_account"
default_password = "your_default_password"
default_idNumber = "your_id_number"
default_credit_num = "your_credit_number"
default_safe_num = "your_safe_number"
default_platform_url = "your_ticket_platform_url"
default_platform = "KKTIX"  # 預設平台

# 通用的搶票流程
def start_ticket_booking(account, password, idNumber, credit_num, safe_num, platform_url, platform, booking_time):
    def click_with_retry(selector, by=By.CSS_SELECTOR, retries=3):
        for attempt in range(retries):
            try:
                button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((by, selector)))
                button.click()
                return
            except TimeoutException:
                print(f"按鈕未找到，重試中 ({attempt + 1}/{retries})...")
                time.sleep(5)
        raise Exception(f"無法點擊按鈕：{selector}")

    def wait_for_page_load():
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # 等待開票時間
    current_time = datetime.now()
    while current_time < booking_time:
        print(f"尚未到開票時間：{current_time}，等待中...")
        time.sleep(5)
        current_time = datetime.now()

    try:
        driver = webdriver.Chrome()
        driver.get(platform_url)

        # 刷新頁面直到購票按鈕出現或票券不再顯示"暫無票券"
        refresh_interval = 5  # 刷新間隔，單位為秒
        while True:
            try:
                # 檢查購票按鈕是否可點擊
                button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.outer-wrapper > div.content-wrapper > div > div.tickets > a"))
                )
                print("購票按鈕已出現，停止刷新並進入搶票流程！")
                break  # 找到購票按鈕，跳出循環

            except TimeoutException:
                try:
                    # 檢查是否顯示「暫無票券」
                    no_ticket_text = driver.find_element(By.XPATH, "//span[contains(text(),'暫無票券')]")
                    print("目前無票，繼續刷新頁面...")
                except:
                    print("按鈕和暫無票券都沒出現，繼續刷新...")
                
                driver.refresh()  # 刷新頁面
                time.sleep(refresh_interval)  # 等待刷新間隔

        # 頁面加載完成後繼續搶票流程
        wait_for_page_load()

        if platform == "KKTIX":
            click_with_retry("body > div.outer-wrapper > div.content-wrapper > div > div.tickets > a")

            # 登入流程
            login_button = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="guestModal"]/div[2]/div/div[3]/a[2]')))
            login_button.click()

            account_input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "user_login")))
            account_input.send_keys(account)

            password_input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "user_password")))
            password_input.send_keys(password)

            driver.find_element(By.CSS_SELECTOR, "#new_user > input.btn.btn.normal.btn-login").click()

            # 使用票價來定位
            try:
                price = "800"  # 目標價位
                plus_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), 'TWD${price}')]/following::button[@class='btn-default plus']"))
                )
                plus_button.click()  # 點擊加號按鈕來選擇票數
                print(f"選擇 NT${price} 的票成功！")
            except TimeoutException:
                print(f"無法選擇 NT${price} 的票")

            # 同意條款並繼續
            terms_input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "person_agree_terms")))
            terms_input.click()

            # 下一步
            click_with_retry("#registrationsNewApp > div > div:nth-child(5) > div.form-actions.plain.align-center.register-new-next-button-area > button")

    except Exception as e:
        print(f"出現錯誤: {e}")
        messagebox.showerror("Error", f"搶票失敗: {e}")

# 啟動多個搶票執行緒
def start_multiple_threads(account, password, idNumber, credit_num, safe_num, platform_url, platform, booking_time, num_windows):
    for _ in range(num_windows):
        threading.Thread(target=start_ticket_booking, args=(account, password, idNumber, credit_num, safe_num, platform_url, platform, booking_time)).start()

# 建立 GUI 介面
def create_gui():
    global start_button  # 声明全局变量
    root = tk.Tk()
    root.title("搶票程式")

    # 預設帳號輸入框
    tk.Label(root, text="帳號").grid(row=0, column=0, sticky='e', padx=10, pady=5)
    account_entry = tk.Entry(root)
    account_entry.insert(0, default_account)
    account_entry.grid(row=0, column=1, padx=10, pady=5)

    # 預設密碼輸入框
    tk.Label(root, text="密碼").grid(row=1, column=0, sticky='e', padx=10, pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.insert(0, default_password)
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    # 預設身分證號框
    tk.Label(root, text="身分證字號").grid(row=2, column=0, sticky='e', padx=10, pady=5)
    id_entry = tk.Entry(root)
    id_entry.insert(0, default_idNumber)
    id_entry.grid(row=2, column=1, padx=10, pady=5)

    # 預設信用卡資訊
    tk.Label(root, text="信用卡號碼").grid(row=3, column=0, sticky='e', padx=10, pady=5)
    credit_card_entry = tk.Entry(root, show="*")
    credit_card_entry.insert(0, default_credit_num)
    credit_card_entry.grid(row=3, column=1, padx=10, pady=5)

    # 預設信用卡安全碼
    tk.Label(root, text="信用卡安全碼").grid(row=4, column=0, sticky='e', padx=10, pady=5)
    safe_num_entry = tk.Entry(root, show="*")
    safe_num_entry.insert(0, default_safe_num)
    safe_num_entry.grid(row=4, column=1, padx=10, pady=5)

    # 預設搶票平台URL輸入框
    tk.Label(root, text="搶票平台URL").grid(row=5, column=0, sticky='e', padx=10, pady=5)
    platform_entry = tk.Entry(root)
    platform_entry.insert(0, default_platform_url)
    platform_entry.grid(row=5, column=1, padx=10, pady=5)

    # 預設搶票平台選擇
    tk.Label(root, text="選擇搶票平台").grid(row=6, column=0, sticky='e', padx=10, pady=5)
    platform_var = tk.StringVar()
    platform_var.set(default_platform)  # 默認選擇 KKTIX

    platform_options = ["KKTIX", "tixcraft"]
    platform_menu = tk.OptionMenu(root, platform_var, *platform_options)
    platform_menu.grid(row=6, column=1, padx=10, pady=5)

    # 開票時間選擇
    tk.Label(root, text="開票時間 (YYYY-MM-DD HH:MM:SS)").grid(row=7, column=0, sticky='e', padx=10, pady=5)
    booking_time_entry = tk.Entry(root)
    booking_time_entry.grid(row=7, column=1, padx=10, pady=5)

    # 開啟視窗數量
    tk.Label(root, text="開啟視窗數量").grid(row=8, column=0, sticky='e', padx=10, pady=5)
    num_windows_entry = tk.Entry(root)
    num_windows_entry.insert(0, "1")
    num_windows_entry.grid(row=8, column=1, padx=10, pady=5)

    # 開始搶票按鈕
    start_button = tk.Button(root, text="開始搶票", command=lambda: on_start(
        account_entry.get(), password_entry.get(), id_entry.get(), credit_card_entry.get(), safe_num_entry.get(), platform_entry.get(), platform_var.get(), booking_time_entry.get(), int(num_windows_entry.get())))
    start_button.grid(row=9, column=1, padx=10, pady=10)

    root.mainloop()

def on_start(account, password, idNumber, credit_num, safe_num, platform_url, platform, booking_time_str, num_windows):
    try:
        booking_time = datetime.strptime(booking_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        messagebox.showerror("Error", "請輸入正確的開票時間格式！")
        return
    
    # 禁用開始按鈕避免重複點擊
    start_button.config(state=tk.DISABLED)

    
    start_multiple_threads(account, password, idNumber, credit_num, safe_num, platform_url, platform, booking_time, num_windows)

# 啟動 GUI
if __name__ == "__main__":
    create_gui()
