from selenium import webdriver


class WebDriverEngine(object):

    driver = None

    def __set_chrome_driver(self, driver_path):
        """
        谷歌浏览器驱动
        :return:
        """
        mobile_emulation = {'deviceName': 'iPhone X'}
        options = webdriver.ChromeOptions()
        options.add_experimental_option('mobileEmulation', mobile_emulation)
        return webdriver.Chrome(executable_path=driver_path, options=options)

    def __set_firefox_driver(self, driver_path):
        """
        火狐浏览器的驱动
        :return:
        """
        mobile_emulation = 'iPhone X'
        options = webdriver.FirefoxOptions()
        options.add_argument(mobile_emulation)
        return webdriver.Firefox(executable_path=driver_path)

    def get_chrome(self, driver_path=None):
        """
        打开谷歌浏览器
        :param driver_path: 驱动路径
        :return: dirver
        """
        if self.__class__.driver is not None:
            return self.__class__.driver
        else:
            self.__class__.driver = self.__set_chrome_driver(driver_path)
            return self.__class__.driver

    def get_firefox(self, driver_path):
        """
        打开火狐浏览器
        :param driver_path: 驱动路径
        :return: dirver
        """
        if self.__class__.driver is not None:
            return self.__class__.driver
        else:
            self.__class__.driver = self.__set_firefox_driver(driver_path)
            return self.__class__.driver
