import time

import fake_useragent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


def chromer(login: str, wordpass: str):
    """Авторизация для браузера Chrome"""
    user = fake_useragent.UserAgent().random  # Создаём фейкового юзера

    options = Options()  # Создаём параметры для большей реалистичности
    options.add_argument(f"--user-agent={user}")
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)  # Запускаем бота

    driver.get(
        'https://accounts.google.com/v3/signin/identifier?elo=1&ifkv=AdF4I755v4RPrRuYlFe6D5bYHOhIc4OQDa0WI_Vf9lv-5jGGpP1V9O8V3EAYZjumAigcA9nVP7dP&ddm=0&flowName=GlifWebSignIn&flowEntry=ServiceLogin&continue=https%3A%2F%2Faccounts.google.com%2FManageAccount%3Fnc%3D1')
    email = driver.find_element(value='identifierId')
    email.send_keys(login)

    nextBtn = driver.find_element(value='identifierNext')
    nextBtn.click()  # Отправка логина
    time.sleep(5)

    password = driver.find_element(by='name', value='Passwd')
    password.send_keys(wordpass)

    nextBtn = driver.find_element(value='passwordNext')
    nextBtn.click()  # Отправка пароля
    time.sleep(20)

    driver.get_cookies()
    driver.get("https://takeout.google.com/settings/takeout/custom/photos?utm_medium=organic-nav&utm_source=google-photos&hl=ru")
    time.sleep(5)

    nextBtn = driver.find_element(by='xpath', value="//*[text() = 'Продолжить']")
    nextBtn.click()
    time.sleep(3)

    select = Select(driver.find_element(By.CSS_SELECTOR, value="[aria-label='File size']"))
    select.select_by_visible_text("50 ГБ")
    time.sleep(3)

    nextBtn = driver.find_element(by='xpath', value="//*[text() = 'Создать экспорт']")
    nextBtn.click()  # Нажимаем необходимые кнопки, тк форма всегда одинаковая
    time.sleep(3)

    driver.delete_all_cookies()
    driver.quit()


if __name__ == '__main__':
    path_to_chrome_driver = 'apath/awebdriver.exe'
