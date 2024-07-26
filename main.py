import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import fake_useragent


def chromer(login: str, wordpass: str):
    """Авторизация для браузера Chrome"""
    user = fake_useragent.UserAgent().random

    options = Options()
    options.add_argument(f"--user-agent={user}")
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)

    driver.get(
        'https://accounts.google.com/v3/signin/identifier?elo=1&ifkv=AdF4I755v4RPrRuYlFe6D5bYHOhIc4OQDa0WI_Vf9lv-5jGGpP1V9O8V3EAYZjumAigcA9nVP7dP&ddm=0&flowName=GlifWebSignIn&flowEntry=ServiceLogin&continue=https%3A%2F%2Faccounts.google.com%2FManageAccount%3Fnc%3D1')
    email = driver.find_element(value='identifierId')
    email.send_keys(login)

    nextBtn = driver.find_element(value='identifierNext')
    nextBtn.click()
    time.sleep(5)

    password = driver.find_element(by='name', value='Passwd')
    password.send_keys(wordpass)

    nextBtn = driver.find_element(value='passwordNext')
    nextBtn.click()
    time.sleep(20)


path_to_chrome_driver = 'apath/awebdriver.exe'

