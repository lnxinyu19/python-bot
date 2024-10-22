import time
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 2024-10-21
# 按下窗戶鍵(ctrl右邊 alt左邊) 輸入cmd後 enter >複製以下指令貼上 按下enter
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\新祐\Documents\google-profile" --profile-directory="Profile 1"
# 1. 拓元務必先登入會員
# 3. 執行指令: 底下的小視窗點一下 按下鍵盤的↑使用上一次的指令 按下後應該顯示 --->  python main.py 確認後按下enter


# 使用 Chrome 调试端口连接到已打开的浏览器
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"  # 调试端口的地址和端口号

# 创建一个新的 WebDriver 实例
driver = webdriver.Chrome(options=options)

# 此时，driver 已经连接到现有的 Chrome 窗口，并可以继续操作
driver.get("https://tixcraft.com/activity/game/24_dpr")
# # 12/5 購票按鈕
# # //*[@id="gameList"]/table/tbody/tr[1]/td[4]/button
# # 12/6 購票按鈕
# # //*[@id="gameList"]/table/tbody/tr[2]/td[4]/button
# # 12/7 購票按鈕
# # //*[@id="gameList"]/table/tbody/tr[3]/td[4]/button
# # 12/8 購票按鈕
# # //*[@id="gameList"]/table/tbody/tr[4]/td[4]/button
buy_date_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gameList"]/table/tbody/tr[1]/td[4]/button')))
driver.execute_script("arguments[0].click();", buy_date_button)


# driver.execute_script("window.scrollBy(0, 2000);")
# time.sleep(0.3)  # 延迟 1 秒，确保页面滚动完成

# # 搖滾區
# # //*[@id="group_0"]/li[1]
# # //*[@id="group_0"]/li[2]
# # 測試用
# select_seat = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//li[@class="select_form_a"]/a[contains(text(), "3600")]')))
select_seat = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "4880")]')))
# 滾動到元素可見位置
driver.execute_script("arguments[0].scrollIntoView();", select_seat)
driver.execute_script("arguments[0].click();", select_seat)
# select_seat.click()


# # 下拉選單 選擇張數
# 搖滾區應該是配合這個下拉選單 //*[@id="TicketForm_ticketPrice_01"]

ticket_dropdown = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "form-select")))
select = Select(ticket_dropdown)
# 選擇兩張
select.select_by_value("2")

driver.execute_script("window.scrollBy(0, 500);")
time.sleep(0.3)  # 延迟 1 秒，确保页面滚动完成

# term_checkbox = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="TicketForm_agree"]')))
# term_checkbox.click()


verify_code_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="TicketForm_verifyCode"]')))
driver.execute_script("arguments[0].focus();", verify_code_input)

WebDriverWait(driver, 60).until(
    lambda driver: verify_code_input.get_attribute('value') != ''
)
# //*[@id="form-ticket-ticket"]/div[4]/button[2]
# #form-ticket-ticket > div.mgt-32.col-lg-12.col-md-12.col-sm-12.col-xs-12.col-12.text-center > button.btn.btn-primary.btn-green
submit_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-green') and text()='確認張數']")))
submit_button.click()

input("press ENTER countine")

