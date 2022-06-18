import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# путь: python -m pytest -v --driver Chrome --driver-path tests/chromedriver.exe tests/test_task_25_5_1.py

# pytest.driver = webdriver.Chrome() НЕ РАБОТАЕТ !!!
# ОШИБКА: Cannot find reference 'driver' in '__init__.py'

driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')


@pytest.fixture(autouse=True)
def testing():
    # Переходим на страницу авторизации
    driver.get('http://petfriends1.herokuapp.com/login')
    yield
    driver.quit()


def test_show_all_pets():
    # Вводим email
    driver.find_element_by_id('email').send_keys('adenisov.pro@gmail.com')
    # Вводим пароль.
    driver.find_element_by_id('pass').send_keys('Andrey67')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element_by_tag_name('h1').text == "PetFriends"


def test_attributes():
    driver.get('http://petfriends1.herokuapp.com/all_pets')
    images = WebDriverWait(driver, 10).until(
      ec.presence_of_element_located((By.CSS_SELECTOR, '.card-deck .card-img-top')))
    names = WebDriverWait(driver, 10).until(ec.presence_of_element_located(
        (By.CSS_SELECTOR, '.card-deck .card-title')
    ))
    descriptions = WebDriverWait(driver, 10).until(
      ec.presence_of_element_located((By.CSS_SELECTOR, '.card-deck .card-text')))
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


# проверка по заданию 25.3.1
def test_my_pets():
    # Вводим email
    driver.find_element_by_id('email').send_keys('adenisov.pro@gmail.com')
    # Вводим пароль
    driver.find_element_by_id('pass').send_keys('Andrey67')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element_by_css_selector('button[type="submit"]').click()
    # Заходим на страницу своих питомцев
    driver.find_element_by_css_selector("div#navbarNav > ul > li > a").click()

    assert driver.find_element_by_tag_name('h2').text == "Andrey Denisov"
    # Выбираем моих питомцев
    del_pet = driver.find_elements_by_xpath('//td[@class="smart_cell"]')
    # Выбираем все элементы фотографий питомцев
    images = driver.find_elements_by_xpath('//th/img')
    # Назначаем переменную для подсчёта количества питомцев с фотографией
    photo_presence = 0
    driver.implicitly_wait(10)
    # Через проверку у всех питомцев, что attribute 'src' не пустое значение, определяем
    # количество питомцев с фотографией
    for i in range(len(del_pet)):
        if images[i].get_attribute('src') != '':
            photo_presence += 1
        else:
            photo_presence = photo_presence
    # Проверяем, что половина всех питомцев имеет фотографию
    assert photo_presence >= (len(del_pet) / 2)
    # У всех питомцев есть имя, возраст и порода.
    assert driver.find_element_by_xpath(
      '//*[@id="all_my_pets"]/table/tbody/tr[1]'
      and '//*[@id="all_my_pets"]/table/tbody/tr[2]'
      and '//*[@id="all_my_pets"]/table/tbody/tr[3]'
    ).text != ''
    # У всех питомцев разные имена, породы и возраст.
    name_breed_age1 = driver.find_element_by_xpath(
      '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[1]'
      and '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[2]'
      and '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[3]'
    )
    name_breed_age2 = driver.find_element_by_xpath(
      '//*[@id="all_my_pets"]/table/tbody/tr[2]/td[1]'
      and '//*[@id="all_my_pets"]/table/tbody/tr[2]/td[2]'
      and '//*[@id="all_my_pets"]/table/tbody/tr[2]/td[3]'
    )
    name_breed_age3 = driver.find_element_by_xpath(
      '//*[@id="all_my_pets"]/table/tbody/tr[3]/td[1]'
      and '//*[@id="all_my_pets"]/table/tbody/tr[3]/td[2]'
      and '//*[@id="all_my_pets"]/table/tbody/tr[3]/td[3]'
    )
    assert name_breed_age1 != name_breed_age2 != name_breed_age3