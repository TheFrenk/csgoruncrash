import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--allow-profiles-outside-user-dir")
options.add_argument(r"user-data-dir=C:\Users\thefr\AppData\Local\Google\Chrome\User Data")
options.add_argument("--profile-directory=Profile 4")
options.add_argument("--mute-audio")

driver = webdriver.Chrome(options=options)

url = "https://csgo5.run/crash"

telegram_api_url = f'https://api.telegram.org/bot6898433254:AAHILffa6X-fcJGpp5MJfspOenyt03CEESo/sendMessage'
chat_id = '-4010718437'

driver.get(url)

wait = WebDriverWait(driver, 10)

def send_telegram_message(message):
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(telegram_api_url, params=params)

def send_telegram_dm(message):
    params = {
        'chat_id': '700535492',
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(telegram_api_url, params=params)

elements_below_threshold = []
last_element_info = None
notification_sent = False
count = 0

try:
    driver.find_element(By.XPATH, "//*[@id='crash']/div[3]/div[2]/div[1]/div[3]/button[2]").click()
    while True:
        new_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="crash"]/div[2]/div[2]/div[1]/a')))
        element_text = new_element.text
        element_url = new_element.get_attribute('href')
        element_crash_type = new_element.get_attribute('data-crash-type')
        if (element_text, element_url) != last_element_info:
            last_element_info = (element_text, element_url)
            print(f'Новый элемент: Текст - {element_text}, URL - {element_url}, Crash Type - {element_crash_type}')

            if count == 3:
                send_telegram_dm(f'После 3 Крашей выпал такой X: {element_text}')

            if element_crash_type == 'red':
                count += 1
                elements_below_threshold.append(last_element_info)
                notification_sent = False
            else:
                count = 0
                elements_below_threshold.clear()
                notification_sent = False

        time.sleep(1)

        if count >= 2 and not notification_sent:
            send_telegram_message(f'{count} краша подряд')
            notification_sent = True
        """
        if count >= 4:
            try:
                quality = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/button/div[2]').text
                price = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/button/div[5]').text
                title = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/button/div[3]').text
                subtitle = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/button/div[4]').text
                print(f"Ставлю {title} - {subtitle} {quality} Ценой в {price}")
                driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/button').click()
                driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/button').click()
            except Exception as e:
                print(f"Ошибка при нажатии кнопки: {e}")
        """

        time.sleep(1)

finally:
    driver.quit()
