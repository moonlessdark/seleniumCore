from selenium import webdriver


class WebDriverEngine(object):
    driver = None

    def __set_chrome_driver(self, driver_path):
        """
        谷歌浏览器驱动
        :return:
        """
        chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument('--proxy-seleniumCore=http://127.0.0.1:8080')
        # chromeOptions.add_argument('--incognito')
        chromeOptions.add_argument('--disable-infobars')
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])

        return webdriver.Chrome(executable_path=driver_path, chrome_options=chromeOptions)

    def __set_firefox_driver(self, driver_path):
        """
        火狐浏览器的驱动
        :return:
        """
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
