from seleniumCore.common.browser_by import BrowserBy
from seleniumCore.element_action.engine.web_engine import WebDriverEngine as web
from seleniumCore.element_action.engine.h5_engine import WebDriverEngine as h5web
from seleniumCore.element_action.web.base_page import BasePage as page
from seleniumCore.element_action.h5.base_page import BasePage as pageh5


class getDriver(object):
    driver = None

    def __init__(self, driver_path: str, browser_type: BrowserBy, driver_type: str = 'web'):
        """
        驱动初始化
        :param driver_path: 浏览器驱动路径
        :param browser_type: 浏览器类型，传参  BrowserBy.Chrome
        :param driver_type: web 或者 h5
        :return:
        """
        if driver_type == 'web':
            if browser_type == 'chrome':
                self.__class__.driver = web().get_chrome(driver_path=driver_path)
            elif browser_type == 'firefox':
                self.__class__.driver = web().get_firefox(driver_path=driver_path)
        else:
            if browser_type == 'chrome':
                self.__class__.driver = h5web().get_chrome(driver_path=driver_path)
            elif browser_type == 'firefox':
                self.__class__.driver = h5web().get_firefox(driver_path=driver_path)


class basePageByWeb(page):
    def __init__(self):
        super(basePageByWeb, self).__init__()
        self.get_driver(getDriver.driver)


class basePageByH5(pageh5):
    def __init__(self):
        super(basePageByH5, self).__init__()
        self.get_driver(getDriver.driver)