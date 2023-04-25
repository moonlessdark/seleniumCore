import time
import os.path
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from seleniumTools.logger.log import Logger
from seleniumCore.common.custom_error import *
import warnings

# 初始化log
logger = Logger(logger="BasePageByH5")  # 这是全局变量,在这个类中只是单纯的引用，并没有重新赋值，所以在调用的时候就不需要再申明了


class BasePage(object):
    """
    定义一个获取页面的基础类，方便调用，万物基于此处。
    """

    def __init__(self):
        # 这里先定义一下，方便其他地方使用
        self.driver = None
        self.element = None

    @staticmethod
    def printf_log() -> Logger:
        """
        打印日志
        :return:
        """
        return logger

    def get_driver(self, webdriver):
        if webdriver is not None:
            self.driver = webdriver
        else:
            logger.error("浏览器驱动未初始化，请先初始化浏览器Driver")

    def get_url(self, url: str):
        self.driver.get(url=url)

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

    # 定位元素方法
    def find_element(self, selector: str):
        """
        只要在页面上找到了这个元素,就会return。不管这个元素的状态是不是可见，是不是可点击。我会用另一个方法来判断。
         这个地方为什么是根据=>来切割字符串，请看页面里定位元素的方法
         submit_btn = "id=>su"
         login_lnk = "xpath => //*[@id='u1']/a[7]"  # 百度首页登录链接定位
         jq_id=>
         js_id=>
         如果采用等号，结果很多xpath表达式中包含一个=，这样会造成切割不准确，影响元素定位
        :param selector: xpath=>//*[@id='u1']/a[7]
        :return: element
        """
        warnings.warn("此方法已废弃，请勿使用", DeprecationWarning)
        if '=>' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split('=>')[0]
        selector_value = selector.split('=>')[1]

        by_str = By.ID if 'id' in selector_by else By.NAME if 'name' in selector_by else By.CLASS_NAME if 'class_name' in selector_by else By.XPATH if 'xpath' in selector_by else By.PARTIAL_LINK_TEXT if 'link' in selector_by else By.CSS_SELECTOR

        if self.wait_element(by=by_str, value=selector_value) is True:
            if selector_by == 'id':
                try:
                    self.element = self.driver.find_element_by_id(selector_value)
                    logger.info("成功找到文案提示为 \' %s \' 的元素 "
                                "其 %s value 是: %s " % (self.element.text, selector_by, selector_value))
                except Exception as e:
                    logger.error("未成功找到元素: %s" % e)
                    self.get_windows_img()
            elif selector_by == 'name':
                try:
                    self.element = self.driver.find_element_by_name(selector_value)
                    logger.info("成功找到文案提示为 \' %s \' 的元素 "
                                "其 %s value 是: %s " % (self.element.text, selector_by, selector_value))
                except Exception as e:
                    logger.error("未成功找到元素: %s" % e)
                    self.get_windows_img()
            elif selector_by == 'class_name':
                try:
                    self.element = self.driver.find_element_by_class_name(selector_value)
                    logger.info("成功找到文案提示为 \' %s \' 的元素 "
                                "其 %s value 是: %s " % (self.element.text, selector_by, selector_value))
                except Exception as e:
                    logger.info('使用class_name方法出现了异常,错误原因：%s  ,接下来尝试使用css_selector方法' % e)
                    selector_value_new = '.' + selector_value.replace(" ", ".")
                    try:
                        self.element = self.driver.find_element_by_css_selector(selector_value_new)
                        logger.info("成功找到文案提示为 \' %s \' 的元素 "
                                    "其 %s value 是: %s " % (self.element.text, selector_by, selector_value_new))
                    except Exception as error:
                        logger.error("未成功找到元素: %s" % error)
                        self.get_windows_img()
            elif selector_by == 'link_text':
                try:
                    self.element = self.driver.find_element_by_link_text(selector_value)
                    logger.info("成功找到文案提示为 \' %s \' 的元素 "
                                "其 %s value 是: %s " % (self.element.text, selector_by, selector_value))
                except Exception as e:
                    logger.error("未成功找到元素: %s" % e)
                    self.get_windows_img()
            elif selector_by == 'partial_link_text':
                """
                模糊匹配<a>标签里的文字
                """
                try:
                    self.element = self.driver.find_element_by_partial_link_text(selector_value)
                    logger.info("成功找到文案提示为 \' %s \' 的元素 "
                                "其 %s value 是: %s " % (self.element.text, selector_by, selector_value))
                except Exception as e:
                    logger.error("未成功找到元素: %s" % e)
                    self.get_windows_img()
            elif selector_by == 'tag_name':
                try:
                    self.element = self.driver.find_element_by_tag_name(selector_value)
                    logger.info("成功找到文案提示为 \' %s \' 的元素 "
                                "其 %s value 是: %s " % (self.element.text, selector_by, selector_value))
                except Exception as e:
                    logger.error("未成功找到元素: %s" % e)
                    self.get_windows_img()
            elif selector_by == 'xpath':
                try:
                    self.element = self.driver.find_element_by_xpath(selector_value)
                    logger.info("成功找到文案提示为 \' %s \' 的元素 "
                                "其 %s value 是: %s " % (self.element.text, selector_by, selector_value))
                except Exception as e:
                    logger.error("未成功找到元素: %s" % e)
                    self.get_windows_img()
            elif selector_by == 'selector':
                self.element = self.driver.find_element_by_css_selector(selector_value)
            else:
                raise Exception("未找到元素，请检查传入的元素参数是否拼写正确!")
        else:
            raise Exception("元素未在页面找到，等待超时")
        return self.element

    def find_element_by(self, by: By, value: str):
        """
        :param by: By.ID
        :param value: 元素value
        :return:
        """
        if self.wait_element(by=by, value=value):
            try:
                self.element = self.driver.find_element(by, value)
                return self.element
            except TimeoutError as e:
                logger.error("元素 %s 未找到,请检查页面或者代码" % value)
                self.get_windows_img()
                return None

    def js_find_element(self, selector: str, index: int = None):
        """
        这个是用来拼凑JS语法。
        有时候是浏览器模拟手机界面的时候，自带的定位方法无效。如果使用了JS的语法写的，那么就可以尝试使用这个方法来定位试试。
        :param selector: 传入的元素信息
        传参方式举例: xpath=>//div[@class_name='list']
        支持传参的类型：js_id，js_class_name，js_selector
        :param index: 如果有多个想同的元素，那么此时需要定位哪一个？
        :return: 拼凑完成的js
        """

        if '=>' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split('=>')[0]
        selector_value = selector.split('=>')[1]
        try:
            if selector_by == 'js_id':
                """
                这个是H5新的方法，那些什么byId啦，ByClassName啦都是Html4以前的东西
                注意，这个定位只用来点击,selector_value的语法是"父 子 子 "
                例如： document.querySelectorAll("#score tbody tr td:nth-of-type");
                """
                if index is not None:
                    # 取第一个找到的元素
                    self.element = 'document.querySelectorAll("#' + selector_value + '")[' + str(index) + ']'
                else:
                    self.element = 'document.querySelectorAll("#' + selector_value + '")[0]'  # 取第一个找到的元素
                logger.info('拼接一下JS_ByID的语法：%s' % self.element)
            elif selector_by == 'js_class_name':
                if index is not None:
                    # 取第一个找到的元素
                    self.element = 'document.querySelectorAll(".' + selector_value + '")[' + str(index) + ']'
                else:
                    self.element = 'document.querySelectorAll(".' + selector_value + '")[0]'  # 取第一个找到的元素
                logger.info('拼接一下JS_ByClassName的语法：%s' % self.element)
            elif selector_by == 'js_selector':
                """
                这里的语法有点不一样，如果既没有ID也没有class,那么就接下来这样
                document.querySelectorAll("input[type='password'][placeholder='请输入新密码']")[1]
                这是input标签的2个属性
                如果这个标签在页面中是唯一的，那么可以直接document.querySelectorAll("placeholder")[0]
                """
                if index is not None:
                    self.element = 'document.querySelectorAll("' + selector_value + '")[' + str(
                        index) + ']'  # 取第N个找到的元素、
                else:
                    self.element = 'document.querySelectorAll("' + selector_value + '")[0]'  # 取第1个找到的元素、
                logger.info('拼接一下JS_BYSelector的语法：%s' % self.element)
            else:
                self.element = None
                logger.info('selector传参错误，已默认赋值为None，等着报错吧亲')
        except Exception:
            logger.error("未找到元素 %s" % selector_value)
            return None
        return self.element

    def jq_find_element(self, selector: str):
        """
        jquery的定位语法
        有时候是浏览器模拟手机界面的时候，自带的定位方法无效。如果使用了J的语法写的，那么就可以尝试使用这个方法来定位试试。
        :param selector: 待查找的元素  xpath=>//div[@class_name='list']
        支持 jq_id，jq_class_name
        :return:
        """

        if '=>' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split('=>')[0]
        selector_value = selector.split('=>')[1]

        # 以下是jq的语法
        try:
            if selector_by == 'jq_id':
                """
                注意，这个定位只用来点击
                """
                self.element = '$(' '"#' + selector_value + '"' ')[0]'
                logger.info('拼接一下JQ_ByID的语法：%s' % self.element)
            elif selector_by == 'jq_class_name':
                """
                注意，这个定位只用来点击
                """
                self.element = '$(' '".' + selector_value + '"' ')[0]'
                logger.info('拼接一下JQ_ByClassName的语法：%s' % self.element)
            else:
                self.element = None
                logger.error("传参错误 %s" % selector_by)
            return self.element
        except Exception:
            logger.error("未找到元素 %s" % selector_value)
            return None

    def find_elements_by(self, by: By, value: str):
        ele = self.find_element_by(by=by, value=value)
        if ele is not None:
            elements = self.driver.find_elements(by=by, value=value)
            return elements

    def send_text(self, by: By, value: str, text: str):
        """
        文本框输入信息
        :param by: By.ID
        :param value: 元素值
        :param text: 需要出入的文字信息
        :return:
        """
        ele = self.find_element_by(by=by, value=value)
        if ele is not None and text is not None:
            self.clear(by=by, value=value)
            ele.send_keys(text)
        else:
            logger.error("元素 %s 参数错误,请检查代码" % value)

    # 输入文本框
    def js_send_text(self, selector: str, text: str):
        """
        这个方法不常用，当selenium自带的send_key无效的时候，用js的send试试
        这个方法我没具体试过，我也不知道行不行。先写在这。
        :param selector: 元素参数
        支持传参的类型：js_id，js_class_name，js_selector
        :param text: input输入的文字
        :return: 输入元素
        """
        element = self.js_find_element(selector)
        js = element + '.value="' + text + '"'
        try:
            self.driver.execute_script(js)
            logger.info('JS语法输入信息：%s' % js)
        except Exception as e:
            logger.info('JS语法输入信息错误，原因：%s' % e)

    # 传输文件
    def send_file(self, by: By, value: str, file_path: str):
        """
        这是为了解决上传文件或者图片，方法参考：
        https://www.cnblogs.com/sylvia-liu/p/4431664.html
        感谢

        执行sendKeys的元素一定要符合input和 type="file"条件,否则就是你没找对上传文件的对象，会上传失败的。
        :param by: 查找方式  By.ID
        :param value: 要上传文件的元素框，有些元素框需要点击一下才能上传。
        :param file_path: 文件路径
        :return: upload img/file
        """
        try:
            file = self.find_element_by(by, value)
        except SendKeyError(ele_value=value) as e:
            logger.error(e.message)
            self.get_windows_img()
        else:
            file.send_keys(file_path)
            logger.info("进行上传图片、文件操作")

    # 清除文本框
    def clear(self, by: By, value: str):
        """
        :param by: By.ID
        :param value: 元素
        :return:
        """
        el = self.find_element_by(by=by, value=value)
        try:
            el.clear()
            logger.info("%s 文案清除成功！" % el.text)
        except Exception as e:
            logger.error("文案清除失败: %s" % e)
            self.get_windows_img()

    # 点击元素
    def click(self, by: By, value: str):
        """
        点击元素
        :param by: By.ID
        :param value: By对应的类型值
        :return:
        """
        if self.wait_element(by, wait_type='click', value=value) is True:
            try:
                self.driver.find_element(by, value).click()
                logger.info("元素 %s click成功" % value)
            except ClickError(ele_value=value) as e:
                logger.error(e.message)
                self.get_windows_img()
        else:
            logger.error('元素 %s 不可点击' % value)

    def js_click(self, selector: str, index=None):
        """
        js点击
        :param selector: xpath=>[@name='id']
        :param index: 数字
        :return:
        """
        element = self.js_find_element(selector, index)
        js = element + '.click()'
        try:
            self.driver.execute_script(js)
            logger.info('JS语法点击元素：%s' % js)
        except Exception as e:
            logger.info('JS语法点击错误，原因：%s' % e)

    @staticmethod
    def sleep(seconds: int):
        time.sleep(seconds)
        logger.info("休眠 %d 秒" % seconds)

    # 获取网页标题
    def get_page_title(self):
        try:
            title = self.driver.title
            if title is not None:
                logger.info("网页的标题(Title)是: %s" % title)
            else:
                logger.info("网页的标题(Title)是空的，压根没写")
            return title
        except Exception as e:
            logger.info("获取网页标题出现异常:%s" % e)

    def get_text_by(self, by: By, value: str):
        """
        获取文本信息
        :param by: By.ID
        :param value: 元素
        :return:
        """
        element = self.find_element_by(by=by, value=value)
        if element is not None:
            el_text = element.text
            return el_text
        return None

    def get_text_by_xpath(self, xpath: str):
        """
        :param xpath: xpath
        :return: 通过xpath获取到的text信息
        """
        return self.get_text_by(by=By.XPATH, value=xpath)

    def get_text_by_class_name(self, class_name_value: str):
        """
        :param class_name_value:
        :return:
        """
        return self.get_text_by(by=By.CLASS_NAME, value=class_name_value)

    def select_text_by_index(self, by: By, value: str, index: int):
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

    def select_text_by_text(self, by: By, value: str, text: str):
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
    def __expect_element(self, selector):
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

    def wait_element(self, by: By, value: str, wait_type: str = 'presence', wait_time: int = 10) -> bool:
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

    # ------------------------------------------------------
    # -------------页面加载JQ---------------------------------
    # ------------------------------------------------------
    def execute_jq(self):
        """
        使用JQ语法之前，需要在页面上先加载一个JQ
        但是有些页面不是用jq写的，只能用最原始的js了。就目前的来说，JQ可能没有，但JS是肯定有的
        """
        command_1 = 'var scriptS = document.createElement("script");' \
                    'scriptS.src = "https://code.jquery.com/jquery-1.12.4.js";' \
                    'document.body.appendChild(scriptS)'
        try:
            self.driver.execute_script(command_1)
            logger.info('动态加载JQ语法')
            self.sleep(10)
        except Exception as e:
            logger.info('动态加载JQ语法失败，失败原因：%s' % e)

    def slide_to_the_element(self, by: By, value: str):
        """
        针对页面比较长有滚动条的情况，滑动滚动条到元素可见可操作的位置
        特殊处理
        :param by: 元素类型
        :param value: 元素值
        :return:
        """
        el = self.find_element_by(by=by, value=value)
        try:
            self.driver.execute_script('arguments[0].scrollIntoView();', el)
            logger.info('滑动滚动条到 %s 处' % el.text)
        except Exception as e:
            logger.error("未找到元素: %s" % e)
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

    def clear_cookie(self):
        """
        清除所有缓存
        :return:
        """
        try:
            self.driver.delete_all_cookies()
            logger.info('清除浏览器的所有cookie.打印一下清除cookie后的cookie : %s' % self.get_cookie())
        except Exception as e:
            logger.info('清除cookie失败，原因：%s' % e)

    def refresh(self):
        """
        刷新
        :return:
        """
        self.driver.refresh()
        self.sleep(2)
        logger.info('刷新一下页面')

    def check_complat_status(self):
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

    def get_attribute(self, elementobj, attributeName: str):
        """
        获取元素属性值
        使用例子：
        返回某个元素的class属性
        result = self.driver.find_element_by(by=By.XPATH, value="//div[@id="name"]/a")
        get_attribute(elementobj=result, attributeName='class')

        参考：https://blog.csdn.net/xcntime/article/details/120315806

        :param elementobj: 已经通过find方法获取到属性对象
        :param attributeName: 这个元素要获取的属性
        :return:
        """
        return elementobj.get_attribute(attributeName)

    def close_alert_tips(self):
        """
        点击 alert 窗口
        :return:
        """
        try:
            if WebDriverWait(self.driver, 10, 0.5).until(ec.alert_is_present()):
                self.driver.switch_to.alert.accept()
        except Exception as e:
            logger.info("alert窗口未检测到或未成功关闭")
