from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import glob
import os
import datetime

def find_element(driver, locator):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

def click_element(driver, locator):
    element = find_element(driver, locator)
    element.click()

def wait_for_element(driver, locator):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

def scroll_to_position(driver, position):
    script = f"window.scrollTo(0, {position});"
    driver.execute_script(script)

def save_elements_to_file(elements, file_path):
    with open(file_path, 'w') as file:
        file.write('\n'.join(elements))

def remove_file(file_path):
    os.remove(file_path)

def main():
    url = 'https://spys.one/sslproxy/'
    firefox_options = Options()
    firefox_options.add_argument("-private")

    driver = webdriver.Firefox(options=firefox_options)
    driver.get(url)

    try:
        time.sleep(3)
        numbers = find_element(driver, (By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[3]/div[2]/button[1]/p'))
        numbers.click()
        time.sleep(3)
    except NoSuchElementException:
        try:
            time.sleep(5)
            numbers = find_element(driver, (By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[3]/div[2]/button[1]/p'))
            numbers.click()
            time.sleep(3)
        except NoSuchElementException:
            pass

    elements = []

    while True:
        element = driver.find_element(By.CSS_SELECTOR, 'option[selected]').text
        time.sleep(3)
        if element == "25":
            select_one_hundred = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/font/select[1]/option[3]')
            time.sleep(3)
            select_one_hundred.click()
            time.sleep(3)
        elif element == "100":
            for i in range(4, 103+1):
                element = driver.find_element(By.XPATH, f'/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[{i}]/td[1]').text
                elements.append(element)

            driver.quit()
            break

    output_file_path = 'output999.txt'
    save_elements_to_file(elements, output_file_path)
    print("Elements saved")

    # ========================2 часть скрипта============================

    time.sleep(1)
    with open(output_file_path, 'r') as f:
        lines = f.readlines()

    url_second = 'https://hidemy.name/ru/proxy-checker/'
    driver = webdriver.Firefox(options=firefox_options)
    driver.get(url_second)
    driver.maximize_window()
    time.sleep(1)

    input_text = find_element(driver, (By.XPATH, '//*[@id="f_in"]'))
    time.sleep(3)
    for line in lines:
        element = line.strip()
        input_text.send_keys(element + Keys.ENTER)

    scroll_height_script = "return Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);"
    scroll_height = driver.execute_script(scroll_height_script)

    # Вычисление позиции прокрутки
    scroll_position = int(scroll_height * 0.1)

    # Прокрутка страницы
    scroll_to_position(driver, scroll_position)

    time.sleep(5)
    btn_click = find_element(driver, (By.ID, 'chkb1'))
    time.sleep(1)
    btn_click.click()

    while True:
        percent = driver.find_element(By.ID, 's_persent').text
        percent = int(percent)
        if percent == 100 or percent == 101 or percent == 102:
            time.sleep(10)
            result = find_element(driver, (By.XPATH, '/html/body/div[1]/div[4]/div/div[3]/a[1]/span'))
            time.sleep(1)
            result.click()
            time.sleep(1)
        if percent == 100 or percent == 101 or percent == 102:
            driver.quit()
            break

    time.sleep(3)

    directory_path = r"изменить на директорию загрузок"
    file_prefix = "checker_2023-05-30_"
    file_extension = ".txt"

    current_time = datetime.datetime.now()
    three_minutes_ago = current_time - datetime.timedelta(minutes=3)
    pattern = f"{directory_path}{file_prefix}*{file_extension}"

    matching_files = glob.glob(pattern)
    result = None

    for file_path in matching_files:
        file_name = os.path.basename(file_path)
        file_creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        if file_creation_time >= three_minutes_ago:
            result = file_path
            break

    print(result)

    # изменить на путь где хранится файл
    file_path_remove = output_file_path
    remove_file(file_path_remove)

if __name__ == "__main__":
    main()
