import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import threading
import time

# 通用的搶票流程
def start_ticket_booking(account, password, idNumber, credit_num, safe_num, platform_url, platform):

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

    try:
        driver = webdriver.Chrome()
        # 打開指定平台的URL
        driver.get(platform_url)
        wait_for_page_load()

        if platform == "KKTIX":
            # KKTIX 的搶票邏輯
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
                plus_button.click()
                plus_button.click()
                print(f"選擇 NT${price} 的票成功！")
            except TimeoutException:
                print(f"無法選擇 NT${price} 的票")
            # # 選擇票數等操作
            # click_with_retry('//*[@id="ticket_750360"]/div/span[4]/button[2]', by=By.XPATH)
            # click_with_retry('//*[@id="ticket_750360"]/div/span[4]/button[2]', by=By.XPATH)

            # 同意條款並繼續
            terms_input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "person_agree_terms")))
            terms_input.click()

            # 下一步
            click_with_retry("#registrationsNewApp > div > div:nth-child(5) > div.form-actions.plain.align-center.register-new-next-button-area > button")
            # Modal
            try:
                modal_button = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#infoModal > div.modal-dialog > div > div.modal-footer > button")))
                modal_button.click()
            except TimeoutException:
                print("Modal button not found, skipping...")

            # 確認座位
            confirm_set_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="registrationsShowApp"]/div[2]/div/div/div/ng-include[2]/div/div/div/div[3]/div/button')))
            confirm_set_button.click()

            # 完成選位
            finish_link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="registrationsShowApp"]/div[2]/div/div/div/ng-include[2]/div/div/div/div[3]/div/div/div/div[1]/a')))
            finish_link.click()


            # 確認表單資訊
            confirm_form_btn = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="registrations_controller"]/div[4]/div[2]/div/div[4]/a')))
            confirm_form_btn.click()

            # 身分證號碼
            ID_input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="registrations_controller"]/div[4]/div[2]/div/div[1]/form/div[2]/table/tbody[2]/tr[1]/td/div/div/div/ul/li/div/div/div/div/div/div/input')))
            ID_input.send_keys(idNumber)

            # 選擇信用卡付款
            select_credit_card = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="payment-type-block"]/td/div/div/div/ul/li[1]/div/div/label')))
            select_credit_card.click()

            # 信用卡號
            credit_input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="payment-type-block"]/td/div/div/div/ul/li[1]/div/div/div/div/div[1]/div/input[1]')))
            credit_input.send_keys(credit_num)

            # 安全碼
            safe_input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="payment-type-block"]/td/div/div/div/ul/li[1]/div/div/div/div/div[3]/div/input')))
            safe_input.send_keys(safe_num)

        elif platform == "tixcraft":
            buy_ticket_btn = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tab-func"]/li[1]/a')))
            buy_ticket_btn.click()

        messagebox.showinfo("Success", "搶票流程完成！")

    except Exception as e:
        print(f"出現錯誤: {e}")
        messagebox.showerror("Error", f"搶票失敗: {e}")

# 啟動搶票執行緒
def start_thread(account, password, idNumber, credit_num, safe_num, platform_url, platform):
    threading.Thread(target=start_ticket_booking, args=(account, password, idNumber, credit_num, safe_num, platform_url, platform)).start()

