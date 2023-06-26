# Для хранения часто употребимых фикстур и хранения глобальных настроек нужно использовать файл conftest.py,
# который должен лежать в директории верхнего уровня в вашем проекте с тестами.
# Можно создавать дополнительные файлы conftest.py в других директориях,
# но тогда настройки в этих файлах будут применяться только к тестам в под-директориях.

import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='Chrome',
                     help="Choose browser: Chrome or firefox")
    parser.addoption('--language', action='store', default='en', help='select language i.e. ru/en/es/ etc')


@pytest.fixture(scope="function")
def browser(request):
    print("\nstart browser for test..")
    browser_name = request.config.getoption('browser_name')
    user_language = request.config.getoption('language')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
    ff_profile = webdriver.FirefoxProfile()
    ff_profile.set_preference("intl.accept_languages", user_language)
    browser = None
    if browser_name in ('Chrome', 'chrome'):
        print('Launch Chrome browser ..........')
        browser = webdriver.Chrome(options=chrome_options)
    elif browser_name in ('Firefox', 'firefox'):
        print('Launch Firefox browser ..........')
        browser = webdriver.Firefox(firefox_profile=ff_profile)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser
    print("\nquit browser..")
    browser.quit()
