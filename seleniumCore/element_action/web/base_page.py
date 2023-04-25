import time
import os.path
import json

from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from seleniumTools.logger.log import Logger
from selenium.webdriver.common.action_chains import ActionChains

# 初始化log
logger = Logger(logger="BasePageByWeb")  # 这是全局变量,在这个类中只是单纯引用，并没有重新赋值，所以在调用的时候就不需要再申明了


class BasePage:
    """
    定义一个获取页面的基础类，方便调用，万物基于此处。
    """

    def __init__(self):
        # 这里先定义一下，方便其他地方使用
        self.driver: WebDriver = None
        self.__element: WebElement = None
        self.is_cap: bool = False  # 遇到错误时是否截图

    @staticmethod
    def printf_log() -> Logger:
        """
        打印日志
        :return:
        """
        return logger

    def get_driver(self, webdriver: WebDriver):
        """
        给元素处理对象赋值一个driver
        :param webdriver:
        :return:
        """
        if webdriver is not None:
            self.driver = webdriver
        else:
            logger.error("浏览器驱动未初始化，请先初始化浏览器Driver")

    def get_url(self, url: str):
        """
        打开浏览器
        :param url:
        :return:
        """
        self.driver.get(url=url)
        logger.info("打开URL: %s" % url)

    def get_url_and_set_cookie(self, url: str, cookie: dict):
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
        if self.is_cap is True:
            file_path = os.path.dirname(os.path.abspath('.'))
            rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
            screen_name = file_path + rq + '.png'
            self.driver.get_screenshot_as_file(screen_name)
            logger.info("执行出错，进行截图!")

    def find_element_by(self, by: By, value: str) -> WebElement:
        """
        查找元素
        :param by: 元素类型
        :param value: 元素value
        :return:
        """
        if self.wait_element(by=by, value=value):
            try:
                return self.driver.find_element(by, value)
            except Exception as e:
                logger.error("元素 %s 处理失败,错误信息: %s" % (value, str(e)))
                self.get_windows_img()

    def find_elements_by(self, by: By, value: str) -> list[WebElement]:
        """
        查询元素集合
        例如： find_elements(By.CSS_SELECTOR, ".el-select-dropdown__item")
        :param by: 元素类型
        :param value: 元素值
        :return:
        """
        try:
            return self.driver.find_elements(by, value)
        except Exception as e:
            logger.error("元素 %s 处理失败,错误信息: %s" % (value, str(e)))
            self.get_windows_img()

    def input_str(self, by: By, value: str, text: str):
        """
         输入文本框
        :param by: By.XPATH
        :param value: By对应的类型值
        :param text: input输入的文字
        :return: 输入元素
        """
        el = self.find_element_by(by, value)
        if el is not None:
            el.clear()
            try:
                el.send_keys(text)
                logger.info("已完成 %s 的文字输入" % value)
            except Exception as e:
                logger.error("元素 %s 处理失败,错误信息: %s" % (value, str(e)))
                self.get_windows_img()

    def send_file(self, by: By, value: str, file_path: str):
        """
        这是为了解决上传文件或者图片，方法参考：
        https://www.cnblogs.com/sylvia-liu/p/4431664.html
        感谢
        执行sendKeys的元素一定要符合input和 type="file"条件,否则就是你没找对上传文件的对象，会上传失败的。
        :param by: By.ID
        :param value: By对应的类型值
        :param file_path: 文件路径
        :return: upload img/file
        """
        file = self.find_element_by(by, value)
        if file is not None:
            try:
                file.send_keys(file_path)
                logger.info("进行上传图片、文件操作")
            except Exception as e:
                logger.error("元素 %s 处理失败,错误信息: %s" % (value, str(e)))
                self.get_windows_img()

    # 清除文本框
    def clear(self, by: By, value: str):
        """
        清空文本框
        :param by:  By.ID
        :param value: By对应的类型值
        :return:
        """
        el = self.find_element_by(by, value)
        if el is not None:
            try:
                el.clear()
                logger.info("%s 文案清除成功！" % el.text)
            except Exception as e:
                logger.error("元素 %s 处理失败,错误信息: %s" % (value, str(e)))
                self.get_windows_img()

    # 点击元素
    def click(self, by: By, value: str):
        """
        点击元素
        :param by: By.ID
        :param value: By对应的类型值
        :return:
        """
        if self.wait_element(by, wait_type='click', value=value):
            try:
                self.find_element_by(by, value).click()
                logger.info("元素 %s click成功" % value)
            except Exception as e:
                logger.error("元素 %s 处理失败,错误信息: %s" % (value, str(e)))
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
    def get_page_title(self) -> str:
        """
        获取网页的标题
        :return:
        """
        title = self.driver.title
        if title is not None:
            logger.info("网页的标题(Title)是: %s" % title)
            return title
        else:
            logger.info("网页的标题(Title)是空的，压根没写")
        return ""

    def get_text_by(self, by: By, value: str) -> str:
        """
        获取文本信息
        :param by: By.ID
        :param value: By对应的类型值
        :return:
        """
        element = self.find_element_by(by=by, value=value)
        if element is not None:
            el_text = element.text
            return el_text
        return ""

    def get_text_by_xpath(self, xpath: str) -> str:
        """
        通过xpath来获取文字信息
        :param xpath: xpath语法
        :return: 通过xpath获取到的text信息
        """
        return self.get_text_by(by=By.XPATH, value=xpath)

    def get_text_by_class_name(self, class_name_value: str) -> str:
        """
        通过元素的class_name来获取文字信息
        :param class_name_value: class_name 内容
        :return:
        """
        return self.get_text_by(by=By.CLASS_NAME, value=class_name_value)

    def select_text_by_index(self, by: By, value: str, index: int):
        """
        下拉框“select”标签选择, 提供 Text 和 index 两种选择方式
        :param index: 第几个元素，从1开始？
        :param by: 元素类型
        :param value: By对应的类型值
        :return:
        """
        el = self.find_element_by(by, value)
        if self.wait_element(by=by, value=value):  # 判断一下这个标签是不是可点击的状态
            try:
                Select(el).select_by_index(index)
                logger.info('通过 index %s 选择下拉框' % index)
            except Exception as e:
                logger.error("元素 %s 处理失败,错误信息: %s" % (value, str(e)))
        else:
            logger.error("未成功选择下拉框,下拉框不可点击")

    def select_text_by_text(self, by: By, value: str, text: str):
        """
        下拉框“select”标签选择, 提供 Text 和 index 两种选择方式
        :param text: 需要选择的文案
        :param by: 元素类型
        :param value: By对应的类型值
        :return:
        """
        el = self.find_element_by(by, value)
        if self.wait_element(by=by, value=value, wait_type='click'):  # 判断一下这个标签是不是可点击的状态
            try:
                Select(el).select_by_visible_text(text)
                logger.info('通过文字 %s 选择下拉框' % value)
            except Exception as e:
                logger.error("元素 %s 处理失败,错误信息: %s" % (value, str(e)))
        else:
            logger.error("未成功选择下拉框,下拉框不可点击")

    def select_ul_li_by_text(self, by: By, value: str, text: str):
        """
        通过ul标签下到li标签选择元素
        :param by: 查询ul标签到
        :param value: 查询ul到值
        :param text:
        :return:
        """
        is_click: bool = False
        el_list = self.find_elements_by(by, value)
        for i in range(len(el_list)):
            if el_list[i].text == text:
                while True:
                    if el_list[i].is_displayed():
                        el_list[i].click()
                        logger.info("已选择下拉框 %s" % text)
                        is_click = True
                        break
                break
        if is_click is False:
            logger.info("未找到对应的下拉框 %s" % value)

    def quit(self):
        """
        关闭浏览器
        :return:
        """
        try:
            self.driver.quit()
            logger.info('关闭浏览器 \n')
        except NameError as e:
            logger.info("未成功关闭浏览器,错误原因是：%s' \n" % e)

    def get_cookie(self) -> str:
        """
        获取浏览器cookie,已json格式保存
        :return:
        """
        cookies = self.driver.get_cookies()
        cookie = json.dumps(cookies)
        logger.info('已获取登陆后的cookie: %s' % cookie)
        return cookie

    def wait_element(self, by: By, value: str, wait_type: str = 'visibility', wait_time: int = 10) -> bool:
        """
        显性等待
        :param by: By.ID
        :param value: By对应的类型值
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
        wait_ele = (by, value)
        try:
            if WebDriverWait(self.driver, wait_time, 2).until(ec.presence_of_element_located(wait_ele)):
                if wait_type == 'visibility':
                    WebDriverWait(self.driver, wait_time, 2).until(ec.visibility_of_element_located(wait_ele))
                    return True
                elif wait_type == 'invisibility':
                    WebDriverWait(self.driver, wait_time, 2).until(ec.invisibility_of_element_located(wait_ele))
                    return True
                elif wait_type == 'click':
                    WebDriverWait(self.driver, wait_time, 2).until(ec.element_to_be_clickable(wait_ele))
                    return True
                elif wait_type == 'selected':
                    """
                    select标签是否已选中，一般用在下来列表
                    """
                    WebDriverWait(self.driver, wait_time, 1).until(ec.element_to_be_selected(wait_ele))
                    return True
                else:
                    return False
        except Exception:
            logger.error("在当前页面未找到元素 %s, 可能页面还未渲染或查找 value 错误" % value)
            return False

    def check_element_status(self, by: By, value: str, element_status: str) -> bool:
        """
        检查元素当前状态
        :param by:
        :param value:
        :param element_status: click, select
        :return:
        """
        el = self.find_element_by(by, value)
        if el is not None:
            if element_status == "click":
                if el.is_enabled():
                    return True
            elif element_status == "selected":
                if el.is_selected():
                    return True
            elif element_status == "visible":
                if el.is_displayed():
                    return True
        return False

    def slide_to_the_element(self, by: By, value: str):
        """
        针对页面比较长有滚动条的情况，滑动滚动条到元素可见可操作的位置
        特殊处理
        :param by: By.ID
        :param value: By对应的类型值
        :return:
        """
        el = self.find_element_by(by=by, value=value)
        try:
            self.driver.execute_script('arguments[0].scrollIntoView();', el)
            logger.info('滑动滚动条到 %s 处' % el.text)
        except Exception as e:
            logger.error("元素 %s 处理失败,错误信息: %s" % (value, str(e)))
            self.get_windows_img()

    def slide_to_the_bottom(self):
        """
        滑动到body的底部
        bottom：底部的意思(来自百度翻译)
        :return:
        """
        time.sleep(1)
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        logger.info('滑动滚动条到页面的底部，“其实是Body的底部，如果是元素溢出的话就没卵用了，嘤嘤嘤”')

    def clear_cookie(self):
        """
        清除所有登录缓存
        :return:
        """
        try:
            self.driver.delete_all_cookies()
            logger.info('清除浏览器的所有cookie.打印一下清除cookie后的cookie : %s' % self.get_cookie())
        except Exception as e:
            logger.error("cookie清除处理失败,错误信息: %s" % str(e))

    def refresh(self):
        """
        刷新
        :return:
        """
        self.driver.refresh()
        time.sleep(2)
        logger.info('刷新一下页面')

    def check_page_complete_status(self, time_out: int = 10) -> bool:
        """
        检测页面是否完全加载完毕
        :return:
        """
        is_ok: bool = False
        for i in range(time_out):
            status = self.driver.execute_script('return document.readyState')
            logger.info("获取网页加载状态：%s" % status)
            if status == 'complete':
                logger.info("网页已经完成全部加载，可以正常的进行下一步了")
                is_ok = True
                return True
        if is_ok is False:
            logger.warning("页面元素在 %d 秒内未全部加载，可能会影响执行结果" % time_out)
            return False

    def get_attribute_by(self, by: By, value: str, attribute_name: str) -> str:
        """
        获取元素属性值
        使用例子：
        返回某个元素的class属性
        self.driver.find_element_by(by=By.XPATH, value="//div[@id="name"]/a").get_attribute(class)
        :param by: 需要获取到元素类型
        :param value: 需要获取到值
        :param attribute_name: 该元素到属性类型
        :return:
        """
        el = self.find_element_by(by, value)
        return self.get_attribute(el, attribute_name)

    @staticmethod
    def get_attribute(element_obj: WebElement, attribute_name: str) -> str:
        """
        获取元素属性值
        使用例子：
        返回某个元素的class属性
        result = self.driver.find_element_by(by=By.XPATH, value="//div[@id="name"]/a")
        get_attribute(element_obj=result, attribute_name='class')

        参考：https://blog.csdn.net/xcntime/article/details/120315806

        :param element_obj: 已经通过find方法获取到属性对象
        :param attribute_name: 这个元素要获取的属性
        :return:
        """
        return element_obj.get_attribute(attribute_name)

    def close_alert_tips(self):
        """
        点击 alert 窗口
        :return:
        """
        try:
            if WebDriverWait(self.driver, 10, 0.5).until(ec.alert_is_present()):
                self.driver.switch_to.alert.accept()
        except Exception as e:
            logger.info("alert窗口未检测到或未成功关闭,错误信息:%s" % str(e))

    def mouse_click_element(self, by: By, value: str):
        """
        鼠标点击元素
        :param by:
        :param value:
        :return:
        """
        el = self.find_element_by(by, value)
        if el is not None:
            try:
                ActionChains(self.driver).click(el).perform()
                logger.error("鼠标已经点击元素 %s" % value)
            except Exception as e:
                logger.error("元素 %s 点击失败,错误信息:%s" % (value, str(e)))

    def mouse_click_and_hold(self, by: By, value: str):
        """
        鼠标点击元素并按住不释放
        :param by:
        :param value:
        :return:
        """
        el = self.find_element_by(by, value)
        if el is not None:
            try:
                ActionChains(self.driver).click_and_hold(el).perform()
                logger.error("鼠标已经点击并按住元素 %s" % value)
            except Exception as e:
                logger.error("元素 %s 点击失败,错误信息:%s" % (value, str(e)))

    def mouse_move_to_element(self, by: By, value: str):
        """
        鼠标移动到元素处
        :param by:
        :param value:
        :return:
        """
        el = self.find_element_by(by, value)
        if el is not None:
            try:
                ActionChains(self.driver).move_to_element(el).perform()
                logger.error("鼠标已经移动至元素 %s" % value)
            except Exception as e:
                logger.error("鼠标移动至元素 %s 时失败,错误信息:%s" % (value, str(e)))

    @staticmethod
    def __js_find_element(by: By, value: str, index: int = 0) -> str:
        """
        这个是用来拼凑JS语法。
        有时候是浏览器模拟手机界面的时候，自带的定位方法无效。如果使用了JS的语法写的，那么就可以尝试使用这个方法来定位试试。
        :param by: 元素类型
        :param value: 元素值
        传参方式举例: xpath=>//div[@class_name='list']
        支持传参的类型：js_id，js_class_name，js_selector
        :param index: 如果有多个想同的元素，那么此时需要定位哪一个？
        :return: 拼凑完成的js
        """
        js_param: str = ""
        if by is By.ID:
            """
            这个是H5新的方法，那些什么byId啦，ByClassName啦都是Html4以前的东西
            注意，这个定位只用来点击,selector_value的语法是"父 子 子 "
            例如： document.querySelectorAll("#score tbody tr td:nth-of-type");
            """
            js_param = 'document.querySelectorAll("#' + value + '")[' + str(index) + ']'
            logger.info('拼接一下JS_ByID的语法：%s' % js_param)
        elif by == By.CLASS_NAME:
            js_param = 'document.querySelectorAll(".' + value + '")[' + str(index) + ']'
            logger.info('拼接一下JS_ByClassName的语法：%s' % js_param)
        elif by == By.CSS_SELECTOR:
            """
            这里的语法有点不一样，如果既没有ID也没有class,那么就接下来这样
            document.querySelectorAll("input[type='password'][placeholder='请输入新密码']")[1]
            这是input标签的2个属性
            如果这个标签在页面中是唯一的，那么可以直接document.querySelectorAll("placeholder")[0]
            """
            js_param = 'document.querySelectorAll("' + value + '")[' + str(index) + ']'  # 取第N个找到的元素、
            logger.info('拼接一下JS_BYSelector的语法：%s' % js_param)
        else:
            logger.info('传参错误，类型不支持，请检查代码')
        return js_param

    @staticmethod
    def __jq_find_element(by: By, value: str, index: int = 0) -> str:
        """
        jquery的定位语法
        有时候是浏览器模拟手机界面的时候，自带的定位方法无效。如果使用了J的语法写的，那么就可以尝试使用这个方法来定位试试。
        :param index:
        :param by: 元素类型
        :param value: 元素值
        支持 jq_id，jq_class_name
        """
        jq_param: str = ""
        if by is By.ID:
            """
            这个是H5新的方法，那些什么byId啦，ByClassName啦都是Html4以前的东西
            注意，这个定位只用来点击,selector_value的语法是"父 子 子 "
            例如： document.querySelectorAll("#score tbody tr td:nth-of-type");
            """
            jq_param = '$(' '"#' + value + '"' ')[' + str(index) + ']'
            logger.info('拼接一下JQ_ByID的语法：%s' % value)
        elif by == By.CLASS_NAME:
            jq_param = '$(' '".' + value + '"' ')[' + str(index) + ']'
            logger.info('拼接一下JQ_ByClassName的语法：%s' % jq_param)
        else:
            logger.info('传参错误，类型不支持，请检查代码')
        return jq_param

    # 输入文本框
    def js_input_str(self, by: By, value: str, text: str, index: int = 0):
        """
        这个方法不常用，当selenium自带的send_key无效的时候，用js的send试试
        这个方法我没具体试过，我也不知道行不行。先写在这。
        支持传参的类型：js_id，js_class_name，js_selector
        :param by: 元素类型
        :param value: 元素值
        :param index: 找到的元素下标
        :param text: input输入的文字
        :return: 输入元素
        """
        js_element = self.__js_find_element(by=by, value=value, index=index)
        js = js_element + '.value="' + text + '"'
        try:
            self.driver.execute_script(js)
            logger.info('JS语法输入信息：%s' % js)
        except Exception as e:
            logger.info('JS语法输入信息错误，原因：%s' % e)

    def js_click(self, by: By, value: str, index=None):
        """
        js点击
        :param by: 元素类型
        :param value: 元素值
        :param index: 找到的元素下标
        :return:
        """
        element = self.__js_find_element(by=by, value=value, index=index)
        js = element + '.click()'
        try:
            self.driver.execute_script(js)
            logger.info('JS语法点击元素：%s' % js)
        except Exception as e:
            logger.info('JS语法点击错误，原因：%s' % e)

    def __execute_jq(self):
        """
        使用JQ语法之前，需要在页面上先加载一个JQ
        但是有些页面不是用jq写的，只能用最原始的js了。就目前的来说，JQ可能没有，但JS是肯定有的
        """
        command_1 = 'var scriptS = document.createElement("script");' \
                    'scriptS.src = "https://code.jquery.com/jquery-1.12.4.js";' \
                    'document.body.appendChild(scriptS)'
        try:
            self.driver.execute_script(command_1)
            logger.info('动态加载JQ语法中，请稍后，10秒后继续执行')
            self.sleep(10)
        except Exception as e:
            logger.info('动态加载JQ语法失败，失败原因：%s' % e)

    def jq_input_str(self, by: By, value: str, text: str, index: int = 0):
        """
        这个方法不常用，当selenium自带的send_key无效的时候，用js的send试试
        这个方法我没具体试过，我也不知道行不行。先写在这。
        支持传参的类型：jq_id，jq_class_name，jq_selector
        :param by: 元素类型
        :param value: 元素值
        :param index: 找到的元素下标
        :param text: input输入的文字
        :return: 输入元素
        """
        self.__execute_jq()

        js_element = self.__jq_find_element(by=by, value=value, index=index)
        js = js_element + '.value="' + text + '"'
        try:
            self.driver.execute_script(js)
            logger.info('JS语法输入信息：%s' % js)
        except Exception as e:
            logger.info('JS语法输入信息错误，原因：%s' % e)

    def jq_click(self, by: By, value: str, index=None):
        """
        jq点击
        :param by: 元素类型
        :param value: 元素值
        :param index: 找到的元素下标
        :return:
        """
        element = self.__jq_find_element(by=by, value=value, index=index)
        js = element + '.click()'
        try:
            self.driver.execute_script(js)
            logger.info('JS语法点击元素：%s' % js)
        except Exception as e:
            logger.info('JS语法点击错误，原因：%s' % e)