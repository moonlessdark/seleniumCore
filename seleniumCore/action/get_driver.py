import unittest

from seleniumTools.HtmlReprot.HTMLTestReportCN import HTMLTestRunner
from seleniumCore.common.browser_by import BrowserBy as browserBy
from seleniumCore.element_action.engine.h5_engine import WebDriverEngine as h5web
from seleniumCore.element_action.engine.web_engine import WebDriverEngine as web
from seleniumCore.element_action.h5.base_page import BasePage as pageh5
from seleniumCore.element_action.web.base_page import BasePage as page


class getDriver(object):
    driver = None

    def __init__(self, driver_path: str, browser_type: browserBy, driver_type: str = 'web', is_headless: bool = False,
                 is_show_pic: bool = True):
        """
        驱动初始化
        :param driver_path: 浏览器驱动路径
        :param browser_type: 浏览器类型，传参  BrowserBy.Chrome
        :param driver_type: web 或者 h5 或者 wechat
        :param is_headless: 是否设置为无头浏览器，暂时只支持 wechat模式
        :param is_show_pic: 是否显示图片，暂时只支持 wechat模式
        :return:
        """
        if driver_type == 'web':
            if browser_type == 'chrome':
                self.__class__.driver = web().get_chrome(driver_path=driver_path)
            elif browser_type == 'firefox':
                self.__class__.driver = web().get_firefox(driver_path=driver_path)
        elif driver_path == "wechat":
            # 是否模拟微信,暂时只支持chrome模拟IPhone微信浏览器
            self.__class__.driver = h5web().get_chrome_wechat_browser(driver_path=driver_path, is_headless=is_headless,
                                                                      is_show_pic=is_show_pic)
        else:
            if browser_type == 'chrome':
                self.__class__.driver = h5web().get_chrome(driver_path=driver_path)
            elif browser_type == 'firefox':
                self.__class__.driver = h5web().get_firefox(driver_path=driver_path)
        self.__class__.driver.maximize_window()


class basePageByWeb(page):
    """
    web页面
    """

    def __init__(self):
        super(basePageByWeb, self).__init__()
        self.get_driver(getDriver.driver)


class basePageByH5(pageh5):
    """
    h5页面
    """

    def __init__(self):
        super(basePageByH5, self).__init__()
        self.get_driver(getDriver.driver)


class assertElement(unittest.TestCase):
    """
    unittest框架的断言
    """

    def __init__(self):
        super(assertElement, self).__init__()


class runSuitHtmlReport:
    def __init__(self, report_save_path: str, report_title: str):
        """
        生成测试报告，保存为html文件
        :param report_save_path: 存放测试报告的路径
        :param report_title: 测试报告标题
        """
        import time
        report_save_path = report_save_path + "/" if "/" not in report_save_path[-1:] else report_save_path
        html_file = report_save_path + "Report_" + time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time())) + \
                    "_HTMLtemplate.html"
        self.fp = open(html_file, "wb")
        self.title = report_title

    def runner_test_suit(self, test_case_path: str, pattern='*.py'):
        """
        执行test_suit并生成测试报告
        :param test_case_path: 存放该测试报告需要执行的测试用例的文件路径,该目录下不要放其他无关的 .py文件
        :param pattern: 文件格式，会匹配存放测试用例的文件名， *.py 表示匹配所有文件
        :return:
        """
        test_case_path = test_case_path + "/" if "/" not in test_case_path[-1:] else test_case_path
        runner = HTMLTestRunner(stream=self.fp, title=self.title, description=u"测试执行情况")
        runner.run(unittest.TestLoader().discover(test_case_path, pattern=pattern))
        self.fp.close()
