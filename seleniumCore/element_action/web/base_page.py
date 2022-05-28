import time
import os.path
import json

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from seleniumCore.common.custom_error import *
from tools.logger.log import Logger

# 初始化log
logger = Logger(logger="BasePageByWeb").get_log()  # 这是全局变量,在这个类中只是单纯引用，并没有重新赋值，所以在调用的时候就不需要再申明了


class BasePage(object):
    """
    定义一个获取页面的基础类，方便调用，万物基于此处。
    """

    def __init__(self):
        # 这里先定义一下，方便其他地方使用
        self.driver = None
        self.__element = None

    def get_driver(self, webdriver):
        if webdriver is not None:
            self.driver = webdriver
        else:
            logger.error("浏览器驱动未初始化，请先初始化浏览器Driver")

    def get_url(self, url: str):
        self.driver.get(url=url)

    def get_url_cookie(self, url: str, cookie: dict):
        """
        :param url: https:www.baidu.com
        :param cookie: 随便传，传就意味着使用cookie。
        :return: 待cookie的url
        """

        self.driver.get(url)  # 需要先打开1个url，不然不能加载cookie

        if cookie is not None:

            for value in cookie:
                name = value['name']
                value = value['value']
                self.driver.add_cookie({'name': name, 'value': value})
                self.driver.refresh()
            logger.info("打开带cookie的URL")
        else:
            logger.info("没有cookie，直接打开url")

    # 获取截图
    def get_windows_img(self):
        """
        在这里把file_path这个参数写死，直接保存到项目的一个文件夹../screenshots/下
        """
        file_path = os.path.dirname(os.path.abspath('.'))
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        screen_name = file_path + rq + '.png'
        self.driver.get_screenshot_as_file(screen_name)
        logger.info("执行出错，进行截图!")

    def find_element_by(self, by: By, value: str):
        """
        :param by: By.ID
        :param value: 元素value
        :return:
        """
        if self.wait_element(by=by, value=value):
            try:
                self.__element = self.driver.find_element(by, value)
                return self.__element
            except TimeoutError:
                logger.error("元素 %s 未找到,请检查页面或者代码" % value)
                self.get_windows_img()
                return None

    # 输入文本框
    def send_text(self, by: By, value: str, text: str):
        """
        :param by: By.XPATH
        :param value: 元素值
        :param text: input输入的文字
        :return: 输入元素
        """
        el = self.find_element_by(by, value)
        el.clear()
        try:
            el.send_keys(text)
            logger.info("已完成 %s 的文字输入" % value)
        except SendKeyError(ele_value=value) as e:
            logger.error(e.message)
            self.get_windows_img()

    # 传输文件
    def send_file(self, by: By, value: str, file_path: str):
        """
        这是为了解决上传文件或者图片，方法参考：
        https://www.cnblogs.com/sylvia-liu/p/4431664.html
        感谢
        执行sendKeys的元素一定要符合input和 type="file"条件,否则就是你没找对上传文件的对象，会上传失败的。
        :param by: By.ID
        :param value: 元素value
        :param file_path: 文件路径
        :return: upload img/file
        """
        try:
            self.find_element_by(by, value).send_keys(file_path)
            logger.info("进行上传图片、文件操作")
        except SendKeyError(ele_value=value) as e:
            logger.error(e.message)
            self.get_windows_img()

    # 清除文本框
    def clear(self, by: By, value: str):
        """
        清空文本框
        :param by:  By.ID
        :param value: 元素value
        :return:
        """
        try:
            el = self.find_element_by(by, value)
            el.clear()
            logger.info("%s 文案清除成功！" % el.text)
        except ClearError(ele_value=value) as e:
            logger.error(e.message)
            self.get_windows_img()

    # 点击元素
    def click(self, by: By, value: str):
        """
        点击元素
        :param by: By.ID
        :param value: 元素value
        :return:
        """
        if self.wait_element(by, wait_type='click', value=value) is True:
            try:
                self.find_element_by(by, value).click()
                logger.info("元素 %s click成功" % value)
            except ClickError(ele_value=value) as e:
                logger.error(e.message)
                self.get_windows_img()
        else:
            logger.error('元素 %s 不可点击' % value)

    @staticmethod
    def sleep(seconds: int):
        """
        休眠
        :param seconds: 秒
        :return:
        """
        time.sleep(seconds)
        logger.info("休眠 %d 秒" % seconds)

    # 获取网页标题
    def get_page_title(self):
        title = self.driver.title
        if title is not None:
            logger.info("网页的标题(Title)是: %s" % title)
            return title
        else:
            logger.info("网页的标题(Title)是空的，压根没写")
        return None

    def get_text_by(self, by: By, value: str):
        """
        获取文本信息
        :param by: By.ID
        :param value: 元素value
        :return:
        """
        element = self.find_element_by(by=by, value=value)
        if element is not None:
            el_text = element.text
            return el_text
        return None

    def get_text_by_xpath(self, xpath: str):
        """

        :param xpath: xpath语法
        :return: 通过xpath获取到的text信息
        """
        return self.get_text_by(by=By.XPATH, value=xpath)

    def get_text_by_class_name(self, class_name_value: str):
        """

        :param class_name_value: class_name 内容
        :return:
        """
        return self.get_text_by(by=By.CLASS_NAME, value=class_name_value)

    def select_text_index_by_index(self, by: By, value: str, index: int):
        """
        下拉框“select”标签选择, 提供 Text 和 index 两种选择方式
        :param index: 第几个元素，从1开始？
        :param by: 元素类型
        :param value:
        :return:
        """
        el = self.find_element_by(by, value)
        if self.wait_element(by=by, value=value):  # 判断一下这个标签是不是可点击的状态
            try:
                Select(el).select_by_index(index)
                logger.info('通过 index %s 选择下拉框' % index)
            except FindError(ele_value=value) as e:
                logger.error(e.message)
        else:
            logger.error("未成功选择下拉框,下拉框不可点击")

    def select_text_index_by_text(self, by: By, value: str, text: str):
        """
        下拉框“select”标签选择, 提供 Text 和 index 两种选择方式
        :param text: 需要选择的文案
        :param by: 元素类型
        :param value:
        :return:
        """
        el = self.find_element_by(by, value)
        if self.wait_element(by=by, value=value, wait_type='click'):  # 判断一下这个标签是不是可点击的状态
            try:
                Select(el).select_by_visible_text(text)
                logger.info('通过文字 %s 选择下拉框' % value)
            except FindError(ele_value=value) as e:
                logger.error(e.message)
        else:
            logger.error("未成功选择下拉框,下拉框不可点击")

    def quit(self):
        try:
            self.driver.quit()
            logger.info('关闭浏览器 \n')
        except NameError as e:
            logger.info("未成功关闭浏览器,错误原因是：%s' \n" % e)

    def get_cookie(self):
        cookies = self.driver.get_cookies()
        cookie = json.dumps(cookies)
        logger.info('已获取登陆后的cookie: %s' % cookie)
        return cookie

    # -------------------------------------------------------------------------------------
    # ---------等待元素加载----------------------------------------------------------------
    # -------------------------------------------------------------------------------------
    def __expect_element(self, selector: str):
        """
        这个方法是搭配显性等待用的。逻辑参考了  find_element()
        :param selector:
        :return:
        """
        global locator

        if '=>' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split('=>')[0]
        selector_value = selector.split('=>')[1]
        if selector_by == 'id':
            locator = (By.ID, selector_value)
        elif selector_by == 'name':
            locator = (By.NAME, selector_value)
        elif selector_by == 'link_text':
            locator = (By.LINK_TEXT, selector_value)
        elif selector_by == 'partial_link_text':
            locator = (By.PARTIAL_LINK_TEXT, selector_value)
        elif selector_by == 'class_name':
            if ' ' in selector_value:  # 判断元素中是否包含空格，如果有的话就需要用CSS_SELECTOR方法来处理了
                selector_value_new = '.' + selector_value.replace(" ", ".")
                locator = (By.CSS_SELECTOR, selector_value_new)
            else:
                locator = (By.CLASS_NAME, selector_value)
        elif selector_by == 'xpath':
            locator = (By.XPATH, selector_value)
        elif selector_by == 'tag_name':
            locator = (By.TAG_NAME, selector_value)
        elif selector_by == 'selector':
            locator = (By.CSS_SELECTOR, selector_value)
        elif selector_by == 'js_class_name':
            locator = (By.CLASS_NAME, selector_value)
            selector_by = 'class_name'
        elif selector_by == 'js_id':
            locator = (By.ID, selector_value)
            selector_by = 'id'
        elif selector_by == 'jq_id':
            locator = (By.ID, selector_value)
            selector_by = 'id'
        elif selector_by == 'jq_class_name':
            locator = (By.CLASS_NAME, selector_value)
            selector_by = 'class_name'
        else:
            locator = ()
            logger.info('传参错误，请检查传参类型')
        return locator, selector_by, selector_value

    def wait_element(self, by: By, value: str, wait_type: str = 'visibility', wait_time: int = 10) -> bool:
        """
        显性等待
        :param by: By.ID
        :param value: 元素值
        :param wait_time: 等待时间，默认10秒
        :param wait_type: 元素应该处于什么状态
        等待的类型 ：
        存在   presence
        显示   visibility
        不显示但存在 invisibility
        可点击 click
        已选择 selected
        :return: 返回True或者False
        """
        locator = (by, value)
        try:
            if WebDriverWait(self.driver, wait_time, 2).until(ec.presence_of_element_located(locator)):
                if wait_type == 'visibility':
                    try:
                        WebDriverWait(self.driver, wait_time, 2).until(ec.visibility_of_element_located(locator))
                        return True
                    except VisibilityError(ele_value=value) as e:
                        logger.error(e.message)
                        return False
                elif wait_type == 'invisibility':
                    try:
                        WebDriverWait(self.driver, wait_time, 2).until(ec.invisibility_of_element_located(locator))
                        return True
                    except InVisibilityError(ele_value=value) as e:
                        logger.error(e.message)
                        return False
                elif wait_type == 'click':
                    try:
                        WebDriverWait(self.driver, wait_time, 2).until(ec.element_to_be_clickable(locator))
                        return True
                    except ClickError(ele_value=value) as e:
                        logger.error(e.message)
                        return False
                elif wait_type == 'selected':
                    """
                    select标签是否已选中，一般用在下来列表
                    """
                    try:
                        WebDriverWait(self.driver, wait_time, 1).until(ec.element_to_be_selected(locator))
                        return True
                    except SelectError(ele_value=value) as e:
                        logger.error(e.message)
                        return False
                else:
                    return True
        except Exception as e:
            logger.error('元素 ' + value + ' 未找到，请检查页面元素或者代码')
            return False

    def slide_to_the_element(self, by: By, value: str):
        """
        针对页面比较长有滚动条的情况，滑动滚动条到元素可见可操作的位置
        特殊处理
        :param by: By.ID
        :param value: 元素value
        :return:
        """
        el = self.find_element_by(by=by, value=value)
        try:
            self.driver.execute_script('arguments[0].scrollIntoView();', el)
            logger.info('滑动滚动条到 %s 处' % el.text)
        except FindError as e:
            logger.error(e.message)
            self.get_windows_img()

    def slide_to_the_bottom(self):
        """
        滑动到body的底部
        bottom：底部的意思(来自百度翻译)
        :return:
        """
        self.sleep(1)
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        self.sleep(1)
        logger.info('滑动滚动条到页面的底部，“其实是Body的底部，如果是元素溢出的话就没卵用了，嘤嘤嘤”')

    def save_cookie(self):
        """
        存储获取的页面cookie，只在登录使用
        :return:
        """
        cookies = self.get_cookie()
        return cookies

    def clear_cookie(self):
        """
        清除所有登录缓存
        :return:
        """
        try:
            self.driver.delete_all_cookies()
            logger.info('清除浏览器的所有cookie.打印一下清除cookie后的cookie : %s' % self.get_cookie())
        except ClearError as e:
            logger.info(e.message)

    def refresh(self):
        """
        刷新
        :return:
        """
        self.driver.refresh()
        self.sleep(2)
        logger.info('刷新一下页面')

    def check_page_complat_status(self):
        """
        检测页面是否完全加载完毕
        :return:
        """
        i = 0
        while i < 4:
            status = self.driver.execute_script('return document.readyState')
            logger.info("获取网页加载状态：%s" % status)
            if status == 'complete':
                logger.info("网页已经完成全部加载，可以进行下一步了")
                # return True  # 强行return直接中断循环
                break
            elif i == 4 & status != 'complete':
                logger.info("网页在10秒内依旧未完整加载，可能会影响元素的获取")
                # return False
                break
            i = i + 1
