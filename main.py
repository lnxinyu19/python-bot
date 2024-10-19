import time
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# cmd 先啟動一個視窗
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\新祐\Documents\google-profile" --profile-directory="Profile 1"

# 使用 Chrome 调试端口连接到已打开的浏览器
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"  # 调试端口的地址和端口号

# 创建一个新的 WebDriver 实例
driver = webdriver.Chrome(options=options)

# 此时，driver 已经连接到现有的 Chrome 窗口，并可以继续操作
driver.get("https://tixcraft.com/activity/game/25_casty")

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


driver.execute_script("window.scrollBy(0, 500);")
time.sleep(0.3)  # 延迟 1 秒，确保页面滚动完成

# # 搖滾區
# # //*[@id="group_0"]/li[1]
# # //*[@id="group_0"]/li[2]
# # 測試用
select_seat = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//li[@class="select_form_a"]/a[contains(text(), "3280")]')))
# driver.execute_script("arguments[0].click();", select_seat)
select_seat.click()


# # 下拉選單 選擇張數
# 搖滾區應該是配合這個下拉選單 //*[@id="TicketForm_ticketPrice_01"]

ticket_dropdown = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "form-select")))
select = Select(ticket_dropdown)
# 選擇兩張
select.select_by_value("2")

driver.execute_script("window.scrollBy(0, 500);")
time.sleep(0.3)  # 延迟 1 秒，确保页面滚动完成

term_checkbox = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="TicketForm_agree"]')))
term_checkbox.click()


verify_code_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="TicketForm_verifyCode"]')))
driver.execute_script("arguments[0].focus();", verify_code_input)



# try:
#     current_directory = os.getcwd()

#     print("当前工作目录是：", current_directory)

#     # 等待验证码图片加载出来
#     captcha_image_element = WebDriverWait(driver, 20).until(
#         EC.visibility_of_element_located((By.ID, "TicketForm_verifyCode-image"))
#     )

#     driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", captcha_image_element)
#     time.sleep(1)  # 延迟 1 秒，确保页面滚动完成

#     # 截取验证码图片并保存
#     captcha_image_path = 'captcha.png'
#     captcha_image_element.screenshot(captcha_image_path)
#     print(f"验证码图片已保存为 '{captcha_image_path}'")

#     # 检查图片是否成功保存
#     if not os.path.exists(captcha_image_path):
#         raise Exception("验证码图片保存失败，请检查保存路径")

#     # 使用 PIL 打开图片
#     captcha_image = Image.open(captcha_image_path)

#     # 图像灰度化
#     captcha_image = captcha_image.convert('L')

#     # 使用中值滤波去噪
#     captcha_image = captcha_image.filter(ImageFilter.MedianFilter(size=3))

#     # 二值化处理
#     threshold_value = 140
#     captcha_image = captcha_image.point(lambda x: 0 if x < threshold_value else 255)

#     # 图像锐化
#     captcha_image = captcha_image.filter(ImageFilter.SHARPEN)

#     # 保存预处理后的图片，方便检查（可选）
#     processed_image_path = 'captcha_processed.png'
#     captcha_image.save(processed_image_path)
#     print(f"预处理后的验证码图片已保存为 '{processed_image_path}'")

#     if os.path.exists(captcha_image_path):
#         print(f"验证码图片已成功保存为：{os.path.join(current_directory, captcha_image_path)}")
#     else:
#         print("验证码图片保存失败，请检查路径")

#     # 使用 Tesseract OCR 识别验证码
#     captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 7 -c tessedit_char_whitelist=abcdedfghijklmnopqrstuvwxyz')

#     # 打印识别到的验证码内容
#     print(f"识别到的验证码是: {captcha_text.strip()}")

# except Exception as e:
#     print(f"发生了错误: {e}")

input("press ENTER countine")

