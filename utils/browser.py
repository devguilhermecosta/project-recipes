from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver import ChromeOptions
from time import sleep
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent  # raiz do projeto
CHROMEDRIVER_NAME = 'chromedriver.exe'  # passamos o nome do driver a ser usado  # noqa: E501
CHROMEDRIVER_PATH = str(ROOT_PATH / 'bin' / CHROMEDRIVER_NAME)  # passamos o caminho do driver  # noqa: E501
# para executar em outro pc basta alterar a variável CHROMEDRIVER_NAME, se necessário  # noqa: E501


def make_chrome_browser(*options) -> WebDriver:
    chrome_options: ChromeOptions = webdriver.ChromeOptions()

    for option in options:
        chrome_options.add_argument(option)

    chrome_service: Service = Service(executable_path=CHROMEDRIVER_PATH)
    browser: WebDriver = webdriver.Chrome(service=chrome_service,
                                          options=chrome_options,
                                          )

    return browser


if __name__ == '__main__':
    browser: WebDriver = make_chrome_browser('--headless')
    browser.get('https://www.google.com')
    sleep(2)
    browser.quit()