# 建立 GUI 介面
def create_gui():
    root = tk.Tk()
    root.title("word.exe")

    # 帳號輸入框
    tk.Label(root, text="帳號").grid(row=0, column=0, sticky='e', padx=10, pady=5)
    account_entry = tk.Entry(root)
    account_entry.grid(row=0, column=1, padx=10, pady=5)

    # 密碼輸入框
    tk.Label(root, text="密碼").grid(row=1, column=0, sticky='e', padx=10, pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    # 身分證字號框
    tk.Label(root, text="身分證字號").grid(row=2, column=0, sticky='e', padx=10, pady=5)
    id_entry = tk.Entry(root, show="*")
    id_entry.grid(row=2, column=1, padx=10, pady=5)

    # 信用卡資訊
    tk.Label(root, text="信用卡號碼").grid(row=3, column=0, sticky='e', padx=10, pady=5)
    credit_card_entry = tk.Entry(root, show="*")
    credit_card_entry.grid(row=3, column=1, padx=10, pady=5)

    # 信用卡安全碼
    tk.Label(root, text="信用卡安全碼").grid(row=4, column=0, sticky='e', padx=10, pady=5)
    safe_num_entry = tk.Entry(root)
    safe_num_entry.grid(row=4, column=1, padx=10, pady=5)

    # 搶票平台URL輸入框
    tk.Label(root, text="搶票平台URL").grid(row=5, column=0, sticky='e', padx=10, pady=5)
    platform_entry = tk.Entry(root)
    platform_entry.grid(row=5, column=1, padx=10, pady=5)

    # 搶票平台選擇
    tk.Label(root, text="選擇搶票平台").grid(row=6, column=0, sticky='e', padx=10, pady=5)
    platform_var = tk.StringVar()
    platform_var.set("KKTIX")  # 默認選擇 KKTIX

    platform_options = ["KKTIX", "tixcraft"]
    platform_menu = tk.OptionMenu(root, platform_var, *platform_options)
    platform_menu.grid(row=6, column=1, padx=10, pady=5)

    # 開始搶票按鈕
    start_button = tk.Button(root, text="開始搶票", command=lambda: on_start(
        account_entry.get(), password_entry.get(), id_entry.get(), credit_card_entry.get(), safe_num_entry.get(), platform_entry.get(), platform_var.get()))
    start_button.grid(row=7, column=1, padx=10, pady=10)

    root.mainloop()

def on_start(account, password, idNumber, credit_num, safe_num, platform_url, platform):
    if not account or not password or not idNumber or not credit_num or not safe_num or not platform_url:
        messagebox.showwarning("Missing Info", "請填寫所有資訊！")
    else:
        start_thread(account, password, idNumber, credit_num, safe_num, platform_url, platform)

# 啟動 GUI
if __name__ == "__main__":
    create_gui()




# # 目標網站的URL
# driver.get('https://kklivetw.kktix.cc/events/9a55v8ea451hj3gfj')
# # 下一步按鈕
# next_step_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.outer-wrapper > div.content-wrapper > div > div.tickets > a")))
# next_step_button.click()

# # KKTIX會跳出提示登入或註冊窗，找登入按鈕
# login_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="guestModal"]/div[2]/div/div[3]/a[2]')))
# login_button.click()

# # 輸入帳號
# account_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "user_login")))
# account_input.send_keys(my_account)

# # 輸入密碼
# password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "user_password")))
# password_input.send_keys(my_password)

# # 按下登入鈕
# driver.find_element(By.CSS_SELECTOR, "#new_user > input.btn.btn.normal.btn-login").click()

# # 位置 & 張數
# ticket_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ticket_750358"]/div/span[4]/button[2]')))
# ticket_btn.click()
# ticket_btn.click()

# # 同意服務條款
# terms_input =  WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "person_agree_terms")))
# terms_input.click()

# # 下一步
# next_step_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#registrationsNewApp > div > div:nth-child(5) > div.form-actions.plain.align-center.register-new-next-button-area > button")))
# next_step_button.click()

# # Modal
# modal_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#infoModal > div.modal-dialog > div > div.modal-footer > button")))
# modal_button.click()

# # 確認座位
# confirm_set_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="registrationsShowApp"]/div[2]/div/div/div/ng-include[2]/div/div/div/div[3]/div/button')))
# confirm_set_button.click()

# # 完成選位 //*[@id="registrationsShowApp"]/div[2]/div/div/div/ng-include[2]/div/div/div/div[3]/div/div/div/div[1]/a
# finish_link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="registrationsShowApp"]/div[2]/div/div/div/ng-include[2]/div/div/div/div[3]/div/div/div/div[1]/a')))
# finish_link.click()


# input("press ENTER countine")

