from selenium import webdriver


class WebDriverEngine(object):
    driver = None

    def __set_chrome_wechat_broswer_driver(self, driver_path: str, is_headless: bool = False, is_show_pic: bool = True):
        """
        以谷歌浏览器模拟微信内置浏览器
        :param driver_path: 谷歌浏览器的驱动文件路径
        :param is_headless: 是否启用无头模式
        :param is_show_pic: 是否显示图片
        :return:
        """
        mobile_emulation = {'deviceName': 'iPhone 8'}
        options = webdriver.ChromeOptions()
        user_ag: str = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.24(0x1800182c) NetType/WIFI Language/zh_CN"
        options.add_argument('user-agent=%s' % user_ag)
        options.add_experimental_option('mobileEmulation', mobile_emulation)
        if is_show_pic is False:
            pref = {
                # 不显示图片
                'profile.default_content_setting_values': {
                    'images': 2
                }
            }
            options.add_experimental_option('prefs', pref)
        if is_headless is True:
            # 无头模式
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        mobile_driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
        mobile_driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_ag, "platform": "iphone"})
        return mobile_driver

    def __set_chrome_driver(self, driver_path: str):
        """
        谷歌浏览器驱动
        :return:
        """
        mobile_emulation = {'deviceName': 'iPhone 8'}
        options = webdriver.ChromeOptions()
        options.add_experimental_option('mobileEmulation', mobile_emulation)
        mobile_driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
        return mobile_driver

    def __set_firefox_driver(self, driver_path):
        """
        火狐浏览器的驱动
        :return:
        """
        mobile_emulation = 'iPhone X'
        options = webdriver.FirefoxOptions()
        options.add_argument(mobile_emulation)
        return webdriver.Firefox(executable_path=driver_path)

    def get_chrome(self, driver_path: str):
        """
        打开谷歌浏览器
        :param wechat_emulation: 是否模拟微信
        :param driver_path: 驱动路径
        :return: driver
        """
        if self.__class__.driver is not None:
            return self.__class__.driver
        else:
            self.__class__.driver = self.__set_chrome_driver(driver_path)
            return self.__class__.driver

    def get_chrome_wechat_browser(self, driver_path: str, is_headless: bool = False, is_show_pic: bool = True):
        """
        以谷歌浏览器模拟微信内置浏览器
        :param driver_path: 谷歌浏览器的驱动文件路径
        :param is_headless: 是否启用无头模式 True是开启
        :param is_show_pic: 是否显示图片 True是显示
        :return:
        """
        if self.__class__.driver is not None:
            return self.__class__.driver
        else:
            self.__class__.driver = self.__set_chrome_wechat_broswer_driver(driver_path, is_headless, is_show_pic)
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
