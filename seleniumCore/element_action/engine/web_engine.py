from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class WebDriverEngine(object):
    web_driver: WebDriver = None

    """
    关于一些浏览器参数的使用
    .add_argument('--start-maximized') 最大化窗口运行
    .add_argument('--incognito') 使用无痕模式
    .add_argument('--disable-infobars') 禁止策略化
    .add_argument('--no-sandbox') 解决DevToolsActivePort文件不存在的报错
    .add_argument('window-size=1920x3000') 指定浏览器分辨率
    .add_argument('--disable-gpu') 谷歌禁用GPU加速
    .add_argument('--disable-javascript') 禁用javascript
    .add_argument('--incognito') 隐身模式（无痕模式）
    .add_argument('--start-maximized') 最大化运行（全屏窗口）,不设置，取元素会报错
    .add_argument('--hide-scrollbars') 隐藏滚动条, 应对一些特殊页面
    .add_argument('blink-settings=imagesEnabled=false') 不加载图片, 提升速度
    .add_argument('--headless') 浏览器不提供可视化页面（无头模式）. linux下如果系统不支持可视化不加这条会启动失败
    .add_argument('lang=en_US') 设置语言
    .add_argument('User-Agent=xxxxxx') 设置User-Agent属性
    .add_argument('--kiosk-printing') 默认打印机进行打印
    .binary_location = r"...\chrome.exe" 手动指定使用的浏览器位置
    .add_experimental_option("debuggerAddress", "127.0.0.1:9222") 调用原来的浏览器，不用再次登录即可重启
    .add_experimental_option('excludeSwitches', ['enable-automation']) 以开发者模式启动调试chrome，可以去掉提示受到自动软件控制
    .add_experimental_option('useAutomationExtension', False) 去掉提示以开发者模式调用
    .add_argument('–no-sandbox') # 沙盒模式运行
    .add_argument('–disable-setuid-sandbox') # 禁用沙盒
    .add_argument('–disable-dev-shm-usage') # 大量渲染时候写入/tmp而非/dev/shm
    .add_argument('–user-data-dir={profile_path}'.format(profile_path)) # 用户数据存入指定文件
    .add_argument('no-default-browser-check) # 不做浏览器默认检查
    .add_argument("–disable-popup-blocking") # 允许弹窗
    .add_argument("–disable-extensions") # 禁用扩展
    .add_argument("–ignore-certificate-errors") # 忽略不信任证书
    .add_argument("–no-first-run") # 初始化时为空白页面
    .add_argument('–start-maximized') # 最大化启动
    .add_argument('–disable-notifications') # 禁用通知警告
    .add_argument('–enable-automation') # 通知(通知用户其浏览器正由自动化测试控制)
    .add_argument('–disable-xss-auditor') # 禁止xss防护
    .add_argument('–disable-web-security') # 关闭安全策略
    .add_argument('–allow-running-insecure-content') # 允许运行不安全的内容
    .add_argument('–disable-webgl') # 禁用webgl
    .add_argument('–homedir={}') # 指定主目录存放位置
    .add_argument('–disk-cache-dir={临时文件目录}') # 指定临时文件目录
    .add_argument(‘disable-cache') # 禁用缓存
    设置prefs属性，屏蔽'保存密码'提示框
    prefs = {"":""}
    prefs["credentials_enable_service"] = False
    prefs["profile.password_manager_enabled"] = False
    .add_experimental_option("prefs", prefs)
    """

    def __init__(self):
        self.is_no_show_pic_param: dict = {'profile.default_content_setting_values': {'images': 2}}  # 不显示图片
        self.mobile_emulation: dict = {'deviceName': 'iPhone 8'}
        self.user_ag: str = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.24(0x1800182c) NetType/WIFI Language/zh_CN"

    def __set_edge_driver(self, driver_path, is_show_pic: bool, is_headless: bool, web_type: str) -> WebDriver:
        """
        设置浏览器驱动对象
        :param web_type: web or h5
        :param driver_path: 浏览器驱动文件
        :param is_show_pic: 是否显示图片
        :param is_headless: 是否启用无头模式
        :return:
        """
        options = webdriver.EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 关闭测试模式
        options.add_experimental_option('useAutomationExtension', False)  # 去掉提示以开发者模式调用
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        if web_type == "h5":
            options.add_argument('user-agent=%s' % self.user_ag)
            options.add_experimental_option('mobileEmulation', self.mobile_emulation)
        if is_show_pic is False:
            options.add_experimental_option('prefs', self.is_no_show_pic_param)
        if is_headless:
            # 无头模式
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        edge_driver = webdriver.Edge(executable_path=driver_path, options=options)
        if web_type == "wechat":
            # 模拟手机端微信
            edge_driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": self.user_ag, "platform": "iphone"})
        return edge_driver

    def __set_chrome_driver(self, driver_path, is_show_pic: bool, is_headless: bool, web_type: str) -> WebDriver:
        """
        设置浏览器驱动对象
        :param web_type: web or h5
        :param driver_path: 浏览器驱动文件
        :param is_show_pic: 是否显示图片
        :param is_headless: 是否启用无头模式
        :return:
        """
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 关闭测试模式
        options.add_experimental_option('useAutomationExtension', False)  # 去掉提示以开发者模式调用
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        if web_type in ("h5", 'wechat'):
            options.add_argument('user-agent=%s' % self.user_ag)
            options.add_experimental_option('mobileEmulation', self.mobile_emulation)
        if is_show_pic is False:
            options.add_experimental_option('prefs', self.is_no_show_pic_param)
        if is_headless:
            # 无头模式
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        chrome_driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
        if web_type == "wechat":
            # 模拟手机端微信
            chrome_driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": self.user_ag, "platform": "iphone"})
        return chrome_driver

    def __set_firefox_driver_driver(self, driver_path, is_headless: bool, web_type: str) -> WebDriver:
        """
        设置浏览器驱动对象
        :param web_type: web or h5 or wechat
        :param driver_path: 浏览器驱动文件
        :param is_headless: 是否启用无头模式
        :return:
        """
        options = webdriver.FirefoxOptions()
        if web_type in ("h5", "wechat"):
            options.add_argument('iPhone X')
        if is_headless:
            # 无头模式
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        firefox_driver = webdriver.Firefox(executable_path=driver_path, options=options)
        if web_type == "wechat":
            # 模拟手机端微信
            firefox_driver.command_executor('Network.setUserAgentOverride', {"userAgent": self.user_ag, "platform": "iphone"})
        return firefox_driver

    def get_fireFox(self, driver_path, driver_type: str = 'web', is_headless: bool = False, is_show_pic: bool = True):
        """
        打开edge浏览器
        :param driver_type: web or h5 or wechat
        :param driver_path: 驱动路径
        :param is_show_pic: 是否显示图片
        :param is_headless: 是否启用 无头模式
        :return: WebDriver
        """
        if self.__class__.web_driver is not None:
            return self.__class__.web_driver
        else:
            self.__class__.web_driver = self.__set_firefox_driver_driver(driver_path=driver_path, is_headless=is_headless,
                                                                         web_type=driver_type)
            return self.__class__.web_driver

    def get_edge(self, driver_path, driver_type: str = 'web', is_headless: bool = False, is_show_pic: bool = True):
        """
        打开edge浏览器
        :param driver_type: web or h5 or wechat
        :param driver_path: 驱动路径
        :param is_show_pic: 是否显示图片
        :param is_headless: 是否启用 无头模式
        :return: WebDriver
        """
        if self.__class__.web_driver is not None:
            return self.__class__.web_driver
        else:
            self.__class__.web_driver = self.__set_edge_driver(driver_path=driver_path, is_headless=is_headless,
                                                               is_show_pic=is_show_pic, web_type=driver_type)
            return self.__class__.web_driver

    def get_chrome(self, driver_path, driver_type: str = 'web', is_headless: bool = False, is_show_pic: bool = True):
        """
        打开edge浏览器
        :param driver_type: web or h5 or wechat
        :param driver_path: 驱动路径
        :param is_show_pic: 是否显示图片
        :param is_headless: 是否启用 无头模式
        :return: WebDriver
        """
        if self.__class__.web_driver is not None:
            return self.__class__.web_driver
        else:
            self.__class__.web_driver = self.__set_chrome_driver(driver_path=driver_path, is_headless=is_headless,
                                                                 is_show_pic=is_show_pic, web_type=driver_type)
            return self.__class__.web_driver
